# Implementation Plan: Vintage Christmas Films

**Type:** feature
**Slug:** vintage-christmas-films
**Date:** 2025-12-06

## Task Breakdown

### Phase 1: Data Implementation

#### Task impl_001: Add Vintage Christmas Films Game Data

**Priority:** High

**Files:**
- `src/bingo/data.py`
- `tests/test_data.py`

**Description:**
Define 30 BingoItem objects for vintage Christmas films covering 4 silent films from 1898-1908.

**Steps:**
1. Add VINTAGE_CHRISTMAS_FILMS list with 30 BingoItem objects
2. Each item has: order (1-30), emoji pair, description
3. Organize by film (Santa Claus, Winter Straw Ride, Night Before Christmas, Christmas Burglars)
4. Update get_game_data() to include new game
5. Write unit tests for the new game data

**Acceptance Criteria:**
- [ ] 30 BingoItem objects defined
- [ ] All emoji pairs are unique
- [ ] Items numbered 1-30 sequentially
- [ ] get_game_data("vintage_christmas_films") returns the list
- [ ] Tests pass

**Verification:**
```bash
uv run python -c "from bingo.data import get_game_data; print(len(get_game_data('vintage_christmas_films')))"
uv run pytest tests/test_data.py -v
```

**Dependencies:**
- None

---

### Phase 2: CLI Updates

#### Task impl_002: Add Game Selection to CLI

**Priority:** High

**Files:**
- `src/bingo/cli.py`
- `tests/test_cli.py` (if exists)

**Description:**
Add `--game` option to both `key` and `cards` subcommands to select which movie's bingo items to use.

**Steps:**
1. Add `--game` option with choices to `key` command
2. Add `--game` option with choices to `cards` command
3. Pass game selection to data retrieval
4. Update help text

**Acceptance Criteria:**
- [ ] `bingo key --game vintage_christmas_films` works
- [ ] `bingo cards --game vintage_christmas_films -n 1` works
- [ ] Default game is still meet_me_in_st_louis

**Verification:**
```bash
uv run bingo key --help  # Should show --game option
uv run bingo cards --help  # Should show --game option
```

**Dependencies:**
- impl_001

---

### Phase 3: PDF Configuration

#### Task impl_003: Add Configurable PDF Title

**Priority:** High

**Files:**
- `src/bingo/pdf.py`

**Description:**
Configure PDF title based on selected game so that vintage Christmas films cards have the correct title.

**Steps:**
1. Add GAME_TITLES dictionary mapping game names to titles
2. Update generate_key_pdf to accept game parameter
3. Update generate_card_pdf to accept game parameter
4. Use appropriate title based on game

**Acceptance Criteria:**
- [ ] Vintage Christmas films PDFs have "VINTAGE CHRISTMAS FILMS BINGO" title
- [ ] Meet Me In St. Louis PDFs still have correct title
- [ ] Both key and card PDFs use correct titles

**Verification:**
```bash
uv run bingo key --game vintage_christmas_films -o output/vintage_key.pdf
# Visually verify PDF title
```

**Dependencies:**
- impl_001, impl_002

---

### Phase 4: Testing

#### Task test_001: Unit Tests for New Game Data

**Priority:** High

**Files:**
- `tests/test_data.py`

**Description:**
Add comprehensive unit tests for the vintage Christmas films game data.

**Steps:**
1. Test that exactly 30 items are returned
2. Test that all emoji pairs are unique
3. Test that orders are 1-30 sequentially
4. Test that unknown game raises ValueError

**Acceptance Criteria:**
- [ ] All tests pass
- [ ] Coverage for new code ≥ 80%

**Verification:**
```bash
uv run pytest tests/test_data.py -v --cov=bingo.data
```

**Dependencies:**
- impl_001

---

#### Task test_002: Integration Tests for PDF Generation

**Priority:** High

**Files:**
- `tests/test_pdf.py`

**Description:**
Test that PDF generation works correctly with the new game.

**Steps:**
1. Test key PDF generation with vintage_christmas_films
2. Test card PDF generation with vintage_christmas_films
3. Verify PDF files are created

**Acceptance Criteria:**
- [ ] Key PDF generates without errors
- [ ] Card PDFs generate without errors
- [ ] Tests pass

**Verification:**
```bash
uv run pytest tests/test_pdf.py -v
```

**Dependencies:**
- impl_001, impl_002, impl_003

---

### Phase 5: Quality Assurance

#### Task qa_001: Run Full Quality Gates

**Priority:** High

**Files:**
- All source files

**Description:**
Run all quality checks to ensure the feature meets standards.

**Steps:**
1. Run pytest with coverage
2. Run ruff linting
3. Verify all tests pass

**Acceptance Criteria:**
- [ ] All tests pass
- [ ] Coverage ≥ 80%
- [ ] No linting errors

**Verification:**
```bash
uv run pytest --cov=bingo --cov-report=term
uv run ruff check src/ tests/
```

**Dependencies:**
- test_001, test_002

---

## Task Dependencies Graph

```
impl_001 (Game Data)
    │
    ├──> impl_002 (CLI) ──> impl_003 (PDF Title)
    │                              │
    └──> test_001 ─────────────────┴──> test_002 ──> qa_001
```

## Critical Path

1. impl_001 - Define game data
2. impl_002 - Add CLI game selection
3. impl_003 - Configure PDF title
4. test_002 - Integration tests
5. qa_001 - Quality gates

## Quality Checklist

Before considering this feature complete:

- [ ] All tasks marked as complete
- [ ] Test coverage ≥ 80%
- [ ] All tests passing
- [ ] Linting clean (`uv run ruff check src/ tests/`)
- [ ] 30 unique BingoItem objects defined
- [ ] PDF generation works with `--game vintage_christmas_films`
- [ ] Key shows all 30 items organized by film
- [ ] Manual testing: generate 30 cards and verify

## Notes

### Emoji Pair Strategy

Each film has a consistent first emoji as identifier:
- Santa Claus (1898): 🎅 (U+1F385)
- A Winter Straw Ride (1906): 🎿 (U+1F3BF)
- The Night Before Christmas (1905): 🎄 (U+1F384)
- The Christmas Burglars (1908): 🏠 (U+1F3E0)

### Film Distribution

| Film | Events | Orders |
|------|--------|--------|
| Santa Claus (1898) | 8 | 1-8 |
| A Winter Straw Ride (1906) | 7 | 9-15 |
| The Night Before Christmas (1905) | 8 | 16-23 |
| The Christmas Burglars (1908) | 7 | 24-30 |

### References

- Existing implementation: `src/bingo/data.py`
- Specification: `specs/vintage-christmas-films/spec.md`
- BMAD planning: `planning/vintage-christmas-films/`
