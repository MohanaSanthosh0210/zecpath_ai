"""
NLP-Based Skill Extractor

This module implements sophisticated skill extraction from resume text using:
- Pattern matching for explicit skill mentions
- Named Entity Recognition (NER) for implicit skills
- Contextual analysis
- Spelling variation handling
- Skill stack detection
"""

from email.mime import text
import re
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import warnings
import time
import gc

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    warnings.warn("spacy not available. Some NLP features will be limited.")

try:
    from difflib import SequenceMatcher
    DIFFLIB_AVAILABLE = True
except ImportError:
    DIFFLIB_AVAILABLE = False

from .skill_dictionary import (
    get_all_skills,
    get_skill_by_name,
    normalize_skill_name,
    get_skill_aliases,
    get_skill_category,
    is_skill_stack,
    get_skill_stack_components,
    SKILL_STACKS,
    TECHNICAL_SKILLS,
    BUSINESS_SKILLS,
    CREATIVE_SKILLS,
    SOFT_SKILLS,
)

from utils.logger import logger


class SkillExtractor:
    """
    Extracts technical, business, creative, and soft skills from resume text.
    
    Features:
    - Fuzzy matching for skill detection
    - Context-aware extraction
    - Skill stack decomposition
    - Multi-language support (basic)
    - Confidence scoring
    """
    
    def __init__(self, nlp_model=None, fuzzy_threshold=0.75):
        """
        Initialize the skill extractor.
        
        Args:
            nlp_model: spaCy model for NER (optional)
            fuzzy_threshold: Threshold for fuzzy matching (0-1)
        """
        self.all_skills = get_all_skills()
        self.skill_stacks = SKILL_STACKS
        self.fuzzy_threshold = fuzzy_threshold
        self.nlp_model = nlp_model
        self.extracted_skills = {}
        self._fuzzy_cache = {}

        # Build lowercase index for faster lookup
        self.skill_index = {name.lower(): name for name in self.all_skills.keys()}
        self.alias_index = self._build_alias_index()
        self.skill_patterns = {
            name.lower(): re.compile(r"\b" + re.escape(name.lower()) + r"\b")
            for name in self.all_skills.keys()
        }
        self.alias_patterns = {
            alias.lower(): re.compile(r"\b" + re.escape(alias.lower()) + r"\b")
            for skill_data in self.all_skills.values()
            if "aliases" in skill_data
            for alias in skill_data["aliases"]
        }
        self.version_pattern = re.compile(
            r"\b(python|java|php|c\+\+|javascript|node\.?js|typescript|ruby|golang|go|rust|scala)\s*(\d+(?:\.\d+)?|\w+)",
            flags=re.IGNORECASE,
        )
        self.stack_pattern = re.compile(r"\b([A-Z]{2,5})\b")
        self.context_patterns = [
            re.compile(r"(?:knowledge of|familiar with|expertise in|skilled in|proficient in|experienced with|experience in|worked with|worked on|implemented|developed|built|created)\s+([^.,;\n]+)", flags=re.IGNORECASE),
            re.compile(r"(?:technologies?|tools?|frameworks?|languages?|platforms?)[:\s]+([^.,;\n]+)", flags=re.IGNORECASE),
            re.compile(r"(?:technical skills?)[:\s]+([^.,;\n]+)", flags=re.IGNORECASE),
            re.compile(r"(?:including|includes|such as|for example)\s+([^.,;\n]+)", flags=re.IGNORECASE),
        ]
        
    def _build_alias_index(self) -> Dict[str, str]:
        """Build an index of aliases to canonical skill names"""
        alias_index = {}
        for skill_name, skill_data in self.all_skills.items():
            if "aliases" in skill_data:
                for alias in skill_data["aliases"]:
                    alias_index[alias.lower()] = skill_name
        return alias_index
    
    def extract_skills(self, resume_text: str) -> Dict[str, Dict]:
        """
        Extract all skills from resume text.
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Dictionary of extracted skills with metadata
        """
        try:
            start_time = time.time()
            self.extracted_skills = {}
            logger.info(
    f"Processing Resume Length: {len(resume_text)} characters"
)
        
            # Normalize and prepare text
            normalized_text = self._normalize_text(resume_text)
        
            # Extract skills using multiple methods
            explicit_skills = self._extract_explicit_skills(normalized_text)
            pattern_skills = self._extract_pattern_based_skills(normalized_text)
            context_skills = self._extract_context_based_skills(normalized_text)
        
            # Combine all extracted skills
            all_extracted = {**explicit_skills, **pattern_skills, **context_skills}
        
            # Deduplicate and normalize
            self.extracted_skills = self._deduplicate_skills(all_extracted)
        
            logger.info(f"Extracted {len(self.extracted_skills)} unique skills")
            end_time = time.time()
            logger.info(
    f"Skill Extraction Time: {round(end_time-start_time,2)} sec"
)
            gc.collect()
            return self.extracted_skills
        except Exception as e:
            logger.error(
        f"Skill Extraction Failed: {str(e)}"
    )
            return {}
    def _normalize_text(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\x00-\x7F]+", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text
    
    def _extract_explicit_skills(self, text: str) -> Dict[str, Dict]:
        """
        Extract skills that are explicitly mentioned in text.
        Uses exact matching and alias lookup.
        """
        extracted = {}
        text_lower = text.lower()
        
        # Check against skill index and aliases using precompiled regex patterns
        for skill_name, skill_data in self.all_skills.items():
            skill_found = False
            match_positions = []
            pattern = self.skill_patterns.get(skill_name.lower())

            if pattern:
                for match in pattern.finditer(text_lower):
                    skill_found = True
                    match_positions.append(match.start())

            if "aliases" in skill_data:
                for alias in skill_data["aliases"]:
                    alias_pattern = self.alias_patterns.get(alias.lower())
                    if alias_pattern:
                        for match in alias_pattern.finditer(text_lower):
                            skill_found = True
                            match_positions.append(match.start())

            if skill_found:
                extracted[skill_name] = {
                    "source": "explicit_match",
                    "positions": sorted(match_positions),
                    "count": len(match_positions),
                    "skill_data": skill_data,
                }

        return extracted
    
    def _extract_pattern_based_skills(self, text: str) -> Dict[str, Dict]:
        """
        Extract skills using regex patterns.
        Useful for detecting specialized combinations like version numbers, etc.
        """
        extracted = {}
        text_lower = text.lower()
        
        for match in self.version_pattern.finditer(text_lower):
            tech_name = match.group(1).strip()
            version = match.group(2) if match.group(2) else ""
            
            normalized = normalize_skill_name(tech_name)
            if normalized and normalized not in extracted:
                extracted[normalized] = {
                    "source": "pattern_match",
                    "version": version,
                    "skill_data": get_skill_by_name(normalized),
                }
        
        for match in self.stack_pattern.finditer(text):
            stack_name = match.group(1)
            if is_skill_stack(stack_name):
                components = get_skill_stack_components(stack_name)
                for component in components:
                    if component not in extracted:
                        extracted[component] = {
                            "source": "skill_stack",
                            "stack": stack_name,
                            "skill_data": get_skill_by_name(component),
                        }
        
        return extracted
    
    def _extract_context_based_skills(self, text: str) -> Dict[str, Dict]:
        """
        Extract skills based on contextual keywords.
        E.g., "knowledge of", "experienced in", "proficient with", etc.
        """
        extracted = {}
        
        for pattern in self.context_patterns:
            for match in pattern.finditer(text):
                skill_text = match.group(1).strip()
                potential_skills = re.split(r'[,/\sand\s]+', skill_text)
                
                for potential_skill in potential_skills:
                    potential_skill = potential_skill.strip()
                    matched_skill = self._fuzzy_match_skill(potential_skill)
                    if matched_skill and matched_skill not in extracted:
                        extracted[matched_skill] = {
                            "source": "context_based",
                            "raw_text": potential_skill,
                            "skill_data": get_skill_by_name(matched_skill),
                        }
        
        return extracted
    
    def _fuzzy_match_skill(self, text: str) -> str or None:
        """
        Fuzzy match a text fragment against known skills.
        Returns the best matching skill name or None.
        """
        text_lower = text.lower().strip()
        if len(text_lower) < 2:
            return None
        
        # Exact match first
        if text_lower in self.skill_index:
            return self.skill_index[text_lower]
        
        if text_lower in self.alias_index:
            return self.alias_index[text_lower]
        
        if text_lower in self._fuzzy_cache:
            return self._fuzzy_cache[text_lower]
        
        if not DIFFLIB_AVAILABLE:
            self._fuzzy_cache[text_lower] = None
            return None
        
        best_match = None
        best_ratio = 0
        
        for skill_name in self.skill_index.values():
            ratio = SequenceMatcher(None, text_lower, skill_name.lower()).ratio()
            if ratio > best_ratio and ratio >= self.fuzzy_threshold:
                best_ratio = ratio
                best_match = skill_name
        
        self._fuzzy_cache[text_lower] = best_match
        return best_match
    
    def _deduplicate_skills(self, extracted: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Deduplicate skills that represent the same capability.
        E.g., "React" and "reactjs" → "React"
        """
        deduplicated = {}
        
        for skill_name, skill_info in extracted.items():
            # Normalize skill name
            normalized = normalize_skill_name(skill_name) or skill_name
            
            if normalized in deduplicated:
                # Merge with existing entry
                existing = deduplicated[normalized]
                existing["sources"].add(skill_info.get("source", "unknown"))
                existing["mentions"] += skill_info.get("count", 1)
                if "positions" in skill_info:
                    existing["positions"].extend(skill_info["positions"])
            else:
                # Create new entry
                deduplicated[normalized] = {
                    "name": normalized,
                    "category": get_skill_category(normalized),
                    "sources": {skill_info.get("source", "unknown")},
                    "mentions": skill_info.get("count", 1),
                    "positions": skill_info.get("positions", []),
                    "skill_data": get_skill_by_name(normalized)
                }
        
        return deduplicated
    
    def get_skills_by_category(self, category: str = None) -> Dict[str, List[str]]:
        """Get extracted skills grouped by category"""
        if not self.extracted_skills:
            return {}
        
        by_category = defaultdict(list)
        
        for skill_name, skill_info in self.extracted_skills.items():
            cat = skill_info.get("category", "unknown")
            if category is None or cat == category:
                by_category[cat].append(skill_name)
        
        return dict(by_category)
    
    def get_top_skills(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get top N skills by mention count"""
        if not self.extracted_skills:
            return []
        
        ranked = sorted(
            [(name, info["mentions"]) for name, info in self.extracted_skills.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        return ranked[:n]
    
    def export_extracted_skills(self) -> Dict:
        """
        Export extracted skills in a structured format.
        
        Returns:
            Dictionary with skills organized by category
        """
        if not self.extracted_skills:
            return {}
        
        export = {
            "total_skills": len(self.extracted_skills),
            "skills_by_category": {},
            "all_skills": []
        }
        
        # Organize by category
        for skill_name, skill_info in self.extracted_skills.items():
            category = skill_info.get("category", "unknown")
            
            if category not in export["skills_by_category"]:
                export["skills_by_category"][category] = []
            
            skill_entry = {
                "name": skill_name,
                "category": category,
                "mentions": skill_info.get("mentions", 1),
                "sources": list(skill_info.get("sources", set())),
            }
            
            export["skills_by_category"][category].append(skill_entry)
            export["all_skills"].append(skill_entry)
        
        return export


class SkillExtractorAdvanced(SkillExtractor):
    """
    Advanced skill extractor with NLP capabilities using spaCy.
    Requires spaCy model to be installed.
    """
    
    def __init__(self, nlp_model=None, fuzzy_threshold=0.75):
        """
        Initialize advanced skill extractor.
        
        Args:
            nlp_model: Pre-loaded spaCy model or model name string
            fuzzy_threshold: Threshold for fuzzy matching
        """
        super().__init__(nlp_model, fuzzy_threshold)
        
        # Load spaCy model if provided
        if isinstance(nlp_model, str) and SPACY_AVAILABLE:
            try:
                self.nlp_model = spacy.load(nlp_model)
                logger.info(f"Loaded spaCy model: {nlp_model}")
            except OSError:
                logger.warning(f"Could not load spaCy model: {nlp_model}")
                self.nlp_model = None
    
    def extract_skills_with_ner(self, resume_text: str) -> Dict[str, Dict]:
        """
        Extract skills using Named Entity Recognition.
        Requires spaCy model.
        """
        if not self.nlp_model or not SPACY_AVAILABLE:
            logger.warning("spaCy not available. Using basic extraction.")
            return self.extract_skills(resume_text)
        
        # Get basic extraction first
        basic_skills = self.extract_skills(resume_text)
        
        # Process with spaCy for additional context
        doc = self.nlp_model(resume_text)
        
        # Extract ORG entities that might be tools/frameworks
        for ent in doc.ents:
            if ent.label_ in ["PRODUCT", "ORG"]:
                potential_skill = self._fuzzy_match_skill(ent.text)
                if potential_skill and potential_skill not in basic_skills:
                    basic_skills[potential_skill] = {
                        "name": potential_skill,
                        "source": "ner",
                        "entity_text": ent.text,
                        "category": get_skill_category(potential_skill)
                    }
        
        return basic_skills