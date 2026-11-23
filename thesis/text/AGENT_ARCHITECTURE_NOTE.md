# Thesis Note: Grounded vs Non-Grounded Clinical Scenario Generation

**Status:** PROPOSAL — for consultation with adviser + client.
**Related:** `THESIS_DRAFT_PLAN.md`, `RAG_GENERATION_NOTE.md`
**Date:** 2026-10-07

---

## 1. Context

Adviser is pushing **generative AI** for scenario creation. The comparative
must be experimental (department requirement) but **distinct from a classmate**
who compares single-agent vs multi-agent pipelines for generating lesson videos.

**Final comparative (chosen to avoid copying):**
> **RAG-grounded generation vs non-grounded (plain prompt) generation** — does
> grounding on faculty scenarios reduce clinical hallucination?

Predictive ML (RF/DT/XGB) is **dropped**; student weakness becomes a **rule-based
calculation** (accuracy %, attempts, completion time, missed milestones) that is
only an *input* to the generation prompt.

---

## 2. Terminology lock (avoid defense traps)

| Term | Meaning | For us |
|---|---|---|
| Train from scratch | build a model from zero weights | ❌ no one does this |
| Fine-tune | continue training a pretrained model on our examples | ❌ not used |
| **API + RAG** | rent a model, feed context at inference | ✅ zero training |

Correct line: *"Hindi po ako mag-train from scratch. Gagamit po ako ng existing
model via API + RAG (zero training)."*

---

## 3. The comparative (two conditions)

**Condition A — Non-grounded (baseline)**
- One LLM call with a plain prompt (student weakness + instructions).
- No retrieval; the model writes from its own knowledge.

**Condition B — RAG-grounded (proposed)**
- Retrieve top-k similar faculty scenarios (by `competency_tags` + `difficulty`).
- Feed them as context, then generate.
- Output is grounded in the faculty's own content.

```
Faculty scenarios (DB)
      │  embed → vector store
      ▼
[ vector store ]  ← precomputed once
      ▲
      │  query: "weak in medication_administration, at-risk"
      │  → top-5 similar scenarios
      ▼
Prompt = [system rules] + [5 retrieved scenarios] + [weakness label]
      ▼
LLM (API) → scenario JSON → DRAFT → faculty approves
```

---

## 4. Comparative metrics (Chapter 4)

| Metric | Non-grounded | RAG-grounded |
|---|---|---|
| Schema validity rate (%) | | |
| Clinical plausibility (faculty rating) | | |
| Coherence (orders ↔ diagnosis match) | | |
| Hallucination / contradiction rate | | |
| Latency (sec / scenario) | | |
| Token cost (per scenario) | | |

---

## 5. Statement of the Problem

1. Does RAG-grounded generation produce scenarios with higher schema validity
   and clinical plausibility than non-grounded generation?
2. Does grounding reduce hallucination/contradiction, as measured by faculty
   rating?
3. What is the latency/cost tradeoff of adding retrieval for real-time faculty
   use?

---

## 6. Validation approach (resolved)

- Generated scenarios are **validated by the Nursing Department faculty** — the
  clinical-educational authority; no physician panel required.
- This keeps **data provenance + accreditation** intact: the model drafts, the
  faculty approves before publish.

---

## 7. How it fits Chansey (capstone)

- The winning approach powers an **"AI Draft" button in the Faculty Scenario
  Builder**.
- Flow: rule-based weakness label → (optional RAG) retrieve similar faculty
  scenarios → generate **draft** → faculty reviews/edits → publish.
- Deliverables stay material: an AI-assist authoring feature inside the existing
  `Scenario` module, not a standalone demo.

---

## 8. Differentiation from classmate (shimi)

Classmate's method: **API then fine-tune** (two-stage). Domain: video generation.
Classmate's variable: **agent count** (single vs multi-agent).

| | Shimi | This thesis |
|---|---|---|
| Variable under test | Agent count (single vs multi) | **Grounding (RAG vs no-RAG)** |
| Model work | API **then fine-tune** | **API + RAG only, zero training** |
| Domain | Video (visual/temporal) | Structured clinical scenarios (schema + safety) |
| Contribution | Better video generation | **Reduced clinical hallucination, faculty-validated** |

Three clean separators:

1. **Different variable** — shimi varies agent count; we vary grounding.
2. **No fine-tune** — clinical scenario pairs are scarce (vs plentiful lesson
   videos), so API + RAG is the appropriate method anyway.
3. **Clinical correctness** — a dimension video pipelines do not have.

Defense line: *"Same generative-AI technique, pero different variable
(grounding vs agent count) at different contribution — clinical correctness ng
generated content, zero training."*

---

## 9. Remaining decision

- Prediction is **dropped** (rule-based instead). Confirm with adviser.
- Comparative is **RAG vs no-RAG** (not single vs multi-agent). Confirm.

**Final proposed scope:** Generation core (RAG-grounded vs non-grounded) +
rule-based personalization + faculty (Nursing Department) validator + API+RAG
(no fine-tune for the core comparative). Contribution = reduced clinical
hallucination.

---

## 9b. Trained model (secondary objective, per adviser)

Adviser still wants "our own model." Compromise: keep the comparative as the
**soul**, and add a **secondary** trained model as a deployment artifact.

- **What:** fine-tune a small open model (e.g., Qwen2.5-7B / Gemma) on
  faculty-authored scenarios + our API-generated drafts (**distillation**).
- **Route:** hosted fine-tune API (no GPU) OR LoRA/QLoRA on Colab.
- **Position:** lightweight on-premise generator that matches our schema — NOT
  the main accuracy claim.
- **Recommendation:** further fine-tune with more faculty-validated data.

**Warnings**
1. Data is scarce — rely on generated drafts as synthetic training data; state
   this plainly (distillation) to avoid circularity criticism.
2. Keep it clearly secondary — at most one metric (schema validity). If it
   becomes the measured outcome, scope doubles again.

---

## 10. Decision log

- [ ] Adviser confirms **RAG-grounded vs non-grounded** as the comparative
- [ ] Adviser accepts **dropping predictive ML** (rule-based instead)
- [ ] Nursing Department faculty agree to validate (N raters)
- [ ] Confirm API provider (OpenCode Zen / OpenAI / Gemini) + model version
- [ ] Confirm **no fine-tune** (API + RAG only) to differentiate from shimi
- [ ] Adviser accepts **trained model as secondary objective** (distillation, not core)

*End of note.*
