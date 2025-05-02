from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class PersonalInfo(BaseModel):
    full_name: str = Field(
        ...,
        title="Full Name",
        description="Legal full name as it should appear on the CV"
    )
    location: Optional[str] = Field(
        None,
        title="Location",
        description="Current city and country of residence"
    )
    email: Optional[EmailStr] = Field(
        None,
        title="Email Address",
        description="Professional email address for contact"
    )
    phone: Optional[str] = Field(
        None,
        title="Phone Number",
        description="Phone number (include country code if international)"
    )
    website: Optional[str] = Field(
        None,
        title="Personal Website",
        description="Link to personal website or portfolio (if any)"
    )
    linkedin: Optional[str] = Field(
        None,
        title="LinkedIn Profile",
        description="URL of LinkedIn profile"
    )
    github: Optional[str] = Field(
        None,
        title="GitHub Profile",
        description="URL of GitHub (or GitLab/Bitbucket) profile"
    )

class Summary(BaseModel):
    text: str = Field(
        ...,
        title="Professional Summary",
        description="Brief overview of background, skills, and career goals"
    )

class EducationItem(BaseModel):
    institution: str = Field(
        ...,
        title="Institution Name",
        description="Name of university, college or school"
    )
    degree: Optional[str] = Field(
        None,
        title="Degree",
        description="Degree earned (e.g., B.Sc, M.A., Ph.D.)"
    )
    field_of_study: Optional[str] = Field(
        None,
        title="Field of Study",
        description="Major or concentration"
    )
    start_date: Optional[str] = Field(
        None,
        title="Start Date",
        description="Date when studies began (YYYY-MM)"
    )
    end_date: Optional[str] = Field(
        None,
        title="End Date",
        description="Date of graduation or 'Present' if ongoing"
    )
    location: Optional[str] = Field(
        None,
        title="Institution Location",
        description="City, state/region, country of the institution"
    )
    gpa: Optional[str] = Field(
        None,
        title="GPA",
        description="Grade Point Average, if included"
    )
    coursework: Optional[List[str]] = Field(
        None,
        title="Relevant Coursework",
        description="List of most relevant courses to the field or role"
    )

class ExperienceItem(BaseModel):
    company: str = Field(
        ...,
        title="Company Name",
        description="Organization where the role was held"
    )
    role: str = Field(
        ...,
        title="Job Title",
        description="Position or role title"
    )
    start_date: Optional[str] = Field(
        None,
        title="Start Date",
        description="Date when the role began (YYYY-MM)"
    )
    end_date: Optional[str] = Field(
        None,
        title="End Date",
        description="Date when the role ended or 'Present' if current"
    )
    location: Optional[str] = Field(
        None,
        title="Work Location",
        description="City, state/region, country of the role"
    )
    achievements: Optional[List[str]] = Field(
        None,
        title="Key Achievements",
        description="Bulleted list of major accomplishments in the role"
    )

class Publication(BaseModel):
    title: str = Field(
        ...,
        title="Title",
        description="Full title of the publication"
    )
    authors: Optional[List[str]] = Field(
        None,
        title="Authors",
        description="List of authors in the published order"
    )
    date: Optional[str] = Field(
        None,
        title="Publication Date",
        description="Date of publication (YYYY-MM)"
    )
    publisher: Optional[str] = Field(
        None,
        title="Publisher",
        description="Name of journal, conference, or publisher"
    )
    doi: Optional[str] = Field(
        None,
        title="DOI",
        description="Digital Object Identifier, if available"
    )
    url: Optional[str] = Field(
        None,
        title="URL",
        description="Link to the publication"
    )

class Project(BaseModel):
    name: str = Field(
        ...,
        title="Project Name",
        description="Name of the project"
    )
    description: Optional[str] = Field(
        None,
        title="Description",
        description="Short summary of project purpose and scope"
    )
    url: Optional[str] = Field(
        None,
        title="URL",
        description="Link to demo, repository, or live site"
    )
    start_date: Optional[str] = Field(
        None,
        title="Start Date",
        description="Date when project work began (YYYY-MM)"
    )
    end_date: Optional[str] = Field(
        None,
        title="End Date",
        description="Date when project completed or last updated"
    )
    tools_used: Optional[List[str]] = Field(
        None,
        title="Tools & Technologies",
        description="Languages, frameworks, and tools applied"
    )
    highlights: Optional[List[str]] = Field(
        None,
        title="Highlights",
        description="Notable project features or achievements"
    )

class Skills(BaseModel):
    programming_languages: Optional[List[str]] = Field(
        None,
        title="Programming Languages",
        description="List of programming languages proficiently used"
    )
    frameworks_libraries: Optional[List[str]] = Field(
        None,
        title="Frameworks & Libraries",
        description="Key frameworks or libraries experienced with"
    )
    tools: Optional[List[str]] = Field(
        None,
        title="Tools",
        description="Other relevant tools or platforms"
    )
    other: Optional[List[str]] = Field(
        None,
        title="Other Skills",
        description="Additional relevant skills (e.g., languages, soft skills)"
    )

class CVSchema(BaseModel):
    personal_info: PersonalInfo = Field(
        ...,
        title="Personal Information",
        description="Core contact and identity information"
    )
    summary: Optional[Summary] = Field(
        None,
        title="Professional Summary",
        description="Concise statement of background and objectives"
    )
    education: Optional[List[EducationItem]] = Field(
        None,
        title="Education",
        description="Academic history entries"
    )
    experience: Optional[List[ExperienceItem]] = Field(
        None,
        title="Experience",
        description="Professional work history entries"
    )
    publications: Optional[List[Publication]] = Field(
        None,
        title="Publications",
        description="List of scholarly works"
    )
    projects: Optional[List[Project]] = Field(
        None,
        title="Projects",
        description="Key projects and contributions"
    )
    skills: Optional[Skills] = Field(
        None,
        title="Skills",
        description="Technical and other proficiencies"
    )
