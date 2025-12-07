# Epics: Meet Me In St. Louis Festive Output

**Issue**: #7
**Slug**: meet-me-st-louis-festive-output

## Epic 1: Festive Card Support

**Goal**: Enable festive HTML+PDF generation for Meet Me In St. Louis

### Tasks:
1. Add color scheme to `FESTIVE_COLORS` in html_pdf.py
2. Add film configuration to `create_festive_html()` for single-film games
3. Add subtitle to subtitles dict
4. Test festive generation with `bingo festive -g meet_me_in_st_louis`

---

## Epic 2: File Naming Convention

**Goal**: Update all output file naming to use hyphenated slugs

### Tasks:
1. Update `GAME_FILE_PREFIXES` in cli.py to use hyphenated names
2. Update file generation logic for new naming pattern
3. Ensure numbered cards follow `<slug>_card_NN.pdf` format
4. Update festive output naming

---

## Epic 3: Introduction Document

**Goal**: Create informative introduction for Meet Me In St. Louis

### Tasks:
1. Research and write introduction markdown content:
   - Movie overview (1944 MGM musical)
   - Cast highlights (Judy Garland, Margaret O'Brien)
   - Production context (Technicolor, Arthur Freed Unit)
   - 1904 St. Louis World's Fair setting
   - Musical numbers overview
   - Seasonal/holiday themes
2. Generate PDF from markdown using Playwright
3. Add to output directory

---

## Epic 4: Output Generation & Git Tracking

**Goal**: Generate all outputs and commit to repository

### Tasks:
1. Remove old naming convention files (if present)
2. Generate Meet Me In St. Louis festive HTML+PDF (30 cards)
3. Generate standard cards with new naming
4. Generate key PDF with new naming
5. Add introduction files to output
6. Update Vintage Christmas Films output to new naming (for consistency)
7. Commit all output files to git

---

## Dependencies

- Epic 2 (naming) should be completed before Epic 4 (output generation)
- Epic 1 (festive support) should be completed before generating festive output in Epic 4
- Epic 3 (introduction) is independent and can be done in parallel

## Estimated Scope

- Code changes: ~50-100 lines modified
- Content creation: ~200-400 lines markdown (introduction)
- Output files: ~35 files per game
