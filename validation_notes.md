Validation Notes – NUQRO Test Suite

What is Validation?
-------------------
Validation is evidence that a test measures what it claims. Full validation requires years of research. For a class project, I can only discuss what's missing and what's reasonable.

1. Content Validity (Do questions cover the domain?)
----------------------------------------------------
- IQ: patterns, sequences, arithmetic, analogies – good range, but only 10 items.
- EQ: 3-4 questions per dimension – thin, but acceptable for a demo.
- SQ and AQ: similar situation.
Limitation: A real test would need 20-30 items per scale.

2. Construct Validity (Does it correlate with established tests?)
-----------------------------------------------------------------
I have not run correlations with WAIS, EQ-i, or other validated instruments. I cannot claim NUQRO measures the same constructs as those tests. However, the Z-score method is standard, and questions are face-valid.

3. Reliability (Consistency)
----------------------------
- Internal consistency (Cronbach's alpha): not calculated. With only 10 items, alpha would likely be low.
- Test-retest reliability: unknown. The optional timer may reduce consistency (spontaneous answers vary).
Trade-off: spontaneity is good for ecological validity, bad for reliability.

4. Face Validity (Does it look like a real test?)
--------------------------------------------------
Yes. Users generally accept IQ puzzles and EQ scenarios as plausible.

Known Limitations
-----------------
- Norm tables are simulated, not empirical.
- Small number of questions per test.
- No social desirability (lie) scale – users can fake answers.
- Answer choices always in A,B,C,D order – may introduce order bias.
- Timer is off by default – many users will overthink.

How to Make It a Real Test (Future Work)
----------------------------------------
- Run a pilot with 200+ participants, collect real norms.
- Add 20+ more questions per test.
- Perform factor analysis to confirm dimensions.
- Add a lie scale (e.g., "I have never told a lie").
- Randomise answer option order.
- Validate against real-world outcomes (job performance, grades).

Conclusion for Stanford Code in Place
--------------------------------------
Nuqro demonstrates understanding of psychometric principles: Z-scores, norm tables, sub-scores, and CLI design. It is not clinically valid, but it is a solid teaching tool i guess.