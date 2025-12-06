"""Command-line interface for bingo card generation."""

import argparse
import sys

from .data import get_game_data
from .pdf import create_key_pdf, generate_cards


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
        default="BingoKey_MeetMeInStLouis.pdf",
        help="Output filename (default: BingoKey_MeetMeInStLouis.pdf)",
    )
    key_parser.add_argument(
        "-g", "--game",
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
        default="BingoCard_MeetMeInStLouis",
        help="Filename prefix (default: BingoCard_MeetMeInStLouis)",
    )
    cards_parser.add_argument(
        "-g", "--game",
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
        create_key_pdf(items, args.output)
        return 0

    if args.command == "cards":
        items = get_game_data(args.game)
        filenames = generate_cards(
            items,
            num_cards=args.num,
            output_dir=args.output_dir,
            prefix=args.prefix,
            win_at=args.win_at,
        )
        print(f"Generated {len(filenames)} cards")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
