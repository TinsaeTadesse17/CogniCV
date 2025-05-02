import re
from datetime import datetime
from typing import List, Optional
from pydantic import HttpUrl
from urllib.parse import urlparse

from src.models.dtos import CVSchema 

def escape_latex(text: str) -> str:
    """Escapes special LaTeX characters in a string."""
    if not isinstance(text, str):
        text = str(text)
    chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '\n': r'\\', # Basic newline handling, might need adjustment
    }
    regex = re.compile('|'.join(re.escape(key) for key in chars.keys()))
    return regex.sub(lambda match: chars[match.group(0)], text)

def format_date_month_year(date_str: Optional[str]) -> Optional[str]:
    """Formats 'YYYY-MM' or 'Present' to 'Month YYYY' or 'Present'."""
    if not date_str:
        return None
    if date_str.lower() == 'present':
        return 'Present'
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m')
        # Format as 'Jan 2024'
        return date_obj.strftime('%b %Y')
    except ValueError:
        # Handle cases like just 'YYYY' if needed, or return original
        try:
            date_obj = datetime.strptime(date_str, '%Y')
            return date_obj.strftime('%Y')
        except ValueError:
            return escape_latex(date_str) # Return escaped original if format unknown

def format_date_range(start_date: Optional[str], end_date: Optional[str]) -> str:
    """Formats start and end dates into 'Start Month YYYY – End Month YYYY'."""
    start_formatted = format_date_month_year(start_date)
    end_formatted = format_date_month_year(end_date)

    if start_formatted and end_formatted:
        return f"{start_formatted} – {end_formatted}"
    elif start_formatted:
        return start_formatted
    elif end_formatted: # Should ideally not happen without start date
        return end_formatted
    else:
        return ""

def generate_list_items(items: Optional[List[str]]) -> str:
    """Generates LaTeX \\item lines for a list within the highlights environment."""
    if not items:
        return ""
    return "\n".join([f"            \\item {escape_latex(item)}" for item in items])

def generate_url_text(url: Optional[HttpUrl]) -> str:
    """Generates display text for URLs (e.g., domain or path)."""
    if not url:
        return ""
    parsed_url = urlparse(str(url))
    if parsed_url.netloc:
        # Remove www. if present
        domain = parsed_url.netloc.replace("www.", "")
        # For LinkedIn/GitHub, often the path is more useful
        if "linkedin.com" in domain and parsed_url.path:
             # Remove leading/trailing slashes and 'in/'
            path = parsed_url.path.strip('/').replace('in/', '')
            return f"linkedin.com/{escape_latex(path)}"
        if "github.com" in domain and parsed_url.path:
            path = parsed_url.path.strip('/')
            return f"github.com/{escape_latex(path)}"
        return escape_latex(domain + parsed_url.path.rstrip('/')) # Include path if relevant, remove trailing /
    return escape_latex(str(url)) # Fallback


# --- Main LaTeX Generation Function ---

def generate_cv_latex(cv_data: CVSchema) -> str:
    """
    Generates a LaTeX string for a CV based on the provided CVSchema object
    and a specific LaTeX template structure.
    """
    pi = cv_data.personal_info
    full_name_escaped = escape_latex(pi.full_name)

    # --- Header Section ---
    header_parts = []
    if pi.location:
        header_parts.append(f"\\mbox{{{escape_latex(pi.location)}}}")
    if pi.email:
        header_parts.append(f"\\mbox{{\\hrefWithoutArrow{{mailto:{pi.email}}}{{{escape_latex(pi.email)}}}}}")
    if pi.phone:
        header_parts.append(f"\\mbox{{\\hrefWithoutArrow{{tel:{pi.phone}}}{{{escape_latex(pi.phone)}}}}}")
    if pi.website:
        website_text = generate_url_text(pi.website)
        header_parts.append(f"\\mbox{{\\hrefWithoutArrow{{{pi.website}}}{{{website_text}}}}}")
    if pi.linkedin:
        linkedin_text = generate_url_text(pi.linkedin)
        header_parts.append(f"\\mbox{{\\hrefWithoutArrow{{{pi.linkedin}}}{{{linkedin_text}}}}}")
    if pi.github:
        github_text = generate_url_text(pi.github)
        header_parts.append(f"\\mbox{{\\hrefWithoutArrow{{{pi.github}}}{{{github_text}}}}}")

    header_contact_info = ""
    if header_parts:
        # Join parts with separator
        separator = "\\kern 5.0 pt%\\AND%\\kern 5.0 pt%"
        header_contact_info = f"\n        {separator.join(header_parts)}%"

    # --- Last Updated ---
    # Get current date for the "Last updated" text
    now = datetime.now()
    last_updated_text = now.strftime("%B %Y") # e.g., September 2024

    # --- Preamble Definition ---
    # Use raw strings (r"...") or double backslashes (\\) for LaTeX commands
    latex_preamble = fr"""\documentclass[10pt, letterpaper]{{article}}

% Packages:
\usepackage[
    ignoreheadfoot, % set margins without considering header and footer
    top=2 cm, % seperation between body and page edge from the top
    bottom=2 cm, % seperation between body and page edge from the bottom
    left=2 cm, % seperation between body and page edge from the left
    right=2 cm, % seperation between body and page edge from the right
    footskip=1.0 cm, % seperation between body and footer
    % showframe % for debugging
]{{geometry}} % for adjusting page geometry
\usepackage{{titlesec}} % for customizing section titles
\usepackage{{tabularx}} % for making tables with fixed width columns
\usepackage{{array}} % tabularx requires this
\usepackage[dvipsnames]{{xcolor}} % for coloring text
\definecolor{{primaryColor}}{{RGB}}{{0, 0, 0}} % define primary color
\usepackage{{enumitem}} % for customizing lists
\usepackage{{fontawesome5}} % for using icons
\usepackage{{amsmath}} % for math
\usepackage[
    pdftitle={{{full_name_escaped}'s CV}},
    pdfauthor={{{full_name_escaped}}},
    pdfcreator={{LaTeX with RenderCV}},
    colorlinks=true,
    urlcolor=primaryColor
]{{hyperref}} % for links, metadata and bookmarks
\usepackage[pscoord]{{eso-pic}} % for floating text on the page
\usepackage{{calc}} % for calculating lengths
\usepackage{{bookmark}} % for bookmarks
\usepackage{{lastpage}} % for getting the total number of pages
\usepackage{{changepage}} % for one column entries (adjustwidth environment)
\usepackage{{paracol}} % for two and three column entries
\usepackage{{ifthen}} % for conditional statements
\usepackage{{needspace}} % for avoiding page brake right after the section title
\usepackage{{iftex}} % check if engine is pdflatex, xetex or luatex

% Ensure that generate pdf is machine readable/ATS parsable:
\ifPDFTeX
    \input{{glyphtounicode}}
    \pdfgentounicode=1
    \usepackage[T1]{{fontenc}}
    \usepackage[utf8]{{inputenc}}
    \usepackage{{lmodern}}
\fi

\usepackage{{charter}} % Font

% Some settings:
\raggedright
\AtBeginEnvironment{{adjustwidth}}{{\partopsep0pt}} % remove space before adjustwidth environment
\pagestyle{{empty}} % no header or footer
\setcounter{{secnumdepth}}{{0}} % no section numbering
\setlength{{\parindent}}{{0pt}} % no indentation
\setlength{{\topskip}}{{0pt}} % no top skip
\setlength{{\columnsep}}{{0.15cm}} % set column seperation
\pagenumbering{{gobble}} % no page numbering

\titleformat{{\section}}{{\needspace{{4\baselineskip}}\bfseries\large}}{{}}{{0pt}}{{}}[\vspace{{1pt}}\titlerule]

\titlespacing{{\section}}{{
    % left space:
    -1pt
}}{{
    % top space:
    0.3 cm
}}{{
    % bottom space:
    0.2 cm
}} % section title spacing

\renewcommand\labelitemi{{\vcenter{{\hbox{{\small$\bullet$}}}}}} % custom bullet points
\newenvironment{{highlights}}{{
    \begin{{itemize}}[
        topsep=0.10 cm,
        parsep=0.10 cm,
        partopsep=0pt,
        itemsep=0pt,
        leftmargin=0 cm + 10pt
    ]
}}{{
    \end{{itemize}}
}} % new environment for highlights


\newenvironment{{highlightsforbulletentries}}{{
    \begin{{itemize}}[
        topsep=0.10 cm,
        parsep=0.10 cm,
        partopsep=0pt,
        itemsep=0pt,
        leftmargin=10pt
    ]
}}{{
    \end{{itemize}}
}} % new environment for highlights for bullet entries

\newenvironment{{onecolentry}}{{
    \begin{{adjustwidth}}{{
        0 cm + 0.00001 cm
    }}{{
        0 cm + 0.00001 cm
    }}
}}{{
    \end{{adjustwidth}}
}} % new environment for one column entries

\newenvironment{{twocolentry}}[2][]{{
    \onecolentry
    \def\secondColumn{{#2}}
    \setcolumnwidth{{\fill, 4.5 cm}}
    \begin{{paracol}}{{2}}
}}{{
    \switchcolumn \raggedleft \secondColumn
    \end{{paracol}}
    \endonecolentry
}} % new environment for two column entries

\newenvironment{{threecolentry}}[3][]{{
    \onecolentry
    \def\thirdColumn{{#3}}
    \setcolumnwidth{{, \fill, 4.5 cm}}
    \begin{{paracol}}{{3}}
    {{\raggedright #2}} \switchcolumn
}}{{
    \switchcolumn \raggedleft \thirdColumn
    \end{{paracol}}
    \endonecolentry
}} % new environment for three column entries

\newenvironment{{header}}{{
    \setlength{{\topsep}}{{0pt}}\par\kern\topsep\centering\linespread{{1.5}}
}}{{
    \par\kern\topsep
}} % new environment for the header

\newcommand{{\placelastupdatedtext}}{{% \placetextbox{{<horizontal pos>}}{{<vertical pos>}}{{<stuff>}}
  \AddToShipoutPictureFG*{{% Add <stuff> to current page foreground
    \put(
        \LenToUnit{{\paperwidth-2 cm-0 cm+0.05cm}},
        \LenToUnit{{\paperheight-1.0 cm}}
    ){{\vtop{{{{\null}}\makebox[0pt][c]{{
        \small\color{{gray}}\textit{{Last updated in {last_updated_text}}}\hspace{{\widthof{{Last updated in {last_updated_text}}}}}
    }}}}}}%
  }}%
}}%

% save the original href command in a new command:
\let\hrefWithoutArrow\href

% new command for external links:
% \renewcommand{{\href}}[2]{{\hrefWithoutArrow{{#1}}{{#2}}}} % Remove arrow for all links if desired

\begin{{document}}
    \placelastupdatedtext % Place the last updated text

    % Define the separator for the header
    \newcommand{{\AND}}{{\unskip
        \cleaders\copy\ANDbox\hskip\wd\ANDbox
        \ignorespaces
    }}
    \newsavebox\ANDbox
    \sbox\ANDbox{{$|$}}

    \begin{{header}}
        \fontsize{{25 pt}}{{25 pt}}\selectfont {full_name_escaped}

        \vspace{{5 pt}}

        \normalsize{header_contact_info}
    \end{{header}}

    \vspace{{5 pt - 0.3 cm}}
"""

    # --- Summary Section ---
    summary_latex = ""
    if cv_data.summary:
        summary_latex = fr"""
    \section{{Professional Summary}}
        \begin{{onecolentry}}
            {escape_latex(cv_data.summary.text)}
        \end{{onecolentry}}
"""

    # --- Education Section ---
    education_latex = ""
    if cv_data.education:
        education_items_latex = []
        for i, item in enumerate(cv_data.education):
            date_range = format_date_range(item.start_date, item.end_date)
            degree_info = escape_latex(item.degree or "")
            field_info = escape_latex(item.field_of_study or "")
            institution_info = escape_latex(item.institution)
            location_info = f", {escape_latex(item.location)}" if item.location else ""

            title_line = f"\\textbf{{{institution_info}}}"
            if degree_info or field_info:
                title_line += f", {degree_info}" if degree_info else ""
                title_line += f" in {field_info}" if field_info else ""
            title_line += location_info


            highlights_content = []
            if item.gpa:
                 # Basic check for a URL pattern to make it a link like the example
                gpa_text = escape_latex(item.gpa)
                if "http" in item.gpa: # Very basic URL detection
                     gpa_text = f"\\href{{{item.gpa}}}{{{escape_latex(item.gpa)}}}" # Assume URL is also the text
                highlights_content.append(f"GPA: {gpa_text}")

            if item.coursework:
                highlights_content.append(f"\\textbf{{Coursework:}} {escape_latex(', '.join(item.coursework))}")

            highlights_latex = ""
            if highlights_content:
                highlights_items = "\n".join([f"                \\item {line}" for line in highlights_content])
                highlights_latex = fr"""
        \vspace{{0.10 cm}}
        \begin{{onecolentry}}
            \begin{{highlights}}
{highlights_items}
            \end{{highlights}}
        \end{{onecolentry}}"""

            item_latex = fr"""
        \begin{{twocolentry}}{{
            {date_range}
        }}
            {title_line}\end{{twocolentry}}
{highlights_latex}"""
            # Add vertical space between entries except for the last one
            if i < len(cv_data.education) - 1:
                 item_latex += "\n\n        \\vspace{0.2 cm}\n"

            education_items_latex.append(item_latex)

        if education_items_latex:
             education_latex = fr"""
    \section{{Education}}
{''.join(education_items_latex)}
"""

    # --- Experience Section ---
    experience_latex = ""
    if cv_data.experience:
        experience_items_latex = []
        for i, item in enumerate(cv_data.experience):
            date_range = format_date_range(item.start_date, item.end_date)
            role_info = escape_latex(item.role)
            company_info = escape_latex(item.company)
            location_info = f" -- {escape_latex(item.location)}" if item.location else ""

            title_line = f"\\textbf{{{role_info}}}, {company_info}{location_info}"

            highlights_latex = ""
            if item.achievements:
                highlights_items = generate_list_items(item.achievements)
                highlights_latex = fr"""
        \vspace{{0.10 cm}}
        \begin{{onecolentry}}
            \begin{{highlights}}
{highlights_items}
            \end{{highlights}}
        \end{{onecolentry}}"""

            item_latex = fr"""
        \begin{{twocolentry}}{{
            {date_range}
        }}
            {title_line}\end{{twocolentry}}
{highlights_latex}"""

            # Add vertical space between entries except for the last one
            if i < len(cv_data.experience) - 1:
                 item_latex += "\n\n        \\vspace{0.2 cm}\n"

            experience_items_latex.append(item_latex)

        if experience_items_latex:
            experience_latex = fr"""
    \section{{Experience}}
{''.join(experience_items_latex)}
"""

    # --- Publications Section ---
    publications_latex = ""
    if cv_data.publications:
        publication_items_latex = []
        cv_owner_name = pi.full_name # Name to potentially bold

        for i, item in enumerate(cv_data.publications):
            date_formatted = format_date_month_year(item.date) or ""
            title_info = escape_latex(item.title)

            authors_latex = ""
            if item.authors:
                formatted_authors = []
                for author in item.authors:
                    author_escaped = escape_latex(author)
                    # Bold the CV owner's name if it matches
                    if author.strip().lower() == cv_owner_name.strip().lower():
                         formatted_authors.append(f"\\textbf{{\\textit{{{author_escaped}}}}}")
                    else:
                         formatted_authors.append(f"\\mbox{{{author_escaped}}}")
                authors_latex = f", ".join(formatted_authors)
                authors_latex = f"\n            {authors_latex}\n\n            \\vspace{{0.10 cm}}\n            " # Add formatting

            link_latex = ""
            if item.doi:
                doi_escaped = escape_latex(item.doi)
                # Assume HTTPS for DOI links if no URL provided
                doi_url = str(item.url) if item.url else f"https://doi.org/{item.doi}"
                link_latex = f"\\href{{{doi_url}}}{{{doi_escaped}}}"
            elif item.url:
                link_latex = f"\\href{{{item.url}}}{{{escape_latex(str(item.url))}}}"


            item_latex = fr"""
        \begin{{samepage}} % Keep publication entry on one page if possible
            \begin{{twocolentry}}{{
                {date_formatted}
            }}
                \textbf{{{title_info}}}
            \end{{twocolentry}}

            \vspace{{0.10 cm}}

            \begin{{onecolentry}}
                {authors_latex}{link_latex}
            \end{{onecolentry}}
        \end{{samepage}}"""

            # Add vertical space between entries except for the last one
            if i < len(cv_data.publications) - 1:
                 item_latex += "\n\n        \\vspace{0.2 cm}\n"

            publication_items_latex.append(item_latex)

        if publication_items_latex:
            publications_latex = fr"""
    \section{{Publications}}
{''.join(publication_items_latex)}
"""

    # --- Projects Section ---
    projects_latex = ""
    if cv_data.projects:
        project_items_latex = []
        for i, item in enumerate(cv_data.projects):
            # Determine right column content: URL or Date Range/Date
            right_col_content = ""
            if item.url:
                url_text = generate_url_text(item.url)
                right_col_content = f"\\href{{{item.url}}}{{{url_text}}}"
            else:
                 # Use date if no URL, mimicking the 'Custom Operating System' example
                 right_col_content = format_date_range(item.start_date, item.end_date)


            name_info = escape_latex(item.name)
            title_line = f"\\textbf{{{name_info}}}"

            highlights_content = []
            if item.description:
                highlights_content.append(escape_latex(item.description))
            if item.tools_used:
                 highlights_content.append(f"Tools Used: {escape_latex(', '.join(item.tools_used))}")
            if item.highlights:
                highlights_content.extend([escape_latex(h) for h in item.highlights])

            highlights_latex = ""
            if highlights_content:
                highlights_items = "\n".join([f"                \\item {line}" for line in highlights_content])
                highlights_latex = fr"""
        \vspace{{0.10 cm}}
        \begin{{onecolentry}}
            \begin{{highlights}}
{highlights_items}
            \end{{highlights}}
        \end{{onecolentry}}"""

            item_latex = fr"""
        \begin{{twocolentry}}{{
            {right_col_content}
        }}
            {title_line}\end{{twocolentry}}
{highlights_latex}"""

            # Add vertical space between entries except for the last one
            if i < len(cv_data.projects) - 1:
                 item_latex += "\n\n        \\vspace{0.2 cm}\n"

            project_items_latex.append(item_latex)

        if project_items_latex:
            projects_latex = fr"""
    \section{{Projects}}
{''.join(project_items_latex)}
"""

    # --- Skills/Technologies Section ---
    skills_latex = ""
    if cv_data.skills:
        skills_parts = []
        s = cv_data.skills
        if s.programming_languages:
            skills_parts.append(fr"""\begin{{onecolentry}}
            \textbf{{Languages:}} {escape_latex(', '.join(s.programming_languages))}
        \end{{onecolentry}}""")

        # Combine frameworks/libraries and tools into "Technologies" as per template
        technologies = []
        if s.frameworks_libraries:
            technologies.extend(s.frameworks_libraries)
        if s.tools:
            technologies.extend(s.tools)
        if technologies:
             skills_parts.append(fr"""\begin{{onecolentry}}
            \textbf{{Technologies:}} {escape_latex(', '.join(technologies))}
        \end{{onecolentry}}""")

        # Add 'other' skills if present (optional, adjust formatting as needed)
        if s.other:
             skills_parts.append(fr"""\begin{{onecolentry}}
            \textbf{{Other:}} {escape_latex(', '.join(s.other))}
        \end{{onecolentry}}""")


        if skills_parts:
            # Join parts with vertical space
            skills_content = "\n        \\vspace{0.2 cm}\n        ".join(skills_parts)
            skills_latex = fr"""
    \section{{Technologies}} % Renamed section to match template example
        {skills_content}
"""

    # --- Footer ---
    latex_footer = r"""
\end{document}
"""

    # --- Assemble Final LaTeX String ---
    full_latex_string = (
        latex_preamble +
        summary_latex +
        education_latex +
        experience_latex +
        publications_latex +
        projects_latex +
        skills_latex +
        latex_footer
    )

    return full_latex_string