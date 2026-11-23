# Chapter 2

## Review of Related Literature and Studies

This chapter reviews the research behind generative AI, language model hallucination, and retrieval-augmented generation, and why these matters for nursing scenario authoring. It follows the problem raised in Chapter 1: faculty cannot spare the hours that scenario writing demands, plain language models hallucinate clinical content, and grounding the model on faculty-authored scenarios may close that gap. The review covers generative AI and large language models, clinical hallucination, retrieval-augmented generation, structured output generation, domain adaptation, generative AI in nursing and medical education, and the ethics of using AI in teaching. It then examines individual studies, states the gap in the literature, and closes with a synthesis and the theoretical framework that anchors the study.

### Related Literature

#### Generative AI and Large Language Models

Generative AI refers to systems that produce new text, images, or other content rather than classify or predict labels. The systems that matter for this study are large language models (LLMs). The modern LLM rests on the transformer architecture, introduced by Vaswani et al. (2017), which replaces sequential recurrence with multi-head self-attention so a network can model long-range dependencies in parallel. OpenAI's GPT-3 scaled this view, showing that an autoregressive model trained on massive text corpora can perform tasks it never trained on, simply by conditioning on examples in the prompt (Brown et al., 2020). The model generates text one token at a time, sampling each next token from a probability distribution. Fluency is its design goal. Truthfulness is not.

LLMs come in many sizes. Frontier models run into the hundreds of billions of parameters, while open models run from under one billion to about seventy billion. The biomedical field also has specialized models. BioMistral is a 7-billion-parameter model built from Mistral and further trained on PubMed Central, and it outperforms earlier open biomedical models on standard medical question-answering benchmarks (Labrak et al., 2024). Still, domain pre-training does not eliminate error. BioMistral itself showed a drop in accuracy on the PubMedQA set, which the authors attributed to hallucination on unbalanced classes (Labrak et al., 2024). A model that knows medical vocabulary can still invent an answer.

For this study, the generative model is the engine of the AI draft assistant. The study uses a model through an API and does not train one from scratch, so the review focuses on how a model behaves with and without grounding, not on how to build a model.

#### Clinical Hallucination in Language Model Output

A hallucination is fluent text that is not faithful to the source context or the real world. Ji et al. (2023) provide the standard taxonomy, dividing hallucinations into intrinsic errors that contradict a source and extrinsic errors that produce unverifiable content. In clinical settings the risk is concrete. In tightly controlled clinical summarization, the hallucination rate runs near 1.47 percent, but 44 percent of those hallucinations are major errors that could change a diagnosis or a care plan (Asgari et al., 2025). The picture worsens when prompts contain false detail. When clinician-validated vignettes carried one planted false element, six tested models repeated or elaborated on it in 50 to 82 percent of outputs (Omar et al., 2025). When models map clinical text to standard medical codes, many fail badly, and the ones that use retrieval gain sharply (Klang et al., 2024).

Citation fabrication is a quieter but damaging form of the same problem. Walters and Wilder (2023) asked models to write literature reviews and found that GPT-3.5 fabricated 55 percent of its citations and GPT-4 still fabricated 18 percent. Bhattacharyya et al. (2023) found 47 percent of ChatGPT-generated medical references were fabricated and only 7 percent were both authentic and accurate. Gravel et al. (2023) reported that 69 percent of the medical references suggested by ChatGPT did not exist, though they looked credible. These results matter for teaching materials that cite evidence, and they matter for this thesis because a scenario generator must be able to lean on trusted sources without inventing them.

In nursing scenarios, hallucination takes specific dangerous forms. Drug dosages can be wrong or written in the wrong unit, vital signs can contradict one another, and developmental milestones can sit outside the age group the scenario targets. Because students study the scenario as if it were correct, an ungrounded error does not just waste time. It teaches a wrong clinical behavior that could persist into real practice. This is the risk that motivates the comparative question in Chapter 1.

#### Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) is an architecture that pairs a language model with a retrieval step. Lewis et al. (2020) introduced the framework. A dense retriever turns documents and the input query into vectors, finds the most relevant passages by vector similarity, and passes them to the generator as context. The model then writes its answer conditioned on both the query and the retrieved text. Because the facts come from retrieved documents instead of the model's memory, an answer can be traced to a specific source, and the model has less room to invent what it does not know. Gao et al. (2024) divide RAG designs into Naive RAG, which follows a simple retrieve-read-generate pipeline, Advanced RAG, which adds query rewriting and re-ranking, and Modular RAG, which routes retrieval adaptively and can fuse multiple indexes.

The approach holds up under measurement in medical settings. On the MIRAGE benchmark, which covers 7,663 questions across five medical datasets, retrieval improved the accuracy of six different language models by up to 18 percentage points over chain-of-thought prompting, bringing open models up to the level of a frontier model (Xiong et al., 2024). Almanac, a clinical RAG assistant that retrieves from curated sources like PubMed and BMJ Best Practices, outperformed ChatGPT-4, Bing, and Bard on factuality, completeness, user preference, and adversarial safety when rated by a panel of clinicians (Zakka et al., 2024). A hospital study compared retrieval-enhanced LLMs with human coders on ED diagnosis codes and found the RAG systems won on accuracy and specificity, lifting a small model's exact-match rate from 0.8 percent to 17.6 percent (Klang et al., 2024). On structured output, RAG reduced hallucinated workflow steps from about 21 percent to under 7.5 percent (Béchard & Marquez Ayala, 2024).

RAG is not a guaranteed win, and that honest result is part of the gap this study addresses. Barnett et al. (2024) catalogued seven failure points that appear when engineering real RAG systems: the corpus lacks the needed content, the answer ranks below the top-k cutoff, the document is retrieved but lost before generation, the model ignores formatting instructions, the answer cannot be extracted from noisy context, the output misses the right specificity, and the answer is incomplete. MedMobile, a 3.8-billion-parameter model tuned for medicine, improved through fine-tuning, ensembling, and chain-of-thought prompting, but RAG did not help its multiple-choice answers and slightly hurt accuracy (Vishwanath et al., 2024). The effect of retrieval depends on the task, the corpus, and the model. Controlled comparison is the only way to learn when grounding pays off.

#### Structured Output and Schema Validation

Generating a nursing scenario for a database is not just a writing task. The output must satisfy a schema: age and weight fields, vital sign arrays, medication records, and milestone objects, all typed and non-contradictory. Plain prompting often produces fluent text that breaks that structure. Modern approaches solve the grammar problem in software. Willard and Louf (2023) showed that a language model's generation can be guided by a finite-state machine, so only tokens that keep the output inside a declared structure (a JSON schema or a regular expression) are allowed at each step. Libraries built on that idea guarantee syntactically valid output with almost no overhead.

Syntax is not meaning, and this is where the thesis draws its sharpest line. A model can output a structurally perfect JSON object with heart rate, blood pressure, and temperature fields while the values inside are absurd. Béchard and Marquez Ayala (2024) made the same point for code generation: retrieval mattered for validity, and a well-trained retriever let a small generator match a larger one. In scenario terms, schema validity answers "is the object parseable," and clinical plausibility answers "would a nurse believe the content." Chapter 1 measures both, and the literature says grounding drives the second one.

#### Domain Adaptation: Placing Knowledge into the Model or the Prompt

Two common ways to adapt a general model to a domain are fine-tuning and retrieval. Fine-tuning continues training on domain examples and changes the model weights. Parameter-efficient versions such as QLoRA adjust only small adapter matrices. Fine-tuning teaches style and format. It can make output follow the documentation structure, local terminology, and institutional shorthand of a corpus, but it struggles to memorize long-tail facts, and it needs annotated data and compute. Retrieval injects knowledge at inference time through the prompt, keeps facts in an external store, and updates that store without retraining (Lewis et al., 2020).

Evidence shows RAG can lift accuracy on rare entities where fine-tuning struggles. Soudani, Kanoulas, and Hasibi (2024) compared the two on less popular factual knowledge and found RAG outperformed fine-tuning by a large margin, especially for the least popular entities. The two can even combine: fine-tune for format, retrieve for facts, and the pair wins on smaller models (Soudani et al., 2024). Complementary work on medical question answering reached the same conclusion: RAG and hybrid RAG-plus-fine-tuning consistently beat fine-tuning alone for clinical queries (Pingua et al., 2025).

This study does not fine-tune the core generator. It compares a plain prompt against a RAG prompt, both on the same API model. Fine-tuning appears only as a secondary artifact: a lightweight model distilled from generated drafts, measured on one metric, schema validity. The literature supports that arrangement. Grounding governs factual precision and freshness, while tuning governs format and voice, and for a scenario generator the practical question is whether grounding alone reduces the clinical errors that matter (Lewis et al., 2020).

#### Distillation and Lightweight Models

Knowledge distillation trains a small model to imitate a larger one. In "distill step-by-step," the student learns not only the teacher's answer but the reasoning rationale behind it. A 770-million-parameter T5 model trained this way outperformed a 540-billion-parameter PaLM model on a natural language inference benchmark while using only 80 percent of the training data (Hsieh et al., 2023). Small medical models built by distillation can also exceed expectations. MedMobile, a 3.8-billion-parameter model passed the USMLE-style MedQA benchmark at 75.7 percent, on hardware small enough to run on a laptop or mobile device (Vishwanath et al., 2024).

Distillation matters to this thesis because the adviser asked for "our own model." The secondary objective is a lightweight on-premise generator that matches the scenario schema, trained on faculty scenarios and validated drafts. The literature shows why that goal is realistic but modest: distillation transfers style and structure well, yet it teaches format rather than facts. Factual safety still needs grounding or a knowledge source (Vishwanath et al., 2024). This matches the scope in Chapter 1, which keeps distillation secondary and limits it to schema validity.

#### Generative AI in Nursing and Medical Education

Generative AI has entered nursing education slowly but steadily. Harder (2023) opened the simulation-design conversation, arguing that ChatGPT can speed up a simulation educator's drafting work while everything it produces still needs review. Vaughn and Ford (2024) put that claim to test: five ChatGPT-generated simulations went to 18 expert reviewers, who rated the content favorably but found that pertinent information was missing in every scenario. Reed and Dodson (2024) generated AI backstories as a presimulation strategy and found that students reported less anxiety, more preparatory knowledge, and a stronger connection to the patient's story. Liu et al. (2025) interviewed 13 ICU simulation instructors who used generative AI for case design; the instructors said the tools reduced the time and complexity of drafting, helped beginners structure a scenario, and still required checking for clinical accuracy.

These findings align with the workload problem described in Chapter 1. Nursing programs run on a thin faculty base, and a single high-fidelity scenario can take a day or more of careful work (Bambini, 2016; Watts et al., 2021). If generative AI can remove the first draft, faculty have to audit less and design more. The unresolved question is how much auditing is left when the draft comes from a model with no grounding, and that question is the center of this thesis.

#### Ethical and Data Privacy Considerations

Using a generative model on clinical and educational content raises consent, accuracy, and accountability questions. In the Philippines, Republic Act No. 10173, the Data Privacy Act of 2012, governs personal information, and health data is a special category with stricter protection. This thesis avoids the problem at the source. The grounding corpus is faculty-authored simulation content, generated drafts stay drafts, and real patient data never enters the system. Every scenario produced by the assistant is reviewed and approved by Nursing Department faculty before it can be published, so a human stays responsible for clinical content. The literature supports this human-in-the-loop position. Studies of AI-assisted case design repeatedly conclude that expert review of generated content is a requirement, not an option (Liu et al., 2025; Vaughn & Ford, 2024; Asgari et al., 2025).

### Related Studies

The studies below measure generative models in clinical and educational settings. They were selected because each one speaks to part of this thesis: how RAG and plain generation compare, how small distilled models behave, and how faculty experience AI-assisted scenario work.

| Study | Focus | Method | Key Finding | Relevance to the study |
| --- | --- | --- | --- | --- |
| Lewis et al. (2020) | Retrieval-augmented generation | Neural retrieval plus sequence-to-sequence generation | RAG grounds answers in retrieved documents, improving factuality and providing verifiable sources | Foundation of the RAG-grounded condition |
| Asgari et al. (2025) | Clinical note summarization with LLMs | Clinician-annotated evaluation of 12,999 sentences | 1.47% hallucination rate; 44% of hallucinations are major errors | Baseline risk that grounding must reduce |
| Omar et al. (2025) | Adversarial hallucination in clinical prompts | 300 physician-validated vignettes, six models | Models elaborated on planted false details in 50 to 82% of outputs | Quantifies ungrounded clinical risk |
| Walters and Wilder (2023) | Citation fabrication | 84 generated literature reviews, 636 citations checked | GPT-3.5 fabricated 55% of citations; GPT-4 fabricated 18% | Grounding as a defense against fabricated sources |
| Bhattacharyya et al. (2023) | Citation fabrication in medical content | 115 references from 30 generated papers | 47% fabricated; only 7% authentic and accurate | Same, for medical content |
| Gravel et al. (2023) | Medical reference fabrication | 59 references from 20 medical questions | 69% of references were fabricated | Same, with expert raters |
| Xiong et al. (2024) | Medical RAG benchmark (MIRAGE) | 7,663 questions, 41 RAG configurations | RAG improved accuracy by up to 18 points | Quantifies the grounding benefit at scale |
| Zakka et al. (2024) | Clinical RAG assistant (Almanac) | 314 clinical questions reviewed by clinicians | Grounded retrieval beat standard LLMs on factuality and safety | Grounding evaluated by domain experts |
| Klang et al. (2024) | RAG medical coding | 500 ED visits, masked clinician review | RAG beat human coders; small model exact-match rose 0.8% to 17.6% | Retrieval lifts precision tasks |
| Béchard and Marquez Ayala (2024) | RAG for structured output | Workflow JSON generation | RAG cut hallucinated steps from 21% to under 7.5% | Retrieval improves schema-level validity |
| Barnett et al. (2024) | RAG failure points | Three production case studies | Seven failure points can break retrieval systems | Marks the limits of grounding |
| Vishwanath et al. (2024) | Small clinical model (MedMobile) | Ablation over fine-tuning, ensembling, RAG | RAG did not help; reasoning prompting did | Honest counter-example, grounding is task-dependent |
| Soudani et al. (2024) | RAG versus fine-tuning | Twelve models, low-frequency entity QA | RAG beat fine-tuning, especially for rare facts | Justifies retrieval over retraining |
| Pingua et al. (2025) | RAG versus fine-tuning in medicine | Five open models on MedQuAD | RAG and hybrid RAG plus fine-tuning beat fine-tuning alone | Same, in a medical dataset |
| Hsieh et al. (2023) | Distilling step-by-step | Multi-task distillation with rationales | 770M model beat 540B PaLM with less data | Basis for the secondary distilled artifact |
| Labrak et al. (2024) | BioMistral, open biomedical model | Ten medical QA benchmarks | Outperforms open biomedical peers; still hallucinates on some sets | Domain models reduce but do not remove error |
| Harder (2023) | Gen AI in simulation design | Editorial framing of the issue | AI drafts fast, but expert review is mandatory | Positions the faculty review requirement |
| Vaughn and Ford (2024) | ChatGPT for simulation scenarios | 5 scenarios, 18 expert reviewers | Favorable ratings, but missing content in all scenarios | Direct evidence for the review requirement |
| Liu et al. (2025) | Gen AI for nursing simulation case design | Interviews with 13 ICU instructors | Faster, accessible case design with an accuracy caveat | Direct evidence for faculty experience with AI drafts |
| Reed and Dodson (2024) | Gen AI backstories for simulation | Student survey after presimulation prep | Lower anxiety, more knowledge, stronger connection | Pedagogical benefit of AI content |
| Watts et al. (2021) | INACSL simulation standards | Standards document | Design must meet fidelity and objective standards | Standard the generator must satisfy |

Some studies deserve a closer look.

Vaswani et al. (2017) and Brown et al. (2020) built the foundation. Vaswani's transformer removed recurrence for self-attention, and Brown's GPT-3 showed that scaling that architecture to 175 billion parameters creates a model that can learn tasks from context. The limit for this thesis is that a model this capable is still set up to predict the next token, not to verify a fact, which is exactly why the grounding question exists (Vaswani et al., 2017; Brown et al., 2020).

Lewis et al. (2020) is the origin of RAG. The system combines a dense retriever with a parametric generator, and the authors showed gains on open-domain question answering and generation tasks. Its limit for this thesis is that the original evaluation ran on general knowledge questions. It did not test clinical safety or numerical precision inside an educational system, so the present study inherits an untested application of the architecture (Lewis et al., 2020).

Xiong et al. (2024) is the largest scaled evidence that retrieval works in medicine. Their MIRAGE benchmark ran 41 RAG configurations over more than 1.8 trillion prompt tokens, and the best systems raised accuracy by up to 18 percentage points. The same study reported a log-linear gain with more retrieved snippets and a "lost in the middle" effect when relevant facts sit deep in the context, a practical caution for how the grounding corpus is chunked and ordered (Xiong et al., 2024).

Zakka et al. (2024) is the closest companion on evaluation by human experts. Almanac was rated by a panel of eight board-certified clinicians and two practitioners; it beat the frontier chatbots on factuality, completeness, preference, and adversarial safety over 314 questions. The study shows that retrieval plus human judging is the pattern this thesis follows, with nursing faculty standing in for clinicians (Zakka et al., 2024).

Klang et al. (2024) showed the benefit on a precision task that resembles structured scenario fields. RAG fed one million historical ED records to the model, and a masked physician panel preferred the RAG codes for accuracy and specificity. The smallest model, Qwen-2-7B, jumped from 0.8 percent to 17.6 percent exact match. The lesson is that retrieval matters most for the smallest, cheapest models, which is the deployment reality of a school system (Klang et al., 2024).

Vishwanath et al. (2024) present the cautionary result. MedMobile improved through fine-tuning, ensembling, and chain-of-thought, but retrieval lowered its multiple-choice accuracy, likely because the small model could not carry extra context inside its window. The lesson is not that RAG is useless. It is that the benefit depends on model size, corpus quality, and task type, which is why a controlled comparison in this thesis is needed rather than assumed (Vishwanath et al., 2024).

Harder (2023) and Vaughn and Ford (2024) ground the educational side. The editorial framed the opportunity and the risk; the empirical study found expert reviewers noticed missing content in every AI-generated scenario. Together they support the workflow this thesis builds: an AI draft that faculty review before it can be published (Harder, 2023; Vaughn & Ford, 2024).

### Gaps in the Literature

The reviewed studies show that generative AI can write clinical and educational content quickly, that this speed breaks down on accuracy, and that retrieval can restore much of the accuracy by feeding the model verified documents. Three gaps remain.

First, head-to-head comparisons of grounded and non-grounded generation exist, but almost all of them run on diagnostic question answering, medical coding, or summarization (Xiong et al., 2024; Klang et al., 2024; Asgari et al., 2025). Nursing scenario generation is a different task. A scenario must hold vital signs, orders, drug calculations, and milestones consistent with one another within a single narrative. That internal coherence is not captured by benchmark questions, and no study in this review measured it directly.

Second, the instrument is missing. Clinical evaluations still lean on automated lexical metrics or single benchmarks, which cannot detect a wrong dosage hidden in fluent text (as the citation-fabrication studies show, a model can look authoritative while being wrong). Studies that use human judges for generative clinical content exist, but none in the reviewed set used Nursing Department faculty as the rater for a multi-field scenario generator.

Third, the setting is missing. The literature tests models in isolation or inside clinical decision tools, not inside an educational hospital information system where faculty author, assign, and grade scenarios. No study in this review grounded a generator on the institution's own faculty-authored scenarios and compared it with a plain-prompt baseline in that live context.

These gaps line up with the research questions in Chapter 1. The present study compares RAG-grounded and non-grounded generation on schema validity, clinical plausibility, coherence, hallucination rate, latency, and cost, with Nursing Department faculty as raters, inside the Chansey scenario module. The comparison is not assumed from the literature. It is the contribution.

### Synthesis of the Reviewed Literature and Studies

Generative AI shortens the authoring task that Chapter 1 identifies as a bottleneck. Nurses and educators who use it for case design report large time savings (Liu et al., 2025; Reed & Dodson, 2024), and the models produce structured, well-written drafts. The same literature is blunt about the trade-off. Ungrounded models hallucinate clinical detail at rates that reach a majority of outputs under adversarial conditions (Omar et al., 2025), and even optimized clinical summarization leaves about 44 percent of hallucinations as major errors (Asgari et al., 2025). When asked for evidence, the models fabricate references at alarming rates (Walters & Wilder, 2023; Bhattacharyya et al., 2023; Gravel et al., 2023).

RAG addresses the trade-off by moving facts out of the model's memory and into a retrieved, verifiable corpus (Lewis et al., 2020). Measured results favor it. Retrieval improved medical QA accuracy by up to 18 points (Xiong et al., 2024), beat human coders on a precision task (Klang et al., 2024), and cut hallucinated structured steps by two-thirds (Béchard & Marquez Ayala, 2024). The literature also refuses blanket certainty. Barnett et al. (2024) catalogued seven ways retrieval systems fail, and MedMobile lost accuracy when RAG was bolted on (Vishwanath et al., 2024). Two studies caution that generated content still needs clinical eyes (Liu et al., 2025; Vaughn & Ford, 2024).

Put together, the evidence supports the thesis rather than proving it beforehand. Grounding is the most promising known fix for clinical hallucination, the nursing scenario task has not yet been tested with it, and faculty review is both necessary and expected. The study therefore compares a RAG-grounded generator against a plain-prompt generator inside the faculty scenario builder, keeps faculty approval in the loop, and treats a distilled lightweight model as a secondary artifact. That design is traceable to every strand of this review.

### Theoretical Framework

The study rests on four theories. Each one explains a part of the system, and together they justify why a grounded generator helps nursing faculty.

#### Cognitive Load Theory

Cognitive load theory, developed by Sweller (1988), says that working memory is limited. Learning material imposes three kinds of load: intrinsic load from the complexity of the material itself, extraneous load from poor design or bad tools, and germane load from mental effort that builds understanding. Good instruction minimizes extraneous load so that working memory can be spent building schemas.

Faculty writing a scenario carry high intrinsic load. They must keep vital signs, orders, drug calculations, and milestones consistent across one case. When they check the work of an ungrounded AI draft, they multiply that load. Every number becomes suspect, so the tool that promised to save time forces extra auditing. A grounded generator, conditioned on the faculty's own verified scenarios, removes most of that checking, and faculty can spend their working memory on debriefing and teaching design instead of on verification. In this study, cognitive load theory explains why grounding is a faculty workload solution, not just a technical one.

#### Symbol Grounding

The symbol grounding problem, formulated by Harnad (1990), asks how arbitrary tokens come to mean anything. A statistical model that flips symbols according to co-occurrence patterns never attaches those symbols to the world. An ungrounded language model is that kind of system. It writes the token "500" because "mg" and "amoxicillin" often follow it, not because it knows a dose. Harnad argued that meaning requires the symbols to be anchored to something outside the symbol system. RAG supplies that anchor. The retriever pulls verified facts from the Chansey corpus into the context, so the tokens the generator emits refer to real, institution-approved content instead of probable sequences. In this study, symbol grounding explains why plain-prompt generation is fundamentally prone to hallucination and why retrieval, not better prompting, is the architectural fix.

#### Grounding Theory and Joint Action

Grounding theory, from Clark and Brennan (1991), says that successful communication requires participants to establish common ground, a shared foundation of context and mutual belief. Communication breaks down when one party assumes context the other does not have. A plain prompt gives the model no common ground with the institution. It generates from its broad training distribution, so it may invent orders that contradict local protocols or a formulary the school never uses. RAG establishes common ground explicitly: it retrieves the faculty's own scenario templates and clinical rules and hands them to the model before generation. The generator then works inside the pedagogical boundaries the Nursing Department set. In this study, grounding theory explains why local, faculty-authored retrieval matters over generic knowledge bases.

#### Dual-Memory and Simulation-Based Learning Theory

The RAG architecture itself can be read as a dual-memory model, a framing Lewis et al. (2020) made concrete: a parametric memory (the model weights) that reasons and writes, and a non-parametric memory (the external vector index) that stores verified facts that can be updated without retraining. On the pedagogy side, the NLN Jeffries Simulation Theory (Jeffries, 2012) holds that effective simulations need high fidelity: objectives, realism, and clinical accuracy aligned so students learn correct patterns (Jeffries, Rodgers, & Adamson, 2015). Hallucinated scenarios violate that construct. They break fidelity and let a student internalize a wrong clinical fact, then carry it into practice. The dual-memory model supplies the mechanical reason the generator can stay faithful; Jeffries supplies the educational reason it must.

#### Application of the Theoretical Framework in the Study

Applied to the study, the theories line up with the layers of the system. Cognitive load theory explains the faculty problem in Chapter 1 and predicts the practical benefit of less auditing. Symbol grounding explains why ungrounded generation drifts and why retrieval anchors it. Grounding theory explains why the corpus must be institutional, not generic. Dual-memory and simulation theory tie the architecture to the learning outcome. Together they give the study a coherent reason to compare grounded and non-grounded generation and to validate the output with the people who teach from it.

### References

Alibudbud, R. (2023). Addressing the burnout and shortage of nurses in the Philippines. *SAGE Open Nursing*, 9, 23779608231195737. https://doi.org/10.1177/23779608231195737

American Association of Colleges of Nursing. (2025). *Nursing faculty shortage fact sheet*. https://www.aacnnursing.org/news-data/fact-sheets/nursing-faculty-shortage

Asgari, E., Montaña-Brown, N., Dubois, M., Khalil, S., Balloch, J., Au Yeung, J., & Pimenta, D. (2025). A framework to assess clinical safety and hallucination rates of LLMs for medical text summarisation. *npj Digital Medicine*, 8, 274. https://doi.org/10.1038/s41746-025-01670-7

Bambini, D. (2016). Writing a simulation scenario: A step-by-step guide. *AACN Advanced Critical Care*, 27(1), 62-70. https://doi.org/10.4037/aacnacc2016986

Barnett, S., Kurniawan, S., Thudumu, S., Brannelly, Z., & Abdelrazek, M. (2024). Seven failure points when engineering a Retrieval Augmented Generation system. *Proceedings of the IEEE/ACM 3rd International Conference on AI Engineering (CAIN 2024)*, 194-199. https://doi.org/10.1145/3644815.3644945

Béchard, P., & Marquez Ayala, O. (2024). Reducing hallucination in structured outputs via Retrieval-Augmented Generation. *Findings of the NAACL 2024 Industry Track*, 228-238. https://doi.org/10.18653/v1/2024.naacl-industry.19

Bhattacharyya, M., Miller, V. M., Bhattacharyya, D., & Miller, L. E. (2023). High rates of fabricated and inaccurate references in ChatGPT-generated medical content. *Cureus*, 15(5), e39238. https://doi.org/10.7759/cureus.39238

Brown, T. B., Mann, B., Ryder, N., et al. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, 33, 1877-1901. https://doi.org/10.48550/arXiv.2005.14165

Clark, H. H., & Brennan, S. E. (1991). Grounding in communication. In L. B. Resnick, J. M. Levine, & S. D. Teasley (Eds.), *Perspectives on socially shared cognition* (pp. 127-149). American Psychological Association. https://doi.org/10.1037/10096-006

Commission on Higher Education. (2017). *Policies, standards and guidelines for the Bachelor of Science in Nursing (BSN) program* (CMO No. 15, s. 2017). https://ched.gov.ph/wp-content/uploads/2017/10/CMO-15-s-2017.pdf

Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., Wang, M., & Wang, H. (2024). Retrieval-augmented generation for large language models: A survey. *arXiv preprint arXiv:2312.10997*. https://doi.org/10.48550/arXiv.2312.10997

Gravel, J., D'Amours-Gravel, M., & Osmanlliu, E. (2023). Learning to fake it: Limited responses and fabricated references provided by ChatGPT for medical questions. *Mayo Clinic Proceedings: Digital Health*, 1(3), 226-234. https://doi.org/10.1016/j.mcpdig.2023.05.004

Harder, N. (2023). Using ChatGPT in simulation design: What can (or should) it do for you? *Clinical Simulation in Nursing*, 78, A1-A2. https://doi.org/10.1016/j.ecns.2023.02.011

Harnad, S. (1990). The symbol grounding problem. *Physica D: Nonlinear Phenomena*, 42(1-3), 335-346. https://doi.org/10.1016/0167-2789(90)90087-6

Hsieh, C.-Y., Li, C.-L., Yeh, C.-K., Nakhost, H., Fujii, Y., Ratner, A., Krishna, R., Lee, C.-Y., & Pfister, T. (2023). Distilling step-by-step! Outperforming larger language models with less training data and smaller model sizes. *Findings of the Association for Computational Linguistics: ACL 2023*, 8003-8017. https://doi.org/10.18653/v1/2023.findings-acl.507

Jeffries, P. R., Rodgers, B., & Adamson, K. (2015). NLN Jeffries simulation theory: Brief narrative description. *Nursing Education Perspectives*, 36(5), 292-293. https://doi.org/10.5480/1536-5026-36.5.292

Jeffries, P. R. (Ed.). (2012). *Simulation in nursing education: From conceptualization to evaluation* (2nd ed.). National League for Nursing.

Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., et al. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys*, 55(12), 1-38. https://doi.org/10.1145/3571730

Klang, E., Tessler, I., Apakama, D. U., Abbott, E., Glicksberg, B. S., Arnold, M., et al. (2024). Assessing retrieval-augmented large language model performance in emergency department ICD-10-CM coding compared to human coders. *medRxiv*. https://doi.org/10.1101/2024.10.15.24315526

Labrak, Y., Bazoge, A., Morin, E., Gourraud, P.-A., Rouvier, M., & Dufour, R. (2024). BioMistral: A collection of open-source pretrained large language models for medical domains. *Findings of the Association for Computational Linguistics: ACL 2024*, 5848-5864. https://doi.org/10.18653/v1/2024.findings-acl.348

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems*, 33, 9459-9474. https://arxiv.org/abs/2005.11401

Liu, J., Wang, L., He, X., Xia, Y., Gong, X., Wu, R., Li, S., & Wu, L. (2025). Leveraging generative artificial intelligence to enhance ICU novice simulation instructors' case design: A qualitative study. *Clinical Simulation in Nursing*, Article 101770. https://doi.org/10.1016/j.ecns.2025.101770

Noblezada, J. E., Guanzon, R., Sobrevilla, A. R. J., Patigayon, J. R., Guzon, M. A., Venus, R., Rico, A., & Dumdum, M. M. (2025). Workload of clinical instructors in a highly urbanized city. *Aloysian Interdisciplinary Journal of Social Sciences, Education, and Allied Fields*, 1(10), 1-17. https://doi.org/10.5281/zenodo.17339785

Omar, M., Sorin, V., Collins, J. D., Reich, D., Freeman, R., Gavin, N., et al. (2025). Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support. *Communications Medicine*, 5, 330. https://doi.org/10.1038/s43856-025-01021-3

Pawlik, L., & Deniziak, S. (2026). Reducing hallucinations in medical AI through citation enforced prompting in RAG systems. *Applied Sciences*, 16(6), 3013. https://doi.org/10.3390/app16063013

Pingua, B., Sahoo, A. S., Kandpal, M., Murmu, D., Rautaray, J., & Barik, R. K. (2025). Medical LLMs: Fine-tuning versus retrieval-augmented generation. *Frontiers in Artificial Intelligence* [preprint]. https://pmc.ncbi.nlm.nih.gov/articles/PMC12292519/

Reed, J. M., & Dodson, T. M. (2024). Generative AI backstories for simulation preparation. *Nurse Educator*, 49(4), 184-188. https://doi.org/10.1097/NNE.0000000000001590

Reid, J. A. (2024). Building clinical simulations with ChatGPT in nursing education. *Journal of Nursing Education*, 64(5), e6-e7. https://doi.org/10.3928/01484834-20240424-05

Soudani, H., Kanoulas, E., & Hasibi, F. (2024). Fine tuning vs. retrieval augmented generation for less popular knowledge. *Proceedings of the 2024 Annual International ACM SIGIR Conference (SIGIR-AP)*. https://doi.org/10.1145/3673791.3698415

Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12(2), 257-285. https://doi.org/10.1207/s15516709cog1202_4

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30, 5998-6008. https://doi.org/10.48550/arXiv.1706.03762

Vaughn, J., & Ford, S. H. (2024). Enhancing healthcare education: Leveraging ChatGPT for innovative simulation scenarios. *Clinical Simulation in Nursing*, 89, 101559. https://doi.org/10.1016/j.ecns.2024.101559

Vishwanath, K., Stryker, J., Alyakin, A., Alber, D. A., & Oermann, E. K. (2024). MedMobile: A mobile-sized language model with clinical capabilities. *BMJ Digital Health & AI*, 1(1), e000068. https://doi.org/10.1136/bmjdhai-2024-000068

Walters, W. H., & Wilder, E. I. (2023). Fabrication and errors in the bibliographic citations generated by ChatGPT. *Scientific Reports*, 13, 14045. https://doi.org/10.1038/s41598-023-41032-5

Watts, P. I., McDermott, D. S., Alinier, G., Charnetski, M., Ludlow, J., Horsley, E., Meakim, C., & Nawathe, P. A. (2021). Healthcare Simulation Standards of Best Practice: Simulation design. *Clinical Simulation in Nursing*, 58, 14-21. https://doi.org/10.1016/j.ecns.2021.08.009

Wołk, K. (2025). Evaluating retrieval-augmented generation variants for clinical decision support: Hallucination mitigation and secure on-premises deployment. *Electronics*, 14(21), 4227. https://doi.org/10.3390/electronics14214227

Xiong, G., Jin, Q., Lu, Z., & Zhang, A. (2024). Benchmarking retrieval-augmented generation for medicine. *Findings of the Association for Computational Linguistics: ACL 2024*, 6233-6251. https://doi.org/10.18653/v1/2024.findings-acl.372

Zakka, C., Shad, R., Chaurasia, A., et al. (2024). Almanac: Retrieval-augmented language models for clinical medicine. *NEJM AI*, 1(2). https://doi.org/10.1056/AIoA2300068