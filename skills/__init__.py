"""
Skills Extraction Module

Comprehensive skill extraction engine for resumes with:
- Master skill dictionaries
- NLP-based extraction
- Confidence scoring
- Skill normalization and deduplication
"""

from .skill_dictionary import (
    TECHNICAL_SKILLS,
    BUSINESS_SKILLS,
    CREATIVE_SKILLS,
    SOFT_SKILLS,
    SKILL_STACKS,
    get_all_skills,
    get_skill_by_name,
    normalize_skill_name,
    get_skill_aliases,
    get_skill_category,
    get_skills_by_category,
    is_skill_stack,
    get_skill_stack_components,
)

from .skill_extractor import (
    SkillExtractor,
    SkillExtractorAdvanced,
)

from .skill_confidence_scorer import (
    SkillConfidenceScorer,
    ConfidenceLevel,
    ProficiencyLevel,
)

from .skill_normalizer import (
    SkillNormalizer,
    SkillDeduplicator,
    SkillMerger,
    SkillValidator,
)

__all__ = [
    # Dictionaries
    "TECHNICAL_SKILLS",
    "BUSINESS_SKILLS",
    "CREATIVE_SKILLS",
    "SOFT_SKILLS",
    "SKILL_STACKS",
    "get_all_skills",
    "get_skill_by_name",
    "normalize_skill_name",
    "get_skill_aliases",
    "get_skill_category",
    "get_skills_by_category",
    "is_skill_stack",
    "get_skill_stack_components",
    
    # Extractors
    "SkillExtractor",
    "SkillExtractorAdvanced",
    
    # Scoring
    "SkillConfidenceScorer",
    "ConfidenceLevel",
    "ProficiencyLevel",
    
    # Normalization
    "SkillNormalizer",
    "SkillDeduplicator",
    "SkillMerger",
    "SkillValidator",
]