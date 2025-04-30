from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, Field

class Contact(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    website: Optional[HttpUrl] = Field(None, description="Personal website or portfolio")

class Summary(BaseModel):
    summary: str = Field(..., description="A brief professional summary")

class ExperienceItem(BaseModel):
    company: str
    title: str
    start_date: str = Field(..., description="YYYY-MM format")
    end_date: Optional[str] = Field(..., description="YYYY-MM or 'Present'")
    responsibilities: List[str]

class EducationItem(BaseModel):
    institution: str
    degree: str
    start_year: int
    end_year: Optional[int]

class CVSchema(BaseModel):
    contact: Contact
    summary: Summary
    experience: List[ExperienceItem]
    education: List[EducationItem]
    skills: List[str]
