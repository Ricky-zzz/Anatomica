# Chapter 1

## The Problem and Its Background

### Introduction

This chapter presents the background of the study, the statement of the problem, the objectives, the significance, and the scope and limitations of the research.

### Background of the Study

Nursing education prepares students to make clinical decisions under pressure, and simulation-based learning carries much of that training. In the Philippines, CHED Memorandum Order No. 15, series of 2017 requires nursing programs to build clinical reasoning and safe patient management through outcome-based instruction, and simulation is a common way to deliver that without risk to patients (Commission on Higher Education, 2017). Simulation gives students a controlled place to practice deterioration events, medication administration, and documentation, with debriefing afterward (Bambini, 2016; Jeffries, 2012). This training depends on faculty, and faculty are in short supply. A study of 192 clinical instructors in a highly urbanized city in the Central Philippines found that most were part-time staff with only a few years of service (Noblezada et al., 2025). The outflow of experienced nurses to overseas markets adds to the shortage (Alibudbud, 2023). The pattern is global as well. The American Association of Colleges of Nursing (AACN) recorded a 7.2 percent vacancy rate in budgeted full-time faculty positions, and 80.9 percent of those openings require or prefer a doctoral degree. Schools turned away more than 92,000 qualified applications in one academic cycle because they could not staff enough sections (American Association of Colleges of Nursing, 2025).

Those limited faculty hours now compete with scenario authoring. Building one high-fidelity, INACSL-compliant scenario takes extensive work. A complete scenario package holds patient demographics, chief complaint, history, progressive vital signs, laboratory and imaging results, physician orders, medication administration records, and facilitator cues. Reports on scenario authoring place the effort at up to 100 hours for a single scenario, and the authoring steps are well documented (Bambini, 2016). The Healthcare Simulation Standards of Best Practice from the International Nursing Association for Clinical Simulation and Learning require measurable objectives, alignment of physical and conceptual fidelity, and structured facilitation and debriefing, which adds to the design burden (Watts et al., 2021). Research on generative AI in simulation design shows the same friction from the inside: educators report that the tools write usable drafts quickly, but that pertinent content is often missing and the output still needs expert review before a scenario is safe to use (Harder, 2023; Vaughn & Ford, 2024). Schools that cannot spare that time fall back on static case studies or commercial scenario banks. Pre-packaged banks are professionally reviewed, but they cost money, stay fixed, and rarely match local disease profiles, drug formularies, or the documentation habits of the school's own hospital information system.

Generative AI offers a way around the authoring bottleneck. Large language models (LLMs) are transformer-based neural networks trained to predict the next token in a sequence from massive text corpora (Vaswani et al., 2017; Brown et al., 2020). They can draft patient backstories and clinical narratives quickly, and nursing educators report that the tools cut the time needed for case design (Liu et al., 2025; Reed & Dodson, 2024). The risk is accuracy. A language model writes from patterns in its training data, not from verified medical sources, so it can produce text that reads well but is clinically wrong. In tightly controlled clinical summarization, the hallucination rate runs near 1.47 percent, but 44 percent of those hallucinations are major errors that could change a diagnosis or a care plan (Asgari et al., 2025). When clinical prompts contain a planted false detail, six tested models repeated or elaborated on it in 50 to 82 percent of outputs (Omar et al., 2025). The failure extends to references. Studies that asked models to generate bibliographies found that GPT-3.5 fabricated 55 percent of its citations and GPT-4 still fabricated 18 percent (Walters & Wilder, 2023); a second study found 47 percent of generated medical references were fabricated and only 7 percent were both authentic and accurate (Bhattacharyya et al., 2023); a third put the fabrication rate of medical references at 69 percent (Gravel et al., 2023). In a nursing scenario, the same failures appear as wrong drug doses, impossible vital signs, and uncalibrated milestones, and students study the scenario as if it were correct.

Retrieval-Augmented Generation (RAG) addresses this by grounding the output in a specific document set. Lewis et al. (2020) introduced RAG as a design that pairs a language model with a dense retriever. The retriever finds relevant passages from a knowledge base, and the model writes its answer using those passages as context. Because the facts come from the retrieved documents, the model has less room to invent them, and each claim can be traced to a source. The effect has been measured in medical tasks. On the MIRAGE benchmark, retrieval improved the accuracy of six language models by up to 18 percentage points over chain-of-thought prompting (Xiong et al., 2024). Almanac, a clinical RAG system, outperformed ordinary LLMs on factuality, completeness, and safety when judged by clinicians (Zakka et al., 2024). A hospital study found RAG lifted the exact-match rate of a small model's diagnosis codes from 0.8 percent to 17.6 percent (Klang et al., 2024). On structured outputs, retrieval reduced hallucinated workflow steps from about 21 percent to under 7.5 percent (Béchard & Marquez Ayala, 2024). Oncology and multimodal evaluations report similar drops in fabricated clinical content (Pawlik & Deniziak, 2026; Wołk, 2025).

RAG is not a guaranteed fix. Retrieval systems have their own failure points: missing content, low-ranked documents, context that does not fit, wrong formats, and answers that are present but never extracted (Barnett et al., 2024). The benefit also depends on the model and task. Some small models did not gain from retrieval under test, and edge-case retrieval noise can destabilize a generator (Vishwanath et al., 2024). For scenario authoring, the knowledge base would be the faculty's own published scenarios, so a draft inherits the institution's format, competency tags, and local clinical context, and a human reviewer remains responsible for the final content (Liu et al., 2025; Clark & Brennan, 1991).

Current research on generative clinical content mostly tests models in isolation, on general medical text, or outside a working educational hospital information system. Few studies compare a grounded and a non-grounded generator inside the same authoring tool, using the institution's own scenarios as the only source of grounding, and rate the output with faculty judges. The gap is the missing evidence that grounding, and not the model alone, reduces clinical hallucination in nursing scenario generation. To address this, the present study builds an AI draft assistant inside the scenario builder of Chansey, an educational hospital information system, and compares RAG-grounded generation against non-grounded generation on schema validity, clinical plausibility, hallucination rate, latency, and cost.

### Statement of the Problem

Faculty authoring of nursing scenarios is slow, and one scenario can take many hours of faculty work (Bambini, 2016). Generative AI can cut drafting time, but a plain language model writes without institutional grounding and can hallucinate drug doses, vital signs, and milestones (Asgari et al., 2025; Omar et al., 2025). Both options produce fluent text, so the difficulty is not generating a scenario. The difficulty is deciding whether grounding the model on faculty-authored content makes the output safe enough to use. Consequently, it is necessary to evaluate and compare a RAG-grounded generator against a non-grounded one inside the faculty scenario builder.

This study addresses the following research questions:

1. What is the schema validity rate and clinical plausibility of scenarios generated by RAG-grounded and non-grounded generation, as rated by Nursing Department faculty?
2. What is the hallucination and contradiction rate, including coherence between orders and diagnosis, of each generation condition?
3. Is there a significant difference between RAG-grounded and non-grounded generation in schema validity, clinical plausibility, and hallucination rate?
4. What is the latency and token cost of each condition for real-time faculty use?
5. Which generation approach is more suitable for faculty scenario authoring, and why?

### Objectives of the Study

This study develops and evaluates a RAG-grounded AI draft assistant for nursing scenario generation and compares it with non-grounded generation in an educational hospital information system. Specifically, this study aims to:

1. Design and develop the AI draft assistant integrated into the Faculty Scenario Builder, supporting all research questions.
2. Evaluate the schema validity rate and clinical plausibility of RAG-grounded and non-grounded outputs using Nursing Department faculty ratings (RQ1).
3. Determine the hallucination and contradiction rate, including order and diagnosis coherence, of each condition (RQ2).
4. Compare the two conditions for a significant difference using a paired t-test or the Wilcoxon signed-rank test, with McNemar's test for validity and hallucination rates (RQ3).
5. Measure the latency and token cost of each condition (RQ4).
6. Recommend the more suitable approach for faculty scenario authoring (RQ5).

### Significance of the Study

This study investigates whether grounding a generative model on faculty-authored scenarios reduces clinical hallucination in nursing scenario generation.

The findings will benefit Nursing Department faculty by showing whether a grounded draft tool can cut the hours spent writing scenarios while keeping the clinical content under their approval, which frees time for facilitation and debriefing.

The findings will benefit nursing students by increasing the number and variety of scenarios available for practice and by keeping hallucinated clinical details out of the material they study.

The findings will benefit developers and nursing informatics researchers by providing measured evidence on RAG grounding for structured clinical content, an area with few comparative and faculty-validated results inside a working educational hospital information system.

The findings will benefit educational institutions by giving them a tested path to speed up scenario authoring without handing clinical authority to a model, which supports the outcome-based requirements of CHED Memorandum Order No. 15 (Commission on Higher Education, 2017).

The findings will benefit future researchers by leaving a documented pipeline, rubric, and dataset that can be extended to larger corpora, other competencies, or a fine-tuned local model.

### Scope and Limitations

This study covers the development of an AI draft assistant inside the Faculty Scenario Builder of Chansey, an educational hospital information system. The comparison tests two generation conditions. RAG-grounded generation retrieves the top-k faculty-authored scenarios relevant to a competency and difficulty level, while non-grounded generation sends a plain prompt with no retrieval. Both conditions use the same commercial language model through an API, so the study uses a model and does not train one from scratch. The grounding corpus is 12 to 15 faculty-authored scenarios stored in the Chansey database, and outputs follow the existing scenario schema of patient fields, orders, and expected milestones. The metrics are schema validity rate, clinical plausibility, order and diagnosis coherence, hallucination and contradiction rate, latency, and token cost. Nursing Department faculty rate the drafts on a rubric. A rule-based calculation produces a student weakness label from progress logs, and that label feeds the generation prompt. A fine-tuned lightweight model is included as a secondary deployment artifact, measured only on schema validity against the API baseline.

The study has limits. The grounding corpus is small, so results reflect a single institution and may not generalize to other nursing programs. Faculty-authored scenarios hold de-identified simulation content only, and no real patient data is used. Validation comes from Nursing Department faculty, not from a physician panel, so the study does not claim physician-level diagnostic accuracy. The API model provider and version affect reproducibility, because hosted models change or retire over time. The study does not cover autonomous publishing or real clinical deployment, and generated scenarios stay as drafts until faculty approve them. Future work can test a larger corpus, add other competencies, and compare the fine-tuned model against the API baseline on clinical plausibility.

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

Gravel, J., D'Amours-Gravel, M., & Osmanlliu, E. (2023). Learning to fake it: Limited responses and fabricated references provided by ChatGPT for medical questions. *Mayo Clinic Proceedings: Digital Health*, 1(3), 226-234. https://doi.org/10.1016/j.mcpdig.2023.05.004

Harder, N. (2023). Using ChatGPT in simulation design: What can (or should) it do for you? *Clinical Simulation in Nursing*, 78, A1-A2. https://doi.org/10.1016/j.ecns.2023.02.011

Jeffries, P. R., Rodgers, B., & Adamson, K. (2015). NLN Jeffries simulation theory: Brief narrative description. *Nursing Education Perspectives*, 36(5), 292-293. https://doi.org/10.5480/1536-5026-36.5.292

Klang, E., Tessler, I., Apakama, D. U., Abbott, E., Glicksberg, B. S., Arnold, M., et al. (2024). Assessing retrieval-augmented large language model performance in emergency department ICD-10-CM coding compared to human coders. *medRxiv*. https://doi.org/10.1101/2024.10.15.24315526

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems*, 33, 9459-9474. https://arxiv.org/abs/2005.11401

Liu, J., Wang, L., He, X., Xia, Y., Gong, X., Wu, R., Li, S., & Wu, L. (2025). Leveraging generative artificial intelligence to enhance ICU novice simulation instructors' case design: A qualitative study. *Clinical Simulation in Nursing*, Article 101770. https://doi.org/10.1016/j.ecns.2025.101770

Noblezada, J. E., Guanzon, R., Sobrevilla, A. R. J., Patigayon, J. R., Guzon, M. A., Venus, R., Rico, A., & Dumdum, M. M. (2025). Workload of clinical instructors in a highly urbanized city. *Aloysian Interdisciplinary Journal of Social Sciences, Education, and Allied Fields*, 1(10), 1-17. https://doi.org/10.5281/zenodo.17339785

Omar, M., Sorin, V., Collins, J. D., Reich, D., Freeman, R., Gavin, N., et al. (2025). Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support. *Communications Medicine*, 5, 330. https://doi.org/10.1038/s43856-025-01021-3

Pawlik, L., & Deniziak, S. (2026). Reducing hallucinations in medical AI through citation enforced prompting in RAG systems. *Applied Sciences*, 16(6), 3013. https://doi.org/10.3390/app16063013

Reed, J. M., & Dodson, T. M. (2024). Generative AI backstories for simulation preparation. *Nurse Educator*, 49(4), 184-188. https://doi.org/10.1097/NNE.0000000000001590

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30, 5998-6008. https://doi.org/10.48550/arXiv.1706.03762

Vaughn, J., & Ford, S. H. (2024). Enhancing healthcare education: Leveraging ChatGPT for innovative simulation scenarios. *Clinical Simulation in Nursing*, 89, 101559. https://doi.org/10.1016/j.ecns.2024.101559

Vishwanath, K., Stryker, J., Alyakin, A., Alber, D. A., & Oermann, E. K. (2024). MedMobile: A mobile-sized language model with clinical capabilities. *BMJ Digital Health & AI*, 1(1), e000068. https://doi.org/10.1136/bmjdhai-2024-000068

Walters, W. H., & Wilder, E. I. (2023). Fabrication and errors in the bibliographic citations generated by ChatGPT. *Scientific Reports*, 13, 14045. https://doi.org/10.1038/s41598-023-41032-5

Watts, P. I., McDermott, D. S., Alinier, G., Charnetski, M., Ludlow, J., Horsley, E., Meakim, C., & Nawathe, P. A. (2021). Healthcare Simulation Standards of Best Practice: Simulation design. *Clinical Simulation in Nursing*, 58, 14-21. https://doi.org/10.1016/j.ecns.2021.08.009

Wołk, K. (2025). Evaluating retrieval-augmented generation variants for clinical decision support: Hallucination mitigation and secure on-premises deployment. *Electronics*, 14(21), 4227. https://doi.org/10.3390/electronics14214227

Xiong, G., Jin, Q., Lu, Z., & Zhang, A. (2024). Benchmarking retrieval-augmented generation for medicine. *Findings of the Association for Computational Linguistics: ACL 2024*, 6233-6251. https://doi.org/10.18653/v1/2024.findings-acl.372

Zakka, C., Shad, R., Chaurasia, A., et al. (2024). Almanac: Retrieval-augmented language models for clinical medicine. *NEJM AI*, 1(2). https://doi.org/10.1056/AIoA2300068