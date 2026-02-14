# Citation Audit Results

**Date:** February 14, 2026  
**Status:** 21 Citations Need Attention

---

## Summary

- ✅ **282 citations** used in .qmd files
- ✅ **297 bibliography entries** in .bib files  
- ⚠️ **5 fuzzy matches** - exist but case mismatch
- ❌ **16 missing citations** - don't exist in any bib file

---

## Fuzzy Matches (5) - Easy to Fix

These exist in bib files but with different case:

| Citation in .qmd | Bib Entry | Files |
|-----------------|-----------|-------|
| `@cia1955` | `CIA1955` | legitimation-chapter.qmd, mechanisms/academic-initiatives.qmd |
| `@huang2019` | `HUANG2019` | legitimation-chapter.qmd |
| `@kamyshanskaya2021` | `KAMYSHANSKAYA2021` | legitimation-chapter.qmd |
| `@redden2013` | `REDDEN2013` | legitimation-chapter.qmd |
| `@shikerova2022` | `SHIKEROVA2022` | legitimation-chapter.qmd |

**Fix:** Change bib entries to lowercase to match citations

---

## Missing Citations (16) - Need Investigation

These are used in .qmd files but don't exist in any .bib file:

### In projection-abroad-chapter.qmd (4):
- `@HRW20221` - Likely should be `hrw2022` (with lowercase, no "1" suffix)
- `@MISSING_NoVD` - Placeholder, needs actual entry
- `@MISSING_nvg9` - Placeholder, needs actual entry  
- `@MISSING_xgql` - Placeholder, needs actual entry

### In legitimation-chapter.qmd (11):
- `@alex2020` - No entry found
- `@alexiev1985` - Should be `Alexiev19852` or create new entry
- `@center2020` - No entry found (might be `GLOBAL_ENGAGEMENT_CENTER2020`)
- `@china2024` - No entry found
- `@department2024` - No entry found (might be `US_DEPARTMENT_OF...`)
- `@douma2018` - No entry found
- `@mkinen2016` - Should be `MAKINEN2016`
- `@page2025` - No entry found
- `@post2024` - No entry found (might be `THE_WASHINGTON_POST2024`)
- `@soviet1954` - Should be `F1954`
- `@the1971` - No entry found

### In projection-abroad.qmd (1):
- `@methods` - No entry found

---

## Recommended Actions

### Quick Wins (5 minutes):

1. **Fix the 5 fuzzy matches:**
   ```python
   python fix_citation_keys_v2.py
   ```
   This should handle the case mismatches automatically.

2. **Fix obvious mappings:**
   - `@mkinen2016` → exists as `MAKINEN2016` in bib
   - `@alexiev1985` → exists as `Alexiev19852` in bib
   - `@soviet1954` → exists as `F1954` in bib

### Requires Research (30-60 minutes):

3. **Investigate missing citations:**
   - Search legitimation.bib for entries that might match:
     - `center2020` might be `GLOBAL_ENGAGEMENT_CENTER2020`
     - `department2024` might be `US_DEPARTMENT_OF_STATE2024`
     - `post2024` might be `THE_WASHINGTON_POST2024`
   
4. **Handle MISSING_ placeholders:**
   - These are temporary placeholders in projection-abroad-chapter.qmd
   - Either add proper bib entries or remove citations

5. **Add genuinely missing entries:**
   - `@alex2020`, `@china2024`, `@douma2018`, `@page2025`, `@methods`
   - Either find and add bib entries or remove from text

---

## Tools to Use

### Find Missing Citations:
```bash
python find_missing_citations.py
```

### Fix Case Mismatches:
```bash
python fix_citation_keys_v2.py
```

### Manual Fixes:
Edit the files directly:
- `function/legitimation-chapter.qmd`
- `function/projection-abroad-chapter.qmd`
- `function/projection-abroad.qmd`
- `mechanisms/academic-initiatives.qmd`

---

## Impact

**Current state:**
- Site builds successfully ✅
- 21 citations show as "?" in rendered pages ⚠️
- Doesn't prevent deployment, but reduces academic credibility

**After fixes:**
- All citations will resolve properly ✅
- Professional, publication-ready output ✅

---

## Next Steps

1. Run `python fix_citation_keys_v2.py` to fix the 5 fuzzy matches
2. Manually review and fix the 16 missing citations
3. Run `quarto render` to verify all warnings are gone
4. Deploy with confidence!
