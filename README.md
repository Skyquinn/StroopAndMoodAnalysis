**PsychoPy Emotion & Mood Experiment**

**Aim of the Experiment**

This experiment investigates cognitive interference and mood in a simple Stroop-like task. Participants view emotional faces (happy or angry) overlaid with emotion words and respond based on the facial expression, ignoring the word. After the task, they rate their current mood (happiness and anger) on a 1–5 slider. 
**The goals are:**

Demonstrate the classic congruency effect by comparing reaction times (RTs) on congruent vs. incongruent trials.


Measure overall accuracy and examine its relationship with self-reported mood.


Capture participant mood ratings and explore how performance correlates with happiness and anger.


**Instructions to Run the Code**
Clone or copy this repository containing Skylarfinal.py (your PsychoPy script) and emo_conditions.xlsx (the conditions file).


Open a terminal (or Anaconda Prompt) and navigate to the directory:


cd path/to/experiment/folder
Follow on-screen prompts:


Enter participant number (integer ≤ 99) and age (≥ 18).


View welcome and instruction screens.


Complete the 180-trial Stroop-like task.


Rate your current mood on two sliders (happiness and anger).


Data files will be appended to two master CSVs in the same directory:


all_summary.csv: one row per participant (participant nr, age, happy_rating, angry_rating)


all_trials.csv: trial-by-trial data for all participants, with columns for stimulus, RT, response, accuracy, and participant nr.


**Dependencies**

Python ≥ 3.7


PsychoPy (tested with v2024.2)


pandas (for data handling)


openpyxl (to read .xlsx conditions file)


**Colab-R Data Analysis Summary**

I performed exploratory and inferential analyses in Google Colab using R (tidyverse). Data from 18 participants (ages 21–25) were examined across the Stroop-like task and mood sliders.

**Key Findings**

Interference Effect: Mean RT was faster on congruent trials (M = 0.53 s, SD = 0.25) than on incongruent trials (M = 0.58 s, SD = 0.28), confirming a clear congruency (interference) effect.


Accuracy: Overall task accuracy averaged 84.2% across participants (range = 84.2%–95.0%), with one individual achieving the upper bound of 95.0% correct.


Mood Distributions: Happy ratings clustered around 3–4, angry ratings spanned 1–5, and the net-positivity (happy – angry) ranged from –3 to +5.


Mood ↔ Age: A slight positive trend for happiness with age and a small negative trend for anger were observed in scatterplots with linear fits.


Mood ↔ Performance: Happy ratings correlated moderately with accuracy (r ≈ 0.42, p ≈ 0.056); the “High-Happy” group showed marginally faster RTs on both congruent and incongruent trials.


**Plots Created**

Age Histogram (Age)


RT Boxplots (by Congruence)


Happy-Rating Histogram


Angry-Rating Histogram


Mood Boxplots (Happy vs. Angry)


Happy vs. Angry Scatter (45° reference line)


Net-Positivity Histogram (Happy – Angry)


RT by Happy-Group Boxplots (Low vs. High Happy)


Mood vs. Age Trends (jitter + lm line for both ratings)


Happy ↔ Accuracy Scatter (with regression line)


Statistical Summaries & Tests
Descriptive RT Stats: Mean and SD of RT by congruence computed via dplyr.


Accuracy Summary: Proportion correct per participant.


Pearson Correlation: Association between happy rating and accuracy tested with cor.test() (r ≈ 0.42, p ≈ 0.056).

