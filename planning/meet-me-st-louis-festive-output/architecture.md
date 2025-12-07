# Architecture: Meet Me In St. Louis Festive Output

**Issue**: #7
**Slug**: meet-me-st-louis-festive-output

## Overview

This feature extends the existing festive card generation system to support Meet Me In St. Louis, updates file naming conventions, and adds introduction document generation.

## Current Architecture

```
src/bingo/
├── cli.py         # Entry points: key, cards, festive
├── html_pdf.py    # Festive HTML generation + Playwright PDF
├── pdf.py         # ReportLab PDF generation (standard cards)
├── card.py        # Card generation algorithm
└── data.py        # Game definitions (BingoItem lists)

output/            # Generated files (tracked in git)
```

## Changes Required

### 1. html_pdf.py Modifications

**Add to FESTIVE_COLORS:**
```python
"meet_me_in_st_louis": {
    "primary": "#8B0000",      # Dark red (Victorian theme)
    "secondary": "#FFD700",    # Gold
    "background": "#FFF8E7",   # Cream/antique
    "text": "#2F1810",         # Dark brown
}
```

**Add film sections in create_festive_html():**
- Meet Me In St. Louis spans items 1-30 (single film, not multiple)
- Update `films` list structure for single-film games
- Add subtitle to `subtitles` dict

### 2. cli.py Modifications

**File naming updates:**
- Add new naming mode option or update `GAME_FILE_PREFIXES`
- Current: `BingoCard_MeetMeInStLouis_01.pdf`
- New: `meet-me-in-st-louis_card_01.pdf`

**Options:**
- Option A: Add `--naming-style` flag (hyphenated vs camelcase)
- Option B: Update all games to use hyphenated naming (breaking change)
- Option C: Add parallel prefix entries (maintain compatibility)

**Recommended: Option B** - Update to hyphenated naming for consistency.

### 3. Introduction Generation

**New functionality:**
- Create `Introduction_MeetMeInStLouis.md` manually (content)
- Use Playwright to convert to PDF (similar to festive card generation)
- Could extend cli.py with `bingo intro` command (optional)

### 4. Output File Structure

**Current naming:**
```
BingoCard_MeetMeInStLouis_01.pdf
BingoKey_MeetMeInStLouis.pdf
```

**New naming:**
```
meet-me-in-st-louis_card_01.pdf
meet-me-in-st-louis_key.pdf
meet-me-in-st-louis_cards-festive.html
meet-me-in-st-louis_cards-festive.pdf
meet-me-in-st-louis_introduction.md
meet-me-in-st-louis_introduction.pdf
```

## Implementation Approach

### Phase 1: Code Updates
1. Update `FESTIVE_COLORS` in html_pdf.py
2. Update film sections for Meet Me In St. Louis
3. Update file naming in cli.py

### Phase 2: Content Creation
4. Write introduction markdown content
5. Generate introduction PDF

### Phase 3: Output Generation
6. Generate festive HTML+PDF cards
7. Generate standard cards with new naming
8. Generate key PDF
9. Commit all output to git

## Dependencies

- Playwright (PDF generation from HTML)
- ReportLab (standard PDF generation)
- Google Fonts: Mountains of Christmas (festive template)

## Testing

- Existing tests should continue to pass
- Verify festive output generates correctly
- Verify file naming matches new convention
- Manual verification of PDF visual output
