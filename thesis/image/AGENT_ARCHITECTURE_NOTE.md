# Agent Architecture Note: Scenario-to-Patient-Face Generation Microservice

**Status:** PROPOSED — for consultation with adviser + client.
**Related:** `THESIS_DRAFT_PLAN.md` (same folder)
**Date:** 2026-10-31

---

## 1. Context

Dr. Evan wants the Chansey Scenario Builder to generate a **patient face
visualization** from the scenario's patient description. This note defines
the technical delivery: a **Python microservice** that the Laravel app calls
over HTTP, built as an **agentic workflow** (LLM + image model + VLM).

Why a microservice:

1. The AI stack (LLM SDKs, image APIs, FLAME, PyTorch) is Python-native;
   Laravel stays a thin client (matches AGENTS.md thin-controller rule).
2. The pre-oral demo needs something runnable: `uvicorn` + one CLI command
   that visibly produces an image. A separate service gives us that.
3. We have **no GPU**. Diffusion runs on paid APIs (Gemini). The 3D arm is
   CPU-only by design (FLAME is linear blendshape math). This architecture
   note locks that constraint in.

**Hard rules:**

- The pipeline is a **constant**, not an experimental variable (classmate
  owns one-shot vs agentic for video generation). Every arm uses parse ->
  expand -> render -> verify -> approve.
- **Zero training.** Fine-tuning waits until Chansey has a corpus of
  instructor-approved images + usage logs (MeMa precedent: fine-tuning on
  patient faces needs thousands of consented photos — not our current stage).
- SVG is **out** (StarVector is trained on icons/diagrams; faces are
  out-of-distribution). Modalities: PNG (diffusion) and 3D (parametric).
- **Realism target (Oct 31):** Dr. Evan does NOT require photorealistic
  faces. Stylized output is accepted; success = clinical-sign fidelity +
  teaching usefulness.
- **Client loop:** build what we can -> Dr. Evan tests -> iterate. Each trial
  session feeds the sign catalog, severity scales, and visual style. Keep the
  service's render parameters config-driven so his feedback is a config
  change, not a rebuild.

---

## 2. Component Overview

```
Laravel (Chansey, faculty scenario form)
   │  HTTP JSON
   ▼
FastAPI microservice (services/facegen)
   │
   ├── ParserAgent     LLM: free text -> trait schema JSON
   ├── ExpanderAgent   LLM: disease-only input -> proposed visible signs
   │                   (instructor confirmation required before render)
   ├── RenderAgent A   Diffusion PNG: Gemini image API
   │                   prompt compile -> generate -> VLM check -> localized
   │                   edit (max 2 loops)
   ├── RenderAgent B   Parametric 3D: FLAME 2023 Open (CPU)
   │                   shape/expression params + region material/color params
   │                   + structural-sign blendshapes -> offscreen render PNG
   └── VerifierAgent   VLM: per-trait checklist against the image
                       -> {present, missing, extra} report
```

Shared across everything: the **trait schema** (single source of truth) and
the **sign catalog** (`catalog/signs.json`), co-designed with Dr. Evan.

---

## 3. Trait Schema (single source of truth)

```json
{
  "sex": "female",
  "age": "adult",
  "skin_tone": "monk_3",
  "signs": [
    { "sign": "rhinorrhea", "severity": "moderate", "region": "nose",
      "laterality": null },
    { "sign": "jaundice", "severity": "mild", "region": "sclera_skin",
      "laterality": null },
    { "sign": "pallor", "severity": "moderate", "region": "lips",
      "laterality": null }
  ],
  "source": "description"
}
```

Sign catalog categories (each maps to a renderer strategy):

| Category | Examples | Diffusion (A) | Parametric 3D (B) |
|---|---|---|---|
| Color | jaundice, pallor, cyanosis, flushing | prompt + edit loop | region material/tint params (deterministic) |
| Structural symmetric | periorbital edema, sweating, glassy eyes | prompt | blendshape/geometry params |
| Structural asymmetric | ptosis, facial droop | weak (documented) | unilateral blendshapes (hardest work, go/no-go) |
| Secretions | runny nose, weepy eye | prompt | geometry/material props (stylized) |

---

## 4. Endpoints (FastAPI)

| Method | Path | Input | Output |
|---|---|---|---|
| POST | `/v1/parse` | `{text}` | trait schema JSON |
| POST | `/v1/expand` | `{disease, sex, age, skin_tone}` | proposed signs (for instructor confirmation) |
| POST | `/v1/render/png` | `{schema, mode: "one-shot"\|"agentic"}` | PNG bytes + audit trail |
| POST | `/v1/render/3d` | `{schema}` | PNG bytes + FLAME params + optional GLB |
| POST | `/v1/verify` | `{image_b64, schema}` | checklist report `{present[], missing[], extra[]}` |
| POST | `/v1/generate` | `{text, modality: "png"\|"3d"}` | full pipeline one-call (demo/convenience) |
| GET  | `/health` | — | `{status, providers: {gemini, flame}}` |

`/v1/generate` runs the whole fixed pipeline in one call and is the endpoint
the Laravel button and the pre-oral demo use. The granular endpoints exist
so each agent can be tested and shown separately at defense.

---

## 5. Agent Responsibilities & Flow

### 5.1 ParserAgent (LLM, e.g. Gemini flash)
Free text -> strict JSON via the trait schema. Unknown/multi-meaning terms
must resolve to catalog entries or be flagged for instructor review. Never
invent signs not derivable from the input.

### 5.2 ExpanderAgent (LLM, instructor-in-the-loop)
Input is disease-only ("high fever"): propose typical visible signs
(flushed cheeks, sweating, glassy eyes) with severity defaults. The proposal
is returned to the Laravel UI; Dr. Evan confirms/edits; only then is it
rendered. **The system never silently invents clinical content** — this is a
core defense point.

### 5.3 RenderAgent A — Diffusion PNG (Gemini image API)
- Model: Gemini 2.5 Flash Image ("Nano Banana") or Gemini 3 image preview.
- Prompt compiler turns the schema into a clinical description with explicit
  skin tone (Fitzpatrick/Monk), laterality, and severity terms (demographic
  prompt injection mitigates the documented light-skin bias).
- `mode=agentic`: after generation, the VerifierAgent checks traits; missing
  traits trigger a localized edit call (same image + instruction), max 2
  loops. Extra signs trigger a removal edit.
- Audit trail: prompt, model id, edits, verifier reports, token count,
  latency, seed. (This is the experimental data for Chapter 4.)

### 5.4 RenderAgent B — Parametric 3D (FLAME 2023 Open, CPU)
- FLAME 2023 Open is CC-BY-4.0 — license is safe to state at pre-oral.
- Schema -> FLAME identity/expression params + age cues (shape params).
- Color signs -> per-region albedo/tint parameters on the texture map
  (deterministic; cannot hallucinate).
- Structural signs -> blendshapes (bilateral: built-in expression basis;
  unilateral like ptosis/droop: custom blendshapes — the go/no-go spike).
- Offscreen render to PNG (trimesh/pyrender or PyTorch3D CPU; later three.js
  in-browser for an interactive viewer on the student side).
- Audit trail: full parameter vector (reproducible by construction).

### 5.5 VerifierAgent (VLM)
Per-trait checklist vs the rendered image -> `{present, missing, extra}`.
Trust is bounded: FineGRAIN (NeurIPS 2025) shows VLM judges agree with
humans only ~67% and fail on some categories, so the VLM report is a screen,
and Dr. Evan's approval is the hard gate. We measure VLM-vs-clinician kappa
as part of the study.

### 5.6 Approve (human)
Laravel UI shows the generated face + verifier report; Dr. Evan approves or
regenerates. Approved images are stored on the scenario (AI-generated label)
and logged (future fine-tune corpus).

---

## 6. Provider Strategy (no GPU, Oct 2026)

| Component | Provider | License / Note |
|---|---|---|
| LLM (parse/expand) | Gemini API (flash tier) | via AI Studio key; Plus subscription is NOT an API key — verify access |
| Text-to-image + edit | Gemini image API (Nano Banana / Gemini 3 image preview) | iterative editing strength; SynthID watermark (provenance) |
| VLM (verify) | Gemini vision API (or GPT vision) | one provider to keep latency/prompting consistent |
| 3D geometry | FLAME 2023 Open | CC-BY-4.0; CPU-only |
| Open-weights fallback (documented, not run now) | Qwen-Image-Edit (Apache 2.0, 20B) / FLUX.1 Kontext [dev] (non-commercial) | needs GPU we don't have; listed for licensing honesty in Chapter 2 |

Open items: does OpenCode Go 3 expose an image generation/editing endpoint?
(Check before locking the provider section.)

---

## 7. Laravel Integration (client only)

- Migration: add `face_image_path`, `face_asset_type` (`png`|`3d`),
  `face_trait_schema` (json), `face_audit` (json) to `scenarios`.
- `ScenarioFaceService` — HTTP client to the microservice
  (`FACE_SERVICE_URL` + `FACE_SERVICE_TOKEN` in `.env`), constructor-injected.
- `Faculty/ScenarioFaceController` — thin: validate (Form Request) ->
  authorize (Gate) -> call service -> return preview; approve action
  persists the asset to the scenario.
- Route: `POST /faculty/scenarios/{scenario}/face/generate` +
  `POST .../face/approve` in `routes/faculty.php`.
- Console command `php artisan face:demo "description" --modality=3d` — same
  call for terminal demos and CI.
- The faculty Scenario form (Blade, post-porting) gets a "Generate patient
  visual" button next to the patient description field.

---

## 8. Pre-Oral Demo Script

```powershell
# terminal 1 — microservice
cd services/facegen
uvicorn app.main:app --port 8000

# terminal 2 — one command, visible output
python -m facegen generate `
  --text "runny nose, yellowish eyes, pale lips, female" `
  --modality 3d --out demo_3d.png

python -m facegen generate `
  --text "runny nose, yellowish eyes, pale lips, female" `
  --modality png --mode agentic --out demo_png.png

# or through the app
php artisan face:demo "high fever, male adult" --modality png --mode agentic
```

Show: (1) the JSON schema printed, (2) the verifier checklist report, (3)
the two PNG outputs side by side, (4) the audit trail (tokens, latency,
edits). That single flow covers parse, expand (disease-only), both
renderers, verify, and the data you will analyze in Chapter 4.

---

## 9. Risks & Fallbacks

| Risk | Mitigation |
|---|---|
| Unilateral blendshapes too hard (3D) | Go/no-go after the Week-3 spike; sign set reshuffles to color/structural symmetric; study does not depend on 3D |
| Gemini API access/billing | AI Studio free tier for the demo; budget small paid tier for the full run; provider swap is a config change, not a redesign |
| Diffusion fails a trait in 2 edit loops | Output is marked "best effort" + verifier report shown to instructor; trait recall is a measured outcome, not an assumption |
| Visual style misses Dr. Evan's taste | He accepted stylized output (Oct 31); style is config-driven (palette, severity tints, stylization level) and tuned during client trial sessions — his feedback is a config change |
| Identity resemblance to real people | Synthetic parametric or seeded diffusion; AI label; instructor approval gate; no real photos anywhere |
| Rate limits during full experiment | Queue generations; cache repeated seeds; log token cost per run |

---

## 10. Future (data-rich stage, post-deployment)

- Usage logs + instructor-approved images become the fine-tune set
  (MeMa/AAAI 2025 pattern, but with our own consent-free synthetic data).
- Optionally train a renderer or a LoRA on the approved corpus and compare
  against the API baseline on the same metrics.
- Three.js interactive viewer on the student ward view (rotate the 3D head),
  and possibly full-body later if Dr. Evan asks (head scope for now).
