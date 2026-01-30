"""SQLAlchemy ORM models for portfolio database."""
from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Profile(Base):
    """Profile model - stores personal information."""
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, default=1)
    name = Column(String(100), nullable=False)
    name_kana = Column(String(100))  # Japanese phonetic
    name_vi = Column(String(100))    # Vietnamese name
    gender = Column(String(10))
    date_of_birth = Column(String(10))  # YYYY-MM-DD format
    school = Column(String(200))
    graduation_year = Column(Integer)
    field = Column(String(200))
    # Multilingual: {"ja": "4年", "vi": "4 năm", "en": "4 years"}
    work_experience = Column(JSON, default={})
    japan_residence = Column(JSON, default={})
    japanese_level = Column(String(10))

    # Contact information
    email = Column(String(100))
    phone = Column(String(20))
    # Multilingual address as JSON: {"ja": "...", "vi": "...", "en": "..."}
    address = Column(JSON, default={})
    # Social links as JSON: {"facebook": "...", "messenger": "...", "github": "..."}
    social_links = Column(JSON, default={})

    # Multilingual self-PR as JSON: {"ja": "...", "vi": "...", "en": "..."}
    self_pr = Column(JSON, nullable=False, default={})

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Profile(id={self.id}, name='{self.name}')>"


class SkillCategory(Base):
    """Skill category model - groups skills by type."""
    __tablename__ = "skill_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(50), unique=True, nullable=False)  # e.g., "programming_languages"
    display_order = Column(Integer, default=0)

    # Relationship to skills
    skills = relationship("Skill", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SkillCategory(id={self.id}, key='{self.key}')>"


class Skill(Base):
    """Skill model - individual technology/tool."""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    level = Column(Integer, nullable=False)  # 1-5 proficiency rating
    # Multilingual: {"ja": "2年7ヶ月", "vi": "2 năm 7 tháng", "en": "2y 7m"}
    experience = Column(JSON, default={})
    category_id = Column(Integer, ForeignKey("skill_categories.id"), nullable=False)
    category_key = Column(String(50))  # Denormalized for easier queries
    display_order = Column(Integer, default=0)

    # Relationship to category
    category = relationship("SkillCategory", back_populates="skills")

    def __repr__(self):
        return f"<Skill(id={self.id}, name='{self.name}', level={self.level})>"


class Project(Base):
    """Project model - work experience entry."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Multilingual fields as JSON: {"ja": "...", "vi": "...", "en": "..."}
    name = Column(JSON, nullable=False)
    description = Column(JSON, nullable=False)
    highlights = Column(JSON, nullable=False)  # {"ja": [...], "vi": [...], "en": [...]}

    role = Column(String(100))  # Developer, Team Leader, BrSE, etc.
    team_size = Column(String(20))
    technologies = Column(JSON)  # ["C#", "JavaScript", ...]
    environment = Column(String(200))
    phases = Column(JSON)  # ["製造", "単体テスト", ...]
    start_date = Column(String(20))  # "YYYY-MM" format
    end_date = Column(String(20), nullable=True)
    # Duration is auto-calculated from start_date and end_date
    # This field is deprecated but kept for backward compatibility
    duration = Column(JSON, nullable=True)

    # Relevance scores for role-based sorting (1-5)
    relevance_leader = Column(Integer, default=1)
    relevance_brse = Column(Integer, default=1)
    relevance_fullstack = Column(Integer, default=1)

    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Project(id={self.id}, role='{self.role}')>"

    def get_relevance(self, role: str) -> int:
        """Get relevance score for a specific role."""
        relevance_map = {
            "leader": self.relevance_leader,
            "brse": self.relevance_brse,
            "fullstack": self.relevance_fullstack
        }
        return relevance_map.get(role, 1)


class RoleEmphasis(Base):
    """Role emphasis model - role-specific highlight keywords."""
    __tablename__ = "role_emphasis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(20), nullable=False, unique=True)  # "leader", "brse", "fullstack"
    # Keywords as JSON: {"ja": [...], "vi": [...], "en": [...]}
    keywords = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<RoleEmphasis(id={self.id}, role='{self.role}')>"
