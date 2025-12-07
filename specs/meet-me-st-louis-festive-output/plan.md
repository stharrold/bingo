# Implementation Plan: Meet Me In St. Louis Festive Output

**Type:** feature
**Slug:** meet-me-st-louis-festive-output
**Date:** 2025-12-07

## Task Breakdown

### Epic 1: Festive Card Support

#### Task E1_01: Add Color Scheme

**Priority:** High

**Files:**
- `src/bingo/html_pdf.py`

**Description:**
Add Meet Me In St. Louis color scheme to `FESTIVE_COLORS` dict in html_pdf.py

**Steps:**
1. Open `src/bingo/html_pdf.py`
2. Locate `FESTIVE_COLORS` dictionary
3. Add new entry for "meet_me_in_st_louis" with Victorian-era color scheme

**Acceptance Criteria:**
- [ ] Color scheme added to FESTIVE_COLORS
- [ ] Colors: primary=#8B0000, secondary=#FFD700, background=#FFF8E7, text=#2F1810

**Verification:**
```bash
podman-compose run --rm dev python -c "from bingo.html_pdf import FESTIVE_COLORS; print(FESTIVE_COLORS.get('meet_me_in_st_louis'))"
```

**Dependencies:**
- None

---

#### Task E1_02: Add Film Configuration

**Priority:** High

**Files:**
- `src/bingo/html_pdf.py`

**Description:**
Update `create_festive_html()` to support Meet Me In St. Louis as a single-film game

**Steps:**
1. Locate `create_festive_html()` function
2. Add film section for meet_me_in_st_louis spanning items 1-30
3. Add subtitle to subtitles dict
4. Handle single-film vs multi-film game distinction

**Acceptance Criteria:**
- [ ] Film configuration added for meet_me_in_st_louis
- [ ] Subtitle displays correctly on festive cards
- [ ] Items 1-30 render correctly

**Verification:**
```bash
podman-compose run --rm dev bingo festive -g meet_me_in_st_louis -n 1
```

**Dependencies:**
- E1_01 (color scheme must exist)

---

#### Task E1_03: Test Festive Generation

**Priority:** High

**Files:**
- None (testing only)

**Description:**
Verify festive HTML+PDF generation works correctly for Meet Me In St. Louis

**Steps:**
1. Generate festive HTML output
2. Generate festive PDF output
3. Verify visual output matches expected color scheme
4. Verify emoji icons display correctly

**Acceptance Criteria:**
- [ ] Festive HTML generates without errors
- [ ] Festive PDF generates without errors
- [ ] Colors match specified scheme
- [ ] Emoji icons render correctly

**Verification:**
```bash
podman-compose run --rm dev bingo festive -g meet_me_in_st_louis -n 30 --pdf
```

**Dependencies:**
- E1_01, E1_02

---

### Epic 2: File Naming Convention

#### Task E2_01: Update GAME_FILE_PREFIXES

**Priority:** High

**Files:**
- `src/bingo/cli.py`

**Description:**
Update `GAME_FILE_PREFIXES` to use hyphenated slugs for file naming

**Steps:**
1. Open `src/bingo/cli.py`
2. Locate `GAME_FILE_PREFIXES` dictionary
3. Update values to use hyphenated format (meet-me-in-st-louis, vintage-christmas-films)

**Acceptance Criteria:**
- [ ] GAME_FILE_PREFIXES updated with hyphenated values
- [ ] meet_me_in_st_louis maps to "meet-me-in-st-louis"
- [ ] vintage_christmas_films maps to "vintage-christmas-films"

**Verification:**
```bash
podman-compose run --rm dev python -c "from bingo.cli import GAME_FILE_PREFIXES; print(GAME_FILE_PREFIXES)"
```

**Dependencies:**
- None

---

#### Task E2_02: Update File Generation Logic

**Priority:** High

**Files:**
- `src/bingo/cli.py`

**Description:**
Update file generation to use new naming pattern: `<slug>_<type>.<ext>`

**Steps:**
1. Update key command file naming
2. Update cards command file naming
3. Update festive command file naming
4. Ensure numbered cards follow `<slug>_card_NN.pdf` format

**Acceptance Criteria:**
- [ ] Key files named: `<slug>_key.pdf`
- [ ] Card files named: `<slug>_card_NN.pdf`
- [ ] Festive files named: `<slug>_cards-festive.html/pdf`

**Verification:**
```bash
podman-compose run --rm dev bingo key -g meet_me_in_st_louis -o output/
ls output/meet-me-in-st-louis_key.pdf
```

**Dependencies:**
- E2_01

---

### Epic 3: Introduction Document

#### Task E3_01: Write Introduction Content

**Priority:** Medium

**Files:**
- `output/meet-me-in-st-louis_introduction.md` (new)

**Description:**
Create introduction markdown document with movie context

**Steps:**
1. Research movie history and context
2. Write sections covering:
   - Movie overview (1944 MGM musical)
   - Cast highlights (Judy Garland, Margaret O'Brien)
   - Production context (Technicolor, Arthur Freed Unit)
   - 1904 St. Louis World's Fair setting
   - Musical numbers overview
   - Seasonal/holiday themes
3. Format as markdown

**Acceptance Criteria:**
- [ ] Introduction document created
- [ ] All required sections included
- [ ] Concise and informative (similar length to vintage films intro)

**Verification:**
```bash
test -f output/meet-me-in-st-louis_introduction.md && echo "OK"
```

**Dependencies:**
- None (can be done in parallel)

---

#### Task E3_02: Generate Introduction PDF

**Priority:** Medium

**Files:**
- `output/meet-me-in-st-louis_introduction.pdf` (generated)

**Description:**
Convert introduction markdown to PDF using Playwright

**Steps:**
1. Create HTML template for introduction
2. Use Playwright to convert to PDF
3. Ensure formatting matches other output documents

**Acceptance Criteria:**
- [ ] PDF generates from markdown
- [ ] Formatting is clean and readable
- [ ] File saved to output directory

**Verification:**
```bash
test -f output/meet-me-in-st-louis_introduction.pdf && echo "OK"
```

**Dependencies:**
- E3_01

---

### Epic 4: Output Generation & Git Tracking

#### Task E4_01: Clean Old Output Files

**Priority:** Low

**Files:**
- `output/` directory

**Description:**
Remove old naming convention files if present

**Steps:**
1. Identify files with old naming pattern (BingoCard_*, BingoKey_*)
2. Remove old files for Meet Me In St. Louis
3. Keep vintage_christmas_films files until renamed

**Acceptance Criteria:**
- [ ] Old naming pattern files removed
- [ ] No duplicate files in output

**Verification:**
```bash
ls output/ | grep -E "^Bingo" || echo "No old files"
```

**Dependencies:**
- E2_01, E2_02 (new naming ready)

---

#### Task E4_02: Generate All Meet Me In St. Louis Output

**Priority:** High

**Files:**
- `output/` directory

**Description:**
Generate complete set of Meet Me In St. Louis output files

**Steps:**
1. Generate festive HTML+PDF (30 cards)
2. Generate standard PDF cards (30 cards)
3. Generate key PDF
4. Verify all files use new naming convention

**Acceptance Criteria:**
- [ ] 30 festive cards generated
- [ ] 30 standard cards generated
- [ ] Key PDF generated
- [ ] All files use hyphenated naming

**Verification:**
```bash
podman-compose run --rm dev bingo festive -g meet_me_in_st_louis -n 30 --pdf
podman-compose run --rm dev bingo cards -g meet_me_in_st_louis -n 30
podman-compose run --rm dev bingo key -g meet_me_in_st_louis
ls output/meet-me-in-st-louis_* | wc -l
```

**Dependencies:**
- E1_01, E1_02, E2_01, E2_02

---

#### Task E4_03: Update Vintage Christmas Films Output

**Priority:** Low

**Files:**
- `output/` directory

**Description:**
Regenerate Vintage Christmas Films output with new naming convention

**Steps:**
1. Remove old vintage_christmas_films output files
2. Regenerate with new naming convention
3. Verify consistency with Meet Me In St. Louis output

**Acceptance Criteria:**
- [ ] Vintage films output uses hyphenated naming
- [ ] All vintage films files regenerated

**Verification:**
```bash
podman-compose run --rm dev bingo festive -g vintage_christmas_films -n 30 --pdf
ls output/vintage-christmas-films_* | wc -l
```

**Dependencies:**
- E2_01, E2_02

---

#### Task E4_04: Commit Output to Git

**Priority:** High

**Files:**
- `output/` directory
- `.gitignore`

**Description:**
Ensure all output files are tracked in git

**Steps:**
1. Verify .gitignore doesn't exclude output files
2. Stage all new/updated output files
3. Commit with descriptive message

**Acceptance Criteria:**
- [ ] output/ directory tracked in git
- [ ] All generated files committed
- [ ] No output files in .gitignore

**Verification:**
```bash
git status output/
git ls-files output/ | wc -l
```

**Dependencies:**
- E4_02, E4_03

---

## Task Dependencies Graph

```
E1_01 ─> E1_02 ─> E1_03
                    ↓
E2_01 ─> E2_02 ──────┼──> E4_01 ─> E4_02 ─> E4_04
                    │              ↓
E3_01 ─> E3_02 ─────────────────────┘
                              ↓
                         E4_03 ──> E4_04
```

## Critical Path

1. E1_01 (Color Scheme)
2. E1_02 (Film Config)
3. E2_01 (File Prefixes)
4. E2_02 (File Generation)
5. E4_02 (Generate Output)
6. E4_04 (Git Commit)

## Parallel Work Opportunities

- E1_* (Festive Support) and E2_* (File Naming) can start in parallel
- E3_* (Introduction) is independent and can be done anytime
- E4_01 (Clean Old Files) can be done after E2_* completes

## Quality Checklist

Before considering this feature complete:

- [ ] All tasks marked as complete
- [ ] All existing tests passing (`podman-compose run --rm dev pytest`)
- [ ] Linting clean (`podman-compose run --rm dev ruff check .`)
- [ ] Festive output generates correctly for both games
- [ ] File naming consistent across all output
- [ ] Introduction document complete
- [ ] All output files committed to git

## Notes

### Implementation Tips

- Check existing vintage_christmas_films implementation as reference
- Use existing Playwright PDF generation patterns
- Keep file naming changes minimal and consistent

### Common Pitfalls

- Forgetting to update both games when changing file naming
- Missing font loading issues in Playwright PDF generation
- Not waiting for Google Fonts to load before PDF conversion

### Resources

- `src/bingo/html_pdf.py` - Reference implementation for vintage films
- `output/Introduction_VintageChristmasFilms.md` - Reference introduction format
- `planning/meet-me-st-louis-festive-output/` - BMAD planning documents
