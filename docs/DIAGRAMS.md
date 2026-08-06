# System Diagrams

The diagrams below illustrate the main components and common request/processing sequences. Use these as a basis for PNG export or further refinement.

**Component Diagram (Mermaid flowchart)**

```mermaid
flowchart TD
  A[Job Description / Resume Upload] --> B[Resume Parser]
  B --> C[Structured Resume / JD Storage]
  C --> D[ATS Engine]
  D --> E[Score Normalizer]
  E --> F[Ranking & Shortlisting]

  subgraph InterviewFlow [Interview & Screening]
    G[Audio Capture] --> H[Speech-to-Text Service]
    H --> I[Transcript Cleaner]
    I --> J[Answer Understanding - NLP]
    J --> K[Screening Scoring]
    K --> L[Behavior Analysis]
    K --> M[Technical Scoring]
  end

  J --> N[Conversation Flow Engine]
  M --> O[Technical Report Generator]
  L --> P[Behavioral Report Generator]

  F --> Q[Unified Scoring Engine]
  O --> Q
  P --> Q
  Q --> R[Recruiter View / Final Report]
  S[Observability & Logging] ---|collects| B
  S ---|collects| H
  S ---|collects| K
  S ---|collects| Q

```

**Sequence Diagram: Resume -> ATS -> Shortlist**

```mermaid
sequenceDiagram
  participant Client
  participant API
  participant Parser
  participant ATS
  participant Normalizer
  participant Ranking

  Client->>API: POST /resume/upload (file)
  API->>Parser: parse(file)
  Parser-->>API: structured_resume
  API->>ATS: POST /ats/evaluate (resume, job)
  ATS-->>API: ats_score
  API->>Normalizer: normalize(ats_score)
  Normalizer-->>API: normalized_score
  API->>Ranking: insert(candidate, normalized_score)
  Ranking-->>API: shortlist_status
  API-->>Client: 200 {status, score}

```

**Sequence Diagram: Screening Call -> Scoring & Report**

```mermaid
sequenceDiagram
  participant Interviewer
  participant AudioService
  participant STT
  participant Cleaner
  participant NLP
  participant Scoring
  participant Behavior
  participant Report

  Interviewer->>AudioService: Upload(audio)
  AudioService->>STT: transcribe(audio)
  STT-->>Cleaner: raw_transcript
  Cleaner->>NLP: clean_transcript
  NLP-->>Scoring: structured_answers
  Scoring->>Behavior: request_behavior_analysis
  Behavior-->>Scoring: behavior_metrics
  Scoring-->>Report: generate(candidate_report)
  Report-->>Interviewer: deliver(report)

```

Notes
- Export: render the Mermaid blocks in your preferred editor or Mermeid CLI to PNG/SVG.
- Files referenced in the diagrams map to code in the repository: `main.py`, `technical_scoring/`, `hr_scoring/`, `scoring/unified_scoring_engine.py`, `adaptive_followup/`.
