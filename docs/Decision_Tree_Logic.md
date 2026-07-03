# Decision Tree Logic

## Overview

The Decision Tree controls how the AI interviewer selects the next question after every candidate response.

It combines:

- Response Quality
- Confidence
- Conversation History
- Difficulty Adaptation
- Follow-Up Strategy

---

# Decision Tree

```
Candidate Response
        │
        ▼
Is response incomplete?
        │
 ┌──────┴──────┐
 │             │
Yes            No
 │             │
 ▼             ▼
Clarification  Is response vague?
                     │
             ┌───────┴────────┐
             │                │
            Yes               No
             │                │
             ▼                ▼
      Clarification      Is confidence high?
                               │
                     ┌─────────┴─────────┐
                     │                   │
                    Yes                  No
                     │                   │
                     ▼                   ▼
             Scenario Question     Deepening Question
                     │
                     ▼
          Already Asked Before?
                     │
             ┌───────┴────────┐
             │                │
            Yes               No
             │                │
             ▼                ▼
      Move to Next Topic   Ask Follow-Up
```

---

# Decision Rules

## Rule 1

Incomplete Answer

↓

Clarification

---

## Rule 2

Vague Answer

↓

Clarification

---

## Rule 3

Simple Answer

↓

Deepening Question

---

## Rule 4

Confident Answer

↓

Scenario Question

---

## Rule 5

Repeated Question

↓

Skip and Continue Interview

---

# Final Output

The Decision Engine returns:

- Follow-Up Type
- Difficulty Level
- Follow-Up Question
- Repetition Status
- Conversation History
- Decision Summary