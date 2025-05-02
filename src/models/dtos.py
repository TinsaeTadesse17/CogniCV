from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List

class PersonalInfo(BaseModel):
    full_name: str
    location: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    website: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None

class Summary(BaseModel):
    text: str

class EducationItem(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None # e.g. '2000-09'
    end_date: Optional[str] = None   # e.g. '2005-05' or 'Present'
    location: Optional[str] = None
    gpa: Optional[str] = None
    coursework: Optional[List[str]] = None

class ExperienceItem(BaseModel):
    company: str
    role: str
    start_date: Optional[str]  # e.g., '2005-06'
    end_date: Optional[str]    # e.g., '2007-08' or 'Present'
    location: Optional[str]
    achievements: Optional[List[str]]

class Publication(BaseModel):
    title: str
    authors: Optional[List[str]]
    date: Optional[str]  # e.g. '2004-01'
    publisher: Optional[str] = None # Not used in the template, but kept for schema consistency
    doi: Optional[str] = None
    url: Optional[HttpUrl] = None

class Project(BaseModel):
    name: str
    description: Optional[str] = None
    url: Optional[HttpUrl] = None
    start_date: Optional[str] = None # Added based on example ('2002')
    end_date: Optional[str] = None # Added based on example (not present, but could be)
    tools_used: Optional[List[str]] = None
    highlights: Optional[List[str]] = None

class Skills(BaseModel):
    programming_languages: Optional[List[str]] = None
    frameworks_libraries: Optional[List[str]]  = None # Merged with technologies in template
    tools: Optional[List[str]] = None              # Merged with technologies in template
    other: Optional[List[str]] = None                 # Can be added if needed, not in template

class CVSchema(BaseModel):
    personal_info: PersonalInfo
    summary: Optional[Summary]
    education: Optional[List[EducationItem]]
    experience: Optional[List[ExperienceItem]]
    publications: Optional[List[Publication]]
    projects: Optional[List[Project]]
    skills: Optional[Skills]
