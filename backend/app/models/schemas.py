# Pydantic response/request models (MatchResponse, etc.)
from pydantic import BaseModel, Field


class ExperienceSchema(BaseModel):
    company: str = Field(..., description="Name of the company")
    role: str = Field(..., description="Role or position held")
    start_date: str = Field(..., description="Start date of the experience")
    end_date: str = Field(..., description="End date of the experience")
    description: str = Field(
        ..., description="Description of responsibilities and achievements"
    )


class EducationSchema(BaseModel):
    institution: str = Field(..., description="Name of the educational institution")
    degree: str = Field(..., description="Degree or qualification obtained")
    start_date: str = Field(..., description="Start date of the education")
    end_date: str = Field(..., description="End date of the education")
    field_of_study: str = Field(..., description="Field of study or major")


class SkillSchema(BaseModel):
    hard_skills: list[str] = Field(..., description="List of hard skills")
    soft_skills: list[str] = Field(..., description="List of soft skills")


class ResumeSchema(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    email: str = Field(..., description="Email address of the candidate")
    phone_number: str = Field(..., description="Phone number of the candidate")
    skills: list[SkillSchema] = Field(..., description="List of skills")
    experience: list[ExperienceSchema] = Field(
        ..., description="List of work experiences"
    )
    education: list[EducationSchema] = Field(
        ..., description="List of educational qualifications"
    )


class JobDescriptionSchema(BaseModel):
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company offering the job")
    experience: str = Field(..., description="Required years of experience or level")
    description: str = Field(..., description="Detailed job description")
    required_skills: list[SkillSchema] = Field(
        ..., description="List of required skills"
    )
    nice_to_have_skills: list[SkillSchema] = Field(
        ..., description="List of nice-to-have skills"
    )
    responsibilities: list[str] = Field(..., description="List of job responsibilities")
