"""
Skill Normalization and Deduplication

This module handles:
- Normalizing skill names to canonical forms
- Deduplicating similar skills
- Merging skill information
- Resolving spelling variations
- Handling abbreviations and acronyms
"""

import re
from typing import Dict, List, Set, Tuple
from difflib import SequenceMatcher
from collections import defaultdict

from .skill_dictionary import (
    normalize_skill_name,
    get_all_skills,
    get_skill_by_name,
    SPELLING_VARIATIONS,
)

from utils.logger import logger


class SkillNormalizer:
    """
    Normalizes and standardizes skill names to canonical forms.
    """
    
    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize the skill normalizer.
        
        Args:
            similarity_threshold: Threshold for considering skills similar (0-1)
        """
        self.similarity_threshold = similarity_threshold
        self.all_skills = get_all_skills()
        self.canonical_skills = set(self.all_skills.keys())
        
    def normalize(self, skill_name: str) -> str or None:
        """
        Normalize a skill name to its canonical form.
        
        Args:
            skill_name: Raw skill name
            
        Returns:
            Canonical skill name or None if not recognized
        """
        if not skill_name:
            return None
        
        skill_name = skill_name.strip()
        
        # Try exact match
        if skill_name in self.canonical_skills:
            return skill_name
        
        # Try case-insensitive exact match
        skill_lower = skill_name.lower()
        for canonical in self.canonical_skills:
            if canonical.lower() == skill_lower:
                return canonical
        
        # Try spelling variations
        normalized = normalize_skill_name(skill_name)
        if normalized:
            return normalized
        
        # Try fuzzy matching
        fuzzy_match = self._fuzzy_match(skill_name)
        if fuzzy_match:
            return fuzzy_match
        
        return None
    
    def _fuzzy_match(self, skill_name: str) -> str or None:
        """
        Find best matching canonical skill using fuzzy matching.
        
        Args:
            skill_name: Skill name to match
            
        Returns:
            Best matching canonical skill or None
        """
        skill_lower = skill_name.lower()
        best_match = None
        best_score = 0
        
        for canonical in self.canonical_skills:
            score = SequenceMatcher(None, skill_lower, canonical.lower()).ratio()
            if score > best_score and score >= self.similarity_threshold:
                best_score = score
                best_match = canonical
        
        return best_match
    
    def normalize_batch(self, skills: List[str]) -> Dict[str, str]:
        """
        Normalize a batch of skill names.
        
        Args:
            skills: List of skill names
            
        Returns:
            Dictionary mapping original to normalized names
        """
        mapping = {}
        for skill in skills:
            normalized = self.normalize(skill)
            if normalized:
                mapping[skill] = normalized
        
        return mapping


class SkillDeduplicator:
    """
    Deduplicates and merges similar skills.
    Combines information from multiple mentions of the same skill.
    """
    
    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize the deduplicator.
        
        Args:
            similarity_threshold: Threshold for considering skills duplicates
        """
        self.similarity_threshold = similarity_threshold
        self.normalizer = SkillNormalizer(similarity_threshold)
        
    def deduplicate(self, skills_dict: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Deduplicate skills, merging similar ones into canonical forms.
        
        Args:
            skills_dict: Dictionary of skills with metadata
            
        Returns:
            Deduplicated dictionary with merged information
        """
        deduplicated = {}
        normalized_mapping = {}  # Track which skills map to which canonical
        
        # First pass: normalize all skill names
        for skill_name, skill_info in skills_dict.items():
            normalized = self.normalizer.normalize(skill_name)
            
            if normalized:
                if normalized not in deduplicated:
                    deduplicated[normalized] = self._create_merged_entry(
                        normalized, skill_info
                    )
                else:
                    # Merge with existing entry
                    deduplicated[normalized] = self._merge_skill_entries(
                        deduplicated[normalized], skill_info
                    )
                
                normalized_mapping[skill_name] = normalized
            else:
                # Couldn't normalize - keep as is but mark as unverified
                if skill_name not in deduplicated:
                    deduplicated[skill_name] = self._create_merged_entry(
                        skill_name, skill_info
                    )
                    deduplicated[skill_name]["verified"] = False
        
        logger.info(f"Deduplicated {len(skills_dict)} skills to {len(deduplicated)} unique skills")
        
        return deduplicated
    
    def _create_merged_entry(self, skill_name: str, skill_info: Dict) -> Dict:
        """Create a new merged skill entry"""
        return {
            "name": skill_name,
            "mentions": skill_info.get("mentions", 1),
            "sources": set([skill_info.get("source", "unknown")]),
            "positions": skill_info.get("positions", []),
            "confidence": skill_info.get("confidence", 0.5),
            "verified": True,
            "original_names": {skill_name},
            "skill_data": skill_info.get("skill_data", {}),
        }
    
    def _merge_skill_entries(self, existing: Dict, new: Dict) -> Dict:
        """Merge information from two skill entries"""
        # Sum mentions
        existing["mentions"] = existing.get("mentions", 0) + new.get("mentions", 1)
        
        # Combine sources
        existing["sources"].add(new.get("source", "unknown"))
        
        # Combine positions
        if "positions" in new and new["positions"]:
            existing["positions"].extend(new.get("positions", []))
        
        # Update confidence (use max)
        existing["confidence"] = max(
            existing.get("confidence", 0),
            new.get("confidence", 0)
        )
        
        # Track original names
        if "original_names" not in existing:
            existing["original_names"] = set()
        existing["original_names"].add(new.get("name", "unknown"))
        
        return existing
    
    def find_duplicates(self, skills_dict: Dict[str, Dict]) -> List[Tuple[str, str, float]]:
        """
        Find potential duplicate skills and their similarity scores.
        
        Args:
            skills_dict: Dictionary of skills
            
        Returns:
            List of (skill1, skill2, similarity_score) tuples
        """
        duplicates = []
        skills_list = list(skills_dict.keys())
        
        for i, skill1 in enumerate(skills_list):
            for skill2 in skills_list[i+1:]:
                similarity = self._calculate_similarity(skill1, skill2)
                
                if similarity >= self.similarity_threshold:
                    duplicates.append((skill1, skill2, similarity))
        
        # Sort by similarity (highest first)
        return sorted(duplicates, key=lambda x: x[2], reverse=True)
    
    def _calculate_similarity(self, skill1: str, skill2: str) -> float:
        """Calculate similarity between two skill names"""
        skill1_lower = skill1.lower()
        skill2_lower = skill2.lower()
        
        # Exact match
        if skill1_lower == skill2_lower:
            return 1.0
        
        # Use SequenceMatcher for similarity
        return SequenceMatcher(None, skill1_lower, skill2_lower).ratio()


class SkillMerger:
    """
    Merges skill information from multiple extraction attempts.
    Combines confidence scores, mentions, and metadata.
    """
    
    def __init__(self):
        """Initialize the skill merger"""
        self.deduplicator = SkillDeduplicator()
    
    def merge_multiple_extractions(self, extractions_list: List[Dict[str, Dict]]) -> Dict[str, Dict]:
        """
        Merge results from multiple skill extraction runs.
        
        Args:
            extractions_list: List of skill dictionaries from different extractors
            
        Returns:
            Merged dictionary with combined information
        """
        merged = {}
        
        # Collect all skills from all extractions
        for extraction in extractions_list:
            for skill_name, skill_info in extraction.items():
                normalized = self.deduplicator.normalizer.normalize(skill_name)
                
                if not normalized:
                    normalized = skill_name
                
                if normalized not in merged:
                    merged[normalized] = {
                        "name": normalized,
                        "mentions": 0,
                        "sources": set(),
                        "confidences": [],
                        "extraction_count": 0,
                    } 
                # Accumulate information
                merged[normalized]["mentions"] += skill_info.get("mentions", 1)
                merged[normalized]["sources"].add(skill_info.get("source", "unknown"))
                
                if "confidence" in skill_info:
                    merged[normalized]["confidences"].append(skill_info["confidence"])
                
                merged[normalized]["extraction_count"] += 1
        
        # Calculate aggregate statistics
        for skill_name, skill_info in merged.items():
            if skill_info["confidences"]:
                # Average confidence from multiple extractions
                skill_info["confidence"] = sum(skill_info["confidences"]) / len(skill_info["confidences"])
                skill_info["confidence"] = round(skill_info["confidence"], 3)
            
            # Remove temporary fields
            del skill_info["confidences"]
        
        logger.info(f"Merged {len(extractions_list)} extraction results into {len(merged)} unique skills")
        
        return merged


class SkillValidator:
    """
    Validates extracted skills against the known skill dictionary.
    Identifies verified and unverified skills.
    """
    
    def __init__(self):
        """Initialize the validator"""
        self.all_skills = get_all_skills()
        self.canonical_skills = set(self.all_skills.keys())
    
    def validate_skill(self, skill_name: str) -> Dict:
        """
        Validate a single skill.
        
        Args:
            skill_name: Skill name to validate
            
        Returns:
            Validation result dictionary
        """
        normalized = normalize_skill_name(skill_name)
        is_verified = normalized is not None
        
        return {
            "original_name": skill_name,
            "normalized_name": normalized,
            "is_verified": is_verified,
            "category": get_skill_by_name(normalized)["category"] if is_verified else None,
        }
    
    def validate_batch(self, skills_list: List[str]) -> Dict:
        """
        Validate a batch of skills.
        
        Args:
            skills_list: List of skill names
            
        Returns:
            Validation results grouped by verification status
        """
        verified = []
        unverified = []
        
        for skill in skills_list:
            result = self.validate_skill(skill)
            if result["is_verified"]:
                verified.append(result)
            else:
                unverified.append(result)
        
        return {
            "total_skills": len(skills_list),
            "verified_count": len(verified),
            "unverified_count": len(unverified),
            "verification_rate": round(len(verified) / len(skills_list) * 100, 2) if skills_list else 0,
            "verified_skills": verified,
            "unverified_skills": unverified,
        }
    
    def get_unverified_skills(self, skills_dict: Dict[str, Dict]) -> List[str]:
        """
        Get list of unverified skills from extraction.
        
        Args:
            skills_dict: Dictionary of extracted skills
            
        Returns:
            List of unverified skill names
        """
        unverified = []
        for skill_name in skills_dict.keys():
            if not self.validate_skill(skill_name)["is_verified"]:
                unverified.append(skill_name)
        
        return unverified