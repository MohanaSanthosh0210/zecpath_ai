"""
Master Skill Dictionary for Resume Skill Extraction

This module contains comprehensive skill dictionaries organized by categories:
- Technical Skills
- Business Skills
- Creative Skills
- Soft Skills

It also includes:
- Skill synonyms for normalization
- Skill stacks (combined skill sets)
- Spelling variations
"""

# ==================== CORE SKILL DICTIONARIES ====================

TECHNICAL_SKILLS = {
    # Programming Languages
    "Python": {"aliases": ["python3", "py", "python2"], "category": "programming_language"},
    "Java": {"aliases": ["java8", "java11", "java17"], "category": "programming_language"},
    "JavaScript": {"aliases": ["js", "node.js", "nodejs", "typescript", "ts"], "category": "programming_language"},
    "C++": {"aliases": ["cpp", "c++11", "c++17", "c++20"], "category": "programming_language"},
    "C#": {"aliases": ["csharp", "c#", "dotnet"], "category": "programming_language"},
    "Go": {"aliases": ["golang", "go lang"], "category": "programming_language"},
    "Rust": {"aliases": ["rust lang"], "category": "programming_language"},
    "SQL": {"aliases": ["mysql", "postgresql", "sql server", "plsql"], "category": "programming_language"},
    "PHP": {"aliases": ["php7", "php8"], "category": "programming_language"},
    "R": {"aliases": ["r programming"], "category": "programming_language"},
    "Ruby": {"aliases": ["ruby on rails", "rails"], "category": "programming_language"},
    "Kotlin": {"aliases": ["kotlin lang"], "category": "programming_language"},
    "Swift": {"aliases": ["swift ios"], "category": "programming_language"},
    "Scala": {"aliases": ["scala lang"], "category": "programming_language"},

    # Web Frameworks & Libraries
    "React": {"aliases": ["reactjs", "react.js", "react native"], "category": "web_framework"},
    "Angular": {"aliases": ["angularjs", "angular.js", "angular 2+"], "category": "web_framework"},
    "Vue.js": {"aliases": ["vuejs", "vue"], "category": "web_framework"},
    "Django": {"aliases": ["django framework", "django rest"], "category": "web_framework"},
    "Flask": {"aliases": ["flask framework"], "category": "web_framework"},
    "Spring": {"aliases": ["spring boot", "spring framework"], "category": "web_framework"},
    "Express.js": {"aliases": ["expressjs", "express"], "category": "web_framework"},
    "FastAPI": {"aliases": ["fastapi framework"], "category": "web_framework"},
    "Laravel": {"aliases": ["laravel framework"], "category": "web_framework"},
    "ASP.NET": {"aliases": ["asp net", "asp.net core"], "category": "web_framework"},

    # Databases & Data Storage
    "MySQL": {"aliases": ["mysql8"], "category": "database"},
    "PostgreSQL": {"aliases": ["postgres", "postgresql"], "category": "database"},
    "MongoDB": {"aliases": ["mongo", "mongodb nosql"], "category": "database"},
    "Redis": {"aliases": ["redis cache"], "category": "database"},
    "Elasticsearch": {"aliases": ["elastic", "elasticsearch"], "category": "database"},
    "Cassandra": {"aliases": ["cassandra database"], "category": "database"},
    "DynamoDB": {"aliases": ["dynamodb aws"], "category": "database"},
    "Firebase": {"aliases": ["firebase database"], "category": "database"},
    "Neo4j": {"aliases": ["neo4j graph"], "category": "database"},
    "Oracle": {"aliases": ["oracle database"], "category": "database"},
    "SQL Server": {"aliases": ["sqlserver", "mssql"], "category": "database"},

    # Cloud Platforms
    "AWS": {"aliases": ["amazon aws", "amazon web services"], "category": "cloud"},
    "Azure": {"aliases": ["microsoft azure"], "category": "cloud"},
    "Google Cloud": {"aliases": ["gcp", "google cloud platform"], "category": "cloud"},
    "Heroku": {"aliases": ["heroku platform"], "category": "cloud"},
    "DigitalOcean": {"aliases": ["digital ocean"], "category": "cloud"},
    "Kubernetes": {"aliases": ["k8s", "k8"], "category": "cloud"},
    "Docker": {"aliases": ["docker containerization"], "category": "cloud"},

    # DevOps & Tools
    "Git": {"aliases": ["github", "gitlab", "bitbucket", "version control"], "category": "devops"},
    "Jenkins": {"aliases": ["jenkins ci"], "category": "devops"},
    "GitLab CI": {"aliases": ["gitlab ci/cd"], "category": "devops"},
    "GitHub Actions": {"aliases": ["github actions", "actions"], "category": "devops"},
    "Terraform": {"aliases": ["terraform iac"], "category": "devops"},
    "Ansible": {"aliases": ["ansible automation"], "category": "devops"},
    "Linux": {"aliases": ["ubuntu", "centos", "linux administration", "unix"], "category": "devops"},
    "Docker": {"aliases": ["docker containers"], "category": "devops"},
    "Nginx": {"aliases": ["nginx server"], "category": "devops"},
    "Apache": {"aliases": ["apache server"], "category": "devops"},

    # Data Science & ML
    "Machine Learning": {"aliases": ["ml", "machine learning"], "category": "data_science"},
    "Deep Learning": {"aliases": ["neural networks", "deep learning"], "category": "data_science"},
    "TensorFlow": {"aliases": ["tensorflow", "tf"], "category": "data_science"},
    "PyTorch": {"aliases": ["pytorch", "torch"], "category": "data_science"},
    "scikit-learn": {"aliases": ["sklearn", "scikit learn"], "category": "data_science"},
    "Pandas": {"aliases": ["pandas library", "pd"], "category": "data_science"},
    "NumPy": {"aliases": ["numpy", "numerical python"], "category": "data_science"},
    "Matplotlib": {"aliases": ["matplotlib plotting"], "category": "data_science"},
    "Jupyter": {"aliases": ["jupyter notebook"], "category": "data_science"},
    "Data Analysis": {"aliases": ["data analytics", "analytics"], "category": "data_science"},
    "Natural Language Processing": {"aliases": ["nlp", "nlp"], "category": "data_science"},
    "Computer Vision": {"aliases": ["cv", "image processing"], "category": "data_science"},

    # Frontend Technologies
    "HTML": {"aliases": ["html5", "html/css"], "category": "frontend"},
    "CSS": {"aliases": ["css3", "sass", "scss", "less"], "category": "frontend"},
    "Bootstrap": {"aliases": ["bootstrap framework"], "category": "frontend"},
    "Tailwind CSS": {"aliases": ["tailwindcss", "tailwind"], "category": "frontend"},
    "Material Design": {"aliases": ["material ui", "material"], "category": "frontend"},
    "AJAX": {"aliases": ["asynchronous javascript"], "category": "frontend"},
    "Webpack": {"aliases": ["webpack bundler"], "category": "frontend"},

    # Testing & QA
    "Unit Testing": {"aliases": ["unittest", "unit tests"], "category": "testing"},
    "Jest": {"aliases": ["jest testing"], "category": "testing"},
    "Pytest": {"aliases": ["pytest framework"], "category": "testing"},
    "Selenium": {"aliases": ["selenium testing"], "category": "testing"},
    "JUnit": {"aliases": ["junit testing"], "category": "testing"},
    "TestNG": {"aliases": ["testng framework"], "category": "testing"},
    "Mocha": {"aliases": ["mocha testing"], "category": "testing"},

    # APIs & Communication
    "REST API": {"aliases": ["rest", "restful api"], "category": "api"},
    "GraphQL": {"aliases": ["graphql api"], "category": "api"},
    "SOAP": {"aliases": ["soap web services"], "category": "api"},
    "WebSocket": {"aliases": ["websockets", "socket.io"], "category": "api"},
    "gRPC": {"aliases": ["grpc"], "category": "api"},

    # Design Patterns & Architecture
    "Microservices": {"aliases": ["microservices architecture"], "category": "architecture"},
    "Design Patterns": {"aliases": ["design patterns"], "category": "architecture"},
    "SOLID Principles": {"aliases": ["solid"], "category": "architecture"},
    "MVC": {"aliases": ["model view controller"], "category": "architecture"},
    "Agile": {"aliases": ["agile methodology", "scrum", "kanban"], "category": "architecture"},

    # Version Control & Collaboration
    "Jira": {"aliases": ["jira", "atlassian jira"], "category": "tools"},
    "Confluence": {"aliases": ["confluence", "wiki"], "category": "tools"},
    "Slack": {"aliases": ["slack communication"], "category": "tools"},
}

BUSINESS_SKILLS = {
    "Project Management": {"aliases": ["project coordination", "pm"], "category": "management"},
    "Product Management": {"aliases": ["product manager", "product lead"], "category": "management"},
    "Business Analysis": {"aliases": ["business analyst", "ba"], "category": "management"},
    "Requirements Gathering": {"aliases": ["requirements elicitation", "stakeholder analysis"], "category": "management"},
    "Resource Planning": {"aliases": ["resource allocation", "capacity planning"], "category": "management"},
    "Risk Management": {"aliases": ["risk assessment"], "category": "management"},
    "Process Improvement": {"aliases": ["optimization", "lean", "six sigma"], "category": "management"},
    "Strategic Planning": {"aliases": ["strategy", "business strategy"], "category": "management"},
    "Financial Analysis": {"aliases": ["financial modeling", "budgeting"], "category": "finance"},
    "Budget Management": {"aliases": ["budgeting", "cost control"], "category": "finance"},
    "Sales": {"aliases": ["selling", "sales management", "account management"], "category": "sales"},
    "Marketing": {"aliases": ["digital marketing", "content marketing", "seo"], "category": "marketing"},
    "Customer Service": {"aliases": ["customer support", "client management"], "category": "customer"},
    "Negotiation": {"aliases": ["contract negotiation"], "category": "management"},
    "Communication": {"aliases": ["presentation", "public speaking"], "category": "soft_skills"},
    "Team Leadership": {"aliases": ["leadership", "team management"], "category": "management"},
    "Data-Driven Decision Making": {"aliases": ["analytics", "business intelligence"], "category": "management"},
}

CREATIVE_SKILLS = {
    "Graphic Design": {"aliases": ["design", "visual design", "ui design"], "category": "design"},
    "UI/UX Design": {"aliases": ["user experience", "ux", "ui"], "category": "design"},
    "Web Design": {"aliases": ["web designer"], "category": "design"},
    "Motion Graphics": {"aliases": ["animation", "video editing"], "category": "design"},
    "Adobe Creative Suite": {"aliases": ["photoshop", "illustrator", "premiere", "indesign"], "category": "design_tools"},
    "Figma": {"aliases": ["figma design"], "category": "design_tools"},
    "Sketch": {"aliases": ["sketch design"], "category": "design_tools"},
    "Content Writing": {"aliases": ["copywriting", "technical writing"], "category": "writing"},
    "Video Production": {"aliases": ["videography", "film"], "category": "media"},
    "Photography": {"aliases": ["photo editing"], "category": "media"},
}

SOFT_SKILLS = {
    "Critical Thinking": {"aliases": ["analytical skills", "problem solving"], "category": "cognitive"},
    "Adaptability": {"aliases": ["flexibility", "versatility"], "category": "interpersonal"},
    "Collaboration": {"aliases": ["teamwork", "cooperation"], "category": "interpersonal"},
    "Communication": {"aliases": ["presentation skills", "writing skills"], "category": "interpersonal"},
    "Time Management": {"aliases": ["organizational skills", "prioritization"], "category": "productivity"},
    "Attention to Detail": {"aliases": ["meticulousness"], "category": "productivity"},
    "Creativity": {"aliases": ["creative thinking", "innovation"], "category": "cognitive"},
    "Emotional Intelligence": {"aliases": ["eq", "empathy"], "category": "interpersonal"},
    "Conflict Resolution": {"aliases": ["mediation"], "category": "interpersonal"},
    "Mentoring": {"aliases": ["coaching", "training"], "category": "interpersonal"},
}

# ==================== SKILL STACKS (Combined Skill Sets) ====================

SKILL_STACKS = {
    "MERN": {"skills": ["MongoDB", "Express.js", "React", "Node.js"], "description": "JavaScript full-stack"},
    "MEAN": {"skills": ["MongoDB", "Express.js", "Angular", "Node.js"], "description": "JavaScript full-stack"},
    "LAMP": {"skills": ["Linux", "Apache", "MySQL", "PHP"], "description": "Web stack"},
    "JAM": {"skills": ["JavaScript", "APIs", "Markdown"], "description": "Jamstack architecture"},
    "LEMP": {"skills": ["Linux", "Nginx", "MySQL", "PHP"], "description": "Web stack"},
    "Full Stack": {"skills": ["Frontend", "Backend", "Database"], "description": "Full-stack development"},
    "DevOps": {"skills": ["Docker", "Kubernetes", "CI/CD"], "description": "DevOps tools"},
    "AWS Ecosystem": {"skills": ["AWS", "Lambda", "S3", "RDS"], "description": "AWS services"},
    "ML Pipeline": {"skills": ["Python", "TensorFlow", "Data Analysis"], "description": "Machine learning"},
}

# ==================== SPELLING VARIATIONS & NORMALIZATIONS ====================

SPELLING_VARIATIONS = {
    "javascript": "JavaScript",
    "js": "JavaScript",
    "python3": "Python",
    "py": "Python",
    "java8": "Java",
    "java11": "Java",
    "golang": "Go",
    "postgres": "PostgreSQL",
    "mongo": "MongoDB",
    "react": "React",
    "angular": "Angular",
    "vue": "Vue.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "cpp": "C++",
    "csharp": "C#",
    "dotnet": "C#",
    "mvc": "MVC",
    "rest": "REST API",
    "restful": "REST API",
    "graphql": "GraphQL",
    "docker": "Docker",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "gcp": "Google Cloud",
    "azure": "Azure",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "ux": "UI/UX Design",
    "ui": "UI/UX Design",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "ci/cd": "CI/CD",
    "agile": "Agile",
    "scrum": "Scrum",
    "kanban": "Kanban",
    "selenium": "Selenium",
    "jest": "Jest",
    "pytest": "Pytest",
    "junit": "JUnit",
    "jenkins": "Jenkins",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "nginx": "Nginx",
    "apache": "Apache",
}

# ==================== UNIFIED SKILL REGISTRY ====================

def get_all_skills():
    """Combine all skill dictionaries into one registry"""
    return {
        **TECHNICAL_SKILLS,
        **BUSINESS_SKILLS,
        **CREATIVE_SKILLS,
        **SOFT_SKILLS
    }


def get_skill_by_name(skill_name):
    """Retrieve skill definition by name (case-insensitive)"""
    all_skills = get_all_skills()
    # Try exact match first
    if skill_name in all_skills:
        return all_skills[skill_name]
    
    # Try case-insensitive match
    skill_lower = skill_name.lower()
    for skill, definition in all_skills.items():
        if skill.lower() == skill_lower:
            return definition
    
    return None


def normalize_skill_name(skill_name):
    """Normalize skill name using spelling variations dictionary"""
    skill_lower = skill_name.lower().strip()
    
    # Check spelling variations
    if skill_lower in SPELLING_VARIATIONS:
        return SPELLING_VARIATIONS[skill_lower]
    
    # Check if it's already a known skill
    if skill_name in get_all_skills():
        return skill_name
    
    # Try case-insensitive match
    for canonical, normalized in SPELLING_VARIATIONS.items():
        if canonical == skill_lower:
            return normalized
    
    return None


def get_skill_aliases(skill_name):
    """Get all aliases for a given skill"""
    skill = get_skill_by_name(skill_name)
    if skill and "aliases" in skill:
        return skill["aliases"]
    return []


def get_skill_category(skill_name):
    """Get category of a skill"""
    skill = get_skill_by_name(skill_name)
    if skill and "category" in skill:
        return skill["category"]
    return "unknown"


def get_skills_by_category(category):
    """Get all skills in a specific category"""
    all_skills = get_all_skills()
    return {
        name: skill for name, skill in all_skills.items()
        if skill.get("category") == category
    }


def is_skill_stack(term):
    """Check if a term is a known skill stack"""
    return term.upper() in SKILL_STACKS


def get_skill_stack_components(stack_name):
    """Get component skills for a skill stack"""
    if stack_name.upper() in SKILL_STACKS:
        return SKILL_STACKS[stack_name.upper()]["skills"]
    return []