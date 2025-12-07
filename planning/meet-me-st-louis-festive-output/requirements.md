# Requirements: Meet Me In St. Louis Festive Output

**Issue**: #7
**Slug**: meet-me-st-louis-festive-output

## Overview

Redo the output for "Meet Me In St. Louis" to match the "Vintage Christmas Films" format, including:
1. Festive HTML+PDF output with color schemes
2. New file naming convention: `<movie-slug-with-hyphens>_<document-type>.<ext>`
3. Introduction document (like Vintage Christmas Films)
4. All output files tracked in git

## User Stories

### US-1: Festive Output Format
**As a** party host
**I want** Meet Me In St. Louis bingo cards in the festive HTML+PDF format
**So that** they match the visual style of the Vintage Christmas Films cards

**Acceptance Criteria:**
- [ ] Festive HTML template generates for Meet Me In St. Louis
- [ ] PDF export works via Playwright
- [ ] Color scheme is defined for the movie (seasonal/festive theme)
- [ ] Cards display correctly with emoji icons

### US-2: Consistent File Naming
**As a** user
**I want** all output files to use hyphenated slug naming
**So that** file names are consistent and easy to manage

**Acceptance Criteria:**
- [ ] Output files use format: `meet-me-in-st-louis_<type>.<ext>`
- [ ] Types include: `cards-festive`, `cards`, `key`, `introduction`
- [ ] Numbered cards follow pattern: `meet-me-in-st-louis_card_01.pdf`
- [ ] CLI options support new naming convention

### US-3: Introduction Document
**As a** party host
**I want** an introduction document for Meet Me In St. Louis
**So that** guests have context about the movie before playing bingo

**Acceptance Criteria:**
- [ ] Markdown introduction covering movie history, cast, production
- [ ] PDF version generated from markdown
- [ ] Similar structure to Vintage Christmas Films introduction
- [ ] Includes sections on: musical numbers, cast, 1904 World's Fair context, seasonal themes

### US-4: Git-Tracked Output
**As a** developer
**I want** all generated output files tracked in git
**So that** the repository includes ready-to-use bingo materials

**Acceptance Criteria:**
- [ ] output/ directory contains all generated files
- [ ] Files are committed to the repository
- [ ] .gitignore does NOT exclude output files

## Functional Requirements

### FR-1: Code Changes
- Update `html_pdf.py` with Meet Me In St. Louis color scheme in `FESTIVE_COLORS`
- Update `html_pdf.py` with film sections for `create_festive_html()`
- Update `cli.py` to support new file naming convention
- Optionally update `GAME_FILE_PREFIXES` to use hyphenated slugs

### FR-2: Content Creation
- Write Introduction_MeetMeInStLouis.md with movie context
- Generate PDF from introduction markdown

### FR-3: Output Generation
- Generate festive HTML+PDF for Meet Me In St. Louis (30 cards)
- Generate standard key PDF
- Rename existing output files to new naming convention

## Non-Functional Requirements

- Maintain backward compatibility with existing CLI commands
- Follow existing code patterns in html_pdf.py
- Introduction should be informative but concise (similar length to vintage films intro)
