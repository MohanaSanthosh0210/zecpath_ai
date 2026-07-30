# Threshold Optimization

Purpose

Improve hiring decision quality by adjusting scoring
thresholds based on previous evaluation outcomes.

---

Current Thresholds

Selection Threshold

80

Review Threshold

60

---

Optimization Rules

If False Positive Rate exceeds the configured limit:

Increase Selection Threshold

↓

Reduce incorrect selections

If False Negative Rate exceeds the configured limit:

Decrease Review Threshold

↓

Reduce incorrect rejections

---

Expected Output

Updated Threshold Configuration