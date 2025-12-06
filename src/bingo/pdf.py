"""PDF generation for bingo cards and keys."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .card import BingoCard
from .data import BingoItem

# Font paths - can be overridden
FONT_DIR = Path(__file__).parent.parent.parent / "fonts"
NOTO_EMOJI_PATH = FONT_DIR / "NotoEmoji-VariableFont.ttf"
NOTO_SANS_PATH = Path.home() / "Library/Fonts/NotoSans-Regular.ttf"

_fonts_registered = False


def register_fonts() -> None:
    """Register fonts with ReportLab."""
    global _fonts_registered
    if _fonts_registered:
        return

    # Register Noto Emoji for emoji characters
    if NOTO_EMOJI_PATH.exists():
        pdfmetrics.registerFont(TTFont("NotoEmoji", str(NOTO_EMOJI_PATH)))

    # Register Noto Sans for regular text (fallback to Helvetica)
    if NOTO_SANS_PATH.exists():
        pdfmetrics.registerFont(TTFont("NotoSans", str(NOTO_SANS_PATH)))

    _fonts_registered = True


def get_text_font() -> str:
    """Get the font name for regular text."""
    if NOTO_SANS_PATH.exists():
        return "NotoSans"
    return "Helvetica"


def get_emoji_font() -> str:
    """Get the font name for emoji."""
    if NOTO_EMOJI_PATH.exists():
        return "NotoEmoji"
    return "Helvetica"


def create_key_pdf(
    items: list[BingoItem],
    filename: str = "BingoKey.pdf",
    title1: str = "Bingo Key:",
    title2: str = "Meet Me In St. Louis",
) -> None:
    """Create a PDF with the bingo key (all items listed).

    Args:
        items: List of BingoItem objects.
        filename: Output filename.
        title1: First line of title.
        title2: Second line of title.
    """
    register_fonts()
    text_font = get_text_font()
    emoji_font = get_emoji_font()

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setTitle(f"{title1} {title2}")

    # Draw title
    c.setFont(text_font, 24)
    c.drawCentredString(width / 2, height - 50, title1)
    c.drawCentredString(width / 2, height - 75, title2)

    # Table settings
    y_offset_init = height - 110
    x_offset = 50
    y_offset = y_offset_init
    row_height = 20
    col_widths = [60, 455]  # Emoji, Description (removed Timestamp column)

    # Draw table header
    headers = ["Emoji", "Description"]
    c.setFont(text_font, 12)
    c.setFillColor(colors.grey)
    c.rect(x_offset, y_offset - row_height, sum(col_widths), row_height, fill=1)
    c.setFillColor(colors.whitesmoke)
    for i, header in enumerate(headers):
        c.drawString(x_offset + sum(col_widths[:i]) + 5, y_offset - row_height + 5, header)
    y_offset -= row_height

    # Draw table rows
    c.setFillColor(colors.black)
    for item in items:
        # Emoji column
        c.setFont(emoji_font, 10)
        c.drawString(x_offset + 5, y_offset - row_height + 5, item.emoji)

        # Description column
        c.setFont(text_font, 9)
        # Truncate long descriptions
        desc = item.description
        if len(desc) > 85:
            desc = desc[:82] + "..."
        c.drawString(x_offset + col_widths[0] + 5, y_offset - row_height + 5, desc)

        y_offset -= row_height

    # Draw grid lines
    y_offset = y_offset_init
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    for _ in range(len(items) + 2):
        c.line(x_offset, y_offset, x_offset + sum(col_widths), y_offset)
        y_offset -= row_height
    x_pos = x_offset
    for w in col_widths:
        c.line(x_pos, y_offset_init, x_pos, y_offset_init - row_height * (len(items) + 1))
        x_pos += w
    c.line(x_pos, y_offset_init, x_pos, y_offset_init - row_height * (len(items) + 1))

    c.save()
    print(f"Saved to {filename}")


def create_card_pdf(
    card: BingoCard,
    items: list[BingoItem],
    filename: str = "BingoCard.pdf",
    title1: str = "Bingo Card:",
    title2: str = "Meet Me In St. Louis",
) -> None:
    """Create a PDF with a bingo card.

    Args:
        card: The BingoCard to render.
        items: List of BingoItem objects for emoji mapping.
        filename: Output filename.
        title1: First line of title.
        title2: Second line of title.
    """
    register_fonts()
    text_font = get_text_font()
    emoji_font = get_emoji_font()

    c = canvas.Canvas(filename, pagesize=letter)
    page_width, page_height = letter
    c.setTitle(f"{title1} {title2}")

    # Draw title
    c.setFont(text_font, 24)
    c.drawCentredString(page_width / 2, page_height - 100, title1)
    c.drawCentredString(page_width / 2, page_height - 125, title2)

    # Grid settings
    grid_size = 5
    cell_size = 80
    margin_x = (page_width - (grid_size * cell_size)) / 2
    margin_y = (page_height - (grid_size * cell_size)) / 2 - 20  # Offset for title

    # Draw grid lines
    c.setLineWidth(2)
    c.setStrokeColor(colors.black)
    for i in range(grid_size + 1):
        # Horizontal lines
        c.line(margin_x, margin_y + i * cell_size, margin_x + grid_size * cell_size, margin_y + i * cell_size)
        # Vertical lines
        c.line(margin_x + i * cell_size, margin_y, margin_x + i * cell_size, margin_y + grid_size * cell_size)

    # Get emoji grid
    emoji_grid = card.get_emoji_grid(items)

    # Fill grid cells with emoji
    c.setFont(emoji_font, 28)
    for row in range(grid_size):
        for col in range(grid_size):
            emoji = emoji_grid[row][col]
            x = margin_x + col * cell_size + cell_size / 2
            # Invert row for PDF coordinates (0,0 is bottom-left)
            y = margin_y + (grid_size - row - 1) * cell_size + cell_size / 2 - 10
            c.drawCentredString(x, y, emoji)

    c.save()
    print(f"Saved to {filename}")


def generate_cards(
    items: list[BingoItem],
    num_cards: int = 10,
    output_dir: str = ".",
    prefix: str = "BingoCard",
    title1: str = "Bingo Card:",
    title2: str = "Meet Me In St. Louis",
    win_at: int = 20,
) -> list[str]:
    """Generate multiple bingo cards as PDFs.

    Args:
        items: List of BingoItem objects.
        num_cards: Number of cards to generate.
        output_dir: Directory for output files.
        prefix: Filename prefix.
        title1: First line of title.
        title2: Second line of title.
        win_at: The number at which cards should win.

    Returns:
        List of generated filenames.
    """
    from .card import generate_valid_card

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filenames = []
    for i in range(1, num_cards + 1):
        card = generate_valid_card(win_at=win_at, total_items=len(items))
        filename = str(output_path / f"{prefix}_{i:02d}.pdf")
        create_card_pdf(card, items, filename, title1, title2)
        filenames.append(filename)

    return filenames
