from typing import List, Optional
from pydantic import BaseModel, EmailStr

class Contact(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None

class Summary(BaseModel):
    summary: Optional[str] = None

class ExperienceItem(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    start_date: Optional[str] = None  # Format: YYYY-MM
    end_date: Optional[str] = None    # Format: YYYY-MM or 'Present'
    responsibilities: Optional[List[str]] = None

class EducationItem(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None

class CVSchema(BaseModel):
    contact: Optional[Contact] = None
    summary: Optional[Summary] = None
    experience: Optional[List[ExperienceItem]] = None
    education: Optional[List[EducationItem]] = None
    skills: Optional[List[str]] = None
