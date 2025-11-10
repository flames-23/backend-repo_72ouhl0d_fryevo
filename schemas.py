"""
Database Schemas for Interview Builder

Each Pydantic model represents a collection in MongoDB.
Collection name is the lowercase of the class name.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Question(BaseModel):
    """
    Questions candidates can be asked during interviews
    Collection: "question"
    """
    text: str = Field(..., description="The question text")
    category: Optional[str] = Field(None, description="Topic area, e.g., Algorithms, System Design")
    difficulty: Optional[str] = Field(None, description="e.g., Easy, Medium, Hard")
    role: Optional[str] = Field(None, description="Target role, e.g., Backend, Frontend, Data")
    type: Optional[str] = Field(None, description="e.g., Behavioral, Coding, System Design")
    expected_answer: Optional[str] = Field(None, description="Guidance for interviewer on what to expect")
    tags: List[str] = Field(default_factory=list, description="Searchable tags")


class InterviewTemplate(BaseModel):
    """
    Interview templates contain structure and a set of question IDs
    Collection: "interviewtemplate"
    """
    title: str = Field(..., description="Template name, e.g., Frontend Senior Loop")
    role: Optional[str] = Field(None, description="Primary role this template targets")
    seniority: Optional[str] = Field(None, description="e.g., Junior, Mid, Senior, Staff")
    description: Optional[str] = Field(None, description="Notes for interviewers")
    question_ids: List[str] = Field(default_factory=list, description="Associated question IDs (as strings)")


class Candidate(BaseModel):
    """
    Candidate information
    Collection: "candidate"
    """
    name: str
    email: str
    role_applied: Optional[str] = None


class Interview(BaseModel):
    """
    An actual scheduled interview for a candidate
    Collection: "interview"
    """
    candidate_name: str
    candidate_email: str
    role: Optional[str] = None
    template_id: Optional[str] = Field(None, description="Linked template ID if used")
    question_ids: List[str] = Field(default_factory=list)
    scheduled_at: Optional[datetime] = Field(None, description="ISO timestamp for scheduled time")
    mode: Optional[str] = Field(None, description="e.g., Onsite, Remote, Phone Screen")
    notes: Optional[str] = None

# Add additional collections as needed (e.g., feedback, scorecards) by following the same pattern.
