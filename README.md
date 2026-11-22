# Anatomica

> **Comparative Evaluation of Diffusion-Based versus Parametric 3D Generation of Patient Facial Visualizations from Clinical Scenario Descriptions**  
> *Research Domain: Nursing Informatics / Multimodal Generative AI*

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Architecture: Fixed Agentic Pipeline](https://img.shields.io/badge/Architecture-Fixed_Pipeline-green.svg)]()

---

## 1. Overview

**Anatomica** is an experimental comparative engine designed to generate patient facial visualizations directly from clinical descriptions.

In clinical and nursing simulation education, instructors write case scenarios describing patient conditions. However, students frequently struggle to visualize physical manifestations (e.g., jaundice, cyanosis, ptosis, and facial droop) accurately without visual aids. While generic text-to-image models exist, literature documents that they frequently fail to reproduce asymmetric facial signs and exhibit systemic skin-tone biases.

Anatomica evaluates two rendering modalities under **one fixed agentic pipeline**:

```text
Natural Clinical Description (e.g., "runny nose, yellowish eyes, pale lips, female adult")
                                │
                                ▼
                       1. TraitSchema Parser (LLM)
                                │
         ┌──────────────────────┴──────────────────────┐
         ▼                                             ▼
  [Arm 0: Diffusion Image]                      [Arm 1: Parametric 3D]
  - Gemini / Imagen API                         - FLAME 2023 Open Head Model
  - Demographic prompt injection                - Deterministic region tints (albedo)
  - VLM self-correction loop                    - Unilateral/bilateral blendshapes
         │                                             │
         └──────────────────────┬──────────────────────┘
                                ▼
                       2. Offscreen Render to PNG
                                │
                                ▼
                       3. VLM Trait Verifier (Checklist)
                                │
                                ▼
                 Output PNG + Detailed Audit JSON Log
```

---

## 2. Experimental Arms

| Dimension | Arm 1 (Diffusion Image) | Arm 2 (Parametric 3D Model) |
|---|---|---|
| **Underlying Engine** | Latent Diffusion / Imagen API | FLAME 2023 Open (CC-BY-4.0) |
| **Color Signs** (jaundice, cyanosis) | Prompt injection & iterative edit loops | Deterministic region albedo tinting (zero hallucination) |
| **Structural / Asymmetric** (ptosis, droop) | Text conditioning (empirically prone to symmetry error) | Unilateral blendshape coefficients |
| **Skin-Tone Control** | Monk Scale demographic prompt conditioning | Explicit albedo palette mapping |
| **Hardware Requirement** | Cloud API (no local GPU required) | CPU-compatible offscreen rendering |
| **Determinism** | Stochastic (seed-dependent) | 100% deterministic parameter vector |

---

## 3. Directory Layout

```text
anatomica/
├── main.py                     # CLI Interactive Presentation Tool
├── requirements.txt            # Python dependencies (all open-source / free tier)
├── .env.example                # API key template
├── .gitignore
├── README.md                   # Project documentation
├── SUBTREE.md                  # Repository synchronization notes
│
├── config/
│   ├── settings.py             # Environment configuration and paths
│   └── signs.json              # Standardized clinical facial sign catalog
│
├── src/
│   ├── schema/
│   │   └── trait_schema.py     # Pydantic schema for demographic and clinical traits
│   ├── agents/
│   │   ├── parser.py           # Natural text to TraitSchema extractor
│   │   ├── expander.py         # Disease name to visible manifestations expander
│   │   └── verifier.py         # VLM-based visual sign audit checklist
│   ├── renderers/
│   │   ├── base.py             # Abstract Base Renderer definition
│   │   ├── diffusion.py        # Arm 1: Diffusion pipeline
│   │   └── parametric.py       # Arm 2: Parametric 3D FLAME pipeline
│   ├── pipeline/
│   │   └── orchestrator.py     # Fixed comparative workflow coordinator
│   └── utils/
│       ├── audit.py            # Audit trail JSON logger
│       ├── image_io.py         # Image helper functions
│       └── naming.py           # Standardized slug and timestamp generator
│
├── results/
│   ├── arm1/                   # Generated PNGs and audit JSONs for Arm 1
│   └── arm2/                   # Generated PNGs and audit JSONs for Arm 2
│
├── assets/
│   └── flame/                  # FLAME model weights directory
│
└── tests/                      # Automated test suite
```

---

## 4. Getting Started

### Prerequisites

- **Python 3.10+** installed
- **Git**
- Optional: A free Google AI Studio API key (for live cloud generation). Offline heuristic fallbacks are included for local testing.

### Installation

#### On Windows (PowerShell)

```powershell
# 1. Clone the repository
git clone https://github.com/Ricky-zzz/Anatomica.git
cd Anatomica

# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
```

#### On macOS / Linux (Bash)

```bash
# 1. Clone the repository
git clone https://github.com/Ricky-zzz/Anatomica.git
cd Anatomica

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 5. Configuration

Copy the example environment file:

```bash
# Windows:
copy .env.example .env

# macOS / Linux:
cp .env.example .env
```

Open `.env` in any text editor and insert your Gemini API Key from [Google AI Studio](https://aistudio.google.com/apikey):

```env
GEMINI_API_KEY=AIzaSy...your_actual_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_IMAGE_MODEL=imagen-3.0-generate-002
```

> **Note:** If `GEMINI_API_KEY` is omitted, Anatomica operates in **offline demonstration mode** using heuristic clinical parsing and synthetic visualization canvases.

---

## 6. Running the Interactive Demo

Launch the interactive presentation CLI:

```bash
python main.py
```

### Demonstration Walkthrough

1. **Input:** Type a patient description when prompted:
   ```text
   > adult female patient with pale lips, yellow eyes, and runny nose
   ```
2. **Clinical Parsing:** Anatomica parses demographic data and maps clinical signs to normalized anatomical regions:
   - *Sex:* Female
   - *Age:* Adult
   - *Skin Tone:* Monk Scale 4
   - *Signs:* Jaundice (sclera), Pallor (lips), Rhinorrhea (nose)
3. **Modality Selection:** Choose the experimental arm:
   - `0` for **Arm 1 (Diffusion Image)**
   - `1` for **Arm 2 (Parametric 3D Model)**
4. **Output:** 
   - The generated image is saved to `results/arm1/` or `results/arm2/`.
   - A synchronized `.json` audit trail recording latency, parameters, and VLM verification metrics is logged alongside the visual.

---

## 7. Running Tests

To verify the schema, parser heuristics, and pipeline offline operations:

```bash
pytest tests/
```

---

## 8. License & Attribution

- **Source Code:** Released under the [MIT License](LICENSE).
- **FLAME 2023 Open:** Head model topology and blendshape basis are licensed under [CC-BY-4.0](https://flame.is.tue.mpg.de/) by the Max Planck Institute for Intelligent Systems.
