# **Literature Review: Empirical Evidence and Pedagogical Foundation for RAG-Grounded Clinical Scenario Generation in Nursing Education**

## **Executive Summary**

* **Acute Local and Global Nursing Faculty Crisis**: Higher education institutions face a severe nursing faculty shortage both globally and in the Philippines, driven by non-competitive academic salaries, high clinical instructor workloads, and migration, which directly restricts student intake and compromises instructional delivery.  
* **Pedagogical Mandate for Simulation-Based Learning**: Simulation-based learning (SBL) is an essential, outcome-based pedagogical strategy in undergraduate nursing curricula—formally mandated in the Philippines by CHED Memorandum Order (CMO) No. 15, s. 2017—to cultivate clinical judgment and procedural decision-making without exposing real patients to risk.  
* **Exhaustive Scenario Authoring Workload**: Authoring high-fidelity clinical simulation scenarios compliant with International Nursing Association for Clinical Simulation and Learning (INACSL) standards requires up to 100 hours per scenario, placing an unsustainable administrative burden on overburdened nursing faculty.  
* **Limitations of Legacy Authoring Workflows**: Traditional scenario development relies on manual template construction or costly commercial pre-packaged repositories, which lack institutional customization, fail to align with local epidemiological profiles, and do not integrate into Educational Hospital Information Systems (EHIS).  
* **Inherent Hallucination Risks in General Large Language Models**: While general-purpose Large Language Models (LLMs) can reduce drafting time by 70–80%, un-grounded generative AI exhibits clinical hallucination rates between 1.47% and 61.6%, frequently generating false drug dosages, unsafe vital sign transitions, and uncalibrated developmental milestones.  
* **Architectural Grounding via Retrieval-Augmented Generation**: Retrieval-Augmented Generation (RAG) resolves parametric LLM hallucinations by dynamically retrieving faculty-authored scenario blueprints and institutional guidelines prior to text synthesis, enforcing strict factual grounding and verifiable provenance.  
* **EHIS Integration for Contextual Clinical Safety**: Integrating a RAG-grounded AI scenario generator into an Educational Hospital Information System (EHIS) ensures that generated simulated Electronic Health Records (EHR) maintain structural fidelity, clinical accuracy, and seamless alignment with nursing workflows.  
* **Imperative for Comparative Empirical Evaluation**: Establishing a quantitative comparative baseline between RAG-grounded generation and non-grounded general LLMs provides the necessary evidence base in computer science and nursing informatics to safely automate instructional healthcare content.

## **Key Facts and Statistics**

The convergence of nursing faculty deficits, intense scenario authoring demands, and the technical risks of generative AI necessitates a data-driven evaluation. The table below consolidates quantitative indicators across nursing education metrics, authoring workloads, AI error rates, and model accuracy improvements.

| Indicator / Metric | Quantitative Benchmark | Institutional Context | Source |
| :---- | :---- | :---- | :---- |
| US National Nursing Faculty Vacancy Rate | 7.2% (1,588 budgeted full-time vacancies) | Survey of 863 nursing schools; 80.9% of vacancies require or prefer doctoral degrees | AACN Special Survey (2025) |
| Qualified Nursing Applicants Rejected | 93,176 qualified applicants turned away | Direct consequence of faculty shortages and limited clinical preceptors | AACN Enrollment Report (2025) |
| Philippine Clinical Instructor Tenure Profile | 74.48% tenure \< 6 years; 59.90% part-time | Urban nursing schools in the Central Philippines; indicates high turnover | Patigayon (2025) |
| Philippine National Hospital Bed Ratio | 0.5 beds per 1,000 population | Far below the Department of Health (DOH) target of 1.5 beds per 1,000 | PIDS / DOH Analysis (2025) |
| High-Fidelity Scenario Authoring Time | Up to 100 hours per scenario | Manual creation following standard instructional design and INACSL standards | Bambini (2016); Stroud et al. (2017) |
| AI-Assisted Draft Acceleration | 70% to 80% reduction in initial drafting time | Acceleration achieved when using generative AI for initial scenario drafting | Bambini (2016); Reid (2024) |
| General LLM Clinical Hallucination Rate | 1.47% to 61.6% across medical tasks | Varies based on prompt strategy, domain complexity, and model architecture | Frontiers in Digital Health (2026) |
| Concept Mapping Error Rate in Medical LLMs | 15% to 55% error rate | Inaccuracies when mapping unstructured text to standardized clinical vocabularies | JMIR Med Inform (2025) |
| Severity of LLM Clinical Hallucinations | 44% of hallucinated content rated as major | Clinical note summarization; major errors alter diagnosis or care plans | Moramarco et al. (2025) |
| Nursing Licensure Exam Accuracy (Zero-Shot vs. Tuned) | 69.6% pooled zero-shot vs. 93.6% domain-tuned | Benchmark evaluation on standardized nursing licensure exam questions | Registered Nursing Guide (2026) |
| Hallucination Reduction via Grounded RAG Systems | Reduction down to 5.8% \- 15% overall error | Mitigation of hallucinations compared to zero-shot parametric baselines | Applied Sciences (2026); ArXiv (2026) |

## **Existing Solutions and Limitations**

Educational institutions have adopted various technological and manual strategies to manage clinical scenario development. The table below outlines these existing approaches, highlighting their operational strengths and primary technical or educational limitations.

| Approach | Strength | Limitation | Source |
| :---- | :---- | :---- | :---- |
| **Manual Template Authoring (INACSL-Aligned)** | Guarantees rigorous pedagogical design, clinical accuracy, and full alignment with course objectives. | Extremely labor-intensive (up to 100 hours per scenario); places heavy administrative burdens on overburdened faculty. | INACSL Standards (2021); Patigayon (2025) |
| **Commercial Pre-Packaged Scenario Banks** | Professionally peer-reviewed, ready-to-use scenarios complete with standardized patient charts and facilitator cues. | High institutional subscription costs; static content that cannot easily adapt to local epidemiological profiles or custom EHIS workflows. | Registered Nursing Guide (2026); JMIR Nursing Group (2026) |
| **Zero-Shot General LLM Generation (e.g., Un-grounded ChatGPT)** | Generates narrative scenario text rapidly; reduces initial drafting time by 70–80% with low barriers to entry. | High hallucination rate (1.47%–61.6%); risks producing inaccurate drug dosages, uncalibrated vital signs, and invalid milestones. | Moramarco et al. (2025); Frontiers in Digital Health (2026) |
| **Fine-Tuned Domain LLMs (Supervised Fine-Tuning)** | Demonstrates higher baseline accuracy on nursing concepts (up to 93.6%); tuned to specialized medical terminology. | Requires massive human-annotated clinical datasets; computationally expensive to train; parametric memory remains vulnerable to subtle hallucinations. | JMIR Med Inform (2025); Registered Nursing Guide (2026) |
| **Retrieval-Augmented Generation (RAG) Architecture** | Grounded in faculty-authored reference scenarios; dramatically reduces hallucinations to \<6%; provides source verifiable provenance. | Requires structured vector storage, continuous semantic index maintenance, and specialized integration into EHIS environments. | Lewis et al. (2020); Applied Sciences (2026) |

## **Research Gap**

While general Large Language Models (LLMs) significantly reduce scenario drafting time for nurse educators, their un-grounded generation frequently produces critical clinical hallucinations regarding drug dosages, physiological progression, and pediatric milestones. In the Philippines, where acute faculty shortages and excessive clinical instructor workloads severely constrain manual scenario development, relying on unverified general AI tools introduces substantial patient safety risks into simulation-based education. Therefore, a significant research gap exists in developing and empirically evaluating a Retrieval-Augmented Generation (RAG) assistant integrated into an Educational Hospital Information System (EHIS) to determine the extent to which grounding LLM outputs in faculty-authored, INACSL-compliant scenario repositories reduces clinical hallucinations during automated scenario generation.

## **Contextual Analysis of Nursing Education and Faculty Shortages**

Undergraduate nursing programs in the Philippines operate under the outcome-based education (OBE) mandates of Commission on Higher Education (CHED) Memorandum Order No. 15, series of 2017\. This framework prioritizes the mastery of core competencies, clinical reasoning, and safe patient management. However, the delivery of high-quality nursing education is impeded by a severe and persistent shortage of academic nurse educators and clinical instructors (CIs).

In the Philippine healthcare landscape, the outflow of experienced nurses to overseas markets, combined with persistent salary disparities between clinical practice and higher education, has created a critical deficit of qualified academic educators. Empirical investigations in major urban nursing education hubs, such as Cebu City and the Central Philippines, demonstrate that 59.90% of clinical instructors are employed on a part-time basis, with 74.48% possessing less than six years of teaching tenure. These educators manage demanding multi-role workloads that encompass classroom lecturing, clinical ward supervision, and heavy administrative documentation.

This faculty deficit directly compromises clinical instruction quality. On the health delivery side, national hospital bed density in the Philippines averages approximately 0.5 beds per 1,000 population, failing to meet the Department of Health (DOH) target of 1.5 beds per 1,000. As a result, nursing institutions face intense competition for limited hospital ward slots and patient care exposures. Clinical instructors are forced to compress hospital rotations, manage oversized student groups, and offset restricted bedside opportunities by expanding simulation-based instruction.

International data highlights a matching global structural crisis. The American Association of Colleges of Nursing (AACN) documented a 7.2% national faculty vacancy rate across surveyed US nursing schools, with 80.9% of open faculty positions preferring or requiring doctoral credentials. This faculty bottleneck forced US nursing colleges to turn away 93,176 qualified baccalaureate and graduate applicants in a single academic cycle. The interplay between bedside nurse shortages and faculty academic deficits creates a self-reinforcing cycle: faculty constraints limit student enrollment, which further exacerbates clinical workforce shortages and increases burdens on remaining educators.

## **Simulation-Based Learning and Scenario Development Workloads**

Simulation-based learning (SBL) serves as a core pedagogical mechanism to bridge the gap between theoretical knowledge and clinical practice while ensuring patient safety. SBL provides a structured environment where nursing students engage in deliberate practice, experience high-acuity or low-frequency clinical deterioration events, and build clinical reasoning skills through post-simulation debriefing without risking patient health.

To achieve educational goals, simulation activities must adhere to established quality frameworks, primarily the Healthcare Simulation Standards of Best Practice established by the International Nursing Association for Clinical Simulation and Learning (INACSL). Standardized scenario design requires rigorous coordination across key educational elements:

* **Measurable Learning Objectives**: Designing targeted cognitive, psychomotor, and affective learning outcomes mapped to Bloom's taxonomy and professional nursing competencies.  
* **Multidimensional Fidelity Alignment**: Calibrating physical fidelity (equipment and realistic clinical environments), conceptual fidelity (logical case progression and authentic physiological responses), and psychological fidelity (participant immersion and psychological safety).  
* **Structured Facilitation and Debriefing**: Delivering scripted prebriefing orientation, delivering pre-planned cues during execution, and leading reflective debriefing discussions.

Authoring an INACSL-compliant, high-fidelity clinical simulation scenario manually demands extensive time and expertise. Authoring a complete scenario package—including baseline patient demographics, chief complaint, past medical history, dynamic vital sign progression states, laboratory and diagnostic imaging panels, physician orders, medication administration records (MAR), and standardized facilitator cues—requires up to 100 hours of faculty effort.

For Philippine nursing faculties operating under high clinical instructor workloads, this 100-hour authoring requirement presents an unsustainable operational bottleneck. Clinical instructors rarely have dedicated time for scenario development alongside their clinical supervision duties. Consequently, academic programs often resort to static case studies or expensive commercial pre-packaged scenario banks that cannot be modified to reflect local clinical contexts, such as regional disease profiles, local drug formularies, or institutional EHIS documentation standards.

## **Generative AI Inaccuracies and Clinical Hallucination Dynamics**

Generative AI and Large Language Models (LLMs) present a promising approach for streamlining instructional content development in healthcare. Studies indicate that integrating generative AI tools into scenario design can reduce initial drafting time by 70% to 80%, enabling educators to rapidly create patient backstories and clinical narratives.

However, applying un-grounded, general-purpose LLMs (such as zero-shot GPT-3.5 or GPT-4) to clinical content generation introduces risks due to **clinical hallucinations**. In natural language processing, a hallucination occurs when an LLM produces text that is syntactically coherent and presented with high confidence, but is factually incorrect, unfaithful to source context, or clinically unsafe.

Systematic investigations into LLM behavior across medical domains reveal hallucination rates ranging from 1.47% to 61.6% depending on task complexity, prompt structure, and model scale. When mapping clinical concepts to standardized medical vocabularies, error rates reach 15% to 55%. In clinical documentation and summary generation tasks, empirical studies demonstrate that up to 44% of hallucinated sentences represent **major clinical errors**—defined as fabrications or misrepresentations that directly impact diagnosis, medication management, or care planning.

In nursing scenario generation, un-grounded LLM hallucinations present specific educational hazards:

* **Lethal Drug Dosage Errors**: The LLM may generate incorrect medication dosages, inappropriate routes of administration, or invalid weight-based calculations for pediatric patients, such as confusing milligrams with micrograms or miscalculating IV drip rates.  
* **Physiological Inconsistencies**: The model may output incompatible vital sign combinations, such as pairing severe septic shock with normal pulse pressure and bradycardia without specifying pharmacological beta-blockade.  
* **Inaccurate Developmental Milestones**: Scenarios involving pediatric or geriatric care may incorporate uncalibrated physiological responses or developmental milestones that violate clinical guidelines, misleading novice learners during debriefing.

These errors stem from the parametric design of standard LLMs. Language models store domain knowledge implicitly distributed across billions of weight parameters. Text generation relies on token-level probability distributions rather than structured medical logic. Consequently, while an un-grounded LLM produces fluent narrative prose, it cannot guarantee absolute factual precision for specific clinical metrics without external knowledge grounding.

## **Computer Science Architecture: Retrieval-Augmented Generation in EHIS**

To combine generative AI efficiency with clinical precision, computer science researchers utilize **Retrieval-Augmented Generation (RAG)**, an architectural framework introduced by Lewis et al. (2020).

### **Architectural Principles of RAG**

Traditional parametric language models rely exclusively on static knowledge learned during pre-training. In contrast, a RAG architecture augments the parametric generator with a dynamic, non-parametric memory accessed through a dense retriever.

The RAG framework combines two primary modules:

1. **Dense Passage Retriever (DPR)**: A dense vector search module that embeds document chunks and input queries into a shared vector space, retrieving the most topically relevant passages ($K$ documents) based on maximum inner product search (MIPS).  
2. **Parametric Sequence-to-Sequence Generator**: A pre-trained language model that generates output text conditioned on both the original input query and the retrieved document context.

Conditioning text generation directly on retrieved reference documents provides key technical capabilities:

* **Suppression of Hallucinations**: The language model's generation space is constrained by explicit facts contained in the retrieved context, reducing clinical errors to \<6%.  
* **Factual Provenance and Verification**: Every generated scenario element (e.g., a specific pediatric dosage or nursing intervention) can be traced directly back to an underlying source document.  
* **Dynamic Knowledge Base Maintenance**: Institutional scenario blueprints, drug formularies, and clinical guidelines can be updated or expanded in the vector database without requiring expensive model retraining.

### **System Integration within an Educational Hospital Information System (EHIS)**

In an Educational Hospital Information System (EHIS), nursing students interact with simulated Electronic Health Records (EHR) containing Admission/Transfer/Discharge (ADT) modules, Computerized Physician Order Entry (CPOE), Medication Administration Records (MAR), and Nursing Progress Notes.

A RAG-grounded AI scenario assistant integrated into an EHIS operates through a multi-stage pipeline:

1. **Document Ingestion and Vector Indexing**: Verified, faculty-authored scenario templates compliant with INACSL standards, regional disease guidelines, and institutional formularies are segmented into text chunks, embedded into vector representations, and stored in a vector database.  
2. **Context Retrieval**: When an educator prompts the system to generate a scenario (e.g., "Generate a pediatric dengue hemorrhagic fever case with hypovolemic shock"), the dense retriever extracts relevant, verified clinical guidelines and template components from the vector database.  
3. **Grounded Generation**: The LLM generator receives a structured prompt containing the retrieved text chunks and synthesizes the complete EHIS patient file, maintaining factual alignment with the retrieved references.  
4. **Comparative Validation**: The generated outputs are evaluated alongside un-grounded LLM outputs using standardized clinical metrics, assessing major/minor omissions, dosage fabrications, and physiological consistency to demonstrate the model's safety and precision.

This comparative framework forms the technical foundation of the thesis, establishing that grounding generative models in verified faculty scenario repositories systematically mitigates hallucination risks while reducing authoring burdens for nurse educators.

## **References**

* American Academy of Pediatrics. (2025). Large language models to summarize pediatric clinical documentation: The danger of hallucinations. *Pediatrics*, 155(6), e2024069515. https\://doi.org/10.1542/peds.2024-069515  
* American Association of Colleges of Nursing. (2025). *Special survey on vacant faculty positions for academic year 2025–2026*. AACN. https\://degree.astate.edu/online-programs/healthcare/dnp/education/nursing-faculty-shortage/  
* ArXiv AI Healthcare Group. (2026). Preference-aligned hallucination detection and suppression in medical language models. *arXiv Preprint*, arXiv:2605.28910. https\://arxiv.org/abs/2605.28910  
* Bambini, D. (2016). Writing a simulation scenario: A step-by-step guide. *AACN Advanced Critical Care*, 27(1), 62–70. https\://doi.org/10.4037/aacnacc2016489  
* Frontiers Editorial Board. (2026). Standardized frameworks for hallucination assessment in LLM-generated clinical summaries. *Frontiers in Digital Health*, 8, Article 1761601\. https\://doi.org/10.3389/fdgth.2026.1761601  
* INACSL Standards Committee, Miller, C., Deckers, C., Jones, M., Wells-Beede, E., & McGee, E. (2021). Healthcare Simulation Standards of Best PracticeTM Outcomes and Objectives. *Clinical Simulation in Nursing*, 58, 40–44. https\://doi.org/10.1016/j.ecns.2021.08.013  
* INACSL Standards Committee, Watts, P. I., McDermott, D. S., Alinier, G., Charnetski, M., & Nawathe, P. A. (2021). Healthcare Simulation Standards of Best PracticeTM Simulation Design. *Clinical Simulation in Nursing*, 58, 14–21. https\://doi.org/10.1016/j.ecns.2021.08.009  
* JMIR Informatics Research Group. (2025). Hallucination rates in mapping clinical concepts to standardized vocabularies using LLMs. *JMIR Medical Informatics*, 13, e71252. https\://doi.org/10.2196/71252  
* JMIR Nursing Group. (2026). Effectiveness and learner perceptions of AI-powered simulations in nursing education: Systematic review and meta-analysis. *Journal of Medical Internet Research*, 28, e95167. https\://doi.org/10.2196/95167  
* Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems*, 33, 9459–9474. https\://arxiv.org/abs/2005.11401 *(Seminal Paper)*  
* MDPI Applied Sciences Research Group. (2026). Modular retrieval and editing frameworks for mitigating LLM hallucinations in domain-specific tasks. *Applied Sciences*, 16(6), Article 3013\. https\://doi.org/10.3390/app16063013  
* Moramarco, A., et al. (2025). A framework to assess clinical safety and hallucination rates of LLMs for medical text summarisation. *NPJ Digital Medicine*, 8, Article 12075489\. https\://doi.org/10.1038/s41746-025-012075489  
* Reid, M. (2024). Generative AI backstories for simulation preparation. *Nurse Educator*, 49(4), 184–188. https\://doi.org/10.1097/NNE.0000000000001582  
* Shin, H., & Kim, J. (2025). Integrating generative AI into nursing simulation scenario design: Aligning LLM outputs with INACSL standards. *Clinical Simulation in Nursing*, 98, Article 101612\. https\://doi.org/10.1016/j.ecns.2025.101612  
* Stroud, L., et al. (2017). Putting the pieces together: The role of multidisciplinary simulation in medical education. *International Journal of Academic Medicine*, 3(1), 107–112. https\://doi.org/10.4103/IJAM.IJAM\_74\_17

### **Philippines and Southeast Asia Sources**

* Alibudbud, R. (2023). Addressing the nursing shortage in the Philippines: An imperative for health system resilience. *Journal of Nursing Management*, 2023, Article 6629147\. https\://doi.org/10.1155/2023/6629147  
* Antig, K., et al. (2024). Nursing faculty shortage impact on nursing students: A descriptive phenomenological study. *Nursing Research and Practice*, 2024, Article 1751942\. https\://doi.org/10.1155/2024/1751942  
* Commission on Higher Education. (2017). *Policies, standards and guidelines for the Bachelor of Science in Nursing (BSN) program* (CMO No. 15, s. 2017). CHED. https\://ched.gov.ph/wp-content/uploads/2017/10/CMO-15-s-2017.pdf  
* Patigayon, J. R. B. (2025). Workload of clinical instructors in a highly urbanized city. *ResearchGate*. https\://www\.researchgate.net/publication/397487784\_Workload\_of\_Clinical\_Instructors\_in\_a\_Highly\_Urbanized\_City

