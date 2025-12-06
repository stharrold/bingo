"""Tests for bingo.data module."""

import pytest

from bingo.data import (
    MEET_ME_IN_ST_LOUIS,
    VINTAGE_CHRISTMAS_FILMS,
    BingoItem,
    get_game_data,
)


def test_bingo_item_dataclass():
    """Test BingoItem dataclass creation."""
    item = BingoItem(order=1, emoji="🎵", description="Test song")
    assert item.order == 1
    assert item.emoji == "🎵"
    assert item.description == "Test song"


def test_meet_me_in_st_louis_has_30_items():
    """Test that Meet Me In St. Louis has exactly 30 items."""
    assert len(MEET_ME_IN_ST_LOUIS) == 30


def test_meet_me_in_st_louis_items_ordered():
    """Test that items are ordered 1-30."""
    for i, item in enumerate(MEET_ME_IN_ST_LOUIS, start=1):
        assert item.order == i


def test_meet_me_in_st_louis_items_have_emoji():
    """Test that all items have non-empty emoji."""
    for item in MEET_ME_IN_ST_LOUIS:
        assert item.emoji, f"Item {item.order} has no emoji"


def test_meet_me_in_st_louis_items_have_description():
    """Test that all items have non-empty description."""
    for item in MEET_ME_IN_ST_LOUIS:
        assert item.description, f"Item {item.order} has no description"


def test_get_game_data_valid():
    """Test get_game_data with valid game name."""
    items = get_game_data("meet_me_in_st_louis")
    assert len(items) == 30
    assert items[0].order == 1


def test_get_game_data_invalid():
    """Test get_game_data with invalid game name."""
    with pytest.raises(ValueError, match="Unknown game"):
        get_game_data("invalid_game")


# Tests for Vintage Christmas Films

def test_vintage_christmas_films_has_30_items():
    """Test that vintage Christmas films has exactly 30 items."""
    assert len(VINTAGE_CHRISTMAS_FILMS) == 30


def test_vintage_christmas_films_items_ordered():
    """Test that items are ordered 1-30."""
    for i, item in enumerate(VINTAGE_CHRISTMAS_FILMS, start=1):
        assert item.order == i


def test_vintage_christmas_films_items_have_emoji():
    """Test that all items have non-empty emoji."""
    for item in VINTAGE_CHRISTMAS_FILMS:
        assert item.emoji, f"Item {item.order} has no emoji"


def test_vintage_christmas_films_items_have_description():
    """Test that all items have non-empty description."""
    for item in VINTAGE_CHRISTMAS_FILMS:
        assert item.description, f"Item {item.order} has no description"


def test_vintage_christmas_films_unique_emojis():
    """Test that all emoji pairs are unique."""
    emojis = [item.emoji for item in VINTAGE_CHRISTMAS_FILMS]
    assert len(emojis) == len(set(emojis)), "Emoji pairs must be unique"


def test_get_game_data_vintage_christmas_films():
    """Test get_game_data with vintage_christmas_films."""
    items = get_game_data("vintage_christmas_films")
    assert len(items) == 30
    assert items[0].order == 1
    assert items[0].description == "Santa Claus (1898) - Film begins"
