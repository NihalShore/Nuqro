How NUQRO's Age Norm Tables Were Built

Purpose
-------
Age-normalised scoring needs means and standard deviations of raw scores for each age group. Real tests get these from large pilot studies. For NUQRO (project), I simulated reasonable numbers.

Age Groups Used
---------------
- 10-12
- 13-15
- 16-18
- 19-25
- 26-35
- 36-50
- 51+

Assumptions Behind the Numbers
------------------------------
- IQ: increases from childhood to middle adulthood, then slowly declines.
- EQ and SQ: increase with life experience and age.
- AQ: increases with maturity, may dip in very old age.

Example Norm Row (IQ, age 19-25)
--------------------------------
mean = 45, sd = 9

Interpretation: a 22-year-old scoring 45 on raw 0-100 scale is exactly average. A score of 54 is one standard deviation above average (z=1.0), leading to adjusted IQ = 100 + 1.0*15 = 115.

How NUQRO Uses These Norms
--------------------------
1. User finishes a test, raw score (0-100) is calculated.
2. Program finds user's age group and retrieves mean and sd.
3. z = (raw_score - mean) / sd
4. For IQ: adjusted = 100 + z*15
5. For EQ/SQ/AQ: adjusted = clamp(50 + z*15, 0, 100)

Future Improvements
-------------------
- Replace simulated norms with real pilot data.
- Add more age groups (e.g., 5-9, 70+).
- Automatically update norms as more data is collected.

Important Caveat
----------------
These norms are for educational demonstration only. Do not use NUQRO for real psychological assessment.