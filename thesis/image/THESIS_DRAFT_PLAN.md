# Thesis Draft Plan: Scenario-to-Patient-Face Generation in an Educational HIS

**Working Title:** *Comparative Evaluation of Diffusion-Based versus Parametric 3D Generation of Patient Facial Visualizations from Clinical Scenario Descriptions in an Educational Hospital Information System*

**Type:** Development + Comparative Experimental Evaluation
**Domain:** Nursing Informatics / Generative AI (Multimodal: LLM + Text-to-Image + VLM)
**Integration:** Chansey HIS — Faculty Scenario Builder (visual asset for each scenario patient)

> **Scope decision (locked with adviser):** The thesis pivoted from
> **RAG-grounded scenario generation** to **patient facial visualization**.
> Dr. Evan does NOT want the system to generate scenario text — instructors
> will author scenarios themselves. What he wants: when he types a patient
> description (e.g., "runny nose, yellowish eyes, pale lips, female"), the
> system also generates a face (PNG, SVG, or 3D) showing those traits so
> students can visualize the patient's condition. Disease-only input (e.g.,
> "high fever") must still produce a reasonable default visual.
>
> **Comparative (locked):** rendering **modality** — diffusion PNG vs
> parametric 3D head — under ONE pipeline held constant. The classmate's
> thesis is one-shot vs agentic (for video generation), so pipeline depth is
> NOT our variable. Our pipeline is a constant; the modality is the IV.
>
> **Realism (locked, Oct 31):** Dr. Evan does NOT require photorealistic
> faces. Stylized/parametric output is acceptable. Success = sign fidelity +
> teaching usefulness, not photorealism.
>
> **Development flow (locked):** build what we can -> Dr. Evan tests ->
> iterate. Trial and error with the client; his feedback drives the sign
> catalog, severity scales, and visual style. Client testing sessions are
> built into the timeline (not an afterthought).
> The old plan (RAG scenario generation) is retained for reference at
> `../text/THESIS_DRAFT_PLAN.md` and is superseded by this document.

---

## 1. Problem Statement

Nursing simulation scenarios describe patient conditions in text. Students
cannot see the patient, so visual signs (jaundice, pallor, cyanosis, ptosis)
must be imagined. Photoreal clinical images exist only as copyrighted
textbook photos or real patient photos (privacy + consent problems).
Generative AI can synthesize faces from text, but plain text-to-image models
are documented to fail on clinical facial signs: they hallucinate details,
handle asymmetric signs (ptosis, droop) poorly, and heavily overrepresent
light skin tones.

The research problem: **which rendering modality — diffusion-generated PNG
or a parametric 3D head — reproduces the described clinical signs more
faithfully, plausibly, and consistently, at what cost?**

The tension to be tested: diffusion is photoreal but uncontrollable; a
parametric 3D head is stylized but deterministic (color signs are region
parameters that cannot hallucinate). Note: since Dr. Evan accepts stylized
output, realism is a SECONDARY axis; clinical-sign fidelity and teaching
usefulness are the primary success criteria.

---

## 2. Objectives

### Primary (Experimental — the "soul" of the study)
1. Compare **diffusion PNG (Arm A)** vs **parametric 3D head (Arm B)** on:
   - trait recall rate (per-trait presence vs clinician-authored checklist)
   - hallucinated extra signs (false positives)
   - clinical plausibility (faculty rubric rating)
   - skin-tone fidelity (Fitzpatrick/Monk I-VI)
   - consistency across seeds (diffusion only)
   - latency, token cost, and GPU requirement

### Secondary (Development / Deployment artifact)
2. Build the **scenario-to-face pipeline** as a Python microservice that the
   Laravel Chansey app calls (parse -> expand -> render -> verify -> approve).
3. Support **disease-only input**: the LLM proposes typical visible signs and
   the instructor confirms/edits before rendering. The system never silently
   invents clinical content.
4. (Post-deployment, future work) fine-tune once Chansey has accumulated a
   corpus of instructor-approved images + usage logs.

---

## 3. Scope & Delimitations

| In Scope | Out of Scope |
|---|---|
| Face/head only (Dr. Evan approved head scope; full body is future work) | Full-body or whole-scene generation |
| Diffusion PNG vs parametric 3D comparison | Predictive ML (dropped entirely) |
| SVG: considered and eliminated on prior-art evidence (StarVector is trained on icons/diagrams, not natural images) | SVG as an experimental arm |
| Agentic workflow only (zero training for the core) | Training/fine-tuning until data-rich |
| Nursing Department faculty (Dr. Evan + faculty) as raters and end users | Physician diagnostic validation |
| De-identified synthetic faces, AI-labeled, instructor-approved | Real patient photos / real clinical deployment |

**Ethics:** no real patient photos (MeMa shows the consent/ethics burden);
generated faces are labeled AI-generated; hard instructor approval gate; skin
tone inclusion is a measured evaluation axis (O'Malley et al. 2024); SynthID
watermark where the API supports it.

---

## 4. Data Sources (System-Generated, No External Dataset)

| Source | Use |
|---|---|
| `scenarios` patient description fields (faculty-authored) | Input text + future fine-tune corpus |
| Trait schema JSON + sign catalog (co-designed with Dr. Evan) | Single source of truth for all renderers |
| Approved generated images + usage logs | Future fine-tune set (MeMa pattern) |
| Pre-registered test set (24-30 scenario descriptions) | Experimental stimuli |

**Already built in the capstone:** scenario module (template -> instance),
faculty builder UI (Blade after porting), classes/sections management.

---

## 5. System Architecture (Chansey Integration)

### 5.1 Pipeline (FIXED across arms — not a variable)

```
Faculty free text (description or disease name)
      │
 1. Parse    LLM -> trait schema JSON (sex, age, skin tone, signs w/ severity, laterality, region)
 2. Expand   (disease-only input) LLM proposes visible signs -> instructor confirms/edits
      │
      ├── Arm A: Diffusion PNG (Gemini image API)
      │     prompt compile -> generate -> VLM check -> localized edit (max 2 loops)
      └── Arm B: Parametric 3D head (FLAME 2023 Open)
            schema -> FLAME shape/expression + material/color params + blendshapes -> render
      │
 3. Verify   VLM checks each trait against the image (clinician-authored checklist)
 4. Approve  Dr. Evan approves -> attach to scenario, labeled AI-generated
```

### 5.2 Delivery form: Python microservice + Laravel client

- **Microservice (Python/FastAPI)** — `services/facegen/`: owns LLM calls,
  Gemini image API, FLAME math (CPU-only), VLM verification, offscreen render.
- **Laravel (client)** — thin `ScenarioFaceController` + HTTP client service;
  a "Generate patient visual" button on the faculty Scenario form; stores
  `image_path`, `asset_type`, `trait_schema` on the scenario row.
- **No GPU anywhere:** diffusion runs on APIs (Gemini); FLAME is linear
  blendshape math on CPU; interactive viewing later via three.js (WebGL in
  the browser, not the server).

See `AGENT_ARCHITECTURE_NOTE.md` for endpoints, schema, and demo commands.

---

## 6. Experimental Design (for Defense)

### 6.1 Main comparison: modality, one pipeline

- **Arm A** — Diffusion PNG via API (Gemini 2.5 Flash Image / Gemini 3 image
  preview; iterative editing loop held constant).
- **Arm B** — Parametric 3D head: FLAME 2023 Open (CC-BY-4.0) + region
  material/color params + structural-sign blendshapes, rendered to a static
  profile PNG (and an interactive model where the viewer supports it).
- **Held constant:** LLM parser, trait schema, disease->sign expansion with
  instructor confirmation, VLM verifier, approval gate.
- **Stimuli:** N = 24-30 pre-registered scenario descriptions covering:
  color signs (jaundice, pallor, cyanosis, flushing), structural/asymmetric
  (ptosis, facial droop, edema), secretions (runny nose), non-specific
  (fever); both sexes; Fitzpatrick/Monk I-VI; mix of trait-list and
  disease-only inputs.
- **Metrics:** trait recall, hallucinated extra signs, faculty plausibility
  rating, skin-tone fidelity, seed consistency (3 repeats, Arm A), latency,
  token cost, GPU need.
- **Statistical tests:** McNemar (per-trait correctness, paired), Wilcoxon
  signed-rank (ratings), Cohen's kappa / Krippendorff's alpha for raters AND
  for VLM-vs-clinician agreement (justifies the automated judge).

### 6.2 Sub-analyses (same data, no new arms)

- Per-sign-type performance (color vs structural vs asymmetric).
- Per-skin-tone fidelity (bias axis).
- Trait-list input vs disease-only input.
- Cost/latency profile per modality for real classroom use.

### 6.3 Validation

- Nursing Department faculty rate generated faces on a rubric (plausibility,
  faithfulness, teaching usefulness); 2-3 raters for reliability.
- Checklist instrument co-designed with Dr. Evan (he is a main user).

---

## 7. MVP Checklist

### Phase 0: Pre-paper (week 1)
- [ ] Lock title + RQs + SOP with adviser
- [ ] Rewrite Chapter 1 (reuse nursing-education framing; swap authoring -> visualization problem)
- [ ] Confirm Gemini API access (Plus subscription != API key) or OpenCode Go image endpoint

### Phase 1: Spikes (weeks 2-3)
- [ ] Gemini API spike: parse -> generate -> edit loop on 3 descriptions
- [ ] FLAME 3D spike (go/no-go): jaundice (color), ptosis (structural), droop (asymmetric)
- [ ] Trait schema + sign catalog + rubric co-design with Dr. Evan
- [ ] First Dr. Evan trial: show spike outputs, collect sign/severity feedback

### Phase 2: Microservice + Laravel hook (weeks 3-4)
- [ ] FastAPI service: /parse, /expand, /render/png, /render/3d, /verify, /generate
- [ ] Laravel: migration columns, ScenarioFaceController, button on faculty Scenario form
- [ ] Chapter 3 methodology; pre-register 24-30 test descriptions
- [ ] Second Dr. Evan trial: full pipeline on his own descriptions in the UI

### Phase 3: Pilot + defense prep (week 5)
- [ ] Pilot: 5 scenarios x 2 arms; screenshots, timing, cost
- [ ] Chapter 1-3 drafts + defense slides + grill rehearsal
- [ ] Third Dr. Evan trial: pilot outputs -> final style/severity lock before pre-oral

### Phase 4: Full evaluation (post-pre-oral)
- [ ] Run full 24-30 scenario set, collect metrics, faculty rating sessions
- [ ] Statistical analysis (Chapter 4) + discussion (Chapter 5)

### Phase 5: Future (data-rich)
- [ ] Usage logs + approved images -> fine-tune (MeMa precedent) or train a
      renderer; compare against API baseline

---

## 8. RRL Anchors (Verified Citations for Chapter 2)

1. **MedDiT** (IJCAI 2025; arXiv:2408.12236) — closest prior art: LLM + KG +
   LoRA'd diffusion for simulated-patient images. Position against: we use
   instructor free text, faces (not X-rays), zero training, modality
   comparison with a skin-tone axis.
2. **Kumar et al. 2024** (JMIR Med Educ, e52155) — DALL-E 2 / Midjourney on
   facial signs: hypothyroidism OK (symmetric), Horner syndrome failed all
   120 images (asymmetric). Strongest "plain prompting fails" evidence.
3. **Fan et al. 2023** (Med Sci Educator, 10.1007/s40670-023-01942-5) —
   generated faces with pathology for education; validates concept; warns
   non-clinicians can be misled.
4. **Skin-tone bias**: O'Malley et al. 2024 (JMIR AI, 10.2196/58275 —
   demographic prompt injection fixes distribution); Joerg et al. 2025
   (JEADV, 10.1111/jdv.20849 — 89.8% light skin, 15% identifiable); Yang et
   al. 2025 (JID — VLM skin-tone disparities).
5. **MeMa** (Tian et al., AAAI 2025; arXiv:2412.10804) — 42k synthetic
   patient faces; vanilla SD cannot render manifestations, fine-tuned SD can;
   needs 39k real photos + ethics approval -> justifies our train-later stance.
6. **Text2Face** (arXiv:2303.02688) — text -> FLAME shape via CLIP; texture
   via DALL-E mapping (color signs unreliable). We extend with clinical
   material parameters.
7. **HeadSculpt** (NeurIPS 2023) — text-to-3D heads; code never released.
   Cite as related work, not a dependency.
8. **FLAME 2023 Open** (MPI) — CC-BY-4.0 head model; PyTorch layer + DECA.
9. **FineGRAIN** (NeurIPS 2025; arXiv:2512.02161) — VLM judges for T2I
   prompt adherence (~67% human agreement; weak on some categories) ->
   justifies checklist design AND clinician validation of the VLM judge.
10. **Open models**: Qwen-Image-Edit (Apache 2.0, 20B); FLUX.1 Kontext [dev]
    (open weights, NON-commercial license); Gemini 2.5 Flash Image API
    ("Nano Banana", iterative editing + SynthID provenance).
11. **StarVector** (arXiv:2312.11556) — text-to-SVG trained on icons/diagrams
    only; evidence for dropping SVG as an arm.
12. Nursing education context carried over: Bambini 2016, Jeffries 2012/2015,
    Watts et al. 2021, CHED CMO 15 s.2017 (see `../text/references.md`).

---

## 9. Defense Talking Points (Prep)

| Panel Question | Prepared Answer |
|---|---|
| "Novelty vs MedDiT?" | They generate chest X-rays from a knowledge graph with a trained LoRA. We generate faces from instructor free text, untrained, and run a controlled modality comparison with a skin-tone axis. |
| "Why not just use ChatGPT images?" | Kumar 2024: asymmetric signs fail 0/120. Joerg 2025: 15% identifiable, ~90% light-skinned. Arm A quantifies the fix; Arm B removes the failure class by construction. |
| "Kopya ba kay [classmate] (one-shot vs agentic)?" | No — his variable is pipeline depth for video; mine is output modality for clinical fidelity in patient faces. My pipeline is held constant across arms. |
| "How do you know the images are clinically correct?" | Clinician-authored trait checklist is ground truth; Dr. Evan's approval is a hard gate; the VLM judge is only a screen, trusted to the extent kappa shows (FineGRAIN: ~67% agreement — we validate it, not assume it). |
| "Who decides what 'high fever' looks like?" | The LLM proposes visible signs; the instructor confirms or edits. Nothing publishes silently. |
| "Why not train a model now?" | MeMa needed 39k real patient photos + hospital ethics approval. We are agentic-only until Chansey accumulates instructor-approved images; that log becomes the future training set. |
| "Is the 3D arm even AI?" | The agentic chain (LLM parse -> schema -> parameter mapping -> VLM verify) is the AI; the mesh is a deterministic renderer — and that determinism is the study's hypothesis. |
| "Why does the 3D arm look cartoonish / not photoreal?" | Dr. Evan explicitly accepted stylized output — teaching usefulness and sign fidelity are the criteria, not photorealism. He was part of every style decision via iterative client testing. |
| "What if 3D doesn't work?" | The design does not depend on it: the 3D arm has a 2-week go/no-go spike, and the diffusion arm alone is a complete system. |
| "Ethics of fake patient faces?" | Synthetic, AI-labeled, instructor-approved, no real photos, skin-tone-inclusive by design, SynthID watermark where supported. |
| "Sample size?" | 24-30 scenarios x 2 arms x 3 seeds (diffusion); paired within-scenario comparisons; power limits stated honestly. |

---

## 10. File Structure

```
thesis/
├── text/                        # OLD plan (RAG scenario generation) - reference only
│   ├── THESIS_DRAFT_PLAN.md
│   ├── AGENT_ARCHITECTURE_NOTE.md
│   ├── references.md
│   ├── combined_draft*.md
│   ├── chap_1/ ...
│   └── chap_2/ ...
└── image/                       # NEW plan (patient face generation)
    ├── THESIS_DRAFT_PLAN.md     # this file
    └── AGENT_ARCHITECTURE_NOTE.md

services/facegen/                # Python microservice (created in Phase 2)
├── app/
│   ├── main.py                  # FastAPI app
│   ├── schema.py                # trait schema models (pydantic)
│   ├── agents/
│   │   ├── parser.py            # LLM: text -> trait schema
│   │   ├── expander.py          # LLM: disease -> visible signs
│   │   ├── render_png.py        # Gemini image API (generate + edit loop)
│   │   ├── render_3d.py         # FLAME + material params + blendshapes
│   │   └── verifier.py          # VLM checklist
│   ├── catalog/
│   │   └── signs.json           # sign catalog (color/structural/asymmetric/secretions)
│   └── providers/
│       ├── gemini.py            # LLM + image + VLM client
│       └── flame.py             # FLAME 2023 Open loader (CPU)
├── tests/
└── pyproject.toml

laravel/                         # client integration
├── app/Http/Controllers/Faculty/ScenarioFaceController.php
├── app/Services/ScenarioFaceService.php   # HTTP client to the microservice
├── app/Console/Commands/FaceDemoCommand.php
├── database/migrations/xxxx_add_face_assets_to_scenarios_table.php
└── routes/faculty.php           # /faculty/scenarios/{scenario}/face/generate
```

---

## 11. Lock-In Confirmations & Open Items

- [x] Adviser: scenario TEXT generation dropped; instructors author scenarios
- [x] Adviser: patient face generation (PNG / SVG / 3D); head scope approved
- [x] Comparative = rendering modality (diffusion PNG vs parametric 3D);
      pipeline held constant (classmate owns one-shot vs agentic)
- [x] Evaluators = Dr. Evan + Nursing Department faculty (main users)
- [x] No GPU -> API-first for diffusion; CPU-only for 3D
- [x] Pre-oral target: late Nov / early Dec 2026
- [x] Realism relaxed (Oct 31): stylized output accepted by Dr. Evan;
      flow = build -> Dr. Evan tests -> iterate (trial and error with client)
- [ ] Confirm Gemini API key access (Plus subscription is NOT an API key);
      verify whether OpenCode Go 3 exposes an image generation endpoint
- [ ] Which sign types matter most to Dr. Evan (color signs = low-risk 3D;
      asymmetric signs = hardest blendshape work)
- [ ] Rater pool: confirm 2-3 faculty raters for kappa
- [ ] Pre-register the 24-30 test descriptions before the pilot

---

## 12. Pre-Oral Timeline (from Oct 31, 2026)

| Week | Dates | Work |
|---|---|---|
| 1 | Nov 1-7 | Lock title + RQs + SOP with adviser; Chapter 1 rewrite |
| 2 | Nov 8-14 | Chapter 2 RRL (Section 8 citations); Gemini API spike (3 descriptions) |
| 3 | Nov 15-21 | FLAME 3D spike (go/no-go); checklist + rubric co-design; Dr. Evan trial 1 |
| 4 | Nov 22-28 | Chapter 3 methodology; microservice + Laravel button; pre-register test set; Dr. Evan trial 2 |
| 5 | Dec 1+ | Pilot (5 scenarios x 2 arms); Dr. Evan trial 3; slides; grill rehearsal; pre-oral |

Client-testing loop: every Dr. Evan trial feeds the next build iteration
(sign catalog, severity scales, visual style). The trial notes double as
Chapter 4 "system iteration" material and defense evidence.

---

**Last Updated:** 2026-10-31
**Status:** New scope locked (patient face generation). Pre-oral late Nov / early Dec. Early-week focus is the capstone porting branch; thesis work is evenings/weekends around it.
**Owner:** [Your Name] — BS CS, Golden Gate Colleges
