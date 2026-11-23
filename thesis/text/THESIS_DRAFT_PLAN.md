# Thesis Draft Plan: Retrieval-Augmented Generative AI for Nursing Scenario Generation

**Working Title:** *Development and Comparative Evaluation of a Retrieval-Augmented Generative AI Assistant for Nursing Scenario Generation in an Educational Hospital Information System*

**Type:** Development + Comparative Experimental Evaluation
**Domain:** Nursing Informatics / Generative AI (NLP + RAG)
**Integration:** Chansey HIS — Scenario Module (Faculty Builder + Student Simulator)

> **Scope decision (locked with adviser):** The thesis pivoted from *predictive
> ML* (RF/DT/XGB adaptive recommendation) to **generative AI**. The comparative
> is **RAG-grounded vs non-grounded scenario generation**. Predictive ML is
> dropped; student weakness becomes a **rule-based calculation** that only feeds
> the generation prompt. See `RAG_GENERATION_NOTE.md` and
> `AGENT_ARCHITECTURE_NOTE.md` for the full rationale.

---

## 1. Problem Statement

Faculty authoring nursing simulation scenarios is manual and time-consuming.
Generative AI can draft scenarios, but **plain LLM generation hallucinates**
(wrong drugs, doses, milestones) because it has no grounding in institutional
content. The research problem is: **does retrieval-augmented generation (RAG),
grounded in faculty-authored scenarios, reduce clinical hallucination compared
to non-grounded generation?**

---

## 2. Objectives

### Primary (Experimental — the "soul" of the study)
1. Compare **RAG-grounded** vs **non-grounded** generation on:
   - schema validity rate
   - clinical plausibility (faculty rating)
   - coherence (orders ↔ diagnosis)
   - hallucination / contradiction rate
   - latency + token cost

### Secondary (Development / Deployment artifact)
2. Build an **"AI Draft" assistant** in the Faculty Scenario Builder that
   generates a *draft* scenario (patient + orders + milestones) which faculty
   review and approve before publish.
3. **Fine-tune a lightweight model** (secondary, per adviser) on faculty
   scenarios + generated drafts (distillation) as an on-premise alternative.

### Personalization (rule-based, NOT ML)
4. Compute a student weakness label from `progress_logs` (accuracy %, attempts,
   completion time, missed milestones) and inject it into the generation prompt.

---

## 3. Scope & Delimitations

| In Scope | Out of Scope |
|---|---|
| RAG-grounded vs non-grounded generation comparison | Predictive ML (RF/DT/XGB) — dropped |
| Faculty-authored scenarios as the grounding corpus | Training a model from scratch |
| Fine-tuned lightweight model (secondary artifact) | Autonomous publish (always faculty-approved) |
| Faculty (Nursing Department) validation of drafts | Physician diagnostic validation |
| Rule-based student weakness label | Multi-agent pipeline comparison (that's a classmate's) |
| API + RAG (zero training for the core) | Real clinical deployment / medical device |

**Ethics:** De-identified simulation content only; generated scenarios are
drafts until faculty approve; no patient data.

---

## 4. Data Sources (System-Generated, No External Dataset)

| Source | Use |
|---|---|
| `scenarios` (faculty-authored, with `difficulty` + `competency_tags`) | RAG grounding corpus + fine-tune examples |
| `scenario_orders` (pre-defined orders) | grounding + output schema |
| `scenario_progress_logs` | rule-based weakness label (input) |
| Generated drafts (validated) | optional fine-tune distillation data |

**Already built in the capstone (done):**
- `scenarios.difficulty` + `scenarios.competency_tags` columns
- `sections` + class management for grouping students/faculty

---

## 5. System Architecture (Chansey Integration)

### 5.1 Generation pipeline (Python, served via API)

```
Faculty scenarios (DB)
      │  embed → vector store (embed once, cache)
      ▼
[ vector store ]
      ▲
      │  query: weakness label + competency_tags + difficulty
      ▼
Prompt = [system rules] + [top-k retrieved scenarios] + [weakness label]
      │
      ├── Condition A (baseline): NO retrieval (plain prompt)
      └── Condition B (proposed): RAG-grounded
      ▼
LLM (API) → scenario JSON (validated against schema) → DRAFT
```

### 5.2 Chansey services (follows AGENTS.md patterns)

| Service | Responsibility |
|---|---|
| `ScenarioEmbeddingService` | Embed faculty scenarios → vector store (cached) |
| `ScenarioGenerationService` | Build prompt (grounded / non-grounded), call LLM API, parse + validate JSON |
| `StudentWeaknessCalculator` | **Rule-based** — accuracy %, attempts, time, missed milestones → weakness label |
| `FineTuneExportService` (secondary) | Export faculty scenarios + validated drafts as JSONL for fine-tuning |

### 5.3 Controllers & Routes (new, minimal)

```php
// Faculty side
Route::prefix('faculty/generate')->name('faculty.generate.')->group(fn () => [
    Route::post('draft', [ScenarioGenerationController::class, 'draft'])->name('draft'),
    Route::post('approve', [ScenarioGenerationController::class, 'approve'])->name('approve'),
]);
// "AI Draft" button in the existing Scenario Builder form
```

**Workflow:** Faculty clicks "AI Draft" → weakness/difficulty passed → system
generates a `draft` scenario → faculty reviews/edits → publish (existing flow).

---

## 6. Experimental Design (for Defense)

### 6.1 Main comparison: RAG vs no-RAG
- **Conditions:** A = plain prompt (no retrieval); B = RAG-grounded (top-k faculty scenarios).
- **Stimuli:** N = 60–100 generation requests across competencies × difficulties.
- **Metrics:** schema validity, hallucination rate, coherence, faculty plausibility score, latency, token cost.
- **Statistical test:** paired/independent t-test or Wilcoxon on faculty ratings; McNemar for validity/hallucination rates.

### 6.2 Secondary: fine-tuned model (deployment artifact)
- Fine-tune a small open model on faculty scenarios + generated drafts (distillation).
- **One metric only:** schema validity vs the API baseline. Keep clearly secondary.

### 6.3 Validation
- Nursing Department faculty rate generated drafts (plausibility, coherence) on a rubric.
- Inter-rater reliability (Krippendorff's alpha / Cohen's kappa) where possible.

---

## 7. MVP Checklist

### Phase 0: Pre-paper (can start before capstone deploy)
- [ ] Finalize title + SOP with adviser
- [ ] RRL: "retrieval-augmented generation clinical", "LLM hallucination healthcare", "RAG vs non-RAG evaluation"
- [ ] Write Chapter 1 (Problem, Objectives, Scope) + Chapter 3 methodology skeleton

### Phase 1: Corpus + embeddings
- [ ] Author/seed 12–15 faculty scenarios (with `difficulty` + `competency_tags`)
- [ ] `ScenarioEmbeddingService` + vector store

### Phase 2: Generation pipeline
- [ ] `ScenarioGenerationService` (prompt build + API call + JSON validation)
- [ ] Non-grounded (A) + RAG-grounded (B) modes
- [ ] "AI Draft" button in Scenario Builder + draft → approve → publish

### Phase 3: Evaluation
- [ ] Run 60–100 generations (A vs B), collect metrics
- [ ] Faculty rating rubric + inter-rater reliability
- [ ] Statistical analysis + tables/plots (Chapter 4)

### Phase 4: Secondary fine-tune (optional, per adviser)
- [ ] Export JSONL → fine-tune (hosted API or LoRA/Colab) → schema-validity check

### Phase 5: Writing
- [ ] Chapters 1–3 (already drafted in Phase 0) → 4 (results) → 5 (discussion)

---

## 8. RRL Anchors (Search Keywords for Chapter 2)

1. "retrieval-augmented generation" (RAG) — Lewis et al. 2020+
2. "LLM hallucination" + "healthcare / clinical / medical"
3. "RAG vs non-grounded generation" evaluation
4. "generative AI" + "medical education / nursing simulation"
5. "structured output" / "JSON schema" + "function calling" LLM
6. "knowledge distillation" / "fine-tuning on synthetic data" (for the secondary model)

---

## 9. Defense Talking Points (Prep)

| Panel Question | Prepared Answer |
|---|---|
| "Bakit generative, hindi predictive?" | Prediction was rule-derivable from logs; the real gap is scenario authoring, which generative AI targets. |
| "Hindi ba hallucination ang problema?" | That is exactly the research question — we test if RAG grounding reduces it, faculty-validated. |
| "Kopya ba kay [classmate] (single vs multi-agent)?" | No — his variable is agent count; ours is grounding (RAG vs no-RAG), a clinical-safety question. |
| "Bakit API, hindi train from scratch?" | Training from scratch is infeasible; API + RAG is zero-training and grounds on our own data. |
| "San galing ang data?" | Faculty-authored scenarios in Chansey (capstone data), not external. |
| "Sino nag-validate?" | Nursing Department faculty — the clinical-educational authority. |
| "May sarili ba kayong model?" | Yes (secondary) — a fine-tuned lightweight model (distillation), positioned as deployment artifact. |

---

## 10. File Structure (Thesis Code)

```
thesis/
├── rag/
│   ├── embed.py               # embed faculty scenarios → vector store
│   ├── store.py               # vector store (sqlite-vec / FAISS / numpy)
│   ├── generate.py            # grounded vs non-grounded generation
│   ├── validate.py            # JSON schema validation
│   └── evaluate.py            # metrics + stats
├── finetune/                  # secondary
│   ├── export_jsonl.py
│   └── train.py               # hosted API or LoRA/Colab
├── laravel/
│   ├── app/Services/
│   │   ├── ScenarioEmbeddingService.php
│   │   ├── ScenarioGenerationService.php
│   │   └── StudentWeaknessCalculator.php
│   ├── app/Http/Controllers/Faculty/ScenarioGenerationController.php
│   └── routes/faculty.php     # /faculty/generate/*
├── validation/
│   ├── rubric.md              # faculty plausibility/coherence rubric
│   └── analysis.ipynb
└── docs/
    ├── chapter_outline.md
    ├── defense_slides_outline.md
    └── gantt_chart.md
```

---

## 11. Prof Lock-In Confirmations (from PM)

- [x] Adviser agreed to **generation** as the core
- [x] **Drop predictive ML** → rule-based weakness calculation
- [x] Comparative = **RAG-grounded vs non-grounded** (not single vs multi-agent)
- [x] **Faculty (Nursing Department) = validator**
- [ ] Adviser accepts **trained model as secondary** (distillation, not core)
- [ ] Confirm API provider (OpenCode Zen / OpenAI / Gemini) + model version

---

## 12. Scenario Isolation Mechanism (Template vs Instance)

**Critical implementation note (kept from prior plan):** The Scenario Module uses
a **template → instance** pattern so many students can run one scenario without
conflict. The generator targets the **template** (`scenarios`), not instances.

```
1 Scenario (faculty-authored template)
    ↓ assigned to N students
N ScenarioAssignments → N ScenarioSessions → N SIM Patients/Admissions
```

**For generation:** the "AI Draft" creates a new `scenarios` row (draft) from
faculty scenarios in the corpus; it does not touch live sessions.

---

## 13. Next Immediate Actions

1. **Send title + scope confirmation PM** to prof (Section 11 outstanding items)
2. **Start the paper now** — Chapter 1 + RRL + methodology skeleton (no capstone deploy needed)
3. Author/seed 12–15 faculty scenarios for the grounding corpus
4. Prototype `embed.py` + `generate.py` (grounded vs non-grounded) locally
5. Build the "AI Draft" flow in the Faculty Scenario Builder

---

**Last Updated:** 2026-10-07
**Status:** Scope pivoted to generative AI (RAG vs no-RAG). Paper can start now; system work after capstone deploy.
**Owner:** [Your Name] — BS CS, Golden Gate Colleges
