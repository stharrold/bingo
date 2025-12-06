# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

**Bingo card generator for movie watching parties:**
- Generates PDF bingo cards with emoji icons
- Creates bingo keys showing all items
- Cards are designed to win at a specific moment in the movie
- Uses Noto Emoji font for cross-platform emoji rendering

## Essential Commands

```bash
# Build container (once)
podman-compose build

# Run any command (containerized - preferred)
podman-compose run --rm dev <command>

# Alternative: Run directly with uv (when podman unavailable)
uv run <command>

# Common operations
podman-compose run --rm dev pytest                    # Run tests
podman-compose run --rm dev pytest -v -k test_name    # Single test
podman-compose run --rm dev ruff check .              # Lint
podman-compose run --rm dev ruff check --fix .        # Auto-fix
podman-compose run --rm dev bingo key                 # Generate key PDF
podman-compose run --rm dev bingo cards -n 20         # Generate 20 cards

# Or without container:
uv sync
uv run pytest
uv run bingo key
```

## Project Structure

```
bingo/
├── src/bingo/
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   ├── data.py         # Bingo items data (Meet Me In St. Louis)
│   ├── card.py         # Card generation logic
│   └── pdf.py          # PDF generation with Noto font
├── tests/
│   ├── test_data.py    # Data module tests
│   ├── test_card.py    # Card generation tests
│   └── test_pdf.py     # PDF generation tests
├── fonts/
│   └── NotoEmoji-VariableFont.ttf  # Bundled emoji font
├── output/             # Generated PDFs (gitignored)
├── .claude/            # Claude Code skills and commands
│   ├── commands/       # Slash commands (/workflow/*, /1_specify, etc.)
│   └── skills/         # 9 specialized skills
├── .agents/            # Cross-tool AI config (mirrors .claude/)
├── docs/reference/     # Workflow documentation
├── Containerfile       # Podman container definition
├── podman-compose.yml  # Container orchestration
├── WORKFLOW.md         # Workflow overview
└── pyproject.toml      # Project configuration
```

## CLI Usage

```bash
# Generate bingo key (all items listed)
bingo key [-o OUTPUT_FILE]

# Generate bingo cards
bingo cards [-n NUM_CARDS] [-o OUTPUT_DIR] [-w WIN_AT]
```

## Adding New Games

To add a new movie/game:

1. Edit `src/bingo/data.py`:
   - Create a new list of `BingoItem` objects
   - Add to `get_game_data()` function

2. Each item needs:
   - `order`: Sequential number (1-30)
   - `emoji`: Unicode emoji string (e.g., "\U0001F3B5\U0001F3A1")
   - `description`: Quote or song title from the movie

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
