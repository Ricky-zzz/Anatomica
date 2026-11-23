# Chapter 1 Writing Guide: What Each Part Does and How to Write It

Examples come from the senior's paper: *LBPH vs CNN face recognition for a web-based employee attendance system (FaceNow)*.

---

## The Big Picture: Chapter 1 Is One Argument

Chapter 1 is not six separate sections. It is a single chain of reasoning, and each part answers one question the reader will ask in order:

| Part | The question it answers | One-line job |
|---|---|---|
| Introduction | "What is in this chapter?" | Roadmap |
| Background of the Study | "Why does this topic matter, and what is the gap?" | Context, then gap |
| Statement of the Problem | "What exactly is the problem, and what must be answered?" | Problem plus research questions |
| Objectives of the Study | "What will you do to answer those questions?" | Research questions turned into action |
| Significance of the Study | "Who benefits, and how?" | Value of the study |
| Scope and Limitations | "What does the study cover, and where does it stop?" | Boundaries and honesty |

**The golden rule is alignment:** every research question (RQ) must have a matching objective (O), and every objective must be something you can measure and test later in Chapters 3 and 4. If an RQ has no matching objective, or an objective has no RQ, the chapter is broken.

---

## 1. INTRODUCTION

### What it is
A short paragraph (2-4 sentences) that previews the chapter. It does not argue anything.

### Question it answers
**"What will I find in this chapter?"**

### How to write it
1. One sentence: "This chapter presents..."
2. List the parts in the same order they appear.
3. Stop. Do not add background or opinions here.

### Template
> This chapter presents an overview of the research, detailing the [background], [problem statement], [objectives], [significance], [scope, and limitations] of the study.

### Example from the senior's paper
> "This chapter presents an overview of the research, detailing the background, problem statement, objectives, significance, scope, and limitations of the study."

### Common mistakes
- Putting citations or arguments here.
- Listing parts in a different order than they appear.

---

## 2. BACKGROUND OF THE STUDY

### What it is
The context that leads the reader, step by step, from a broad topic to your specific gap. It works as a funnel: **broad, then narrower, then your exact problem.**

### Questions it answers
- **Why** is this topic important? (context)
- **What** has already been done or is currently used? (existing solutions)
- **What is wrong or missing?** (the gap)
- **What will this study do about it?** (the purpose)

### The funnel structure (write one paragraph per layer)

| Paragraph | Purpose | What the senior did |
|---|---|---|
| 1. Broad context | Why does the general topic matter? | Attendance monitoring matters in workplaces; manual methods are inefficient and error-prone; organizations are moving to biometrics. |
| 2. Existing technology | What tools exist? | Biometrics in general, then fingerprint, with its limitation (needs contact, affected by dirt or moisture). |
| 3. Your specific technology | Introduce what your study is about | Facial recognition: contactless, but affected by lighting, expressions, image quality. |
| 4. The options being compared | Define the approaches or variables | LBPH (traditional, texture-based) vs CNN (deep learning, learns features automatically). |
| 5. The gap and your purpose | What is missing in past research, and what will you do? | Past studies test in controlled labs and offline datasets, not real operation. So this study analyzes LBPH vs CNN in an actual attendance system. |

### How to write it
1. **Start broad and general** (the field or industry problem).
2. **Cite sources for every factual claim** (author, year). The background is where most of your literature goes.
3. **Narrow down** one layer at a time. Each paragraph should lead naturally to the next.
4. **State the limitation of existing methods.** This creates the need for your study.
5. **End with the gap and one sentence of purpose.** Use "To address this issue, the present study..."

### Sentence starters
- "X plays a critical role in..." (opening)
- "Traditionally, ... however, research indicates that..." (problem with old way)
- "With ongoing technological advancements, ..." (trend)
- "Existing research frequently ... but ..." (the gap)
- "To address this issue, the present study ..." (purpose)

### Example from the senior's paper (the gap and purpose)
> "Existing research frequently evaluates these algorithms in controlled laboratory settings... This gap restricts understanding of their practical performance... To address this issue, the present study conducts a performance analysis of LBPH and CNN-based algorithms within a face recognition-based employee attendance monitoring system..."

### Checklist
- [ ] Moves from broad to specific
- [ ] Every claim has a citation
- [ ] Defines key terms (LBPH, CNN, biometrics) in plain language
- [ ] States a clear gap
- [ ] Ends with the study's purpose

### Common mistakes
- Starting too narrow, so the reader doesn't see why it matters.
- Listing facts with no logical flow between paragraphs.
- No gap stated. Without a gap, the study has no reason to exist.
- Copying citations you haven't read.

---

## 3. STATEMENT OF THE PROBLEM

### What it is
The precise, focused problem your study addresses, followed by the **research questions (RQs)** you will answer.

### Questions it answers
- **What exactly is the problem?** (narrower than the background)
- **What do we still not know?**
- **What specific questions will the study answer?**

### How it differs from the Background
The Background says "here is the big picture and the gap." The Statement of the Problem says "here is the exact problem and the exact questions." It is shorter, sharper, and ends with numbered questions.

### Structure (3 steps)
1. **Context sentence(s):** the shift or situation (manual to digital, face recognition as the technology).
2. **The problem or dilemma:** both options work, but choosing between them is hard because of design, environment, computing limits, and system performance.
3. **The need, then the questions:** "Consequently, it is necessary to evaluate and compare... This study addresses the following research questions:"

### How to write the research questions
- Write them as **real questions** ending in "?"
- Make each one **measurable**: name the variables or metrics.
- Cover **each thing you will do**: performance, operational performance, user perception, difference, recommendation.
- Keep a **logical order**: describe, then compare, then decide.

### Question types in the senior's paper

| RQ | Type | What it asks |
|---|---|---|
| RQ1 | Descriptive | Performance in holdout evaluation (accuracy, precision, recall, F1) |
| RQ2 | Descriptive | Performance in real operation (accuracy, time, FRR, FAR) |
| RQ3 | Descriptive | User perception (reliability, ease of use, speed) |
| RQ4 | Comparative / inferential | Is there a **significant difference** between the algorithms? |
| RQ5 | Decision | Which algorithm is more suitable, and why? |

### Template for research questions
- "What is the performance of [A] and [B] in terms of [metrics] using [method]?"
- "What is the level of [perception] regarding [factors]?"
- "Is there a significant difference between [A] and [B] in terms of [metrics]?"
- "Which [option] is more suitable for [purpose], considering [factors]?"

### Checklist
- [ ] The problem is stated in 1-2 paragraphs, not a full essay
- [ ] Explains *why* the choice is hard
- [ ] 3-6 numbered research questions
- [ ] Each question names its metrics or variables
- [ ] Includes a "significant difference" question if you plan a statistical test

### Common mistakes
- Yes/no questions that cannot be measured ("Is the system good?").
- Questions that do not match your methods.
- Restating the whole Background instead of narrowing it.

---

## 4. OBJECTIVES OF THE STUDY

### What it is
The **actions** you will take to answer the research questions. Objectives are the research questions rewritten as tasks.

### Questions it answers
- **What will this study accomplish?**
- **How will each research question be answered?**

### Structure
1. **General objective:** one sentence on the overall aim ("This study evaluates and compares...").
2. **Specific objectives:** numbered list, one per major task.

### How to write them
- Start each with an **action verb**: *design, develop, evaluate, assess, describe, compare, recommend*.
- Make each **specific and measurable** (name the metrics and methods).
- Keep them in the **order the work happens**: build, test, measure, compare, recommend.
- Make sure **each objective maps to one RQ**.

### Verb guide

| Verb | Use for |
|---|---|
| Design / develop | Building the system |
| Evaluate / assess | Measuring performance |
| Describe | Descriptive results like user perception |
| Compare / determine | Statistical testing |
| Recommend | Final decision |

### Alignment table from the senior's paper (use this to check yours)

| Objective | Matches | Method (goes in Chapter 3) | Result (goes in Chapter 4) |
|---|---|---|---|
| O1: Design and develop the web-based system | (Supports all RQs) | Development approach | System description |
| O2: Holdout evaluation (accuracy, precision, recall, F1) | RQ1 | Train/test split | Table of metrics |
| O3: Operational performance (live accuracy, time, FRR, FAR) | RQ2 | Live testing | Table of metrics |
| O4: Describe user perception | RQ3 | Survey | Mean / interpretation |
| O5: Paired t-test for differences | RQ4 | Paired t-test | p-values |
| O6: Recommend the most suitable algorithm | RQ5 | Synthesis | Conclusion |

### Checklist
- [ ] One general objective plus numbered specific objectives
- [ ] Every objective begins with an action verb
- [ ] Number of objectives matches the research questions
- [ ] Each objective is testable or measurable
- [ ] Statistical test is named where relevant

### Common mistakes
- Vague verbs like "understand" or "know."
- Objectives that do not match the research questions.
- Promising something you cannot measure.

---

## 5. SIGNIFICANCE OF THE STUDY

### What it is
An explanation of **who benefits from the study and how.**

### Questions it answers
- **Who will use or benefit from the results?**
- **What exactly will they gain?**
- **Why does the study matter beyond this paper?**

### How to write it
1. Start with **one short paragraph** restating what the study investigates (1-2 sentences).
2. Then write **one paragraph per beneficiary**, ordered from most to least directly affected.
3. In each paragraph use this formula: **Who + what they gain + how the findings help.**
4. Be **specific.** Avoid "this will help everyone."

### Formula
> "The findings will benefit **[group]** by **[specific gain]**, enabling them to **[action/outcome]**."

### Beneficiaries from the senior's paper

| Group | What they gain |
|---|---|
| Developers / technical professionals | Evidence to choose between LBPH and CNN for biometric attendance systems |
| Students and future researchers | Practical understanding of ML and biometrics; a base for further research |
| Schools and large organizations | A modern, contactless attendance approach with a clear implementation path |

### Checklist
- [ ] Each beneficiary is named
- [ ] Each paragraph says *what* the group gains
- [ ] Benefits come directly from your findings
- [ ] No repeated sentences or generic claims

### Common mistakes
- Repeating the same sentence in different paragraphs.
- Listing groups with no explanation of the benefit.
- Claiming benefits your study cannot actually deliver.

---

## 6. SCOPE AND LIMITATIONS

### What it is
Two things in one section:
- **Scope** is what the study *includes* (the boundaries).
- **Limitations** is what the study *cannot* cover or may be weak at (the honest weaknesses).

### Questions it answers
- **What is covered?** (algorithms, system, metrics, tools, participants)
- **What is NOT covered?** (excluded items)
- **What could affect the validity or generalizability of the results?**

### How to write it

**Scope paragraph(s):**
1. State the **topic and tools** (Django, Python, JavaScript).
2. List the **exact things tested** (only LBPH and CNN).
3. List the **metrics and evaluation types** (holdout and operational).
4. Mention **methodological controls** (identical testing for fairness, unseen test data).

**Limitations paragraph(s):**
1. Sample problems: small dataset, limited demographics (age, gender, ethnicity).
2. Environment problems: extreme lighting, occlusion, camera quality, angles, large-scale deployment.
3. Technical exclusions: no anti-spoofing; other algorithms not considered.
4. Close by saying these limits show where **future research** is needed.

### Scope vs. limitations quick test

| If it is... | It belongs in... |
|---|---|
| A choice **you made** (we only test LBPH and CNN) | Scope |
| Something **outside your control** that weakens results (small sample, camera quality) | Limitations |

### Checklist
- [ ] Scope names the algorithms, tools, and metrics
- [ ] Limitations are honest and specific
- [ ] Every metric in Scope is actually measured in your study
- [ ] Ends by pointing to future research

### Common mistakes
- Putting limitations only in vague words ("some problems may occur").
- Listing something in Scope that your study does not measure. **The senior's paper mentions "security" as a compared metric, but no security measure appears in the research questions or objectives.** Match your Scope to your objectives.
- Hiding limitations to look stronger. Honesty strengthens credibility.

---

## Final Alignment Check (Do This Before Submitting)

Fill in this table for your own topic. Every row should connect left to right with no gaps.

| Gap in Background | Research Question | Objective | Metric / Test | Where Answered |
|---|---|---|---|---|
| (the missing knowledge) | RQ1 | O1 | (metric) | Chapter 4 |
| | RQ2 | O2 | | |
| | RQ3 | O3 | | |

### Final quality checklist
- [ ] Background ends with a clear gap and purpose
- [ ] Problem statement narrows the background and lists RQs
- [ ] One objective per RQ, same order
- [ ] Significance names real beneficiaries
- [ ] Scope matches what you actually measure
- [ ] Limitations are honest
- [ ] Terms are consistent throughout (use the same names every time: LBPH, CNN, FAR, FRR)
- [ ] Every cited source is real and listed in your references
- [ ] Typos fixed (the senior's paper has "monitoring-monitoring" in the Statement of the Problem)

---

## Reminder About Using the Senior's Paper

Use it as a **model for structure and flow, not for wording.** Your topic, problem, gap, and research questions must be your own. Copying its sentences risks plagiarism, and your study will have different metrics, tools, and participants.
