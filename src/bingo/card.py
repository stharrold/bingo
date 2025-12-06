"""Bingo card generation logic."""

import random
from dataclasses import dataclass

from .data import BingoItem


@dataclass
class BingoCard:
    """A 5x5 bingo card."""
    grid: list[list[int]]  # 5x5 grid of item order numbers

    def get_emoji_grid(self, items: list[BingoItem]) -> list[list[str]]:
        """Convert the numeric grid to emoji representation.

        Args:
            items: List of BingoItem objects to map from.

        Returns:
            5x5 grid of emoji strings.
        """
        order_to_emoji = {item.order: item.emoji for item in items}
        return [[order_to_emoji[self.grid[i][j]] for j in range(5)] for i in range(5)]


def generate_card(win_at: int = 20, total_items: int = 30) -> BingoCard:
    """Generate a bingo card that wins when a specific number is called.

    The card is designed so that when numbers are called in order (1, 2, 3, ...),
    bingo is achieved exactly when `win_at` is called.

    Args:
        win_at: The number at which bingo should be achieved.
        total_items: Total number of items in the game.

    Returns:
        A BingoCard with a 5x5 grid.
    """
    # Initialize a 5x5 bingo card with None
    card = [[None for _ in range(5)] for _ in range(5)]

    # Place win_at in a random position
    idx_win = (random.randint(0, 4), random.randint(0, 4))
    card[idx_win[0]][idx_win[1]] = win_at

    # Find all cells that intersect with win_at (same row, column, or diagonal)
    # These cells must be filled with values < win_at to ensure we win at win_at
    values_lt_win = list(range(1, win_at))
    random.shuffle(values_lt_win)

    idxs_intersect = set()

    # Same row
    for j in range(5):
        if j != idx_win[1]:
            idxs_intersect.add((idx_win[0], j))

    # Same column
    for i in range(5):
        if i != idx_win[0]:
            idxs_intersect.add((i, idx_win[1]))

    # Main diagonal (top-left to bottom-right)
    if idx_win[0] == idx_win[1]:
        for i in range(5):
            if i != idx_win[0]:
                idxs_intersect.add((i, i))

    # Anti-diagonal (top-right to bottom-left)
    if idx_win[0] + idx_win[1] == 4:
        for i in range(5):
            if i != idx_win[0]:
                idxs_intersect.add((i, 4 - i))

    # Fill intersecting cells with values less than win_at
    for idx in idxs_intersect:
        if card[idx[0]][idx[1]] is None:
            card[idx[0]][idx[1]] = values_lt_win.pop()

    # Fill remaining cells with remaining random values
    remaining_values = values_lt_win + list(range(win_at + 1, total_items + 1))
    random.shuffle(remaining_values)

    for i in range(5):
        for j in range(5):
            if card[i][j] is None:
                card[i][j] = remaining_values.pop()

    return BingoCard(grid=card)


def check_bingo(card: BingoCard, called_numbers: set[int]) -> bool:
    """Check if a card has bingo.

    Args:
        card: The bingo card to check.
        called_numbers: Set of numbers that have been called.

    Returns:
        True if the card has a bingo (complete row, column, or diagonal).
    """
    grid = card.grid

    # Check rows
    for i in range(5):
        if all(grid[i][j] in called_numbers for j in range(5)):
            return True

    # Check columns
    for j in range(5):
        if all(grid[i][j] in called_numbers for i in range(5)):
            return True

    # Check main diagonal
    if all(grid[i][i] in called_numbers for i in range(5)):
        return True

    # Check anti-diagonal
    if all(grid[i][4 - i] in called_numbers for i in range(5)):
        return True

    return False


def simulate_game(card: BingoCard, total_items: int = 30) -> int:
    """Simulate a game where numbers are called in order.

    Args:
        card: The bingo card to simulate.
        total_items: Total number of items to call.

    Returns:
        The number at which bingo was achieved.
    """
    called_numbers = set()
    for number in range(1, total_items + 1):
        called_numbers.add(number)
        if check_bingo(card, called_numbers):
            return number
    return total_items


def generate_valid_card(win_at: int = 20, total_items: int = 30, max_attempts: int = 100) -> BingoCard:
    """Generate a card that wins exactly at the specified number.

    Args:
        win_at: The number at which bingo should be achieved.
        total_items: Total number of items in the game.
        max_attempts: Maximum number of generation attempts.

    Returns:
        A BingoCard that wins exactly at win_at.

    Raises:
        RuntimeError: If unable to generate a valid card.
    """
    for _ in range(max_attempts):
        card = generate_card(win_at, total_items)
        if simulate_game(card, total_items) == win_at:
            return card
    raise RuntimeError(f"Failed to generate card that wins at {win_at} after {max_attempts} attempts")
