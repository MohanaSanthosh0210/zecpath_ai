"""
Skill Extraction Engine - Integration Example & Pipeline

This module demonstrates how to use the complete skill extraction pipeline:
1. Extract skills from resume text
2. Score confidence for each skill
3. Normalize and deduplicate
4. Generate structured output

Usage:
    from skills_integration import SkillExtractionPipeline
    
    pipeline = SkillExtractionPipeline()
    results = pipeline.process_resume(resume_text)
"""

import json
from typing import Dict, List
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .skill_extractor import SkillExtractor, SkillExtractorAdvanced
from .skill_confidence_scorer import SkillConfidenceScorer
from .skill_normalizer import SkillNormalizer, SkillDeduplicator, SkillValidator
from utils.logger import logger


class SkillExtractionPipeline:
    """
    Complete skill extraction pipeline.
    
    Process flow:
    1. Skill Extraction: Find all potential skills in resume text
    2. Normalization: Convert to canonical skill names
    3. Deduplication: Merge similar skills
    4. Confidence Scoring: Calculate confidence for each skill
    5. Validation: Verify against master dictionary
    6. Structured Output: Format results for downstream use
    """
    
    def __init__(self, use_nlp=False, nlp_model=None, fuzzy_threshold=0.75):
        """
        Initialize the skill extraction pipeline.
        
        Args:
            use_nlp: Whether to use advanced NLP extraction
            nlp_model: spaCy model name for NLP
            fuzzy_threshold: Threshold for fuzzy matching
        """
        # Initialize components
        if use_nlp and nlp_model:
            self.extractor = SkillExtractorAdvanced(nlp_model=nlp_model, fuzzy_threshold=fuzzy_threshold)
        else:
            self.extractor = SkillExtractor(fuzzy_threshold=fuzzy_threshold)
        
        self.normalizer = SkillNormalizer(similarity_threshold=0.85)
        self.deduplicator = SkillDeduplicator(similarity_threshold=0.85)
        self.scorer = SkillConfidenceScorer()
        self.validator = SkillValidator()
        
        logger.info("SkillExtractionPipeline initialized")
    
    def process_resume(self, resume_text: str, min_confidence: float = 0.5) -> Dict:
        """
        Process a resume and extract skills with confidence scores.
        
        Args:
            resume_text: Raw resume text
            min_confidence: Minimum confidence threshold for skills
            
        Returns:
            Structured dictionary with extracted skills and metadata
        """
        logger.info("Starting skill extraction pipeline")
        
        # Step 1: Extract skills
        logger.info("Step 1: Extracting skills from text")
        extracted = self.extractor.extract_skills(resume_text)
        logger.info(f"Extracted {len(extracted)} skills")
        
        # Step 2: Normalize skills
        logger.info("Step 2: Normalizing skill names")
        normalized = {}
        for skill_name, skill_info in extracted.items():
            canonical_name = self.normalizer.normalize(skill_name)
            if canonical_name:
                normalized[canonical_name] = skill_info
        
        # Step 3: Deduplicate
        logger.info("Step 3: Deduplicating skills")
        deduplicated = self.deduplicator.deduplicate(normalized)
        
        # Step 4: Score confidence
        logger.info("Step 4: Scoring skill confidence")
        scored_skills = []
        for skill_name, skill_info in deduplicated.items():
            scored = self.scorer.score_skill(
                skill_info,
                context={"text": resume_text}
            )
            scored_skills.append(scored)
        
        # Sort by confidence
        scored_skills.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Step 5: Filter by confidence
        filtered_skills = self.scorer.filter_by_confidence(scored_skills, min_confidence)
        logger.info(f"Filtered to {len(filtered_skills)} skills above {min_confidence} confidence")
        
        # Step 6: Validate
        logger.info("Step 5: Validating skills")
        validated_skills = self._add_validation(filtered_skills)
        
        # Step 7: Structure output
        logger.info("Step 6: Structuring output")
        structured_output = self._structure_output(validated_skills, scored_skills)
        
        logger.info("Skill extraction pipeline completed successfully")
        
        return structured_output
    
    def _add_validation(self, scored_skills: List[Dict]) -> List[Dict]:
        """Add validation information to scored skills"""
        for skill in scored_skills:
            skill_name = skill["skill_name"]
            validation = self.validator.validate_skill(skill_name)
            skill["is_verified"] = validation["is_verified"]
            skill["normalized_name"] = validation["normalized_name"]
        
        return scored_skills
    
    def _structure_output(self, filtered_skills: List[Dict], all_scored_skills: List[Dict]) -> Dict:
        """
        Structure the output in the format specified by resume_schema.json
        """
        # Group by category
        by_category = {}
        for skill in filtered_skills:
            skill_name = skill["skill_name"]
            component_scores = skill.get("component_scores", {})
            category = list(component_scores.keys())[0] if component_scores else "unknown"
            
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(skill_name)
        
        # Get confidence distribution
        stats = self.scorer.get_statistics(all_scored_skills)
        
        # Build structured output
        output = {
            "extraction_metadata": {
                "extraction_method": "NLP-based with pattern matching and fuzzy matching",
                "total_skills_extracted": len(all_scored_skills),
                "filtered_skills_count": len(filtered_skills),
                "min_confidence_threshold": 0.5,
                "pipeline_version": "1.0"
            },
            "skills": filtered_skills,
            "skills_by_category": by_category,
            "statistics": {
                "total_skills": stats.get("total_skills", 0),
                "average_confidence": stats.get("average_confidence", 0),
                "min_confidence": stats.get("min_confidence", 0),
                "max_confidence": stats.get("max_confidence", 0),
                "median_confidence": stats.get("median_confidence", 0),
                "high_confidence_skills": stats.get("high_confidence_skills", 0),
                "confidence_distribution": stats.get("distribution", {})
            },
            "top_skills": [
                {"name": name, "confidence": conf}
                for name, conf in [(s["skill_name"], s["confidence"]) for s in filtered_skills[:10]]
            ]
        }
        
        return output
    
    def process_batch(self, resumes: List[Dict], min_confidence: float = 0.5) -> List[Dict]:
        """
        Process multiple resumes.
        
        Args:
            resumes: List of resume dictionaries with 'text' key
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of processed results
        """
        results = []
        for i, resume in enumerate(resumes):
            logger.info(f"Processing resume {i+1}/{len(resumes)}")
            result = self.process_resume(resume.get("text", ""), min_confidence)
            result["resume_id"] = resume.get("id", f"resume_{i}")
            results.append(result)
        
        return results
    
    def save_results(self, results: Dict, output_dir: str = "data/extracted_skills") -> str:
        """
        Save extraction results to a JSON file.
        
        Args:
            results: Extraction results dictionary
            output_dir: Directory to save results
            
        Returns:
            Path to saved file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        resume_id = results.get("resume_id", "resume")
        filename = f"{resume_id}_skills_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Convert sets to lists for JSON serialization
        serializable_results = self._make_serializable(results)
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved skill extraction results to {filepath}")
        return filepath
    
    def save_batch_results(self, results_list: List[Dict], output_dir: str = "data/extracted_skills") -> List[str]:
        """
        Save multiple extraction results to files.
        
        Args:
            results_list: List of extraction results
            output_dir: Directory to save results
            
        Returns:
            List of saved file paths
        """
        filepaths = []
        for result in results_list:
            filepath = self.save_results(result, output_dir)
            filepaths.append(filepath)
        
        logger.info(f"Saved {len(filepaths)} skill extraction results")
        return filepaths
    
    def save_summary(self, results_list: List[Dict], output_dir: str = "data/extracted_skills") -> str:
        """
        Save a summary of all extraction results.
        
        Args:
            results_list: List of extraction results
            output_dir: Directory to save summary
            
        Returns:
            Path to saved summary file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create summary
        summary = {
            "extraction_date": datetime.now().isoformat(),
            "total_resumes": len(results_list),
            "total_unique_skills": len(set(
                skill["skill_name"]
                for result in results_list
                for skill in result.get("skills", [])
            )),
            "avg_confidence": sum(
                result.get("statistics", {}).get("average_confidence", 0)
                for result in results_list
            ) / len(results_list) if results_list else 0,
            "results": []
        }
        
        # Add per-resume stats
        for result in results_list:
            resume_summary = {
                "resume_id": result.get("resume_id", "unknown"),
                "skills_extracted": result.get("extraction_metadata", {}).get("filtered_skills_count", 0),
                "average_confidence": result.get("statistics", {}).get("average_confidence", 0),
                "high_confidence_skills": result.get("statistics", {}).get("high_confidence_skills", 0),
                "top_skills": [
                    {"name": s["name"], "confidence": s["confidence"]}
                    for s in result.get("top_skills", [])[:5]
                ]
            }
            summary["results"].append(resume_summary)
        
        # Save summary
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(output_dir, f"skills_summary_{timestamp}.json")
        
        serializable_summary = self._make_serializable(summary)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved skill extraction summary to {filepath}")
        return filepath
    
    def _make_serializable(self, obj):
        """
        Convert non-serializable objects (sets, etc.) to JSON-serializable types.
        """
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        else:
            return obj


# ==================== Example Usage ====================

def example_basic_extraction():
    """Example: Basic skill extraction from resume text"""
    
    sample_resume = """
    Senior Software Engineer with 5+ years of experience.
    
    Technical Skills:
    - Languages: Python, JavaScript, Java, C++
    - Web Frameworks: React, Django, Express.js, Spring Boot
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud: AWS (EC2, S3, Lambda), Google Cloud
    - DevOps: Docker, Kubernetes, Jenkins, GitLab CI/CD
    - Data Science: TensorFlow, PyTorch, scikit-learn, Pandas
    
    Experience:
    - Developed MERN stack applications with React and Node.js
    - Led microservices architecture migration
    - Implemented CI/CD pipelines using Jenkins and Docker
    
    Skills:
    - Proficient in Python and JavaScript
    - Expert in React and Django
    - Advanced Kubernetes and Docker expertise
    - Strong background in Machine Learning and Deep Learning
    """
    
    pipeline = SkillExtractionPipeline()
    results = pipeline.process_resume(sample_resume, min_confidence=0.5)
    
    print("\n" + "="*80)
    print("SKILL EXTRACTION RESULTS")
    print("="*80)
    print(f"\nTotal Skills Extracted: {results['extraction_metadata']['total_skills_extracted']}")
    print(f"Filtered Skills (>= 0.5 confidence): {results['extraction_metadata']['filtered_skills_count']}")
    
    print("\n" + "-"*80)
    print("TOP 10 SKILLS")
    print("-"*80)
    for i, skill in enumerate(results["top_skills"], 1):
        print(f"{i:2d}. {skill['name']:<30} Confidence: {skill['confidence']:.1%}")
    
    print("\n" + "-"*80)
    print("STATISTICS")
    print("-"*80)
    stats = results["statistics"]
    print(f"Average Confidence: {stats['average_confidence']:.1%}")
    print(f"High Confidence Skills (>= 70%): {stats['high_confidence_skills']}")
    print(f"Confidence Distribution: {stats['confidence_distribution']}")
    
    return results


def example_detailed_analysis():
    """Example: Detailed skill analysis with all metadata"""
    
    sample_resume = """
    Full Stack Developer
    
    I have expertise in:
    - React and Vue.js for frontend
    - Node.js and Express for backend
    - MongoDB and PostgreSQL
    - Docker containerization
    - AWS services (S3, Lambda, RDS)
    - Git version control
    - Agile and Scrum methodologies
    
    Years of Experience:
    - 3+ years with Python
    - 4+ years with JavaScript
    - 2+ years with DevOps
    """
    
    pipeline = SkillExtractionPipeline()
    results = pipeline.process_resume(sample_resume, min_confidence=0.4)
    
    print("\n" + "="*80)
    print("DETAILED SKILL ANALYSIS")
    print("="*80)
    
    print("\nAll Extracted Skills with Scores:")
    print("-" * 80)
    print(f"{'Skill Name':<30} {'Confidence':<12} {'Sources':<20} {'Verified':<10}")
    print("-" * 80)
    
    for skill in results["skills"][:15]:
        sources = ", ".join(skill.get("sources", [])[:2])
        verified = "✓" if skill.get("is_verified") else "✗"
        print(f"{skill['skill_name']:<30} {skill['confidence']:.1%}          {sources:<20} {verified:<10}")
    
    return results


if __name__ == "__main__":
    # Run examples
    print("\n\n" + "="*80)
    print("SKILL EXTRACTION ENGINE - INTEGRATION EXAMPLES")
    print("="*80)
    
    # Example 1: Basic extraction
    print("\n\n>>> EXAMPLE 1: BASIC EXTRACTION")
    example_basic_extraction()
    
    # Example 2: Detailed analysis
    print("\n\n>>> EXAMPLE 2: DETAILED ANALYSIS")
    example_detailed_analysis()
    
    # Example 3: Batch processing with file saving
    print("\n\n>>> EXAMPLE 3: BATCH PROCESSING WITH FILE SAVING")
    
    sample_resumes = [
        {
            "id": "resume_1",
            "text": """
            Data Scientist
            Skills: Python, TensorFlow, PyTorch, Pandas, NumPy, scikit-learn
            Experience: 5+ years in Machine Learning and Deep Learning
            """
        },
        {
            "id": "resume_2",
            "text": """
            DevOps Engineer
            Skills: Docker, Kubernetes, AWS, Terraform, Jenkins, GitLab CI/CD
            Experience: 4+ years in cloud infrastructure and automation
            """
        },
    ]
    
    pipeline = SkillExtractionPipeline()
    results = pipeline.process_batch(sample_resumes, min_confidence=0.5)
    
    print("\n" + "="*80)
    print("BATCH PROCESSING RESULTS")
    print("="*80)
    
    for result in results:
        print(f"\n{result['resume_id']}: {result['extraction_metadata']['filtered_skills_count']} skills")
        print(f"Average Confidence: {result['statistics']['average_confidence']:.1%}")
    
    # Save batch results
    print("\n" + "-"*80)
    print("Saving Results to Files...")
    print("-"*80)
    
    saved_files = pipeline.save_batch_results(results)
    for filepath in saved_files:
        print(f"✓ Saved: {filepath}")
    
    # Save summary
    summary_file = pipeline.save_summary(results)
    print(f"\n✓ Summary: {summary_file}")
    
    print("\n\n" + "="*80)
    print("Examples completed! Check data/extracted_skills/ for results.")
    print("="*80)