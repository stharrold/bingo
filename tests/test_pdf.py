"""Tests for bingo.pdf module."""

import os
import tempfile

import pytest

from bingo.card import generate_valid_card
from bingo.data import get_game_data
from bingo.pdf import create_card_pdf, create_key_pdf, generate_cards


@pytest.fixture
def items():
    """Get bingo items for testing."""
    return get_game_data("meet_me_in_st_louis")


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_create_key_pdf(items, temp_dir):
    """Test creating a bingo key PDF."""
    filename = os.path.join(temp_dir, "test_key.pdf")
    create_key_pdf(items, filename)

    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0


def test_create_card_pdf(items, temp_dir):
    """Test creating a bingo card PDF."""
    card = generate_valid_card(win_at=20, total_items=len(items))
    filename = os.path.join(temp_dir, "test_card.pdf")
    create_card_pdf(card, items, filename)

    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0


def test_generate_cards(items, temp_dir):
    """Test generating multiple bingo cards."""
    filenames = generate_cards(
        items,
        num_cards=3,
        output_dir=temp_dir,
        prefix="TestCard",
    )

    assert len(filenames) == 3
    for filename in filenames:
        assert os.path.exists(filename)
        assert os.path.getsize(filename) > 0


def test_generate_cards_creates_directory(items, temp_dir):
    """Test that generate_cards creates output directory if needed."""
    output_dir = os.path.join(temp_dir, "nested", "output")
    filenames = generate_cards(
        items,
        num_cards=1,
        output_dir=output_dir,
    )

    assert os.path.isdir(output_dir)
    assert len(filenames) == 1


# Tests for Vintage Christmas Films PDF generation


@pytest.fixture
def vintage_items():
    """Get vintage Christmas films items for testing."""
    return get_game_data("vintage_christmas_films")


def test_create_key_pdf_vintage(vintage_items, temp_dir):
    """Test creating a vintage Christmas films key PDF."""
    filename = os.path.join(temp_dir, "test_vintage_key.pdf")
    create_key_pdf(vintage_items, filename, game="vintage_christmas_films")

    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0


def test_create_card_pdf_vintage(vintage_items, temp_dir):
    """Test creating a vintage Christmas films card PDF."""
    card = generate_valid_card(win_at=20, total_items=len(vintage_items))
    filename = os.path.join(temp_dir, "test_vintage_card.pdf")
    create_card_pdf(card, vintage_items, filename, game="vintage_christmas_films")

    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0


def test_generate_cards_vintage(vintage_items, temp_dir):
    """Test generating multiple vintage Christmas films cards."""
    filenames = generate_cards(
        vintage_items,
        num_cards=3,
        output_dir=temp_dir,
        prefix="VintageCard",
        game="vintage_christmas_films",
    )

    assert len(filenames) == 3
    for filename in filenames:
        assert os.path.exists(filename)
        assert os.path.getsize(filename) > 0
