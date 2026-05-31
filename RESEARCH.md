Research Notes

1. Overview
-----------
Nuqro measures four quotients: IQ, EQ, SQ, AQ. Each uses 10-12 questions, age-normalised scoring, and sub-score breakdowns.

2. IQ – Intelligence Quotient
-----------------------------
- Question type: multiple choice (patterns, math, logic, vocabulary).
- Scoring: 1 point per correct answer. Raw score converted to 0-100.
- Normalisation: Z-score method. Final IQ = 100 + (z * 15).
- Norm tables: stored in data/norms.json (simulated for demonstration).

3. EQ – Emotional Quotient
--------------------------
- Based on Goleman's four dimensions:
  * Self-awareness
  * Self-management
  * Social awareness
  * Relationship management
- Response format: 5-point Likert (1 = strongly disagree, 5 = strongly agree).
- Scoring: each answer mapped to 1-5 points. Raw dimension scores averaged and scaled to 0-100.
- Normalisation: Z-score (mean 50, SD 15), clamped to 0-100.

4. SQ – Social Quotient
-----------------------
- Three factors (from Goleman's social intelligence):
  * Social acting (adapting behaviour)
  * Social cognising (understanding others)
  * Social relating (building rapport)
- Same Likert scale and scoring as EQ.
- Sub-scores for each factor, plus overall SQ (0-100).

5. AQ – Adversity Quotient
--------------------------
- Based on Stoltz's CORE model:
  * Control – perceived ability to influence adversity.
  * Ownership – willingness to take responsibility.
  * Reach – how far adversity spreads into other life areas.
  * Endurance – perceived duration of adversity.
- Reverse-scored items included (e.g., "I feel powerless" lowers Control score).
- Scoring: 1-5 per question, dimension averages scaled to 0-100.
- Overall AQ normalised same as EQ/SQ.

6. Why Age Normalisation?
-------------------------
Raw scores are not comparable across ages. Z-scores put everyone on a common scale. For IQ we use the classic 100/15 scale; for others we clamp to 0-100 for readability.

7. Limitations (honest)
-----------------------
- Norm tables are simulated, not clinically validated.
- Only 10 questions per test (real tests need 20-30).
- Timer is optional – some users may overthink.
- No control for social desirability bias.