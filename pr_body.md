## Summary

Initial setup of FIMI Taxonomy v4.0 with all configuration fixes, citation corrections, and site structure improvements.

## Changes

### Configuration Fixes
- Fixed invalid `margin-footer` in `_quarto.yml` that was preventing site build
- Updated navigation to use Notes listing page

### Bibliography & Citations
- Fixed BibTeX syntax errors in `projection-abroad.bib` (lines 778, 803)
- Standardized 95+ citation keys across all bibliography files
- Fixed case mismatches between citations and bibliography entries

### Site Structure
- Created `notes.qmd` as blog listing page at root level
- Updated navigation to point to Notes instead of blog index
- Removed broken mechanism links from all 7 terrain pages

### Airtable Integration Tools
- Created `update_airtable_functions.py` for syncing function chapters
- Created `update_airtable_mechanisms.py` for syncing mechanism pages

### Automation Scripts
- `fix_citation_keys.py` & v2 - Automated citation key standardization
- `fix_bib_files.py` - BibTeX syntax validator
- `find_missing_citations.py` - Citation audit tool

## Test Plan
- [x] Quarto site builds without errors
- [x] All citations resolve correctly
- [x] Blog listing displays properly
- [x] No broken links in terrain pages
