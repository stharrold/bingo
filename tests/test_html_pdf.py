"""Tests for bingo.html_pdf module."""

import os
import tempfile

import pytest

from bingo.card import generate_valid_card
from bingo.data import get_game_data
from bingo.html_pdf import (
    FESTIVE_COLORS,
    create_festive_html,
    generate_festive_cards,
    generate_snowflakes,
)


@pytest.fixture
def items():
    """Get bingo items for testing."""
    return get_game_data("meet_me_in_st_louis")


@pytest.fixture
def vintage_items():
    """Get vintage Christmas films items for testing."""
    return get_game_data("vintage_christmas_films")


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_festive_colors_defined():
    """Test that festive colors are defined for all games."""
    assert "vintage_christmas_films" in FESTIVE_COLORS
    assert "meet_me_in_st_louis" in FESTIVE_COLORS
    # Check required color keys
    for _game, colors in FESTIVE_COLORS.items():
        assert "primary" in colors
        assert "secondary" in colors
        assert "bg" in colors
        assert "text" in colors


def test_generate_snowflakes():
    """Test snowflake generation."""
    snowflakes = generate_snowflakes(10)
    assert isinstance(snowflakes, str)
    assert "snowflake" in snowflakes
    # Should contain multiple snowflakes
    assert snowflakes.count("snowflake") >= 10


def test_generate_snowflakes_default_count():
    """Test snowflake generation with default count."""
    snowflakes = generate_snowflakes()
    assert snowflakes.count("snowflake") >= 15


def test_create_festive_html(items):
    """Test creating festive HTML content."""
    cards = [generate_valid_card(win_at=20, total_items=len(items)) for _ in range(3)]
    html = create_festive_html(items, cards, game="meet_me_in_st_louis")

    assert "<!DOCTYPE html>" in html
    assert "BINGO" in html
    assert "Meet Me In St. Louis" in html
    assert "bingo-grid" in html
    # Should have key page
    assert "BINGO KEY" in html


def test_create_festive_html_without_key(items):
    """Test creating festive HTML without key page."""
    cards = [generate_valid_card(win_at=20, total_items=len(items)) for _ in range(2)]
    html = create_festive_html(items, cards, game="meet_me_in_st_louis", include_key=False)

    assert "<!DOCTYPE html>" in html
    assert "BINGO" in html
    # Should NOT have key page
    assert "BINGO KEY" not in html


def test_create_festive_html_vintage(vintage_items):
    """Test creating festive HTML for vintage christmas films."""
    cards = [generate_valid_card(win_at=20, total_items=len(vintage_items)) for _ in range(2)]
    html = create_festive_html(vintage_items, cards, game="vintage_christmas_films")

    assert "Vintage Christmas Films" in html
    # Check for film sections in key
    assert "Santa Claus (1898)" in html
    assert "A Winter Straw Ride (1906)" in html


def test_create_festive_html_unknown_game(items):
    """Test creating festive HTML with unknown game uses default colors."""
    cards = [generate_valid_card(win_at=20, total_items=len(items)) for _ in range(1)]
    html = create_festive_html(items, cards, game="unknown_game")

    # Should still generate valid HTML with default styling
    assert "<!DOCTYPE html>" in html
    assert "BINGO" in html


def test_generate_festive_cards(items, temp_dir):
    """Test generating festive bingo cards file."""
    output_file = os.path.join(temp_dir, "test_festive.html")
    result = generate_festive_cards(
        items,
        num_cards=3,
        output_file=output_file,
        game="meet_me_in_st_louis",
    )

    assert os.path.exists(result)
    assert result == output_file
    with open(output_file) as f:
        content = f.read()
    assert "Meet Me In St. Louis" in content


def test_generate_festive_cards_vintage(vintage_items, temp_dir):
    """Test generating festive cards for vintage christmas films."""
    output_file = os.path.join(temp_dir, "test_vintage_festive.html")
    result = generate_festive_cards(
        vintage_items,
        num_cards=5,
        output_file=output_file,
        game="vintage_christmas_films",
        win_at=20,  # Use default win_at
    )

    assert os.path.exists(result)
    with open(output_file) as f:
        content = f.read()
    assert "Vintage Christmas Films" in content


def test_generate_festive_cards_no_key(items, temp_dir):
    """Test generating festive cards without key page."""
    output_file = os.path.join(temp_dir, "test_nokey.html")
    generate_festive_cards(
        items,
        num_cards=2,
        output_file=output_file,
        include_key=False,
    )

    with open(output_file) as f:
        content = f.read()
    assert "BINGO KEY" not in content


def test_create_festive_html_meet_me_sections(items):
    """Test that Meet Me In St. Louis has seasonal sections."""
    cards = [generate_valid_card(win_at=20, total_items=len(items)) for _ in range(1)]
    html = create_festive_html(items, cards, game="meet_me_in_st_louis")

    # Check for seasonal sections
    assert "Summer 1903" in html
    assert "Autumn 1903" in html
    assert "Winter 1903" in html
    assert "Spring 1904" in html


def test_festive_html_has_proper_structure(items):
    """Test that generated HTML has proper structure."""
    cards = [generate_valid_card(win_at=20, total_items=len(items)) for _ in range(2)]
    html = create_festive_html(items, cards, game="meet_me_in_st_louis")

    # Check for required HTML elements
    assert "<html" in html
    assert "</html>" in html
    assert "<head>" in html
    assert "</head>" in html
    assert "<body>" in html
    assert "</body>" in html
    assert "<style>" in html
    # Check for Google Fonts
    assert "Mountains of Christmas" in html
    # Check for card structure
    assert "card-page" in html
    assert "bingo-cell" in html
