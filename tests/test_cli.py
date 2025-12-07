"""Tests for bingo.cli module."""

import os
import sys
import tempfile
from unittest.mock import patch

import pytest

from bingo.cli import GAME_CHOICES, GAME_FILE_PREFIXES, main


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_game_choices_defined():
    """Test that game choices are properly defined."""
    assert len(GAME_CHOICES) >= 2
    assert "meet_me_in_st_louis" in GAME_CHOICES
    assert "vintage_christmas_films" in GAME_CHOICES


def test_game_file_prefixes_match_choices():
    """Test that file prefixes exist for all game choices."""
    for game in GAME_CHOICES:
        assert game in GAME_FILE_PREFIXES
        assert "-" in GAME_FILE_PREFIXES[game]  # Hyphenated format


def test_main_no_args_returns_1():
    """Test that main returns 1 when no command is provided."""
    with patch.object(sys, "argv", ["bingo"]):
        result = main()
    assert result == 1


def test_main_key_command(temp_dir):
    """Test the key command."""
    output_file = os.path.join(temp_dir, "test_key.pdf")
    with patch.object(sys, "argv", ["bingo", "key", "-o", output_file]):
        result = main()
    assert result == 0
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0


def test_main_key_command_vintage(temp_dir):
    """Test the key command with vintage christmas films."""
    output_file = os.path.join(temp_dir, "test_vintage_key.pdf")
    with patch.object(sys, "argv", ["bingo", "key", "-o", output_file, "-g", "vintage_christmas_films"]):
        result = main()
    assert result == 0
    assert os.path.exists(output_file)


def test_main_cards_command(temp_dir):
    """Test the cards command."""
    with patch.object(sys, "argv", ["bingo", "cards", "-n", "3", "-o", temp_dir]):
        result = main()
    assert result == 0
    # Check that cards were generated with hyphenated naming
    files = os.listdir(temp_dir)
    card_files = [f for f in files if f.startswith("meet-me-in-st-louis_card")]
    assert len(card_files) == 3


def test_main_cards_command_with_prefix(temp_dir):
    """Test the cards command with custom prefix."""
    with patch.object(sys, "argv", ["bingo", "cards", "-n", "2", "-o", temp_dir, "-p", "custom_card"]):
        result = main()
    assert result == 0
    files = os.listdir(temp_dir)
    card_files = [f for f in files if f.startswith("custom_card")]
    assert len(card_files) == 2


def test_main_cards_command_vintage(temp_dir):
    """Test the cards command with vintage christmas films."""
    with patch.object(sys, "argv", ["bingo", "cards", "-n", "2", "-o", temp_dir, "-g", "vintage_christmas_films"]):
        result = main()
    assert result == 0
    files = os.listdir(temp_dir)
    card_files = [f for f in files if f.startswith("vintage-christmas-films_card")]
    assert len(card_files) == 2


def test_main_festive_command(temp_dir):
    """Test the festive command (HTML only, no PDF)."""
    output_file = os.path.join(temp_dir, "test_festive.html")
    with patch.object(sys, "argv", ["bingo", "festive", "-n", "3", "-o", output_file]):
        result = main()
    assert result == 0
    assert os.path.exists(output_file)
    # Check HTML content
    with open(output_file) as f:
        content = f.read()
    assert "BINGO" in content
    assert "bingo-grid" in content


def test_main_festive_command_no_key(temp_dir):
    """Test the festive command without key."""
    output_file = os.path.join(temp_dir, "test_festive_nokey.html")
    with patch.object(sys, "argv", ["bingo", "festive", "-n", "2", "-o", output_file, "--no-key"]):
        result = main()
    assert result == 0
    assert os.path.exists(output_file)
    with open(output_file) as f:
        content = f.read()
    # Key page should not be present
    assert "BINGO KEY" not in content


def test_main_festive_command_meet_me(temp_dir):
    """Test the festive command with Meet Me In St. Louis."""
    output_file = os.path.join(temp_dir, "test_festive_mmstl.html")
    with patch.object(sys, "argv", ["bingo", "festive", "-n", "2", "-o", output_file, "-g", "meet_me_in_st_louis"]):
        result = main()
    assert result == 0
    assert os.path.exists(output_file)
    with open(output_file) as f:
        content = f.read()
    assert "Meet Me In St. Louis" in content
