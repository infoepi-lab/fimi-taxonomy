#!/usr/bin/env python3
"""
Generate .qmd pages for the Information Manipulation Taxonomy v4.0 website.

By default, only regenerates MECHANISM pages from mechanisms.csv + examples.csv.
Function pages are manually maintained and should NOT be regenerated
unless explicitly requested.

Usage:
    python3 generate_pages.py              # mechanisms only
    python3 generate_pages.py --dry-run    # preview without writing
    python3 generate_pages.py --functions  # also regenerate function pages
                                           # (WARNING: overwrites manual edits)
"""

import csv
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DRY_RUN = "--dry-run" in sys.argv
INCLUDE_FUNCTIONS = "--functions" in sys.argv

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    """Convert a display name to a filename slug."""
    return name.lower().replace(" ", "-")


def write_file(path: str, content: str):
    """Write content to a file (or print in dry-run mode)."""
    if DRY_RUN:
        print(f"[DRY RUN] Would write {path} ({len(content)} chars)")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Wrote {path}")


def load_examples():
    """Load examples.csv grouped by mechanism name."""
    csv_path = os.path.join(PROJECT_ROOT, "examples.csv")
    examples = {}
    if not os.path.exists(csv_path):
        return examples
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            mech = row.get("mechanism", "").strip()
            if mech:
                examples.setdefault(mech, []).append(row)
    return examples


# Function color mapping for badges
FUNCTION_COLORS = {
    "Command and Control": "#c0392b",
    "Legitimation": "#d35400",
    "Longevity": "#7d3c98",
    "Obfuscation": "#2c3e50",
    "Operational Multipliers": "#2980b9",
    "Projection Abroad": "#16a085",
    "Sabotage": "#922b21",
    "Spillover": "#1a5276",
    "Suppressing Dissent": "#6c3483",
}


# ---------------------------------------------------------------------------
# Function pages (opt-in only — these are manually maintained)
# ---------------------------------------------------------------------------

def generate_function_pages():
    """
    Generate function/<slug>.qmd from function.csv.

    WARNING: Function pages have been manually edited with chapter-derived
    Explainer sections. Only run this if you have updated function.csv to
    match the desired content.
    """
    csv_path = os.path.join(PROJECT_ROOT, "function.csv")
    mech_csv = os.path.join(PROJECT_ROOT, "mechanisms.csv")

    # Load mechanisms grouped by function
    mechanisms_by_func = {}
    with open(mech_csv, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            func = row["function"]
            mechanisms_by_func.setdefault(func, []).append(row)

    # Sort mechanisms alphabetically within each function
    for func in mechanisms_by_func:
        mechanisms_by_func[func].sort(key=lambda r: r["mechanism"])

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["functions"]
            slug = slugify(name)
            definition = row["definition"].strip()
            explainer = row["explainer"].strip()
            mechs = mechanisms_by_func.get(name, [])
            # First sentence of definition for card description
            first_sent = definition.split(". ")[0] + "."
            if len(first_sent) > 200:
                first_sent = first_sent[:197] + "..."
            desc = first_sent.replace('"', '\\"')
            # Build page content
            lines = []
            lines.append("---")
            lines.append(f'title: "{name}"')
            lines.append(f'description: "{desc}"')
            lines.append("categories: [function]")
            lines.append("---")
            lines.append("")

            # Definition
            lines.append("## Definition")
            lines.append("")
            lines.append(definition)
            lines.append("")

            # Explainer
            lines.append("## Explainer")
            lines.append("")
            lines.append(explainer)
            lines.append("")

            # Mechanisms - use Quarto listing instead of manual list
            if mechs:
                lines.append("## Mechanisms")
                lines.append("")
                lines.append(
                    f"This function operates through **{len(mechs)} mechanisms**. "
                    f"Browse the mechanisms associated with {name} below:"
                )
                lines.append("")
                # The actual listing will be added via Quarto listing configuration
                # in the page frontmatter or a separate listing include

            content = "\n".join(lines) + "\n"
            out_path = os.path.join(PROJECT_ROOT, "function", f"{slug}.qmd")
            write_file(out_path, content)


# ---------------------------------------------------------------------------
# Mechanism pages (default — always safe to regenerate)
# ---------------------------------------------------------------------------

def generate_mechanism_pages():
    """Generate mechanisms/<slug>.qmd from mechanisms.csv + examples.csv."""
    csv_path = os.path.join(PROJECT_ROOT, "mechanisms.csv")
    examples = load_examples()

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["mechanism"]
            slug = slugify(name)
            func = row["function"]
            func_slug = slugify(func)
            one_line = row["one_line"].strip()
            description = row["description"].strip()
            color = FUNCTION_COLORS.get(func, "#6c757d")

            lines = []
            lines.append("---")
            lines.append(f'title: "{name}"')
            lines.append(f'description: "{one_line}"')
            lines.append(f'categories: ["{func}"]')
            lines.append("---")
            lines.append("")

            # Function badge using CSS class
            lines.append("::: {.function-badge}")
            lines.append(f"[{func}](../function/{func_slug}.qmd)")
            lines.append(":::")
            lines.append("")

            # Description (skip the one-liner — it's already in the
            # frontmatter description and the card listing)
            if description:
                lines.append(description)
                lines.append("")

            # Examples from examples.csv
            mech_examples = examples.get(name, [])
            if mech_examples:
                lines.append("## Documented Examples")
                lines.append("")
                for ex in mech_examples:
                    quote = ex.get("quote", "").strip()
                    url = ex.get("URL", "").strip()
                    title = ex.get("title", "").strip()
                    if quote:
                        lines.append(f"> {quote}")
                        lines.append(">")
                        if url and title:
                            lines.append(f"> — [{title}]({url})")
                        elif url:
                            lines.append(f"> — [Source]({url})")
                        lines.append("")

            content = "\n".join(lines) + "\n"
            out_path = os.path.join(PROJECT_ROOT, "mechanisms", f"{slug}.qmd")
            write_file(out_path, content)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating pages from CSVs...")
    if DRY_RUN:
        print("(DRY RUN — no files will be written)\n")

    if INCLUDE_FUNCTIONS:
        print("\n=== Function pages ===")
        print("WARNING: Overwriting manually maintained function pages.")
        print("Make sure function.csv is up to date first.\n")
        generate_function_pages()
    else:
        print("\nSkipping function pages (manually maintained).")
        print("Use --functions to regenerate them from function.csv.\n")

    print("=== Mechanism pages ===")
    generate_mechanism_pages()

    print("\nDone.")

