CREATE TABLE screening_interactions (

    interaction_id VARCHAR(50) PRIMARY KEY,

    candidate_id VARCHAR(50),

    job_id VARCHAR(50),

    question_id VARCHAR(50),

    timestamp DATETIME,

    question_text TEXT,

    answer_text TEXT,

    answer_type VARCHAR(50),

    confidence_score FLOAT,

    sentiment_score FLOAT,

    duration_seconds FLOAT,

    language VARCHAR(10)
);
