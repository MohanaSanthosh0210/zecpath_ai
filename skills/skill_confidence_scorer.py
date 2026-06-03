"""
Skill Confidence Scoring

This module implements confidence scoring for extracted skills based on:
- Extraction method (explicit > pattern > context)
- Mention frequency
- Contextual keywords (years, proficiency level)
- Source validation
- Positional analysis (skills in skills section = higher confidence)
"""

import re
from typing import Dict, List, Tuple
from enum import Enum

from utils.logger import logger


class ConfidenceLevel(Enum):
    """Confidence level categories"""
    VERY_HIGH = (0.9, 1.0)
    HIGH = (0.7, 0.89)
    MEDIUM = (0.5, 0.69)
    LOW = (0.3, 0.49)
    VERY_LOW = (0.0, 0.29)


class ProficiencyLevel(Enum):
    """Proficiency levels extracted from text"""
    EXPERT = "expert"
    ADVANCED = "advanced"
    INTERMEDIATE = "intermediate"
    BEGINNER = "beginner"
    UNKNOWN = "unknown"


class SkillConfidenceScorer:
    """
    Scores confidence in extracted skills based on multiple factors.
    Confidence range: 0.0 (no confidence) to 1.0 (absolute confidence)
    """
    
    # Weights for different scoring factors (should sum close to 1.0)
    WEIGHTS = {
        "extraction_method": 0.25,      # How the skill was extracted
        "mention_frequency": 0.20,      # How many times mentioned
        "contextual_keywords": 0.20,    # Presence of strength indicators
        "positional_relevance": 0.15,   # Where in resume (skills section)
        "proficiency_indicators": 0.20, # Years/proficiency level mentioned
    }
    
    # Extraction method scoring
    METHOD_SCORES = {
        "explicit_match": 0.95,          # Direct match with skill dictionary
        "pattern_match": 0.85,           # Pattern-based detection
        "skill_stack": 0.90,             # Part of known stack
        "context_based": 0.70,           # Context-based extraction
        "ner": 0.75,                     # NER-based extraction
        "fuzzy_match": 0.60,             # Fuzzy matching
        "unknown": 0.50,
    }
    
    # Context keywords and their impact
    PROFICIENCY_KEYWORDS = {
        # Expert level
        ("expert", "master", "ninja", "guru"): (ProficiencyLevel.EXPERT, 0.15),
        
        # Advanced level
        ("advanced", "proficient", "strong"): (ProficiencyLevel.ADVANCED, 0.10),
        
        # Intermediate level
        ("intermediate", "moderate", "solid", "good"): (ProficiencyLevel.INTERMEDIATE, 0.05),
        
        # Beginner level
        ("beginner", "novice", "basic", "fundamental"): (ProficiencyLevel.BEGINNER, -0.05),
    }
    
    # Years of experience impact
    EXPERIENCE_THRESHOLDS = {
        (0, 0.5): -0.10,      # Less than 6 months
        (0.5, 1): 0.00,       # 6 months - 1 year
        (1, 2): 0.05,         # 1-2 years
        (2, 3): 0.10,         # 2-3 years
        (3, 5): 0.15,         # 3-5 years
        (5, 10): 0.20,        # 5-10 years
        (10, float('inf')): 0.25,  # 10+ years
    }
    
    def _init_(self):
        """Initialize the confidence scorer"""
        pass
    
    def score_skill(self, skill_info: Dict, context: Dict = None) -> Dict:
        """
        Calculate confidence score for a single skill.
        
        Args:
            skill_info: Skill information from extractor
            context: Additional context (resume text, section info, etc.)
            
        Returns:
            Dictionary with confidence score and component scores
        """
        context = context or {}
        scores = {}
        
        # Score each component
        scores["extraction_method"] = self._score_extraction_method(skill_info)
        scores["mention_frequency"] = self._score_mention_frequency(skill_info)
        scores["contextual_keywords"] = self._score_contextual_keywords(
            skill_info, context.get("text", "")
        )
        scores["positional_relevance"] = self._score_positional_relevance(
            skill_info, context.get("positions", [])
        )
        scores["proficiency_indicators"] = self._score_proficiency_indicators(
            skill_info, context.get("text", "")
        )
        
        # Calculate weighted confidence score
        confidence = self._calculate_weighted_score(scores)
        
        return {
            "skill_name": skill_info.get("name", "unknown"),
            "confidence": round(confidence, 3),
            "confidence_level": self._get_confidence_level(confidence),
            "component_scores": scores,
            "factors": self._explain_score(confidence, scores)
        }
    
    def score_skills_batch(self, skills_list: List[Dict], context: Dict = None) -> List[Dict]:
        """
        Score multiple skills with context.
        
        Args:
            skills_list: List of skill information dictionaries
            context: Optional context dictionary
            
        Returns:
            List of scored skills
        """
        scored_skills = []
        for skill_info in skills_list:
            scored = self.score_skill(skill_info, context)
            scored_skills.append(scored)
        
        return sorted(scored_skills, key=lambda x: x["confidence"], reverse=True)
    
    def _score_extraction_method(self, skill_info: Dict) -> float:
        """Score based on how the skill was extracted"""
        source = skill_info.get("source", "unknown")
        sources = skill_info.get("sources", {source})
        
        if isinstance(sources, set):
            sources = list(sources)
        
        # If multiple sources, use the best one
        if isinstance(sources, (list, set)):
            best_score = max(
                self.METHOD_SCORES.get(s, self.METHOD_SCORES["unknown"])
                for s in sources
            )
            return best_score
        
        return self.METHOD_SCORES.get(source, self.METHOD_SCORES["unknown"])
    
    def _score_mention_frequency(self, skill_info: Dict) -> float:
        """
        Score based on how many times the skill is mentioned.
        More mentions = higher confidence
        """
        mentions = skill_info.get("mentions", 1)
        
        # Linear scaling: 1 mention = 0.7, 2-3 = 0.85, 4+ = 0.95
        if mentions <= 0:
            return 0.5
        elif mentions == 1:
            return 0.70
        elif mentions <= 3:
            return 0.85
        else:
            return min(0.95, 0.70 + (mentions * 0.05))
    
    def _score_contextual_keywords(self, skill_info: Dict, text: str) -> float:
        """Score based on contextual keywords (knowledge of, expert in, etc.)"""
        sources = skill_info.get("sources", set())
        
        # Context-based extraction gets baseline bonus
        if "context_based" in sources:
            return 0.65
        
        # Default baseline for found skills
        return 0.55
    
    def _score_positional_relevance(self, skill_info: Dict, positions: List = None) -> float:
        """
        Score based on where in the resume the skill appears.
        Skills in "Skills" section = higher score
        """
        # If we have position data, could analyze resume structure
        # For now, use basic heuristics
        
        sources = skill_info.get("sources", set())
        
        # Explicit matches (usually from skills section) get higher score
        if "explicit_match" in sources:
            return 0.85
        
        # Pattern matches are fairly reliable
        if "pattern_match" in sources or "skill_stack" in sources:
            return 0.70
        
        # Context-based extraction gets moderate score
        if "context_based" in sources:
            return 0.60
        
        # Default baseline
        return 0.50
    
    def _score_proficiency_indicators(self, skill_info: Dict, text: str) -> float:
        """Score based on proficiency level and years of experience indicators"""
        skill_name = skill_info.get("name", "")
        if not skill_name or not text:
            return 0.50  # Baseline for skills without explicit proficiency
        
        total_boost = 0.50  # Baseline
        
        # Check for proficiency keywords
        for keywords, (level, boost) in self.PROFICIENCY_KEYWORDS.items():
            for keyword in keywords:
                pattern = rf'{keyword}.*?(?:in|with|at|in)\s+{re.escape(skill_name)}'
                if re.search(pattern, text, re.IGNORECASE):
                    total_boost = max(total_boost, 0.50 + boost)
        
        # Check for years of experience
        years_pattern = rf'(\d+)\s*(?:\+)?\s*years?\s*(?:of\s+)?(?:experience\s+)?(?:with|in|at)\s+{re.escape(skill_name)}'
        years_match = re.search(years_pattern, text, re.IGNORECASE)
        
        if years_match:
            try:
                years = float(years_match.group(1))
                for (min_y, max_y), boost in self.EXPERIENCE_THRESHOLDS.items():
                    if min_y <= years < max_y:
                        total_boost = max(total_boost, 0.50 + boost)
                        break
            except ValueError:
                pass
        
        # Clamp between 0.3 and 0.95
        return max(0.30, min(total_boost, 0.95))
    
    def _calculate_weighted_score(self, component_scores: Dict) -> float:
        """
        Calculate weighted confidence score from component scores.
        Uses predefined weights.
        """
        total_score = 0.0
        
        for component, weight in self.WEIGHTS.items():
            score = component_scores.get(component, 0.0)
            total_score += score * weight
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, total_score))
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Map confidence score to confidence level"""
        for level in ConfidenceLevel:
            low, high = level.value
            if low <= confidence <= high:
                return level.name
        return "UNKNOWN"
    
    def _explain_score(self, confidence: float, component_scores: Dict) -> str:
        """Generate human-readable explanation for the score"""
        level = self._get_confidence_level(confidence)
        
        # Find strongest and weakest components
        strongest = max(component_scores.items(), key=lambda x: x[1])
        weakest = min(component_scores.items(), key=lambda x: x[1])
        
        explanation = (
            f"Confidence {level} ({confidence:.1%}). "
            f"Strongest factor: {strongest[0]} ({strongest[1]:.2f}). "
            f"Weakest factor: {weakest[0]} ({weakest[1]:.2f})."
        )
        
        return explanation
    
    def filter_by_confidence(self, scored_skills: List[Dict], min_confidence: float = 0.5) -> List[Dict]:
        """
        Filter scored skills by minimum confidence threshold.
        
        Args:
            scored_skills: List of scored skill dictionaries
            min_confidence: Minimum confidence score (0-1)
            
        Returns:
            Filtered list of skills above threshold
        """
        return [s for s in scored_skills if s["confidence"] >= min_confidence]
    
    def get_confidence_distribution(self, scored_skills: List[Dict]) -> Dict:
        """
        Get distribution of confidence levels.
        
        Args:
            scored_skills: List of scored skill dictionaries
            
        Returns:
            Dictionary with count of skills per confidence level
        """
        distribution = {level.name: 0 for level in ConfidenceLevel}
        
        for skill in scored_skills:
            level = skill.get("confidence_level", "UNKNOWN")
            if level in distribution:
                distribution[level] += 1
        
        return distribution
    
    def get_statistics(self, scored_skills: List[Dict]) -> Dict:
        """
        Get statistics about skill confidence scores.
        
        Args:
            scored_skills: List of scored skill dictionaries
            
        Returns:
            Dictionary with statistics
        """
        if not scored_skills:
            return {}
        
        confidences = [s["confidence"] for s in scored_skills]
        
        return {
            "total_skills": len(scored_skills),
            "average_confidence": round(sum(confidences) / len(confidences), 3),
            "min_confidence": round(min(confidences), 3),
            "max_confidence": round(max(confidences), 3),
            "median_confidence": round(sorted(confidences)[len(confidences) // 2], 3),
            "distribution": self.get_confidence_distribution(scored_skills),
            "high_confidence_skills": len(self.filter_by_confidence(scored_skills, 0.7)),
        }