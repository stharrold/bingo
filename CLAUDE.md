# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

**Bingo card generator for movie watching parties.** Generates PDF bingo cards with emoji icons that are designed to win at a specific moment in the movie (default: item 20 of 30).

## Essential Commands

```bash
# Build container (once)
podman-compose build

# Run any command (containerized - preferred)
podman-compose run --rm dev <command>

# Alternative: Run directly with uv (when podman unavailable)
uv run <command>

# Common operations
podman-compose run --rm dev pytest                    # Run all tests
podman-compose run --rm dev pytest -v -k test_name    # Single test
podman-compose run --rm dev ruff check .              # Lint
podman-compose run --rm dev ruff check --fix .        # Auto-fix lint
podman-compose run --rm dev bingo key                 # Generate key PDF
podman-compose run --rm dev bingo cards -n 20         # Generate 20 cards
podman-compose run --rm dev bingo festive -n 30 --pdf # Generate festive HTML+PDF
```

## Architecture

**Core modules in `src/bingo/`:**
- `data.py` - Game definitions as `BingoItem(order, emoji, description)` lists
- `card.py` - Card generation algorithm (see below)
- `pdf.py` - PDF rendering with ReportLab and bundled Noto Emoji font
- `html_pdf.py` - Festive HTML templates with Playwright PDF export
- `cli.py` - Entry point (`bingo key`, `bingo cards`, `bingo festive`)

**Card generation algorithm (`card.py`):**
1. Place `win_at` number in random cell
2. Find all intersecting cells (same row, column, diagonals)
3. Fill intersecting cells with values < `win_at` (ensures win line completes at `win_at`)
4. Fill remaining cells with other values
5. Validate via simulation; retry if needed

**Font handling (`pdf.py`):** Noto Emoji font bundled in `fonts/` - do not gitignore.

**Festive cards (`html_pdf.py`):** Google Fonts (Mountains of Christmas) loaded via HTML, converted to PDF with Playwright. Uses `document.fonts.ready` to ensure fonts load before PDF generation.

## Available Games

- `meet_me_in_st_louis` - Meet Me In St. Louis (1944) musical
- `vintage_christmas_films` - 4 silent films (1898-1909): Santa Claus, A Winter Straw Ride, The Night Before Christmas, A Trap for Santa Claus

## Adding New Games

To add a new movie/game:

1. Edit `src/bingo/data.py`:
   - Create a new list of `BingoItem` objects
   - Add to `get_game_data()` function
   - Add to `cli.py` GAME_CHOICES and GAME_FILE_PREFIXES

2. Each item needs:
   - `order`: Sequential number (1-30)
   - `emoji`: Unicode emoji string (e.g., "\U0001F3B5\U0001F3A1")
   - `description`: Quote or event from the movie

3. For festive cards, also update `html_pdf.py`:
   - Add color scheme to `FESTIVE_COLORS` dict
   - Add sections list in `create_festive_html()` for key organization
   - Update subtitle in `subtitles` dict

## Output Files

Output files are git-tracked in `output/` using hyphenated naming:
- `<slug>_card_NN.pdf` - Individual cards
- `<slug>_cards-festive.html/pdf` - Festive card collection
- `<slug>_key.pdf` - Answer key
- `<slug>_introduction.md/pdf` - Movie introduction (optional)

## Quality Gates

```bash
# All must pass before PR
podman-compose run --rm dev pytest              # Tests pass
podman-compose run --rm dev ruff check .        # Linting clean
```

## Slash Commands

Use these slash commands for guided workflow execution:

| Command | Phase | Purpose |
|---------|-------|---------|
| `/workflow/all` | All | Orchestrate full workflow with auto-detection |
| `/1_specify` | 1 | Create feature branch and specification |
| `/2_plan` | 2 | Generate design artifacts |
| `/3_tasks` | 3 | Generate ordered task list |
| `/4_implement` | 4 | Execute tasks automatically |
| `/5_integrate` | 5 | Create PRs (feature→contrib→develop) |
| `/6_release` | 6 | Create release (develop→main) |
| `/7_backmerge` | 7 | Sync release to develop and contrib |

## Skills System (9 skills in `.claude/skills/`)

| Skill | Purpose |
|-------|---------|
| workflow-orchestrator | Main coordinator, templates |
| git-workflow-manager | Worktrees, PRs, semantic versioning |
| quality-enforcer | Quality gates (coverage, tests, lint) |
| bmad-planner | Requirements + architecture |
| speckit-author | Specifications |
| tech-stack-adapter | Python/uv/Podman detection |
| workflow-utilities | Archive, directory structure |
| agentdb-state-manager | Workflow state tracking |
| initialize-repository | Bootstrap new repos |

## Branch Structure

```
main (production) ← develop (integration) ← contrib/<username> (active) ← feature/*
```

**PR Flow**: feature → contrib → develop → main

## Critical Guidelines

- **One way to run**: Prefer `podman-compose run --rm dev <command>`
- **End on editable branch**: All workflows must end on `contrib/*` (never `develop` or `main`)
- **ALWAYS prefer editing existing files** over creating new ones
- **NEVER proactively create documentation files** unless explicitly requested
- **Font bundled**: Noto Emoji font is in `fonts/` - don't gitignore it

## Reference Documentation

- `WORKFLOW.md` - Workflow overview
- `docs/reference/workflow-*.md` - Phase-specific workflow docs
