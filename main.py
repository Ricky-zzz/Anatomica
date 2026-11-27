#!/usr/bin/env python3
"""
ANATOMICA — Comparative Patient Facial Visualization Generator
Thesis Project: Diffusion PNG (Arm 1) vs Parametric 3D Head (Arm 2)

Usage:
    python main.py
"""

import sys
from pathlib import Path

# Ensure Anatomica root is on sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    console = Console()
except ImportError:
    console = None


def print_banner():
    title = (
        "ANATOMICA : Patient Face Visualization Generator\n"
        "Comparative Thesis: Diffusion PNG (Arm 1) vs Parametric 3D Head (Arm 2)"
    )
    if console:
        console.print(Panel(title, style="bold cyan", expand=False))
    else:
        print("=" * 70)
        print(title)
        print("=" * 70)


def display_schema(schema):
    if console:
        table = Table(title="Extracted Clinical Trait Schema", style="blue")
        table.add_column("Attribute", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        table.add_row("Sex", schema.sex.value)
        table.add_row("Age", schema.age.value)
        table.add_row("Skin Tone", schema.skin_tone.value)

        signs_str = (
            ", ".join([f"{s.sign} ({s.severity.value}, {s.region})" for s in schema.signs])
            if schema.signs
            else "None detected"
        )
        table.add_row("Signs", signs_str)
        console.print(table)
    else:
        print("\n--- Extracted Clinical Trait Schema ---")
        print(f"Sex: {schema.sex.value}")
        print(f"Age: {schema.age.value}")
        print(f"Skin Tone: {schema.skin_tone.value}")
        signs_str = ", ".join([f"{s.sign} ({s.severity.value})" for s in schema.signs]) or "None"
        print(f"Signs: {signs_str}\n")


def main():
    print_banner()

    from src.pipeline.orchestrator import GenerationPipeline

    pipeline = GenerationPipeline()

    try:
        if console:
            console.print("\n[bold yellow]Step 1:[/bold yellow] Enter patient description (e.g., 'runny nose, yellowish eyes, pale lips, female adult'):")
            desc = console.input("[bold green]> [/bold green]").strip()
        else:
            print("\nStep 1: Enter patient description (e.g., 'runny nose, yellowish eyes, pale lips, female adult'):")
            desc = input("> ").strip()

        if not desc:
            print("Description cannot be empty.")
            return

        print("\nParsing clinical traits...")
        schema = pipeline.parse_input(desc)
        display_schema(schema)

        # Prompt for comparison Arm
        if console:
            console.print("\n[bold yellow]Step 2:[/bold yellow] Select comparative generation arm:")
            console.print("  [bold cyan][0][/bold cyan] Arm 1 — Diffusion Image (Cloudflare Workers AI: FLUX / SDXL)")
            console.print("  [bold cyan][1][/bold cyan] Arm 2 — Parametric 3D Head Model (FLAME Offscreen Render)")
            choice_str = console.input("[bold green]Select (0 or 1): [/bold green]").strip()
        else:
            print("\nStep 2: Select comparative generation arm:")
            print("  [0] Arm 1 — Diffusion Image (Cloudflare Workers AI: FLUX / SDXL)")
            print("  [1] Arm 2 — Parametric 3D Head Model (FLAME Offscreen Render)")
            choice_str = input("Select (0 or 1): ").strip()

        if choice_str not in ["0", "1"]:
            print("Invalid choice. Please run again and select 0 or 1.")
            return

        arm_choice = int(choice_str)
        arm_label = "Arm 1 (Diffusion Image)" if arm_choice == 0 else "Arm 2 (Parametric 3D Model)"
        print(f"\nExecuting {arm_label}...")

        result = pipeline.execute_arm(schema, arm_choice)

        print("\n" + "=" * 60)
        print(f"Generation Complete ({result['latency_ms']:.1f} ms)!")
        print(f"Output Image : {result['image_path']}")
        print(f"Audit Trail  : {result['json_path']}")
        print("=" * 60 + "\n")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n[Error] An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
