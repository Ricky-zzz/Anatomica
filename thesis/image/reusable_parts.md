# reusable_parts.md — Old -> New Paper Reuse Map & Deep-Research Backlog

**Purpose:** Single source of truth for generating the NEW Chapters 1 and 2
(patient-face generation) in a fresh session. Use this file first, then the
source documents it points to. It lists (a) what carries over from the old
RAG paper, (b) what must be rewritten, and (c) exactly what to research next.

**New topic locked (see `THESIS_DRAFT_PLAN.md` and `AGENT_ARCHITECTURE_NOTE.md`
in this folder):** scenario-to-patient-face generation. Comparative = rendering
modality (diffusion PNG vs parametric 3D head) under ONE constant agentic
pipeline (parse -> expand -> render -> verify -> approve). Realism relaxed;
success = sign fidelity + teaching usefulness.

**Source docs:**
- OLD: `../text/THESIS_DRAFT_PLAN.md`, `../text/chap_1/chapter1_v2.md`,
  `../text/chap_2/chapter2_v2.md`, `../text/chap_1/chapter1.md`,
  `../text/chap_2/chapter2.md`, `../text/references.md`,
  `../text/chap_1/THESIS_DRAFT.md`
- NEW: `THESIS_DRAFT_PLAN.md`, `AGENT_ARCHITECTURE_NOTE.md` (this folder)

---

## 0. Quickstart (for the next generation session)

1. Read this file top to bottom.
2. Re-read the NEW plan (`THESIS_DRAFT_PLAN.md`) — sections 1-6, 9, 12.
3. Open `../text/chap_1/chapter1_v2.md` and `../text/chap_2/chapter2_v2.md`
   (the cleanest drafts) in parallel; use Section 4 below to lift verbatim
   blocks.
4. Use `../text/references.md` for citation formatting; use Section 3 to decide
   keep/adapt/drop.
5. Fill research gaps from Section 5 (deep-research backlog) BEFORE writing any
   claim that lacks a citation.
6. Generate Chapter 1 first, then Chapter 2, using the outlines in Section 6.

---

## 0.5 Recency Rule (LOCKED — 5-year window)

**Rule:** the new paper may only cite studies published ~2021 onward
(5 years from 2026; 2020 only if the adviser allows a 6-year push).
Apply this to every "study" in Related Literature / Related Studies.

**Exemptions (CONFIRM with adviser before relying on them):**
- Seminal/classical theory and frameworks (e.g., Cognitive Load, Jeffries
  Simulation Theory, Multimedia Learning) — usually allowed as the
  "theoretical framework" even if old, but keep them to the theory section,
  NOT the RRL "studies".
- Governing policy documents (e.g., CHED CMO 15 s.2017) — policy, not a study.

**Audit of every planned citation (year -> status):**

| Citation | Year | Status | Action |
|---|---|---|---|
| Alibudbud | 2023 | OK | use |
| AACN faculty shortage | 2025 | OK | use |
| Bambini scenario guide | 2016 | OUT | REPLACE with a 2021+ simulation-authoring/workload study, or keep only as seminal design reference (confirm) |
| CHED CMO 15 s.2017 | 2017 | POLICY | treat as policy, likely exempt (confirm) |
| Jeffries (2012 / 2015) | 2012/15 | THEORY | exempt as framework; pair with Watts 2021 (INACSL, in-range) for the "realism" standard |
| Noblezada workload | 2025 | OK | use |
| Sweller cognitive load | 1988 | THEORY | exempt as theory; optional: add a 2021+ cognitive-load-in-simulation review |
| Watts INACSL simulation design | 2021 | OK | use (covers realism/fidelity in-range) |
| Harder | 2023 | OK | use |
| Vaughn & Ford | 2024 | OK | use |
| Liu et al. ICU instructors | 2025 | OK | use |
| Reed & Dodson | 2024 | OK | use |
| Harnad symbol grounding | 1990 | THEORY | exempt as theory, or reframe via recent vision-language grounding (2021+) |
| Clark & Brennan | 1991 | THEORY | exempt as theory, or reframe via recent common-ground/grounding lit (2021+) |
| Ji hallucination survey | 2023 | OK | optional, use as general "hallucination" intro only |
| Ho et al. DDPM | 2020 | BORDERLINE | drop unless 6-year push; cite Rombach 2022 as the primary diffusion ref instead |
| Rombach LDM/Stable Diffusion | 2022 | OK | primary diffusion citation |
| Ramesh DALL-E / DALL-E 2 | 2021/22 | OK | use |
| Betker DALL-E 3 | 2023 | OK | use |
| Saharia Imagen | 2022 | OK | use |
| Podell SDXL | 2023 | OK | use |
| FLUX (BFL) | 2024/25 | OK | use |
| Qwen-Image / -Edit | 2025 | OK | use |
| Brooks InstructPix2Pix | 2023 | OK | use |
| Kumar Horner/hypothyroidism | 2024 | OK | core evidence |
| Fan facial pathology | 2023 | OK | use |
| Haider craniofacial | 2025 | OK | use |
| Pediatric ophthalmology | 2025 | OK | use |
| O'Malley skin tone | 2024 | OK | use |
| Joerg skin tone | 2025 | OK | use |
| Sakunchotpanit | 2025 | OK | use |
| Yang VLM skin tone | 2025 | OK | use |
| Blanz & Vetter 3DMM | 1999 | THEORY | cite once as origin; anchor on a 2023+ FLAME reference instead |
| Li et al. FLAME | 2017 | OUT | FIND FLAME 2023 (FLAME 2023 Open released 2025) as the current citation |
| Feng et al. DECA | 2021 | OK (borderline) | use |
| Rowan Text2Face | 2023 | OK | use |
| Poole DreamFusion | 2022 | OK | use |
| Lin Magic3D | 2023 | OK | use |
| Han HeadSculpt | 2023 | OK | use |
| Tian MeMa | 2025 | OK | use |
| Hayes FineGRAIN | 2025 | OK | use |
| Lin VQAScore | 2024 | OK | use |
| Mayer multimedia learning | 2001 | THEORY | exempt as theory, or find a 2021+ multimedia/visual-learning review |

**Action items from this rule:**
1. Find a 2021+ substitute for Bambini's "~100 hours" workload claim (search:
   "nursing simulation scenario development time study 2022/2023/2024",
   PH or SEA context preferred). If none, keep Bambini as seminal + add a
   recent corroborating workload study.
2. Find the current FLAME citation (FLAME 2023 paper / 2023 Open release).
3. Keep all theory/policy exceptions in the Theoretical Framework and
   Background only — never in the "Related Studies" recency-scored sections.
4. Confirm the exact window (5 vs 6 years) with the adviser and record the
   date used as the cutoff (assume 2021 for now).

---

## 1. What Changed (pivot summary)

| Dimension | OLD (RAG) | NEW (face generation) |
|---|---|---|
| Problem | Faculty spend ~100h writing scenarios | Students cannot SEE the patient's clinical signs |
| Core artifact | AI-drafted scenario text (patient + orders + milestones) | AI-generated patient face (PNG or 3D) from a description |
| Comparative (IV) | RAG-grounded vs non-grounded | Diffusion PNG vs parametric 3D (pipeline constant) |
| "Hallucination" meaning | Fabricated drug doses/vitals/references (text) | Missing/extra/inaccurate visual signs, artifacts, skin-tone bias |
| Grounding mechanism | Retrieve faculty scenarios into prompt | Fixed trait schema (single source of truth) + verifier loop |
| Theoretical anchor | Symbol grounding / RAG dual-memory | Simulation fidelity (Jeffries) + realism/fidelity in teaching |
| Evaluators | Nursing faculty rate drafts | Dr. Evan + Nursing faculty rate faces (rubric + checklist) |
| Personalization | Rule-based student weakness label | DROPPED (not part of new problem) |

**Consequence for writing:** the entire "nursing education context" survives,
the "LLM hallucination + RAG" half of Chapter 2 is replaced by
"diffusion + VLM + 3D face" literature, and the theoretical framework keeps
Cognitive Load + Jeffries fidelity while dropping the RAG-specific theories.

---

## 2. Reuse Map by Document

### 2.1 Chapter 1 — `../text/chap_1/chapter1_v2.md`

| Old section (line) | New section | Disposition | Note |
|---|---|---|---|
| Introduction (5-7) | Introduction | KEEP (2-line boilerplate) | Rewrite the list of covered sections to match new structure |
| Background para 1 (11) | Background | KEEP ~95% | CHED OBE + simulation + faculty shortage + AACN 92k. Only end of sentence needs no change. This is your macro context |
| Background para 2 (13) | Background | ADAPT | Keep Bambini ~100h + Watts standards + Harder/Vaughn&Ford "AI makes drafts but details missing". CUT the "AI writes scenarios" framing; the new bottleneck is "students cannot visualize the described signs" |
| Background para 3 (15) | Background | REWRITE | Text hallucination (Asgari/Omar/Walters/Gravel) -> image failure evidence (Kumar Horner 0/120, Joerg 15%, Fan, skin-tone bias). Keep the *argument shape*, swap every citation |
| Background para 4 (17) | Background | DROP | RAG explanation no longer applies. (Optional: repurpose ONLY if adopting reference-conditioned image gen; plan says no) |
| Background para 5 (19) | Background | DROP | RAG limitations |
| Background para 6 (21) | Background / gap | REWRITE | "Most studies test a model alone / on general medical text / outside a working HIS" -> "Most studies test plain T2I models on dermatology/ophthalmology, none compare rendering modalities inside a school HIS with faculty raters" |
| Statement of the Problem (23-33) | Statement of the Problem | REWRITE | RQs change completely. New RQs below (Section 6) |
| Objectives (35-44) | Objectives | REWRITE | Map to new RQs |
| Significance (46-58) | Significance | KEEP structure, ADAPT body | Same 5 beneficiary paragraphs (faculty, students, developers, schools/CHED, future researchers). Change "cut writing hours" -> "give students a reliable visual of the patient"; keep CHED + faculty-approval framing |
| Scope & Limitations (60-64) | Scope & Limitations | KEEP structure, REWRITE body | New scope = face/head only, two modalities, API-only, no training, 24-30 test descriptions, nursing faculty raters. Keep the "small corpus / one school / API changes over time / no autonomous publish / faculty approve" limitation sentences almost verbatim |

### 2.2 Chapter 2 — `../text/chap_2/chapter2_v2.md`

| Old subsection (line) | New subsection | Disposition | Note |
|---|---|---|---|
| Intro para (5) | Intro | REWRITE | Same one-paragraph roadmap function; new topics |
| Large language models (9-13) | Generative AI foundations | ADAPT | Replace LLM/transformer (Vaswani/Brown) with diffusion models (Rombach/Ho/Ramesh/Saharia/FLUX/Qwen). Keep the sentence "the study uses a model through an API and does not train one from scratch" verbatim-ish |
| Clinical hallucination (15-17) | Visual failure / artifacts in generated images | REWRITE | Text hallucination taxonomy (Ji 2023 intrinsic/extrinsic) -> image artifacts + missing/extra signs + skin-tone bias. New evidence: Kumar, Joerg, Haider, pediatric ophtho |
| Retrieval-Augmented Generation (19-25) | (dropped) | DROP | Entire RAG cluster removed |
| Fitting a model to a field (27-31) | (dropped / condensed) | DROP | Fine-tune vs retrieval (Soudani), distillation (Hsieh) no longer core. Keep only one future-work sentence: "train only once the approved-image corpus is rich (MeMa precedent)" |
| Generative AI in nursing/medical education (33-37) | Generative AI in nursing & medical education | ADAPT | Harder, Vaughn&Ford, Liu stay (AI in nursing ed + human review needed). Reed & Dodson pivots to "realism helps students prepare" (visual depiction). ADD Fan 2023 + Kumar 2024 as the image-specific education studies |
| Ethics and data privacy (39-41) | Ethics and data privacy | KEEP ~85% | RA 10173 paragraph survives. ADD: no real patient photos (MeMa), AI-labeling, likeness/deepfake concern, skin-tone inclusion (O'Malley), provenance watermark (SynthID), model licenses (FLUX non-commercial) |
| Related Studies (43-57) | Related Studies | REWRITE | Regroup: (1) T2I for clinical faces, (2) skin-tone bias, (3) 3D face models, (4) VLM evaluation, (5) synthetic patient data, (6) AI in nursing ed |
| Gaps (59-69) | Gaps | REWRITE | New three gaps (Section 6) |
| Synthesis (71-77) | Synthesis | REWRITE | New synthesis leads to "compare modalities under one schema" |
| Theoretical Framework (79-103) | Theoretical Framework | ADAPT | See 2.3 |

### 2.3 Theoretical Framework (which theories survive)

| Old theory | Disposition | New role |
|---|---|---|
| Cognitive Load Theory (Sweller 1988) | KEEP | Reframe: visualizing signs offloads the instructor from describing/finding images and the student from imagining signs; fewer wrong mental images = less extraneous load. Definition sentence reusable verbatim |
| Symbol Grounding (Harnad 1990) | ADAPT | Reframe: ungrounded diffusion binds text to pixels without clinical meaning -> artifacts. The schema is the external anchor that grounds tokens to specific signs. Keep Harnad definition, swap RAG->schema |
| Grounding Theory (Clark & Brennan 1991) | ADAPT | Reframe: common ground between instructor's description and the renderer is the trait schema; a bare prompt lacks it. Reusable structure |
| Dual-memory + Jeffries Simulation Theory | SPLIT | DROP the dual-memory/RAG half; KEEP Jeffries fidelity (2012; 2015) and ELEVATE it — fidelity/realism is now the CENTRAL theory |
| — (NEW) | ADD | Multimedia Learning / Picture Superiority (Mayer 2001, or Paivio dual-coding) — why a visual aids learning of physical signs |
| — (NEW, optional) | ADD | Representativeness / algorithmic bias (dermatology skin-tone literature) — frames the skin-tone evaluation axis as more than a metric |

---

## 3. Citation Disposition (from `../text/references.md`)

### 3.1 KEEP as-is (move into new paper unchanged)

| Citation | Used for |
|---|---|
| Alibudbud 2023 | PH nurse shortage / migration (background) |
| AACN 2025 | Faculty shortage, 92k turned away (background) |
| Bambini 2016 | Scenario authoring workload (~100h) + simulation design |
| CHED CMO 15 s.2017 | OBE / BSN program standards (background + significance) |
| Jeffries 2012 | NLN Simulation Theory — fidelity (THEORETICAL CORE) |
| Jeffries, Rodgers & Adamson 2015 | Simulation theory narrative (fidelity definition) |
| Noblezada et al. 2025 | PH clinical instructor workload (background) |
| Sweller 1988 | Cognitive Load Theory (theoretical) |
| Watts et al. 2021 | INACSL Simulation Design Standards — "realism" criterion (background) |

### 3.2 ADAPT (keep citation, reframe the claim)

| Citation | Old claim | New claim |
|---|---|---|
| Harder 2023 | ChatGPT speeds simulation drafts but needs review | Same — AI aids nursing ed but needs expert review (context) |
| Vaughn & Ford 2024 | AI simulations miss details | AI content needs human review (context) |
| Liu et al. 2025 | Instructors saved time with AI | AI in case design saves time but still checked (context) |
| Reed & Dodson 2024 | AI backstories reduced anxiety | Realism/backstory improves student preparation -> extend to visuals |
| Harnad 1990 | Symbol grounding -> RAG anchors text | Schema anchors the renderer to real signs |
| Clark & Brennan 1991 | RAG builds common ground | Trait schema is common ground between instructor + renderer |
| Ji et al. 2023 | (optional) hallucination taxonomy for text | Intro a general "hallucination/faithfulness" concept, then pivot to image artifacts |

### 3.3 DROP (text/RAG-specific, no longer relevant)

Asgari 2025; Omar 2025; Walters & Wilder 2023; Gravel 2023; Bhattacharyya 2023;
Lewis 2020; Xiong 2024; Zakka 2024; Klang 2024; Béchard & Marquez Ayala 2024;
Barnett 2024; Gao et al. 2024 (RAG survey); Pawlik 2026; Wołk 2025; Pingua 2025;
Soudani 2024; Labrak 2024 (BioMistral); Vishwanath 2024 (MedMobile); Hsieh 2023.
Optional-drop: Vaswani 2017, Brown 2020 (keep only if you want a one-line
"generative AI" lineage; the new paper's foundation citations are diffusion).

### 3.4 NEW to find (see Section 5 for full detail)

Diffusion foundations (Rombach 2022; Ho 2020; Ramesh 2021/2022; Betker 2023;
Saharia 2022; Podell 2023 SDXL; Black Forest Labs FLUX; Qwen-Image);
image editing (Brooks 2023 InstructPix2Pix; Qwen-Image-Edit; FLUX Kontext);
clinical face gen (Kumar 2024; Fan 2023; Haider 2025; pediatric ophtho 2025);
skin-tone bias (O'Malley 2024; Joerg 2025; Sakunchotpanit 2025; Yang 2025);
3D face (Blanz & Vetter 1999; Li et al. 2017 FLAME; Feng et al. 2021 DECA;
Rowan 2023 Text2Face); text-to-3D (Poole 2022 DreamFusion; Lin 2023 Magic3D;
Han 2023 HeadSculpt); synthetic patient data (Tian et al. 2025 MeMa);
VLM judges (Hayes 2025 FineGRAIN; Lin 2024 VQAScore; GenAIBench);
multimedia learning (Mayer 2001); provenance (SynthID / Google).

---

## 4. Reusable Verbatim Blocks (copy-paste with edit notes)

Each block: `[SOURCE]` then the text to lift, then `[EDIT]` instruction.

### B1 — Simulation + faculty shortage context (nearly verbatim)
`[SOURCE] chapter1_v2.md:11`
"Philippine nursing programs must train students to handle clinical problems
safely, and the Commission on Higher Education requires outcome-based teaching
... American nursing schools reported a 7.2 percent vacancy rate ... turned
away more than 92,000 qualified applicants ..."
`[EDIT]` None. Lift whole paragraph; it is topic-neutral macro context.

### B2 — Authoring workload + AI-draft caution (adapt ending)
`[SOURCE] chapter1_v2.md:13`
"Faculty also lose many hours writing the scenarios themselves ... can reach
about 100 hours for one case (Bambini, 2016) ... realistic detail, and a
planned debriefing (Watts et al., 2021) ... important details were often
missing and someone still had to check ..."
`[EDIT]` Keep through Watts. Then REPOINT: after the workload facts, transition
to "but even a well-written scenario leaves one thing missing: the student
cannot see the patient. Signs like jaundice, pallor, and ptosis are visual..."
(That becomes the bridge to the new problem.)

### B3 — Cognitive Load definition (verbatim)
`[SOURCE] chapter2_v2.md:85`
"Cognitive load theory (Sweller, 1988) says working memory is limited. It
separates the load from the material itself, the load from bad design or tools,
and the load that builds understanding."
`[EDIT]` Keep verbatim; the application sentence that follows is rewritten
(workload -> visualization).

### B4 — Jeffries fidelity (verbatim, now central)
`[SOURCE] chapter2_v2.md:99`
"...the NLN Jeffries Simulation Theory (Jeffries, 2012) says good simulations
need fidelity. That means objectives, realism, and clinical accuracy line up so
students learn the right pattern (Jeffries, Rodgers, & Adamson, 2015)."
`[EDIT]` Keep verbatim; ADD a following sentence: "A generated patient face that
misrenders a sign breaks that fidelity as surely as a hallucinated vital sign
does."

### B5 — Ethics paragraph (verbatim + additions)
`[SOURCE] chapter2_v2.md:41`
"In the Philippines, the Data Privacy Act of 2012, or Republic Act No. 10173,
protects personal data, and health data gets extra protection... real patient
data never enters the system... Every scenario is reviewed and approved by
Nursing Department faculty before it can be published..."
`[EDIT]` Keep verbatim; ADD sentences for: no real patient photos (cite MeMa),
generated faces are labeled AI-generated, likeness/deepfake concern,
skin-tone inclusion (cite O'Malley), provenance watermark (SynthID), and model
license note (FLUX dev non-commercial vs Apache-2.0 Qwen).

### B6 — Scope limitation sentences (near verbatim)
`[SOURCE] chapter1_v2.md:64`
"The document set is small, so the results come from one school... de-identified
simulation content only, and no real patient data is used... The API provider
and version affect repeat results, because hosted models change or retire over
time... generated [output] stays as [draft] until faculty approve..."
`[EDIT]` Swap "document set" -> "test set of 24-30 scenario descriptions" and
"generated scenarios stay as drafts" -> "generated faces stay as unapproved
previews until faculty approve."

---

## 5. Deep-Research Backlog (detailed)

Fill these BEFORE writing the sections that depend on them. Each entry lists:
what to answer, where it feeds, keywords, and verified seed citations.

### T1. Diffusion models for text-to-image (foundations)
- **Feed:** Ch2 "Generative AI foundations"; supports "why diffusion not just LLM".
- **Answer:** how latent diffusion works (noise -> denoise in latent space),
  why it hallucinates detail, why control is weak (vs parametric).
- **Keywords:** "latent diffusion model", "Stable Diffusion", "DALL-E",
  "text-to-image survey".
- **Seeds:** Rombach et al. 2022 (LDM/Stable Diffusion); Ho et al. 2020 (DDPM);
  Ramesh et al. 2021 (DALL-E) & 2022 (DALL-E 2); Betker et al. 2023 (DALL-E 3);
  Saharia et al. 2022 (Imagen); Podell et al. 2023 (SDXL).
- **Extract:** 2-3 sentences of mechanism + the standard limitation
  ("struggles with precise attribute binding" — link to FineGRAIN in T7).

### T2. Text-to-image for CLINICAL/FACIAL signs (core gap evidence)
- **Feed:** Ch1 background (rewritten para 3) + Ch2 related studies + gaps.
- **Answer:** which facial signs T2I models get right/wrong; why asymmetric
  signs fail; what "clinical accuracy" means for faces.
- **Keywords:** "text-to-image Horner syndrome ptosis", "AI generated facial
  pathology medical education", "craniofacial anatomy illustration AI".
- **Seeds (VERIFIED):** Kumar et al. 2024 (JMIR Med Educ e52155 — Horner failed
  0/120, hypothyroidism OK); Fan et al. 2023 (Med Sci Educator
  10.1007/s40670-023-01942-5); Haider et al. 2025 (JCM 14:2136 — craniofacial,
  ICC 0.858, all models flawed); Pediatric ophthalmology 2025
  (Healio 10.3928/01913913-20250724-03 — DALL-E 3 poor).
- **Extract:** the 0/120 stat, "asymmetric vs symmetric" pattern, and
  "non-clinicians can be misled" quote.

### T3. Skin-tone bias in medical image generation (mandatory evaluation axis)
- **Feed:** Ch1/Ch2 ethics + metrics justification + gaps.
- **Answer:** the measured underrepresentation numbers; whether prompt/demographic
  injection fixes it; scale used (Fitzpatrick vs Monk).
- **Keywords:** "skin tone bias AI medical images", "Fitzpatrick scale
  generative AI dermatology", "darker skin underrepresentation DALL-E".
- **Seeds (VERIFIED):** O'Malley et al. 2024 (JMIR AI 10.2196/58275 —
  demographic injection fixes distribution, P=.04); Joerg et al. 2025 (JEADV
  10.1111/jdv.20849 — 89.8% light skin, only 15% identifiable); Sakunchotpanit
  et al. 2025 (CED 10.1093/ced/llaf126); Yang et al. 2025 (JID — VLM skin-tone).
- **Extract:** exact percentages + which scale to adopt for your rubric
  (recommend Monk for multi-tone; justify in methodology).

### T4. Parametric 3D face models / 3DMM (Arm B substrate)
- **Feed:** Ch2 3D literature + methodology (why FLAME) + architecture note.
- **Answer:** what a 3D morphable model is; FLAME parameters (shape, expression,
  pose); whether color/material is part of the model or added by texture;
  license (FLAME 2023 Open = CC-BY-4.0).
- **Keywords:** "3D morphable model face", "FLAME head model", "DECA
  reconstruction", "blendshape expression".
- **Seeds (VERIFIED):** Blanz & Vetter 1999 (3DMM); Li et al. 2017 (FLAME);
  Feng et al. 2021 (DECA); FLAME website flame.is.tue.mpg.de (2023 Open,
  CC-BY-4.0 released Nov 2025); FLAME-Universe GitHub (TimoBolkart).
- **Extract:** the license fact + a one-line "linear shape/expression space"
  description; note that COLOR is NOT in the geometry model (that is your
  contribution: clinical material/color parameters).

### T5. Text-to-3D head generation (positioning + why you build parametric instead)
- **Feed:** Ch2 related studies (position against HeadSculpt/DreamFusion).
- **Answer:** why text-to-3D (score distillation) is GPU-heavy and uncontrolled
  for exact signs; why a deterministic parametric model is the right call for
  clinical fidelity.
- **Keywords:** "text-to-3D head avatar", "DreamFusion score distillation",
  "HeadSculpt".
- **Seeds (VERIFIED):** Poole et al. 2022 (DreamFusion); Lin et al. 2023
  (Magic3D); Han et al. 2023 (HeadSculpt — code not released, repo is a
  DreamFusion fork); Rowan et al. 2023 (Text2Face — shape only, texture via
  DALL-E so color signs unreliable).
- **Extract:** "code never released" + "texture mapped from DALL-E -> color
  signs unreliable" as your differentiators.

### T6. Synthetic patient data & de-identification (ethics + train-later)
- **Feed:** ethics section + future-work + defense ("why not train now").
- **Answer:** how others generate synthetic patient faces safely; the consent/
  ethics burden of real patient photos; identity-leakage mitigation.
- **Keywords:** "synthetic patient face dataset", "medical manifestation
  de-identification", "IP-Adapter identity leakage".
- **Seeds (VERIFIED):** Tian et al. 2025 (MeMa, AAAI 2025, arXiv:2412.10804 —
  42,307 faces, needed 39,323 real photos + hospital ethics approval, used
  IP-Adapter to cut identity leakage 71.8%->1.27%).
- **Extract:** the 39k-photos + ethics-approval fact (your strongest
  "train-later" justification) and the IP-Adapter identity fix (cite as a
  technique you could later adopt).

### T7. VLM evaluation / prompt-adherence judges (your verifier + metrics)
- **Feed:** methodology (verify step) + Ch2 (why validate the judge) + metrics.
- **Answer:** can a VLM reliably check "is this sign present/absent"; its
  known failure modes; how to validate it against clinicians (kappa).
- **Keywords:** "VLM judge prompt adherence", "text-to-image failure modes",
  "VQAScore".
- **Seeds (VERIFIED):** Hayes et al. 2025 (FineGRAIN, NeurIPS 2025,
  arXiv:2512.02161 — VLM-human agreement ~67%, VLMs fail on some categories,
  don't trust blindly); Lin et al. 2024 (VQAScore); GenAIBench.
- **Extract:** the ~67% agreement number + "validate the judge, don't assume it"
  argument.

### T8. Visual fidelity/realism in simulation & multimedia learning (theory)
- **Feed:** theoretical framework (Jeffries fidelity + new multimedia theory).
- **Answer:** why realism/fidelity matters in simulation; why pictures aid
  learning of physical signs (dual-coding/picture superiority); how much
  fidelity is "enough" (low-fidelity can still teach).
- **Keywords:** "simulation fidelity nursing education", "multimedia learning
  pictures dual coding", "fidelity realism clinical simulation".
- **Seeds:** Jeffries 2012/2015 (already have); Mayer 2001 (Multimedia Learning)
  or Mayer 2005 (Cambridge handbook); Paivio dual-coding (optional);
  Maran & Glavin 2003 (low- vs high-fidelity simulation) — VERIFY.
- **Extract:** a defensible claim that "fidelity serves learning, not
  photorealism per se" — supports Dr. Evan's relaxed-realism stance.

### T9. Agentic workflows for image generation (pipeline justification)
- **Feed:** Ch1 significance + Ch2 (why a loop, not one-shot) + defense.
- **Answer:** what an agentic T2I loop is (generate -> verify -> edit -> retry);
  evidence it improves attribute fidelity; why you keep it CONSTANT (not a
  variable) — position vs classmate.
- **Keywords:** "agentic image generation self-correcting", "iterative
  text-to-image editing loop", "LLM verify image generation".
- **Seeds:** Qwen-Image-Edit blog 2025 (chained editing corrects errors step by
  step); FLUX Kontext (iterative editing); InstructPix2Pix (Brooks 2023).
- **Extract:** a "generate->verify->localized-edit" description + the claim
  that a verification loop catches missing traits that one-shot misses.

### T10. Ethics/legal/provenance of AI-generated medical images
- **Feed:** ethics section + defense ("ethics of fake patient faces").
- **Answer:** labeling requirements, likeness/deepfake risk, watermarking
  (SynthID), and open-weight license constraints (FLUX non-commercial).
- **Keywords:** "AI generated medical image ethics", "deepfake likeness
  consent", "SynthID watermark", "FLUX non-commercial license".
- **Seeds (VERIFIED):** FLUX.1 Kontext [dev] = non-commercial license (BFL);
  Qwen-Image / Qwen-Image-Edit = Apache 2.0; Gemini image API = SynthID
  watermark; RA 10173 (already have).
- **Extract:** a short license/provenance table for the defense and ethics.

---

## 6. Suggested New Outlines

### Chapter 1 (patient-face generation)
1. The Problem and Its Background
   1. Introduction
   2. Background of the Study (B1 + B2 + rewritten image-failure paras T2/T3)
   3. Statement of the Problem + RQs:
      - RQ1: What is the per-trait fidelity (recall + hallucinated signs) of
        diffusion-PNG vs parametric-3D generated patient faces?
      - RQ2: What is the clinical plausibility / teaching usefulness of each
        modality, as rated by Nursing faculty?
      - RQ3: Is there a significant difference between the two modalities on
        trait fidelity, plausibility, and skin-tone fidelity?
      - RQ4: What is the latency, token cost, and GPU need of each modality?
      - RQ5: Which modality is more suitable for scenario patient
        visualization in Chansey, and why?
   4. Objectives
   5. Significance (5 beneficiary paragraphs, adapted)
   6. Scope and Limitations (B6)

### Chapter 2 (patient-face generation)
1. Review of Related Literature and Studies
   1. Generative AI foundations — diffusion models (T1), image editing (T9)
   2. Visual failure in generated medical images — artifacts + missing/extra
      signs + skin-tone bias (T2, T3)
   3. Generative AI in nursing & medical education (Harder, Vaughn&Ford, Liu,
      Reed&Dodson + Fan 2023 + Kumar 2024)
   4. Parametric 3D face models (T4) and text-to-3D heads (T5)
   5. VLM evaluation / prompt-adherence judges (T7)
   6. Synthetic patient data & de-identification (T6)
   7. Ethics, provenance, and data privacy (T10, RA 10173)
   2. Related Studies (grouped as in 2.2)
   3. Gaps in the Literature — (1) no modality comparison for clinical facial
      signs; (2) no faculty-rated patient-face generator inside a school HIS;
      (3) skin-tone fidelity unmeasured in nursing simulation visuals
   4. Synthesis
   5. Theoretical Framework — Cognitive Load (B3), Jeffries fidelity (B4),
      Symbol Grounding (adapted), Multimedia Learning (T8), optional bias axis

---

**Last updated:** 2026-10-31
**Use:** generate new Ch1/Ch2 from this file + `THESIS_DRAFT_PLAN.md`.
