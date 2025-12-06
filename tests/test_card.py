"""Tests for bingo.card module."""


from bingo.card import (
    BingoCard,
    check_bingo,
    generate_card,
    generate_valid_card,
    simulate_game,
)
from bingo.data import MEET_ME_IN_ST_LOUIS


def test_bingo_card_grid_size():
    """Test that generated card has 5x5 grid."""
    card = generate_card()
    assert len(card.grid) == 5
    for row in card.grid:
        assert len(row) == 5


def test_bingo_card_contains_25_unique_values():
    """Test that card contains 25 unique values."""
    card = generate_card()
    values = [card.grid[i][j] for i in range(5) for j in range(5)]
    assert len(set(values)) == 25


def test_bingo_card_values_in_range():
    """Test that all values are in range 1-30."""
    card = generate_card()
    for i in range(5):
        for j in range(5):
            assert 1 <= card.grid[i][j] <= 30


def test_bingo_card_contains_win_at():
    """Test that card contains the win_at value."""
    card = generate_card(win_at=20)
    values = [card.grid[i][j] for i in range(5) for j in range(5)]
    assert 20 in values


def test_check_bingo_row():
    """Test check_bingo detects complete row."""
    card = BingoCard(grid=[
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ])
    # First row complete
    assert check_bingo(card, {1, 2, 3, 4, 5})
    # First row incomplete
    assert not check_bingo(card, {1, 2, 3, 4})


def test_check_bingo_column():
    """Test check_bingo detects complete column."""
    card = BingoCard(grid=[
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ])
    # First column complete
    assert check_bingo(card, {1, 6, 11, 16, 21})


def test_check_bingo_main_diagonal():
    """Test check_bingo detects complete main diagonal."""
    card = BingoCard(grid=[
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ])
    # Main diagonal complete
    assert check_bingo(card, {1, 7, 13, 19, 25})


def test_check_bingo_anti_diagonal():
    """Test check_bingo detects complete anti-diagonal."""
    card = BingoCard(grid=[
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ])
    # Anti-diagonal complete
    assert check_bingo(card, {5, 9, 13, 17, 21})


def test_simulate_game():
    """Test simulate_game returns winning number."""
    card = BingoCard(grid=[
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ])
    # Should win when 5 is called (completes first row)
    assert simulate_game(card, total_items=30) == 5


def test_generate_valid_card_wins_at_20():
    """Test that generate_valid_card creates card that wins at specified number."""
    card = generate_valid_card(win_at=20, total_items=30)
    assert simulate_game(card, total_items=30) == 20


def test_generate_valid_card_multiple():
    """Test generating multiple valid cards."""
    for _ in range(5):
        card = generate_valid_card(win_at=20, total_items=30)
        assert simulate_game(card, total_items=30) == 20


def test_bingo_card_get_emoji_grid():
    """Test emoji grid conversion."""
    card = BingoCard(grid=[
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ])
    emoji_grid = card.get_emoji_grid(MEET_ME_IN_ST_LOUIS)

    # Check dimensions
    assert len(emoji_grid) == 5
    for row in emoji_grid:
        assert len(row) == 5

    # Check first item maps correctly
    assert emoji_grid[0][0] == MEET_ME_IN_ST_LOUIS[0].emoji
