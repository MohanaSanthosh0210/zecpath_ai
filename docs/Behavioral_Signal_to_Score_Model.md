# Behavioral Signal-to-Score Mapping Model

## Purpose

Translate observable interview behaviors into measurable, explainable, and normalized scores that can be consumed by the behavioral intelligence pipeline.

## Key Principle

Each signal is converted into a feature, each feature is normalized into a 0–100 score, and then combined into behavioral sub-scores.

## Feature Definitions

### 1. Focus Level

Focus level measures sustained attention and alignment with the interview interaction.

Signals:

- Eye gaze stability toward the interviewer/camera
- Stable head pose
- Low attention-loss frequency

Feature computation:

Focus Score =

(0.40 × Gaze Stability)
+
(0.30 × Head Stability)
+
(0.30 × Attention Continuity)

### 2. Distraction Frequency

Distraction frequency measures interruptions in attention during the interview.

Signals:

- Off-screen gaze events
- Sudden head turns away from center
- Reduced visual alignment during question response windows

Feature computation:

Distraction Score =

(0.45 × Off-Screen Gaze Rate)
+
(0.35 × Head Turn Rate)
+
(0.20 × Attention Gap Rate)

Higher values represent more distraction. This score is later inverted when used in the composite behavioral score.

### 3. Nervous Gestures

Nervous gestures capture visible micro-behaviors associated with stress or uncertainty.

Signals:

- Rapid head micro-movement
- Repeated face-touching or grooming gestures
- Sudden posture changes
- Excessive gaze avoidance after difficult prompting

Feature computation:

Nervousness Score =

(0.35 × Micro-Movement Rate)
+
(0.30 × Gesture Frequency)
+
(0.20 × Posture Shift Rate)
+
(0.15 × Gaze Avoidance Rate)

### 4. Facial Engagement

Facial engagement reflects the candidate’s visible responsiveness to the conversation.

Signals:

- Consistent eye and mouth activity aligned with speech
- Positive or neutral engagement expression
- Lower expression variability under normal speaking conditions

Feature computation:

Engagement Score =

(0.45 × Expression Alignment)
+
(0.25 × Visible Engagement Ratio)
+
(0.30 × Response Consistency)

## Normalization Strategy

Each raw signal should be normalized using a min-max or percentile-based method over the candidate session or benchmark cohort.

Recommended normalization:

- Segment-level normalization by interview window
- Session-level normalization across the whole interview
- Benchmark normalization using baseline behavior ranges for similar interview scenarios

## Composite Behavioral Score

Final score formula:

Behavioral Composite Score =

(0.35 × Focus Score)
+
(0.25 × Engagement Score)
+
(0.20 × Attention Consistency Score)
+
(0.20 × (100 - Nervousness Score))

Interpretation:

- High score: stable attention, expressive engagement, low nervousness
- Medium score: some instability, but recoverable
- Low score: frequent distraction, weak engagement, or visibly stressed behavior

## Example Mapping Table

| Raw Behavior | Signal Measure | Score Contribution |
|---|---|---|
| Gaze fixed on interviewer > 70% of the time | Gaze stability | +25 to focus |
| Off-screen glance every 15–20 seconds | Distraction rate | -12 to focus |
| 2–3 head turns during a single answer | Head instability | -8 to focus |
| Frequent self-touch or face touching | Nervous gesture event | +12 to nervousness |
| Consistent expression aligned to speech | Engagement signal | +15 to engagement |
| Sudden motion burst after difficult question | Stress reaction | +10 to nervousness |

## Output Structure

```json
{
  "focus_score": 82,
  "distraction_score": 23,
  "nervousness_score": 18,
  "engagement_score": 79,
  "attention_consistency": 76,
  "behavioral_score": 80.5,
  "behavioral_flags": [
    "slight gaze variation",
    "low nervousness"
  ]
}
```

## Design Guardrails

- Do not treat isolated gestures as decisive evidence.
- Use confidence intervals for each sub-score.
- Avoid penalizing culturally or situationally different expressions.
- Use temporal context to separate nervousness from genuine cognitive processing.
- Keep all scoring explainable and auditable.
