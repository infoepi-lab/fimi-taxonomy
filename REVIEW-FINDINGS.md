# FIMI Taxonomy v4.0 — Codebase Security & Function Review

**Date:** 2026-02-13
**Scope:** Full project audit covering security, configuration, bibliography pipeline, YAML consistency, and rendering integrity.

---

## Summary

The project is structurally sound with no exposed secrets or critical security vulnerabilities. All fixable issues have been resolved. One item (`nul` file deletion) requires manual action due to filesystem permissions.

---

## Issues Found & Fixed

### 1. ~~`_site/` directory not in `.gitignore`~~ — FIXED

Added `_site/` and `nul` to `.gitignore` to prevent rendered output and Windows artifacts from being committed.

### 2. ~~Mixed CRLF/LF line endings across 26 `.qmd` files~~ — FIXED

All 26 files with Windows-style CRLF line endings have been normalized to Unix LF. A `.gitattributes` file has been created to enforce LF endings going forward for `.qmd`, `.bib`, `.yml`, `.css`, and `.py` files.

### 3. ~~Broken `@MISSING_*` placeholder citation keys~~ — FIXED

The `[@MISSING_xgql; @MISSING_nvg9; @MISSING_NoVD]` and `[@MISSING_NoVD]` active citations in both `mechanisms/cultural-infrastructure.qmd` and `function/projection-abroad-chapter.qmd` have been replaced with clean prose and HTML `<!-- TODO -->` comments preserving the original key names for future reference lookup. No active `[@MISSING_*]` citation brackets remain anywhere in the project.

### 4. ~~Empty `longevity.bib` and `structural-terrain.bib`~~ — FIXED

Both files now contain BibTeX comment headers explaining they await citations. They will parse cleanly without warnings. The 11 Longevity mechanism pages and 8 Structural Terrain mechanism pages that reference them will render without errors.

---

## Remaining Manual Action

### 5. `nul` — Windows artifact file in project root

A file named `nul` exists in the project root. The sandbox filesystem did not permit deletion. **You'll need to delete this manually:**

```bash
rm nul
```

It has already been added to `.gitignore` so it won't be tracked if you're using Git.

---

## Informational (No Action Needed)

### 6. Seven Suppressing Dissent mechanism pages lack `bibliography:` / `csl:` fields

No `.bib` file exists for Suppressing Dissent, and the 7 mechanism pages have no bibliography YAML fields. This is intentionally consistent — the Suppressing Dissent function has no chapter file and no citations. When citations are eventually needed, create `function/suppressing-dissent.bib` and add the fields to: banned-platforms, economic-coercion, forced-confessions, hostage-diplomacy, lawfare, repression, visa-denials.

### 7. No exposed secrets, credentials, or API keys

Full scan returned no results. The project is clean.

---

## Verified — No Issues Found

- **Project structure:** `_quarto.yml` is well-configured with consistent navbar, format settings, and `freeze: auto`.
- **All 9 `.bib` files exist** at their declared paths (6 populated, 2 with placeholder comments, 1 not yet created for Suppressing Dissent).
- **YAML frontmatter consistency:** All 101 mechanism pages have `title`, `description`, and `categories` fields. 94 have `bibliography` and `csl` fields (the 7 Suppressing Dissent pages are the expected exception).
- **Listing configurations:** All 10 function pages use consistent `listing:` blocks with proper `include: categories:` filters.
- **Navbar links:** All 5 navbar sections have valid `index.qmd` targets.
- **`generate_pages.py`:** No security concerns — standard CSV-to-QMD generator with `--dry-run` safety flag.
- **No duplicate YAML fields:** No pages have duplicate `bibliography:` or `csl:` declarations.
- **Line endings:** All `.qmd` files now use LF. `.gitattributes` enforces this going forward.
