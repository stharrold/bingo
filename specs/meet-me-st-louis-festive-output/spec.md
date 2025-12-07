# Specification: Meet Me In St. Louis Festive Output

**Type:** feature
**Slug:** meet-me-st-louis-festive-output
**Date:** 2025-12-07
**Author:** stharrold

## Overview

This feature extends the existing festive card generation system to support "Meet Me In St. Louis" (1944), updates file naming conventions to use hyphenated slugs, and adds introduction document generation. The goal is to make Meet Me In St. Louis bingo cards match the visual style and output format of the Vintage Christmas Films cards.

## Implementation Context

**BMAD Planning:** See `planning/meet-me-st-louis-festive-output/` for complete requirements and architecture.

**Implementation Preferences:**
- **Task Granularity:** Small tasks (1-2 hours each)
- **Follow Epic Order:** True

## Requirements Reference

See: `planning/meet-me-st-louis-festive-output/requirements.md`

Key user stories:
- US-1: Festive Output Format - Match Vintage Christmas Films visual style
- US-2: Consistent File Naming - Hyphenated slug naming convention
- US-3: Introduction Document - Movie context for guests
- US-4: Git-Tracked Output - All files committed to repository

## Detailed Specification

### Component 1: html_pdf.py Modifications

**File:** `src/bingo/html_pdf.py`

**Purpose:** Add color scheme and film configuration for Meet Me In St. Louis festive cards

**Changes Required:**

1. Add to `FESTIVE_COLORS` dict:
```python
"meet_me_in_st_louis": {
    "primary": "#8B0000",      # Dark red (Victorian theme)
    "secondary": "#FFD700",    # Gold
    "background": "#FFF8E7",   # Cream/antique
    "text": "#2F1810",         # Dark brown
}
```

2. Update `create_festive_html()` for single-film games:
- Add film section spanning items 1-30
- Add subtitle entry for "meet_me_in_st_louis"

### Component 2: cli.py Modifications

**File:** `src/bingo/cli.py`

**Purpose:** Update file naming to use hyphenated slugs

**Changes Required:**

1. Update `GAME_FILE_PREFIXES` to use hyphenated names:
```python
GAME_FILE_PREFIXES = {
    "meet_me_in_st_louis": "meet-me-in-st-louis",
    "vintage_christmas_films": "vintage-christmas-films",
}
```

2. Update file generation patterns:
- Cards: `<slug>_card_NN.pdf`
- Key: `<slug>_key.pdf`
- Festive HTML: `<slug>_cards-festive.html`
- Festive PDF: `<slug>_cards-festive.pdf`

### Component 3: Introduction Document

**File:** `output/meet-me-in-st-louis_introduction.md` (new)

**Purpose:** Provide movie context for party guests

**Content Sections:**
- Movie overview (1944 MGM musical)
- Cast highlights (Judy Garland, Margaret O'Brien)
- Production context (Technicolor, Arthur Freed Unit)
- 1904 St. Louis World's Fair setting
- Musical numbers overview
- Seasonal/holiday themes relevant to bingo items

**PDF Generation:** Use Playwright to convert markdown to PDF (similar to festive card generation)

## Data Models

No database changes required. This feature uses existing `BingoItem` data structures.

## Testing Requirements

### Unit Tests

Existing tests should continue to pass. No new unit tests required as this primarily modifies output generation.

### Integration Tests

**Manual verification:**
1. Generate festive HTML+PDF for Meet Me In St. Louis
2. Verify color scheme renders correctly
3. Verify file naming matches new convention
4. Verify introduction PDF generates correctly

### Verification Commands

```bash
# Run all tests
podman-compose run --rm dev pytest

# Lint check
podman-compose run --rm dev ruff check .

# Generate festive output
podman-compose run --rm dev bingo festive -g meet_me_in_st_louis -n 30 --pdf

# Generate standard cards
podman-compose run --rm dev bingo cards -g meet_me_in_st_louis -n 30

# Generate key
podman-compose run --rm dev bingo key -g meet_me_in_st_louis
```

## Quality Gates

- [ ] All existing tests passing
- [ ] Linting clean (ruff check)
- [ ] Festive output generates correctly
- [ ] File naming matches new convention
- [ ] Introduction document generated

## Output Files

Expected output structure after implementation:

```
output/
├── meet-me-in-st-louis_cards-festive.html
├── meet-me-in-st-louis_cards-festive.pdf
├── meet-me-in-st-louis_card_01.pdf
├── meet-me-in-st-louis_card_02.pdf
├── ... (30 cards total)
├── meet-me-in-st-louis_key.pdf
├── meet-me-in-st-louis_introduction.md
└── meet-me-in-st-louis_introduction.pdf
```

## Dependencies

No new dependencies required. Uses existing:
- Playwright (PDF generation from HTML)
- ReportLab (standard PDF generation)
- Google Fonts: Mountains of Christmas (festive template)

## Implementation Notes

### Key Considerations

- Maintain backward compatibility with existing CLI commands
- Follow existing code patterns in html_pdf.py
- Introduction should be informative but concise (similar length to vintage films intro)
- Meet Me In St. Louis spans items 1-30 (single film, not multiple like vintage films)

### Color Scheme Rationale

- Dark red (#8B0000): Victorian-era theme, holiday appropriate
- Gold (#FFD700): Elegant accent, 1904 World's Fair opulence
- Cream (#FFF8E7): Antique/vintage feel
- Dark brown (#2F1810): Readable text on light background

## References

- `planning/meet-me-st-louis-festive-output/requirements.md`
- `planning/meet-me-st-louis-festive-output/architecture.md`
- `planning/meet-me-st-louis-festive-output/epics.md`
- Existing implementation in `src/bingo/html_pdf.py` for vintage_christmas_films
