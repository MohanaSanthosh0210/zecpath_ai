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

## Integrity Detection Extension

### Purpose

The integrity layer is designed to identify suspicious interview behavior that may indicate cheating, external assistance, or non-compliant participation. Unlike the behavioral score, which measures candidate demeanor, the integrity module operates as a separate risk channel with explainable policy-based thresholds and temporal pattern recognition.

### 1. Malpractice Signals

#### A. Tab Switching Frequency

Measures the number of times the candidate exits the interview window or switches to another active application during a response period.

Recommended signal definition:

- Tab switch count per 60-second window
- Switches during response window rather than during question reading
- Repeated focus loss to non-interview surfaces

#### B. Loss of Screen Focus

Captures interruptions in the interview environment when the candidate window loses active focus or the browser/application becomes blurred.

Recommended signal definition:

- Window blur events
- Browser/app inactive events
- Short re-focus delays after interruption

#### C. External Voice Detection

Detects whether a second voice, audio source, or recognizable off-screen assistance is present in the interview audio stream.

Recommended signal definition:

- Multi-speaker audio probability
- Non-candidate speaker energy above baseline
- Voice activity overlapping candidate response timing

#### D. Repeated Looking Away

Measures repeated gaze shifts away from the camera or interviewer region over a short interval.

Recommended signal definition:

- Off-center gaze events per minute
- Consecutive gaze-away events with low return duration
- Look-away bursts during high-stakes answer windows

### 2. Detection Logic

#### Threshold-Based Flags

Each signal is converted into a suspiciousness score using threshold rules.

Recommended thresholds:

- Tab switching:
  - 0–1 switches / minute: normal
  - 2–3 switches / minute: caution
  - 4+ switches / minute: alert

- Screen focus loss:
  - 0–1 blur events / 2 minutes: normal
  - 2 blur events / 2 minutes: caution
  - 3+ blur events / 2 minutes: alert

- External voice detection:
  - Confidence < 0.50: no flag
  - 0.50–0.69: caution
  - >= 0.70: high-confidence assistance signal

- Repeated looking away:
  - 0–2 events / minute: normal
  - 3–4 events / minute: caution
  - 5+ events / minute: alert

#### Pattern Recognition

Thresholds should be complemented with temporal pattern recognition to reduce false positives.

Examples:

- Assistance pattern: tab switch + external voice + look-away within 10 seconds
- Coaching pattern: repeated tab switches occurring after every difficult question
- External prompt pattern: screen focus loss followed by immediate gaze reorientation toward off-screen area

Pattern rule:

Integrity Pattern Score =

(0.30 × Tab Switch Risk)
+
(0.20 × Focus Loss Risk)
+
(0.25 × Voice Assistance Risk)
+
(0.25 × Look-Away Risk)

If the Pattern Score exceeds 0.65 and persists across 2+ consecutive response windows, the interview moves into a higher integrity risk tier.

### 3. Warning and Flagging System

#### Risk Levels

- Level 0: No Integrity Concern
- Level 1: Watchlist / Soft Warning
- Level 2: Elevated Risk / Review Required
- Level 3: High Risk / Immediate Flag

#### Real-Time Alerting

A real-time alert should be generated when any of the following occurs:

- A single high-confidence audio assistance event is detected
- A burst of tab switching or focus loss occurs during one answer window
- Repeated look-away behavior aligns with a suspicious pattern

#### Interview Risk Tagging

Each session should produce an integrity tag payload similar to the following:

```json
{
  "integrity_risk_level": "high",
  "integrity_risk_score": 78,
  "integrity_flags": [
    "tab_switch_burst",
    "external_voice_detected",
    "repeated_look_away_pattern"
  ],
  "warning_mode": "review_required",
  "confidence": 0.82
}
```

### 4. Integration with Behavioral Signals

The integrity risk layer should be integrated into behavioral intelligence as an orthogonal signal, not as a direct subtraction from the behavioral score.

Recommended integration model:

- Behavioral score remains a measure of demeanor and engagement.
- Integrity risk score is stored as a separate policy signal.
- High integrity risk should reduce confidence in the behavioral interpretation.
- A severe integrity flag can trigger a human review or session hold.

#### Recommended Interaction Rules

- Low behavioral score + low integrity risk: candidate may still be assessed normally.
- Low behavioral score + high integrity risk: behavioral evidence should be treated as low-confidence.
- High behavioral score + high integrity risk: review required due to contradictory evidence.

### 5. Auditability and Ethical Guardrails

- Flagging must be based on multiple signals, not a single isolated event.
- All integrity alerts should retain timestamp, window, and confidence metadata.
- The system must support human override and manual reviewer confirmation.
- Candidate culture, environment, and accessibility differences must not be mistaken for malpractice indicators.

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
  ],
  "integrity_risk_level": "medium",
  "integrity_risk_score": 41,
  "integrity_flags": [
    "look_away_burst"
  ]
}
```

## Design Guardrails

- Do not treat isolated gestures as decisive evidence.
- Use confidence intervals for each sub-score.
- Avoid penalizing culturally or situationally different expressions.
- Use temporal context to separate nervousness from genuine cognitive processing.
- Keep all scoring explainable and auditable.
