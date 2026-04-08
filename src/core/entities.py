from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class Skill:
    """Represents a single technical or soft skill."""
    name: str
    category: str  # e.g., "Language", "Framework", "Cloud"
    level: Optional[str] = "Intermediate"

@dataclass
class JobProfile:
    """Represents the target job requirements."""
    id: str
    title: str
    location: str
    description: str
    required_skills: List[str]
    vector: Optional[List[float]] = None
    metadata: Dict = field(default_factory=dict)

@dataclass
class UserProfile:
    """Represents the current state of the candidate."""
    id: str
    skills: List[str]
    experience_summary: str
    vector: Optional[List[float]] = None

@dataclass
class Course:
    """Represents a verified learning resource from your CSV/DB."""
    id: str
    title: str
    provider: str
    url: str
    skill_covered: str
    relevance_score: float = 0.0

@dataclass
class AnalysisResult:
    job_id: str
    match_percentage: float
    gap_skills: List[str]
    matched_skills: List[str]
    gap_vector: List[float]