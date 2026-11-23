# Development and Comparative Evaluation of a Retrieval-Augmented Generative AI Assistant for Nursing Scenario Generation in an Educational Hospital Information System

# Chapter 1

## The Problem and Its Background

### Introduction

This chapter gives the background of the study, the statement of the problem, the objectives, the significance, and the scope and limitations.

### Background of the Study

Philippine nursing programs must train students to handle clinical problems safely, and the Commission on Higher Education requires outcome-based teaching to do it (Commission on Higher Education, 2017). Simulation carries much of that training because students can practice drug administration and emergency response without putting a real patient at risk (Bambini, 2016; Jeffries, 2012). This training needs faculty, and nursing schools do not have enough of them. In one urban area of the Central Philippines, most clinical instructors were part-time and had only a few years of service (Noblezada et al., 2025), and many experienced nurses keep leaving for jobs abroad (Alibudbud, 2023). The shortage is not only local. American nursing schools reported a 7.2 percent vacancy rate in full-time faculty posts and turned away more than 92,000 qualified applicants in a single year because they could not find enough teachers (American Association of Colleges of Nursing, 2025).

Faculty also lose many hours writing the scenarios themselves. A complete scenario needs a patient history, changing vital signs, lab and imaging results, doctor's orders, medication records, and notes for the facilitator, and the work can reach about 100 hours for one case (Bambini, 2016). The Healthcare Simulation Standards of Best Practice add more requirements, such as clear objectives, realistic detail, and a planned debriefing (Watts et al., 2021). Teachers who tried AI for this step said the tools produced a usable draft fast, but that important details were often missing and someone still had to check the content before it was safe to use (Harder, 2023; Vaughn & Ford, 2024). Schools without the time often buy ready-made scenarios instead. These are reviewed by professionals, but they cost money, stay the same over time, and rarely match the local diseases, drug list, or paperwork of the school's own hospital system.

Generative AI can take over part of this work. Large language models are trained on huge amounts of text to predict the next word in a sentence, which lets them write patient stories and clinical notes on demand (Vaswani et al., 2017; Brown et al., 2020). Nursing teachers report that this cuts the time spent on case design (Liu et al., 2025; Reed & Dodson, 2024). The problem is accuracy. These models write from patterns in their training data, not from checked medical sources, so the text can read well and still be wrong. A study of clinical summaries found a hallucination rate near 1.47 percent, and 44 percent of those errors were serious enough to change a diagnosis or a care plan (Asgari et al., 2025). When a patient story held one planted false detail, six models repeated or added to it in 50 to 82 percent of their answers (Omar et al., 2025). The same weakness reaches references. One study found that GPT-3.5 made up 55 percent of its citations and GPT-4 made up 18 percent (Walters & Wilder, 2023), while another found that 69 percent of the medical references it suggested did not exist (Gravel et al., 2023). In a nursing scenario, these mistakes show up as wrong drug doses, impossible vital signs, or milestones that do not fit the patient's age, and students study the scenario as if it were correct.

Retrieval-Augmented Generation, or RAG, is one way to lower these errors. Lewis et al. (2020) designed RAG to pair a language model with a search step. The system first pulls relevant passages from a trusted document set, and then the model writes its answer using those passages as its source. Because the facts come from the documents and not from the model's memory, the model has less room to invent them, and each claim can be traced back to a source. The effect has been measured. On the MIRAGE medical test, adding retrieval raised the accuracy of six models by up to 18 percentage points (Xiong et al., 2024). In a hospital study, retrieval lifted a small model's exact match on diagnosis codes from 0.8 percent to 17.6 percent (Klang et al., 2024). On structured outputs, it cut invented workflow steps from about 21 percent to under 7.5 percent (BÃ©chard & Marquez Ayala, 2024).

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

# Chapter 2

## Review of Related Literature and Studies

This chapter reviews the research behind generative AI, clinical hallucination, and retrieval-augmented generation, and why they matter for nursing scenario writing. It follows the problem from Chapter 1. Faculty have little time to write scenarios, plain language models invent clinical content, and grounding the model on the school's own scenarios may close that gap. The chapter covers large language models, clinical hallucination, retrieval-augmented generation, ways to fit a model to a field, generative AI in nursing and medical education, and ethics. It then looks at the studies behind these ideas, states the gap, and ends with a synthesis and a theoretical framework.

### Related Literature

#### Large language models

Generative AI makes new text instead of sorting or labeling it. The kind that matters here is the large language model, or LLM. Modern LLMs use the transformer design from Vaswani et al. (2017), which reads a whole sentence at once and can connect distant parts of a text. GPT-3 showed that a model trained on enough text can do tasks it was never trained for just by reading examples in the prompt (Brown et al., 2020). The model writes one token at a time, picking the most likely next token. Its goal is fluent text, not true text.

For this study, the model is the engine of the AI draft assistant. The study uses a model through an API and does not train one from scratch, so the review looks at how a model behaves with and without grounding, not at how a model is built.

#### Clinical hallucination

A hallucination is fluent text that is not faithful to its source or the real world. Ji et al. (2023) divide hallucinations into intrinsic errors, which go against the source, and extrinsic errors, which add content that cannot be checked. In clinical work the risk is real. In carefully checked clinical summaries, the hallucination rate was near 1.47 percent, but 44 percent of those errors could change a diagnosis or a care plan (Asgari et al., 2025). When clinician-written cases had one planted false detail, six models repeated or expanded on it in 50 to 82 percent of answers (Omar et al., 2025). The same problem hits references. GPT-3.5 made up 55 percent of its citations and GPT-4 made up 18 percent (Walters & Wilder, 2023), and one study found that 69 percent of suggested medical references did not exist (Gravel et al., 2023). In nursing scenarios the result is wrong doses, conflicting vital signs, or milestones that do not fit the patient. Because students treat the scenario as correct, the error can turn into a wrong habit.

#### Retrieval-Augmented Generation

Retrieval-Augmented Generation, or RAG, pairs a language model with a search step. Lewis et al. (2020) introduced the design. A retriever turns documents and the question into vectors, finds the closest passages, and passes them to the model as context. The model then answers using both the question and the retrieved text. Because the facts come from the documents instead of the model's memory, an answer can be traced to a source, and the model has less room to invent what it does not know.

The approach holds up in medical tests. On the MIRAGE benchmark of 7,663 questions, retrieval raised the accuracy of six models by up to 18 percentage points over plain prompting (Xiong et al., 2024). Almanac, a clinical RAG assistant that searches trusted sources, beat ChatGPT-4, Bing, and Bard on factuality, completeness, preference, and safety when clinicians rated it (Zakka et al., 2024). In a hospital study, retrieval beat human coders on diagnosis codes and lifted a small model's exact match from 0.8 percent to 17.6 percent (Klang et al., 2024). On structured output, it cut invented workflow steps from about 21 percent to under 7.5 percent (BÃ©chard & Marquez Ayala, 2024).

RAG is not always a win, and that is part of the gap this study handles. Barnett et al. (2024) listed seven ways RAG systems fail in practice, from a missing document to an answer that never gets extracted. MedMobile, a small medical model, improved with fine-tuning and reasoning prompts, but retrieval did not help its multiple-choice answers and slightly hurt accuracy (Vishwanath et al., 2024). The effect of retrieval depends on the task, the document set, and the model, so it has to be measured instead of assumed.

#### Fitting a model to a field

Two ways to fit a general model to a field are fine-tuning and retrieval. Fine-tuning trains the model further on examples and changes its weights. It is good for style and format, but it needs labeled data and does not hold rare facts well. Retrieval adds facts at the moment of answering and can be updated without retraining (Lewis et al., 2020). On less common facts, retrieval has done better than fine-tuning, especially for the rarest items (Soudani et al., 2024).

Distillation is a related idea, where a small model learns to copy a larger one. In one method, the small model learns not only the answer but the reason behind it, and a 770-million-parameter model beat a 540-billion-parameter model on one test while using less data (Hsieh et al., 2023). This study does not fine-tune the main generator. It compares a plain prompt against a RAG prompt on the same API model. Fine-tuning appears only as a small side model made by distillation and checked on schema validity alone. Distillation copies style and structure well but does not store facts, so factual safety still needs grounding (Vishwanath et al., 2024).

#### Generative AI in nursing and medical education

Generative AI is entering nursing education. Harder (2023) argued that ChatGPT can speed up a simulation teacher's draft while everything it writes still needs review. Vaughn and Ford (2024) tested that idea. Five AI-written simulations went to 18 expert reviewers, who liked the content but found missing information in every case. Reed and Dodson (2024) used AI backstories before a simulation and found that students were less anxious and knew more about the patient. Liu et al. (2025) interviewed 13 ICU instructors who used AI for case design. They said it saved time and helped beginners, but that the content still had to be checked.

These findings match the workload problem in Chapter 1. Nursing schools run on few faculty, and one good scenario can take a full day (Bambini, 2016; Watts et al., 2021). If AI can write the first draft, teachers can spend more time teaching and less time checking. The open question is how much checking is left when the draft comes from a model with no grounding, and that question is the focus of this study.

#### Ethics and data privacy

Using AI on clinical and school content raises questions about consent, accuracy, and who is responsible. In the Philippines, the Data Privacy Act of 2012, or Republic Act No. 10173, protects personal data, and health data gets extra protection. This study avoids the issue at the source. The document set is faculty-written simulation content, drafts stay drafts, and real patient data never enters the system. Every scenario is reviewed and approved by Nursing Department faculty before it can be published, so a person stays responsible for the content. The research supports this step. Studies of AI-assisted case design keep finding that expert review is required, not optional (Liu et al., 2025; Vaughn & Ford, 2024; Asgari et al., 2025).

### Related Studies

These studies shape the design of the study. They are grouped by what they show.

Studies on ungrounded models show the size of the risk. Asgari et al. (2025) checked clinical summaries sentence by sentence and found a low overall error rate but a high share of serious errors. Omar et al. (2025) tested 300 doctor-checked cases with one false detail each, and the models copied the false detail in most answers. Walters and Wilder (2023) and Gravel et al. (2023) found that models made up a large share of the references they were asked to produce. Together these studies show that a model can sound sure and still be wrong.

Studies on grounding show the opposite pattern. Lewis et al. (2020) introduced RAG and showed that pulling in outside documents improves answers on knowledge-heavy tasks. Xiong et al. (2024) tested many RAG setups on 7,663 medical questions and found accuracy gains of up to 18 points over plain prompting. Zakka et al. (2024) built the clinical assistant Almanac and had clinicians rate it above the leading chatbots on factuality, completeness, and safety. Klang et al. (2024) found that retrieval let a small model beat human coders on diagnosis codes, and BÃ©chard and Marquez Ayala (2024) found that it cut invented steps in structured output from 21 percent to under 7.5 percent.

Grounding is not always a win. Barnett et al. (2024) listed seven ways RAG systems fail in practice, from missing documents to answers that never get extracted. Vishwanath et al. (2024) found that adding retrieval to a small medical model actually lowered its accuracy on multiple-choice questions, likely because the model could not handle the extra context. This is why the effect of grounding has to be measured for each task instead of assumed.

For fitting a model to a field, Soudani et al. (2024) found that retrieval beat fine-tuning on less common facts, especially the rarest ones. Hsieh et al. (2023) showed that a small model can learn from a larger one's reasoning and match part of its performance with less data. Both support keeping the main comparison on grounding and treating a trained small model as a side result.

In teaching, Harder (2023) and Vaughn and Ford (2024) found that AI writes usable drafts but misses details that experts catch. Reed and Dodson (2024) found that AI backstories helped students prepare with less anxiety, and Liu et al. (2025) found that simulation instructors saved time with AI but still had to check the content. Watts et al. (2021) set the design standards any scenario must meet.

Three studies are worth a closer look. Lewis et al. (2020) is the source of RAG itself, a search step plus a generator, but it was first tested on general questions, not on clinical safety or exact numbers, so this study applies it to a new setting. Xiong et al. (2024) gives the largest medical evidence, with gains of up to 18 points and a warning that a model can miss facts placed in the middle of a long context, which matters for how the school's scenarios are split and ordered. Vishwanath et al. (2024) is the warning: retrieval lowered accuracy on a small model, which shows the effect depends on the model, the task, and the document set, and that is why a controlled comparison is needed here.

### Gaps in the Literature

The studies above show that AI can write clinical and teaching content quickly, that the speed costs accuracy, and that retrieval can bring much of the accuracy back by feeding the model checked documents. Three gaps remain.

First, comparisons of grounded and non-grounded models exist, but almost all run on exam questions, medical coding, or summaries (Xiong et al., 2024; Klang et al., 2024; Asgari et al., 2025). A nursing scenario is different. It has to keep vital signs, orders, drug math, and milestones consistent inside one story, and no study here measured that kind of internal coherence.

Second, the judge is missing. Most evaluations use automatic text scores or a single benchmark, which cannot catch a wrong dose hidden in fluent writing. Some studies use human judges, but none used Nursing Department faculty to rate a multi-field scenario generator.

Third, the setting is missing. The literature tests models on their own or inside clinical tools, not inside a school hospital system where faculty write, assign, and grade scenarios. No study here grounded a generator on the school's own scenarios and compared it with a plain prompt in that live setting.

These gaps match the research questions in Chapter 1. This study compares RAG-grounded and non-grounded generation on schema validity, clinical plausibility, coherence, hallucination rate, latency, and cost, with Nursing Department faculty as judges, inside the Chansey scenario module.

### Synthesis of the Reviewed Literature and Studies

Generative AI shortens the writing task that Chapter 1 calls a bottleneck. Teachers who use it report large time savings (Liu et al., 2025; Reed & Dodson, 2024), and the drafts read well. The same research is blunt about the trade-off. Without grounding, models invent clinical detail in most answers under hard conditions (Omar et al., 2025), and even careful clinical summaries leave serious errors (Asgari et al., 2025). When asked for references, they make them up at high rates (Walters & Wilder, 2023; Gravel et al., 2023).

RAG answers the trade-off by moving facts out of the model and into a searchable, checkable set of documents (Lewis et al., 2020). The numbers favor it. Retrieval raised medical question accuracy by up to 18 points (Xiong et al., 2024), beat human coders on a precision task (Klang et al., 2024), and cut invented structured steps by two-thirds (BÃ©chard & Marquez Ayala, 2024). The research also warns against overconfidence. Barnett et al. (2024) listed seven ways retrieval fails, and MedMobile lost accuracy when retrieval was added (Vishwanath et al., 2024). Two studies add that AI content still needs clinical review (Liu et al., 2025; Vaughn & Ford, 2024).

Taken together, the evidence supports the study without proving it in advance. Grounding is the most promising fix for clinical hallucination so far, the nursing scenario task has not been tested with it, and faculty review is both needed and expected. The study therefore compares a RAG-grounded generator against a plain-prompt generator inside the faculty scenario builder, keeps faculty approval in the loop, and treats a small distilled model as a side result.

### Theoretical Framework

The study rests on four theories. Each one explains a part of the system, and together they show why a grounded generator helps nursing faculty.

#### Cognitive load theory

Cognitive load theory (Sweller, 1988) says working memory is limited. It separates the load from the material itself, the load from bad design or tools, and the load that builds understanding. Good teaching cuts the second kind so students can spend working memory on the third.

Faculty writing a scenario already carry a heavy load. They must keep vital signs, orders, drug math, and milestones consistent in one case. Checking an ungrounded AI draft adds more, because every number has to be verified. A grounded generator, tied to the faculty's own checked scenarios, removes most of that checking, so teachers can spend their memory on debriefing and lesson design. Here, cognitive load theory explains why grounding is a workload fix, not only a technical one.

#### Symbol grounding

The symbol grounding problem (Harnad, 1990) asks how symbols get meaning. A model that only predicts likely next tokens never connects those tokens to the world. An ungrounded language model is that kind of system. It writes "500" because "mg" often follows, not because it knows a dose. Harnad argued that symbols need an outside anchor. RAG provides one. It pulls checked facts from the Chansey scenarios into the prompt, so the words the model writes point to real, approved content instead of likely sequences. Here, symbol grounding explains why plain prompting is prone to hallucination and why retrieval, not better wording, is the fix.

#### Grounding theory and joint action

Grounding theory (Clark & Brennan, 1991) says communication works only when both sides share common ground. It breaks down when one side assumes context the other does not have. A plain prompt gives the model no shared context with the school, so it may write orders that clash with local rules. RAG builds that shared context on purpose. It hands the model the faculty's own scenario formats and clinical rules before it writes, and the model then works inside the boundaries the Nursing Department set. Here, grounding theory explains why the document set must come from the school and not from a general source.

#### Dual-memory and simulation-based learning theory

RAG can also be seen as two memories (Lewis et al., 2020). The model weights reason and write, and an outside index stores facts that can be updated without retraining. On the teaching side, the NLN Jeffries Simulation Theory (Jeffries, 2012) says good simulations need fidelity. That means objectives, realism, and clinical accuracy line up so students learn the right pattern (Jeffries, Rodgers, & Adamson, 2015). A hallucinated scenario breaks that fidelity and can teach a wrong fact. The dual-memory idea gives the mechanical reason the generator can stay faithful, and Jeffries gives the teaching reason it must.

#### Application of the theoretical framework in the study

Applied to the study, the theories map to the system. Cognitive load theory explains the faculty problem and predicts less checking. Symbol grounding explains why plain generation drifts and why retrieval anchors it. Grounding theory explains why the document set must be the school's own. Dual-memory and simulation theory tie the design to the learning result. Together they justify comparing grounded and non-grounded generation and checking the output with the people who teach from it.

