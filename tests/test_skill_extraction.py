"""
Skill Extraction Test Suite

Tests the skill extraction engine with real resume data from the workspace.
"""

import os
import sys
import json
from pathlib import Path

import os
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.skill_extractor import SkillExtractor
from skills.skill_confidence_scorer import SkillConfidenceScorer
from skills.skill_normalizer import SkillNormalizer, SkillValidator
from skills.skills_integration import SkillExtractionPipeline
from utils.logger import logger


def test_basic_extraction():
    """Test basic skill extraction"""
    print("\n" + "="*80)
    print("TEST 1: BASIC SKILL EXTRACTION")
    print("="*80)
    
    test_text = """
    Senior Full Stack Developer with 6+ years of experience
    
    Technical Skills:
    - Languages: Python, JavaScript, Java, TypeScript
    - Frontend: React, Vue.js, Angular, HTML5, CSS3
    - Backend: Node.js, Django, Flask, FastAPI
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud: AWS (EC2, S3, Lambda), Google Cloud Platform
    - DevOps: Docker, Kubernetes, Jenkins, GitLab CI/CD
    - Tools: Git, GitHub, Jira, Confluence
    
    Experience:
    - Architected MERN stack applications serving 100k+ users
    - Implemented microservices using Kubernetes
    - Led team of 5 developers in Agile environment
    - Proficient in Python and JavaScript
    """
    
    extractor = SkillExtractor()
    skills = extractor.extract_skills(test_text)
    
    print(f"\nExtracted {len(skills)} skills:")
    for skill_name, skill_info in sorted(skills.items())[:20]:
        print(f"  - {skill_name:<30} ({skill_info.get('source', 'unknown')})")
    
    return skills


def test_confidence_scoring(skills):
    """Test confidence scoring"""
    print("\n" + "="*80)
    print("TEST 2: CONFIDENCE SCORING")
    print("="*80)
    
    scorer = SkillConfidenceScorer()
    
    # Score a few key skills
    sample_skills = list(skills.items())[:5]
    
    print("\nConfidence Scores:")
    print(f"{'Skill Name':<30} {'Confidence':<12} {'Level':<12}")
    print("-" * 60)
    
    for skill_name, skill_info in sample_skills:
        scored = scorer.score_skill(skill_info)
        print(f"{skill_name:<30} {scored['confidence']:.1%}     {scored['confidence_level']:<12}")
    
    return scorer


def test_normalization(skills):
    """Test skill normalization"""
    print("\n" + "="*80)
    print("TEST 3: SKILL NORMALIZATION")
    print("="*80)
    
    normalizer = SkillNormalizer()
    
    # Test some variations
    test_skills = ["pythno", "JS", "react.js", "djangoo", "postgre"]
    
    print("\nNormalization Examples:")
    print(f"{'Original':<20} {'Normalized':<20} {'Matched':<10}")
    print("-" * 60)
    
    for skill in test_skills:
        normalized = normalizer.normalize(skill)
        matched = "[Y]" if normalized else "[N]"
        print(f"{skill:<20} {str(normalized):<20} {matched:<10}")


def test_validation():
    """Test skill validation"""
    print("\n" + "="*80)
    print("TEST 4: SKILL VALIDATION")
    print("="*80)
    
    validator = SkillValidator()
    
    test_skills = ["Python", "React", "Unknown Skill", "Django", "Jira"]
    
    results = validator.validate_batch(test_skills)
    
    print(f"\nValidation Results:")
    print(f"Total Skills: {results['total_skills']}")
    print(f"Verified: {results['verified_count']}")
    print(f"Unverified: {results['unverified_count']}")
    print(f"Verification Rate: {results['verification_rate']}%")
    
    print(f"\nVerified Skills:")
    for skill in results["verified_skills"]:
        print(f"  [Y] {skill['original_name']:<20} → {skill['normalized_name']:<20} ({skill['category']})")
    
    if results["unverified_skills"]:
        print(f"\nUnverified Skills:")
        for skill in results["unverified_skills"]:
            print(f"  [N] {skill['original_name']}")


def test_pipeline():
    """Test complete extraction pipeline"""
    print("\n" + "="*80)
    print("TEST 5: COMPLETE EXTRACTION PIPELINE")
    print("="*80)
    
    resume_text = """
    Data Engineer
    
    I am a results-oriented Data Engineer with 4+ years of experience building 
    scalable data pipelines and platforms.
    
    Technical Expertise:
    - Languages: Python, Scala, SQL, Java
    - Big Data: Apache Spark, Hadoop, Kafka, Airflow
    - Cloud: AWS (S3, EC2, RDS, Lambda), Google Cloud
    - Databases: PostgreSQL, MongoDB, Elasticsearch, Cassandra
    - Tools: Docker, Kubernetes, Git, Jenkins
    - Data Processing: Pandas, NumPy, PySpark
    
    Professional Experience:
    - Architected ETL pipelines using Airflow and Spark
    - Expert in SQL optimization and database design
    - Strong background in building microservices with Python and FastAPI
    - Proficient with AWS infrastructure automation
    """
    
    pipeline = SkillExtractionPipeline()
    results = pipeline.process_resume(resume_text, min_confidence=0.5)
    
    print(f"\nPipeline Results:")
    print(f"Total Skills Extracted: {results['extraction_metadata']['total_skills_extracted']}")
    print(f"Filtered Skills (>= 0.5): {results['extraction_metadata']['filtered_skills_count']}")
    
    stats = results["statistics"]
    print(f"\nStatistics:")
    print(f"  Average Confidence: {stats['average_confidence']:.1%}")
    print(f"  High Confidence Skills: {stats['high_confidence_skills']}")
    print(f"  Confidence Distribution: {stats['confidence_distribution']}")
    
    print(f"\nTop 10 Skills:")
    for i, skill in enumerate(results["top_skills"][:10], 1):
        print(f"  {i:2d}. {skill['name']:<30} {skill['confidence']:.1%}")


def test_with_real_resumes():
    """Test with actual resume data from workspace"""
    print("\n" + "="*80)
    print("TEST 6: REAL RESUME DATA")
    print("="*80)
    
    resumes_dir = Path(__file__).parent.parent / "data" / "cleaned"
    
    if not resumes_dir.exists():
        print(f"Resumes directory not found: {resumes_dir}")
        return
    
    pipeline = SkillExtractionPipeline()
    
    resume_files = list(resumes_dir.glob("*.json"))
    if not resume_files:
        print("No resume files found")
        return
    
    print(f"\nProcessing {len(resume_files)} resume(s)...")
    
    all_results = []
    saved_files = []
    
    for resume_file in resume_files[:3]:  # Process first 3
        try:
            with open(resume_file, 'r', encoding='utf-8') as f:
                resume_data = json.load(f)
                resume_text = resume_data.get("cleaned_text", "")
            
            if not resume_text:
                continue
            
            print(f"\n{resume_file.name}:")
            results = pipeline.process_resume(resume_text, min_confidence=0.5)
            results["resume_id"] = resume_file.stem  # Use filename without extension
            
            # Save individual results
            saved_file = pipeline.save_results(results)
            saved_files.append(saved_file)
            all_results.append(results)
            
            print(f"  Skills Extracted: {results['extraction_metadata']['filtered_skills_count']}")
            print(f"  Saved to: {saved_file}")
            print(f"  Top 5 Skills:")
            for i, skill in enumerate(results["top_skills"][:5], 1):
                print(f"    {i}. {skill['name']:<25} {skill['confidence']:.1%}")
        
        except Exception as e:
            logger.error(f"Error processing {resume_file}: {e}")
            continue
    
    # Save summary
    if all_results:
        summary_file = pipeline.save_summary(all_results)
        print(f"\n\nSummary saved to: {summary_file}")
    
    print(f"\nSaved {len(saved_files)} skill extraction files")


def main():
    """Run all tests"""
    print("\n")
    print("="*80)
    print("SKILL EXTRACTION ENGINE - TEST SUITE")
    print("="*80)
    
    try:
        # Run tests in sequence
        skills = test_basic_extraction()
        test_confidence_scoring(skills)
        test_normalization(skills)
        test_validation()
        test_pipeline()
        test_with_real_resumes()
        
        print("\n" + "="*80)
        print("ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")
    
    except Exception as e:
        logger.error(f"Test error: {e}", exc_info=True)
        print(f"\n[ERROR] Test failed: {e}\n")


if __name__ == "__main__":
    main()