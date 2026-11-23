# Chapter 1

## The Problem and Its Background

### Introduction

This chapter gives the background of the study, the statement of the problem, the objectives, the significance, and the scope and limitations.

### Background of the Study

Philippine nursing programs must train students to handle clinical problems safely, and the Commission on Higher Education requires outcome-based teaching to do it (Commission on Higher Education, 2017). Simulation carries much of that training because students can practice drug administration and emergency response without putting a real patient at risk (Bambini, 2016; Jeffries, 2012). This training needs faculty, and nursing schools do not have enough of them. In one urban area of the Central Philippines, most clinical instructors were part-time and had only a few years of service (Noblezada et al., 2025), and many experienced nurses keep leaving for jobs abroad (Alibudbud, 2023). The shortage is not only local. American nursing schools reported a 7.2 percent vacancy rate in full-time faculty posts and turned away more than 92,000 qualified applicants in a single year because they could not find enough teachers (American Association of Colleges of Nursing, 2025).

Faculty also lose many hours writing the scenarios themselves. A complete scenario needs a patient history, changing vital signs, lab and imaging results, doctor's orders, medication records, and notes for the facilitator, and the work can reach about 100 hours for one case (Bambini, 2016). The Healthcare Simulation Standards of Best Practice add more requirements, such as clear objectives, realistic detail, and a planned debriefing (Watts et al., 2021). Teachers who tried AI for this step said the tools produced a usable draft fast, but that important details were often missing and someone still had to check the content before it was safe to use (Harder, 2023; Vaughn & Ford, 2024). Schools without the time often buy ready-made scenarios instead. These are reviewed by professionals, but they cost money, stay the same over time, and rarely match the local diseases, drug list, or paperwork of the school's own hospital system.

Generative AI can take over part of this work. Large language models are trained on huge amounts of text to predict the next word in a sentence, which lets them write patient stories and clinical notes on demand (Vaswani et al., 2017; Brown et al., 2020). Nursing teachers report that this cuts the time spent on case design (Liu et al., 2025; Reed & Dodson, 2024). The problem is accuracy. These models write from patterns in their training data, not from checked medical sources, so the text can read well and still be wrong. A study of clinical summaries found a hallucination rate near 1.47 percent, and 44 percent of those errors were serious enough to change a diagnosis or a care plan (Asgari et al., 2025). When a patient story held one planted false detail, six models repeated or added to it in 50 to 82 percent of their answers (Omar et al., 2025). The same weakness reaches references. One study found that GPT-3.5 made up 55 percent of its citations and GPT-4 made up 18 percent (Walters & Wilder, 2023), while another found that 69 percent of the medical references it suggested did not exist (Gravel et al., 2023). In a nursing scenario, these mistakes show up as wrong drug doses, impossible vital signs, or milestones that do not fit the patient's age, and students study the scenario as if it were correct.

Retrieval-Augmented Generation, or RAG, is one way to lower these errors. Lewis et al. (2020) designed RAG to pair a language model with a search step. The system first pulls relevant passages from a trusted document set, and then the model writes its answer using those passages as its source. Because the facts come from the documents and not from the model's memory, the model has less room to invent them, and each claim can be traced back to a source. The effect has been measured. On the MIRAGE medical test, adding retrieval raised the accuracy of six models by up to 18 percentage points (Xiong et al., 2024). In a hospital study, retrieval lifted a small model's exact match on diagnosis codes from 0.8 percent to 17.6 percent (Klang et al., 2024). On structured outputs, it cut invented workflow steps from about 21 percent to under 7.5 percent (Béchard & Marquez Ayala, 2024).

RAG is not a guaranteed fix. Retrieval can fail when the document set lacks the answer, when the right document is ranked too low, or when the model ignores the format it was given (Barnett et al., 2024). Some small models also did not improve with retrieval and even lost a little accuracy (Vishwanath et al., 2024). For scenario writing, the document set would be the faculty's own published scenarios. A draft would then follow the school's format, skills, and local context, while a person still checks the final content (Liu et al., 2025; Clark & Brennan, 1991).

Most studies on AI-written clinical content test a model by itself, on general medical text, or outside a working school hospital system. Few compare a grounded and a non-grounded model inside the same writing tool, use the school's own scenarios as the only source, and have faculty judge the result. That is the gap this study fills. It builds an AI draft assistant inside the scenario builder of Chansey, an educational hospital information system, and compares RAG-grounded generation against non-grounded generation on schema validity, clinical plausibility, hallucination rate, latency, and cost.

### Statement of the Problem

Writing a nursing scenario takes many faculty hours (Bambini, 2016). Generative AI can shorten the draft, but a plain model has no tie to the school's own content and can invent drug doses, vital signs, and milestones (Asgari et al., 2025; Omar et al., 2025). Both approaches produce fluent text, so the hard part is not writing a scenario. The hard part is knowing whether grounding the model on faculty-authored content makes the result safe enough to use. This study therefore evaluates and compares a RAG-grounded generator against a non-grounded one inside the faculty scenario builder.

This study answers the following questions:

1. What is the schema validity rate and clinical plausibility of scenarios generated by RAG-grounded and non-grounded generation, as rated by Nursing Department faculty?
2. What is the hallucination and contradiction rate, including coherence between orders and diagnosis, of each generation condition?
3. Is there a significant difference between RAG-grounded and non-grounded generation in schema validity, clinical plausibility, and hallucination rate?
4. What is the latency and token cost of each condition for real-time faculty use?
5. Which generation approach is more suitable for faculty scenario authoring, and why?

### Objectives of the Study

This study develops and evaluates a RAG-grounded AI draft assistant for nursing scenario generation and compares it with non-grounded generation in an educational hospital information system. Specifically, this study aims to:

1. Design and develop the AI draft assistant inside the Faculty Scenario Builder, supporting all research questions.
2. Evaluate the schema validity rate and clinical plausibility of RAG-grounded and non-grounded outputs using Nursing Department faculty ratings (RQ1).
3. Determine the hallucination and contradiction rate, including order and diagnosis coherence, of each condition (RQ2).
4. Compare the two conditions for a significant difference using a paired t-test or the Wilcoxon signed-rank test, with McNemar's test for validity and hallucination rates (RQ3).
5. Measure the latency and token cost of each condition (RQ4).
6. Suggest the better approach for faculty scenario authoring (RQ5).

### Significance of the Study

This study checks whether grounding a generative model on faculty-authored scenarios lowers clinical hallucination in nursing scenario generation.

It will help Nursing Department faculty by showing whether a grounded draft tool can cut the hours spent writing scenarios while keeping the clinical content under their approval, which frees time for teaching and debriefing.

It will help nursing students by giving them more practice scenarios and by keeping invented clinical details out of the material they study.

It will help developers and nursing informatics researchers by giving measured evidence on RAG grounding for structured clinical content, an area with few faculty-checked results inside a working school hospital system.

It will help schools by giving them a tested way to speed up scenario writing without handing clinical control to a model, which supports the outcome-based rules of CHED Memorandum Order No. 15 (Commission on Higher Education, 2017).

It will help future researchers by leaving a documented process, rubric, and dataset that can be extended to larger document sets, other skills, or a trained local model.

### Scope and Limitations

This study covers the building of an AI draft assistant inside the Faculty Scenario Builder of Chansey, an educational hospital information system. The comparison tests two generation setups. RAG-grounded generation pulls the top faculty-authored scenarios for a skill and difficulty level, while non-grounded generation sends a plain prompt with no retrieval. Both use the same commercial language model through an API, so the study uses a model and does not train one from scratch. The document set is 12 to 15 faculty-authored scenarios stored in the Chansey database, and the output follows the existing scenario format of patient fields, orders, and expected milestones. The measures are schema validity, clinical plausibility, order and diagnosis coherence, hallucination and contradiction rate, latency, and cost. Nursing Department faculty rate the drafts on a rubric. A rule-based step creates a student weakness label from progress logs, and that label feeds into the prompt. A small trained model is added as a secondary result and is checked only on schema validity against the API baseline.

The study has limits. The document set is small, so the results come from one school and may not fit other programs. Faculty-authored scenarios hold de-identified simulation content only, and no real patient data is used. The judges are Nursing Department faculty, not doctors, so the study does not claim doctor-level diagnostic accuracy. The API provider and version affect repeat results, because hosted models change or retire over time. The study does not cover automatic publishing or real clinical use, and generated scenarios stay as drafts until faculty approve them. Future work can test a larger document set, add other skills, and compare the trained model against the API baseline on clinical plausibility.
