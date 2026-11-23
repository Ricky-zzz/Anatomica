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

The approach holds up in medical tests. On the MIRAGE benchmark of 7,663 questions, retrieval raised the accuracy of six models by up to 18 percentage points over plain prompting (Xiong et al., 2024). Almanac, a clinical RAG assistant that searches trusted sources, beat ChatGPT-4, Bing, and Bard on factuality, completeness, preference, and safety when clinicians rated it (Zakka et al., 2024). In a hospital study, retrieval beat human coders on diagnosis codes and lifted a small model's exact match from 0.8 percent to 17.6 percent (Klang et al., 2024). On structured output, it cut invented workflow steps from about 21 percent to under 7.5 percent (Béchard & Marquez Ayala, 2024).

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

Studies on grounding show the opposite pattern. Lewis et al. (2020) introduced RAG and showed that pulling in outside documents improves answers on knowledge-heavy tasks. Xiong et al. (2024) tested many RAG setups on 7,663 medical questions and found accuracy gains of up to 18 points over plain prompting. Zakka et al. (2024) built the clinical assistant Almanac and had clinicians rate it above the leading chatbots on factuality, completeness, and safety. Klang et al. (2024) found that retrieval let a small model beat human coders on diagnosis codes, and Béchard and Marquez Ayala (2024) found that it cut invented steps in structured output from 21 percent to under 7.5 percent.

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

RAG answers the trade-off by moving facts out of the model and into a searchable, checkable set of documents (Lewis et al., 2020). The numbers favor it. Retrieval raised medical question accuracy by up to 18 points (Xiong et al., 2024), beat human coders on a precision task (Klang et al., 2024), and cut invented structured steps by two-thirds (Béchard & Marquez Ayala, 2024). The research also warns against overconfidence. Barnett et al. (2024) listed seven ways retrieval fails, and MedMobile lost accuracy when retrieval was added (Vishwanath et al., 2024). Two studies add that AI content still needs clinical review (Liu et al., 2025; Vaughn & Ford, 2024).

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
