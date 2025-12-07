"""Festive HTML-based PDF generation for bingo cards."""

import random
from pathlib import Path

from .card import BingoCard, generate_valid_card
from .data import BingoItem

# Festive color schemes
FESTIVE_COLORS = {
    "vintage_christmas_films": {
        "primary": "#8B0000",  # Dark red
        "secondary": "#228B22",  # Forest green
        "accent": "#FFD700",  # Gold
        "bg": "#FFF8DC",  # Cornsilk
        "border": "#8B4513",  # Saddle brown
        "text": "#2F4F4F",  # Dark slate gray
    },
    "meet_me_in_st_louis": {
        "primary": "#8B0000",  # Dark red (Victorian theme)
        "secondary": "#FFD700",  # Gold
        "accent": "#FFD700",  # Gold
        "bg": "#FFF8E7",  # Cream/antique
        "border": "#8B4513",  # Saddle brown
        "text": "#2F1810",  # Dark brown
    },
}

FESTIVE_HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@400;700&display=swap"
          rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&display=swap"
          rel="stylesheet">
    <style>
        @page {{
            size: letter portrait;
            margin: 0.5in;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Mountains of Christmas', cursive;
            background: {bg};
            margin: 0;
            padding: 20px;
            color: {text};
        }}

        .card-page {{
            page-break-after: always;
            width: 7.5in;
            height: 10in;
            margin: 0 auto 20px;
            padding: 0.3in;
            background: linear-gradient(135deg, {bg} 0%, #FFFFFF 50%, {bg} 100%);
            border: 8px double {border};
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            position: relative;
            overflow: hidden;
        }}

        .card-page:last-child {{
            page-break-after: avoid;
        }}

        /* Decorative corners - aligned with yellow border at 25px */
        .corner {{
            position: absolute;
            font-size: 32px;
            opacity: 0.6;
            line-height: 1;
        }}
        .corner-tl {{ top: 25px; left: 25px; transform: translate(-50%, -50%); }}
        .corner-tr {{ top: 25px; right: 25px; transform: translate(50%, -50%); }}
        .corner-bl {{ bottom: 25px; left: 25px; transform: translate(-50%, 50%); }}
        .corner-br {{ bottom: 25px; right: 25px; transform: translate(50%, 50%); }}

        .title {{
            text-align: center;
            margin-bottom: 15px;
        }}

        .title h1 {{
            font-family: 'Cinzel Decorative', 'Mountains of Christmas', serif;
            font-size: 28px;
            color: {primary};
            margin: 0 0 5px 0;
            letter-spacing: 2px;
        }}

        .title h2 {{
            font-family: 'Mountains of Christmas', cursive;
            font-size: 20px;
            color: {secondary};
            margin: 0;
            font-weight: 400;
        }}

        .subtitle {{
            text-align: center;
            font-size: 14px;
            color: {text};
            margin-bottom: 15px;
            font-style: italic;
        }}

        .bingo-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 4px;
            max-width: 500px;
            margin: 0 auto;
            background: {border};
            padding: 4px;
            border-radius: 10px;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);
        }}

        .bingo-cell {{
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(180deg, #FFFFFF 0%, #F5F5F5 100%);
            border-radius: 5px;
            font-size: 32px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            padding: 5px;
        }}

        .bingo-cell:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}

        /* Alternating cell colors for visual interest */
        .bingo-cell:nth-child(odd) {{
            background: linear-gradient(180deg, #FFFFFF 0%, #FFF8F0 100%);
        }}

        .footer {{
            text-align: center;
            margin-top: 15px;
            font-size: 11px;
            color: {text};
            opacity: 0.7;
        }}

        .decorative-border {{
            position: absolute;
            top: 25px;
            left: 25px;
            right: 25px;
            bottom: 25px;
            border: 2px solid {accent};
            border-radius: 10px;
            pointer-events: none;
            opacity: 0.4;
        }}

        /* Key/Cheat sheet styles */
        .key-page {{
            page-break-after: always;
            width: 7.5in;
            height: 10in;
            margin: 0 auto 20px;
            padding: 0.35in;
            background: linear-gradient(135deg, {bg} 0%, #FFFFFF 50%, {bg} 100%);
            border: 8px double {border};
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            position: relative;
            overflow: hidden;
        }}

        .key-page .title {{
            margin-bottom: 8px;
        }}

        .key-page .title h1 {{
            font-size: 24px;
            margin-bottom: 2px;
        }}

        .key-page .title h2 {{
            font-size: 16px;
        }}

        .key-page .subtitle {{
            font-size: 12px;
            margin-bottom: 8px;
        }}

        .key-page .footer {{
            margin-top: 10px;
            font-size: 10px;
        }}

        .key-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-family: 'Mountains of Christmas', cursive;
        }}

        .key-table th {{
            background: linear-gradient(180deg, {primary} 0%, {secondary} 100%);
            color: white;
            padding: 10px;
            text-align: left;
            font-size: 14px;
            border: 2px solid {border};
        }}

        .key-table td {{
            padding: 8px 10px;
            border: 1px solid {border};
            font-size: 12px;
        }}

        .key-table tr:nth-child(even) {{
            background: rgba(255,255,255,0.5);
        }}

        .key-table tr:nth-child(odd) {{
            background: rgba(245,245,220,0.3);
        }}

        .key-table .emoji-cell {{
            font-size: 20px;
            text-align: center;
            width: 60px;
        }}

        .key-table .film-header {{
            background: {secondary};
            color: white;
            font-weight: bold;
            text-align: center;
        }}

        /* Compact 2-column key grid */
        .key-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4px 16px;
            margin-top: 10px;
            font-family: 'Mountains of Christmas', cursive;
        }}

        .key-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 3px 0;
            border-bottom: 1px dotted {border};
            font-size: 10px;
        }}

        .key-item .emoji {{
            font-size: 14px;
            min-width: 22px;
            text-align: center;
        }}

        .key-item .desc {{
            flex: 1;
            line-height: 1.15;
        }}

        .key-section-header {{
            grid-column: 1 / -1;
            background: linear-gradient(90deg, {secondary}, {primary});
            color: white;
            padding: 4px 8px;
            font-weight: bold;
            font-size: 11px;
            border-radius: 4px;
            margin-top: 6px;
            text-align: center;
            font-family: 'Mountains of Christmas', cursive;
        }}

        .key-section-header:first-child {{
            margin-top: 0;
        }}

        .snowflakes {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            pointer-events: none;
            overflow: hidden;
            opacity: 0.15;
        }}

        .snowflake {{
            position: absolute;
            color: {accent};
            font-size: 20px;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .card-page, .key-page {{
                box-shadow: none;
                margin: 0;
                border-width: 4px;
            }}
            .bingo-cell:hover {{
                transform: none;
            }}
        }}
    </style>
</head>
<body>
{content}
</body>
</html>
'''

CARD_TEMPLATE = '''
<div class="card-page">
    <div class="decorative-border"></div>
    <div class="snowflakes">{snowflakes}</div>
    <div class="corner corner-tl">&#10052;</div>
    <div class="corner corner-tr">&#127876;</div>
    <div class="corner corner-bl">&#127876;</div>
    <div class="corner corner-br">&#10052;</div>

    <div class="title">
        <h1>&#127876; BINGO &#127876;</h1>
        <h2>{game_title}</h2>
    </div>
    <div class="subtitle">{subtitle}</div>

    <div class="bingo-grid">
        {cells}
    </div>

    <div class="footer">
        &#10052; Mark each event as you see it in the films! &#10052;
    </div>
</div>
'''

KEY_TEMPLATE = '''
<div class="key-page">
    <div class="decorative-border"></div>
    <div class="corner corner-tl">&#10052;</div>
    <div class="corner corner-tr">&#127876;</div>
    <div class="corner corner-bl">&#127876;</div>
    <div class="corner corner-br">&#10052;</div>

    <div class="title">
        <h1>&#127876; BINGO KEY &#127876;</h1>
        <h2>{game_title}</h2>
    </div>
    <div class="subtitle">Reference guide for all {num_events} events</div>

    <div class="key-grid">
        {rows}
    </div>

    <div class="footer">
        &#10052; Happy Viewing! &#10052;
    </div>
</div>
'''


def generate_snowflakes(count: int = 15) -> str:
    """Generate random snowflake decorations."""
    snowflakes = []
    symbols = ["&#10052;", "&#10053;", "&#10054;", "&#42;"]
    for _ in range(count):
        x = random.randint(5, 95)
        y = random.randint(5, 95)
        symbol = random.choice(symbols)
        size = random.randint(15, 30)
        snowflakes.append(
            f'<span class="snowflake" style="left:{x}%;top:{y}%;font-size:{size}px">{symbol}</span>'
        )
    return "".join(snowflakes)


def create_festive_html(
    items: list[BingoItem],
    cards: list[BingoCard],
    game: str = "vintage_christmas_films",
    include_key: bool = True,
) -> str:
    """Create festive HTML with bingo cards and optional key.

    Args:
        items: List of BingoItem objects.
        cards: List of BingoCard objects to render.
        game: Game name for styling and title.
        include_key: Whether to include the key/cheat sheet.

    Returns:
        Complete HTML string.
    """
    colors = FESTIVE_COLORS.get(game, FESTIVE_COLORS["vintage_christmas_films"])

    game_titles = {
        "vintage_christmas_films": "Vintage Christmas Films",
        "meet_me_in_st_louis": "Meet Me In St. Louis",
    }
    game_title = game_titles.get(game, game.replace("_", " ").title())

    subtitles = {
        "vintage_christmas_films": (
            "Santa Claus (1898) &bull; A Winter Straw Ride (1906) &bull; "
            "The Night Before Christmas (1905) &bull; A Trap for Santa Claus (1909)"
        ),
        "meet_me_in_st_louis": "A Musical Journey Through the Seasons",
    }
    subtitle = subtitles.get(game, "")

    content_parts = []

    # Generate card pages
    for card in cards:
        emoji_grid = card.get_emoji_grid(items)
        cells = []
        for row in emoji_grid:
            for emoji in row:
                cells.append(f'<div class="bingo-cell">{emoji}</div>')

        card_html = CARD_TEMPLATE.format(
            game_title=game_title,
            subtitle=subtitle,
            cells="\n        ".join(cells),
            snowflakes=generate_snowflakes(12),
        )
        content_parts.append(card_html)

    # Generate key page
    if include_key:
        rows = []
        # Group items by sections based on game
        if game == "vintage_christmas_films":
            sections = [
                ("Santa Claus (1898)", 1, 2),
                ("A Winter Straw Ride (1906)", 3, 8),
                ("The Night Before Christmas (1905)", 9, 16),
                ("A Trap for Santa Claus (1909)", 17, 30),
            ]
        elif game == "meet_me_in_st_louis":
            sections = [
                ("Summer 1903", 1, 8),
                ("Autumn 1903", 9, 16),
                ("Winter 1903", 17, 24),
                ("Spring 1904", 25, 30),
            ]
        else:
            sections = None

        if sections:
            for section_name, start, end in sections:
                rows.append(f'<div class="key-section-header">{section_name}</div>')
                for item in items:
                    if start <= item.order <= end:
                        rows.append(
                            f'<div class="key-item">'
                            f'<span class="emoji">{item.emoji}</span>'
                            f'<span class="desc">{item.description}</span>'
                            f'</div>'
                        )
        else:
            for item in items:
                rows.append(
                    f'<div class="key-item">'
                    f'<span class="emoji">{item.emoji}</span>'
                    f'<span class="desc">{item.description}</span>'
                    f'</div>'
                )

        key_html = KEY_TEMPLATE.format(
            game_title=game_title,
            num_events=len(items),
            rows="\n        ".join(rows),
        )
        content_parts.append(key_html)

    # Combine into full HTML
    html = FESTIVE_HTML_TEMPLATE.format(
        title=f"Bingo Cards - {game_title}",
        content="\n".join(content_parts),
        **colors,
    )

    return html


def generate_festive_cards(
    items: list[BingoItem],
    num_cards: int = 30,
    output_file: str = "bingo_cards_festive.html",
    game: str = "vintage_christmas_films",
    win_at: int = 20,
    include_key: bool = True,
) -> str:
    """Generate festive HTML bingo cards.

    Args:
        items: List of BingoItem objects.
        num_cards: Number of cards to generate.
        output_file: Output HTML filename.
        game: Game name for styling.
        win_at: The number at which cards should win.
        include_key: Whether to include the key/cheat sheet.

    Returns:
        Path to generated HTML file.
    """
    # Generate cards
    cards = []
    for _ in range(num_cards):
        card = generate_valid_card(win_at=win_at, total_items=len(items))
        cards.append(card)

    # Create HTML
    html = create_festive_html(items, cards, game=game, include_key=include_key)

    # Write to file
    output_path = Path(output_file)
    output_path.write_text(html, encoding="utf-8")

    print(f"Generated {num_cards} festive bingo cards: {output_file}")
    if include_key:
        print("Includes cheat sheet as final page")
    print("\nTo create PDF: Open in browser and Print to PDF (Ctrl/Cmd+P)")

    return str(output_path)


def html_to_pdf(html_file: str, pdf_file: str) -> str:
    """Convert HTML file to PDF using Playwright.

    Args:
        html_file: Path to input HTML file.
        pdf_file: Path for output PDF file.

    Returns:
        Path to generated PDF file.
    """
    from playwright.sync_api import sync_playwright

    html_path = Path(html_file).absolute()
    pdf_path = Path(pdf_file).absolute()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_path}", wait_until="networkidle")
        # Wait for Google Fonts to load
        page.wait_for_function("document.fonts.ready")
        page.pdf(path=str(pdf_path), format="Letter", print_background=True)
        browser.close()

    print(f"Generated PDF: {pdf_file}")
    return str(pdf_path)


def markdown_to_pdf(md_file: str, pdf_file: str, game: str = "meet_me_in_st_louis") -> str:
    """Convert markdown file to PDF using Playwright.

    Args:
        md_file: Path to input markdown file.
        pdf_file: Path for output PDF file.
        game: Game name for styling.

    Returns:
        Path to generated PDF file.
    """
    import re

    from playwright.sync_api import sync_playwright

    colors = FESTIVE_COLORS.get(game, FESTIVE_COLORS["meet_me_in_st_louis"])
    md_path = Path(md_file)
    pdf_path = Path(pdf_file).absolute()

    # Read markdown content
    md_content = md_path.read_text(encoding="utf-8")

    # Simple markdown to HTML conversion
    html_content = md_content

    # Convert headers
    html_content = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html_content, flags=re.MULTILINE)
    html_content = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html_content, flags=re.MULTILINE)
    html_content = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html_content, flags=re.MULTILINE)

    # Convert bold and italic
    html_content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html_content)
    html_content = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html_content)

    # Convert unordered lists
    html_content = re.sub(r"^- (.+)$", r"<li>\1</li>", html_content, flags=re.MULTILINE)

    # Wrap consecutive <li> elements in <ul>
    html_content = re.sub(
        r"(<li>.+?</li>\n)+",
        lambda m: f"<ul>{m.group(0)}</ul>",
        html_content,
    )

    # Convert paragraphs (lines not starting with < or empty)
    lines = html_content.split("\n")
    processed_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("<") and not stripped.startswith("---"):
            processed_lines.append(f"<p>{stripped}</p>")
        elif stripped == "---":
            processed_lines.append("<hr>")
        else:
            processed_lines.append(line)
    html_content = "\n".join(processed_lines)

    # Create full HTML document
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Introduction</title>
    <link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@400;700&display=swap"
          rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&display=swap"
          rel="stylesheet">
    <style>
        @page {{
            size: letter portrait;
            margin: 0.75in;
        }}
        body {{
            font-family: 'Mountains of Christmas', Georgia, serif;
            background: {colors['bg']};
            color: {colors['text']};
            line-height: 1.6;
            padding: 20px;
        }}
        h1 {{
            font-family: 'Cinzel Decorative', serif;
            color: {colors['primary']};
            text-align: center;
            border-bottom: 3px double {colors['secondary']};
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        h2 {{
            color: {colors['primary']};
            border-bottom: 1px solid {colors['secondary']};
            padding-bottom: 5px;
            margin-top: 25px;
        }}
        h3 {{
            color: {colors['secondary']};
            margin-top: 20px;
        }}
        p {{
            margin: 10px 0;
            text-align: justify;
        }}
        ul {{
            margin: 10px 0;
            padding-left: 25px;
        }}
        li {{
            margin: 5px 0;
        }}
        strong {{
            color: {colors['primary']};
        }}
        hr {{
            border: none;
            border-top: 2px dashed {colors['secondary']};
            margin: 30px 0;
        }}
        em {{
            font-style: italic;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""

    # Write temporary HTML file
    temp_html = pdf_path.with_suffix(".temp.html")
    temp_html.write_text(html, encoding="utf-8")

    # Convert to PDF
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{temp_html.absolute()}", wait_until="networkidle")
        page.wait_for_function("document.fonts.ready")
        page.pdf(path=str(pdf_path), format="Letter", print_background=True)
        browser.close()

    # Clean up temp file
    temp_html.unlink()

    print(f"Generated PDF: {pdf_file}")
    return str(pdf_path)
