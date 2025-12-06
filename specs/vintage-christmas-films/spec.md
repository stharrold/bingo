# Specification: Vintage Christmas Films

**Type:** feature
**Slug:** vintage-christmas-films
**Date:** 2025-12-06
**Author:** stharrold

## Overview

Add a new bingo game for vintage Christmas films covering 4 silent films from 1898-1908: Santa Claus (1898), A Winter Straw Ride (1906), The Night Before Christmas (1905), and The Christmas Burglars (1908). The feature will generate 30 unique printable bingo cards with emoji pairs representing 30 distinct movie events, plus a cheat sheet explaining each emoji pair.

## Implementation Context

**BMAD Planning:** See `planning/vintage-christmas-films/` for complete requirements and architecture.

**Implementation Approach:**
- Extend existing bingo architecture (no new frameworks)
- Add new game data to `src/bingo/data.py`
- Update CLI to support game selection
- Reuse existing PDF generation with configurable title

## Requirements Reference

See: `planning/vintage-christmas-films/requirements.md`

### Functional Requirements Summary

1. **FR-001:** Define 30 bingo events as BingoItem objects covering 4 films
2. **FR-002:** Generate 30 unique cards, each selecting 25 random events from 30
3. **FR-003:** Create 5x5 grid layout without FREE space
4. **FR-004:** Generate PDF with "VINTAGE CHRISTMAS FILMS BINGO" title
5. **FR-005:** Include cheat sheet as final page organized by film

## Detailed Specification

### Component 1: Game Data Module

**File:** `src/bingo/data.py`

**Purpose:** Define the 30 BingoItem objects for vintage Christmas films

**Implementation:**

```python
# Vintage Christmas Films (1898-1908) bingo items
# Films: Santa Claus (1898), A Winter Straw Ride (1906),
#        The Night Before Christmas (1905), The Christmas Burglars (1908)

VINTAGE_CHRISTMAS_FILMS = [
    # Santa Claus (1898) - 8 events
    BingoItem(1, "\U0001F385\U0001F3A5", "Santa Claus (1898) - Film begins"),
    BingoItem(2, "\U0001F385\U0001F6CF", "Children sleeping in bed"),
    BingoItem(3, "\U0001F385\U0001F319", "Santa appears magically"),
    BingoItem(4, "\U0001F385\U0001F381", "Santa fills stockings"),
    BingoItem(5, "\U0001F385\U0001F3E0", "Rooftop scene"),
    BingoItem(6, "\U0001F385\U0001F4A8", "Santa vanishes"),
    BingoItem(7, "\U0001F385\U0001F476", "Children wake up"),
    BingoItem(8, "\U0001F385\U0001F389", "Children discover presents"),

    # A Winter Straw Ride (1906) - 7 events
    BingoItem(9, "\U0001F3BF\U0001F6F7", "Sleigh ride begins"),
    BingoItem(10, "\U0001F3BF\U0001F3D4", "Winter landscape"),
    BingoItem(11, "\U0001F3BF\U0001F40E", "Horse-drawn sleigh"),
    BingoItem(12, "\U0001F3BF\U00002744", "Snowfall scene"),
    BingoItem(13, "\U0001F3BF\U0001F46B", "Couples riding together"),
    BingoItem(14, "\U0001F3BF\U0001F3A4", "Singing/merriment"),
    BingoItem(15, "\U0001F3BF\U0001F3E1", "Arrival at destination"),

    # The Night Before Christmas (1905) - 8 events
    BingoItem(16, "\U0001F384\U0001F319", "Night scene"),
    BingoItem(17, "\U0001F384\U0001F476", "Children hanging stockings"),
    BingoItem(18, "\U0001F384\U0001F6CF", "Children go to bed"),
    BingoItem(19, "\U0001F384\U0001F385", "Santa comes down chimney"),
    BingoItem(20, "\U0001F384\U0001F381", "Santa arranges gifts"),
    BingoItem(21, "\U0001F384\U0001F36A", "Santa eats cookies"),
    BingoItem(22, "\U0001F384\U0001F4A8", "Santa departs"),
    BingoItem(23, "\U0001F384\U0001F389", "Morning excitement"),

    # The Christmas Burglars (1908) - 7 events
    BingoItem(24, "\U0001F3E0\U0001F5DD", "House exterior"),
    BingoItem(25, "\U0001F3E0\U0001F977", "Burglars appear"),
    BingoItem(26, "\U0001F3E0\U0001F440", "Burglars sneak in"),
    BingoItem(27, "\U0001F3E0\U0001F476", "Child discovers burglars"),
    BingoItem(28, "\U0001F3E0\U0001F6A8", "Alarm raised"),
    BingoItem(29, "\U0001F3E0\U0001F46E", "Burglars caught"),
    BingoItem(30, "\U0001F3E0\U0001F384", "Happy Christmas ending"),
]
```

**Dependencies:**
- Existing `BingoItem` dataclass

### Component 2: CLI Game Selection

**File:** `src/bingo/cli.py`

**Purpose:** Add `--game` option to select which movie's bingo to generate

**Implementation:**

```python
@click.option(
    "--game", "-g",
    type=click.Choice(["meet_me_in_st_louis", "vintage_christmas_films"]),
    default="meet_me_in_st_louis",
    help="Which movie's bingo items to use"
)
```

### Component 3: PDF Title Configuration

**File:** `src/bingo/pdf.py`

**Purpose:** Allow configurable title based on selected game

**Implementation:**

```python
GAME_TITLES = {
    "meet_me_in_st_louis": "MEET ME IN ST. LOUIS BINGO",
    "vintage_christmas_films": "VINTAGE CHRISTMAS FILMS BINGO",
}
```

## Data Models

### BingoItem (existing)

```python
@dataclass
class BingoItem:
    """A single bingo item with order, emoji, and description."""
    order: int
    emoji: str
    description: str
```

No database required - this is a CLI tool with no persistence.

## CLI Interface

### Generate Bingo Key

```bash
bingo key [-o OUTPUT_FILE] [--game vintage_christmas_films]
```

### Generate Bingo Cards

```bash
bingo cards [-n NUM_CARDS] [-o OUTPUT_DIR] [-w WIN_AT] [--game vintage_christmas_films]
```

## Testing Requirements

### Unit Tests

**File:** `tests/test_data.py`

```python
def test_vintage_christmas_films_count():
    """Test that vintage Christmas films has exactly 30 items."""
    items = get_game_data("vintage_christmas_films")
    assert len(items) == 30

def test_vintage_christmas_films_unique_emojis():
    """Test that all emoji pairs are unique."""
    items = get_game_data("vintage_christmas_films")
    emojis = [item.emoji for item in items]
    assert len(emojis) == len(set(emojis))

def test_vintage_christmas_films_order():
    """Test that items are numbered 1-30 sequentially."""
    items = get_game_data("vintage_christmas_films")
    orders = [item.order for item in items]
    assert orders == list(range(1, 31))
```

### Integration Tests

**File:** `tests/test_pdf.py`

```python
def test_generate_vintage_christmas_cards():
    """Test that vintage Christmas cards generate successfully."""
    items = get_game_data("vintage_christmas_films")
    # Generate 1 card for testing
    cards = generate_cards(items, count=1, win_at=25)
    assert len(cards) == 1
    assert len(cards[0]) == 25
```

## Quality Gates

- [ ] Test coverage ≥ 80%
- [ ] All tests passing
- [ ] Linting clean (ruff check)
- [ ] 30 unique BingoItem objects defined
- [ ] PDF generation works with new game
- [ ] Cheat sheet groups items by film

## Implementation Notes

### Key Considerations

- Emoji pairs should be visually distinct and recognizable
- Each film should have a consistent first emoji as identifier:
  - Santa Claus (1898): 🎅 (Santa)
  - A Winter Straw Ride (1906): 🎿 (Skiing/Winter)
  - The Night Before Christmas (1905): 🎄 (Christmas tree)
  - The Christmas Burglars (1908): 🏠 (House)
- Descriptions should be brief but descriptive

### Error Handling

- Unknown game name should raise ValueError with available options
- Invalid emoji characters should fail validation during tests

### Film Research Notes

These are real silent films from the early cinema era:
- **Santa Claus (1898)** - George Albert Smith, UK, 1 minute
- **A Winter Straw Ride (1906)** - American Mutoscope & Biograph
- **The Night Before Christmas (1905)** - Edwin S. Porter
- **The Christmas Burglars (1908)** - D.W. Griffith

## References

- Existing implementation: `src/bingo/data.py` (Meet Me In St. Louis)
- BMAD planning: `planning/vintage-christmas-films/`
