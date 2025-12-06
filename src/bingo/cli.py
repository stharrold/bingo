"""Command-line interface for bingo card generation."""

import argparse
import sys

from .data import get_game_data
from .pdf import create_key_pdf, generate_cards

# Available games and their display names for filenames
GAME_CHOICES = ["meet_me_in_st_louis", "vintage_christmas_films"]
GAME_FILE_PREFIXES = {
    "meet_me_in_st_louis": "MeetMeInStLouis",
    "vintage_christmas_films": "VintageChristmasFilms",
}


def main() -> int:
    """Main entry point for the bingo CLI."""
    parser = argparse.ArgumentParser(
        description="Generate bingo cards for movie watching parties.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  bingo key                     Generate a bingo key PDF
  bingo cards --num 20          Generate 20 bingo cards
  bingo cards -n 10 -o ./cards  Generate 10 cards in ./cards directory
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Key command
    key_parser = subparsers.add_parser("key", help="Generate a bingo key PDF")
    key_parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output filename (default: BingoKey_<game>.pdf)",
    )
    key_parser.add_argument(
        "-g", "--game",
        choices=GAME_CHOICES,
        default="meet_me_in_st_louis",
        help="Game/movie name (default: meet_me_in_st_louis)",
    )

    # Cards command
    cards_parser = subparsers.add_parser("cards", help="Generate bingo cards")
    cards_parser.add_argument(
        "-n", "--num",
        type=int,
        default=10,
        help="Number of cards to generate (default: 10)",
    )
    cards_parser.add_argument(
        "-o", "--output-dir",
        default=".",
        help="Output directory (default: current directory)",
    )
    cards_parser.add_argument(
        "-p", "--prefix",
        default=None,
        help="Filename prefix (default: BingoCard_<game>)",
    )
    cards_parser.add_argument(
        "-g", "--game",
        choices=GAME_CHOICES,
        default="meet_me_in_st_louis",
        help="Game/movie name (default: meet_me_in_st_louis)",
    )
    cards_parser.add_argument(
        "-w", "--win-at",
        type=int,
        default=20,
        help="Number at which cards should win (default: 20)",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == "key":
        items = get_game_data(args.game)
        game_prefix = GAME_FILE_PREFIXES[args.game]
        output = args.output or f"BingoKey_{game_prefix}.pdf"
        create_key_pdf(items, output, game=args.game)
        return 0

    if args.command == "cards":
        items = get_game_data(args.game)
        game_prefix = GAME_FILE_PREFIXES[args.game]
        prefix = args.prefix or f"BingoCard_{game_prefix}"
        filenames = generate_cards(
            items,
            num_cards=args.num,
            output_dir=args.output_dir,
            prefix=prefix,
            win_at=args.win_at,
            game=args.game,
        )
        print(f"Generated {len(filenames)} cards")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
