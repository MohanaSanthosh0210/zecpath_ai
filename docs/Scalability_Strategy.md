# Scalability Strategy

## Horizontal Scaling

Load Balancer

↓

Resume Parser Service

↓

ATS Service

↓

Screening Service

↓

Interview Services

↓

Hiring Intelligence

↓

Report Generator

---

## Scaling Plan

- 10 candidates → 1 instance
- 100 candidates → 2 instances
- 500 candidates → 5 instances
- 1000 candidates → 10 instances
- 5000 candidates → 20 instances

---

## Objectives

- Maintain low response time
- Distribute workload evenly
- Prevent service bottlenecks