from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class Role(str, Enum):
    LEADER = "leader"
    BRSE = "brse"
    FULLSTACK = "fullstack"


class Language(str, Enum):
    JA = "ja"
    VI = "vi"
    EN = "en"


class AnswerMode(str, Enum):
    SINGLE = "single"
    BILINGUAL = "bilingual"


class Skill(BaseModel):
    id: int
    name: str
    level: int
    experience: str
    category: str


class Project(BaseModel):
    id: int
    name: str
    role: str
    team_size: str
    technologies: List[str]
    environment: str
    phases: List[str]
    start_date: str
    end_date: Optional[str]
    duration: str
    description: str
    highlights: List[str]


class SocialLinks(BaseModel):
    facebook: Optional[str] = None
    messenger: Optional[str] = None
    github: Optional[str] = None


class Profile(BaseModel):
    name: str
    name_kana: str
    gender: str
    date_of_birth: Optional[str] = None
    age: int
    school: str
    field: str
    work_experience: str
    japan_residence: str
    japanese_level: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    social_links: Optional[SocialLinks] = None
    self_pr: str


class ChatRequest(BaseModel):
    question: str
    lang: Language = Language.JA
    role: Role = Role.FULLSTACK
    mode: AnswerMode = AnswerMode.SINGLE


class ChatResponse(BaseModel):
    answer: str
    answer_secondary: Optional[str] = None
    sources: List[str] = []


class ProfileResponse(BaseModel):
    profile: Profile
    role_emphasis: List[str]


class SkillsResponse(BaseModel):
    programming_languages: List[Skill]
    frameworks: List[Skill]
    databases: List[Skill]
    cloud: List[Skill]
    other: List[Skill]


class ProjectsResponse(BaseModel):
    projects: List[Project]
    highlighted: List[int]


# ===== CRUD Schemas =====

class ProfileUpdate(BaseModel):
    """Schema for updating profile fields."""
    name: Optional[str] = None
    name_kana: Optional[str] = None
    name_vi: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    school: Optional[str] = None
    graduation_year: Optional[int] = None
    field: Optional[str] = None
    work_experience: Optional[str] = None
    japan_residence: Optional[str] = None
    japanese_level: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None  # Single language address (current language)
    social_links: Optional[SocialLinks] = None


class SelfPrUpdate(BaseModel):
    """Schema for updating self PR for a specific language."""
    content: str


class SkillCreate(BaseModel):
    """Schema for creating a new skill."""
    name: str
    level: int
    experience: str
    category: str


class SkillUpdate(BaseModel):
    """Schema for updating a skill."""
    name: Optional[str] = None
    level: Optional[int] = None
    experience: Optional[str] = None
    category: Optional[str] = None


class SkillResponse(BaseModel):
    """Response for a single skill."""
    id: int
    name: str
    level: int
    experience: str
    category: str


class MultilingualText(BaseModel):
    """Schema for multilingual text fields."""
    ja: str
    vi: str
    en: str


class MultilingualList(BaseModel):
    """Schema for multilingual list fields."""
    ja: List[str]
    vi: List[str]
    en: List[str]


class ProjectCreate(BaseModel):
    """Schema for creating a new project. Duration is auto-calculated from dates."""
    name: MultilingualText
    description: MultilingualText
    highlights: MultilingualList
    role: str
    team_size: str
    technologies: List[str]
    environment: str
    phases: List[str]
    start_date: str  # YYYY-MM format
    end_date: Optional[str] = None  # YYYY-MM format, None = ongoing
    relevance_leader: int = 1
    relevance_brse: int = 1
    relevance_fullstack: int = 1


class ProjectUpdate(BaseModel):
    """Schema for updating a project. Duration is auto-calculated from dates."""
    name: Optional[MultilingualText] = None
    description: Optional[MultilingualText] = None
    highlights: Optional[MultilingualList] = None
    role: Optional[str] = None
    team_size: Optional[str] = None
    technologies: Optional[List[str]] = None
    environment: Optional[str] = None
    phases: Optional[List[str]] = None
    start_date: Optional[str] = None  # YYYY-MM format
    end_date: Optional[str] = None  # YYYY-MM format
    relevance_leader: Optional[int] = None
    relevance_brse: Optional[int] = None
    relevance_fullstack: Optional[int] = None


class ProjectBrief(BaseModel):
    """Brief project info returned after create/update."""
    id: int
    name: MultilingualText
    role: str


class MessageResponse(BaseModel):
    """Generic message response."""
    success: bool
    message: str
