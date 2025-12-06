"""Bingo game data definitions."""

from dataclasses import dataclass


@dataclass
class BingoItem:
    """A single bingo item with order, emoji, and description."""
    order: int
    emoji: str
    description: str


# Meet Me In St. Louis (1944) bingo items
# Songs are prefixed with musical note, quotes with speech bubble
MEET_ME_IN_ST_LOUIS = [
    BingoItem(1, "\U0001F3B5\U0001F3A1", "Meet Me in St. Louis, Louis"),
    BingoItem(2, "\U0001F4AC\U0001F480", "I expect she won't live through the night. She has four fatal diseases."),
    BingoItem(3, "\U0001F4AC\U0001F6D1", "For heaven's sakes, stop that screeching!"),
    BingoItem(4, "\U0001F4AC\U0001F3A1", "I can't believe it. Right here where we live - right here in St. Louis."),
    BingoItem(5, "\U0001F3B5\U0001F3E0", "The Boy Next Door"),
    BingoItem(6, "\U0001F4AC\u2705", "Just when was I voted out of this family?"),
    BingoItem(7, "\U0001F4AC\U0001F37A", "I was drunk last night, dear Mother; I was drunk the night before."),
    BingoItem(8, "\U0001F3B5\U0001F483", "Skip to My Lou"),
    BingoItem(9, "\U0001F3B5\U0001F38B", "Under the Bamboo Tree"),
    BingoItem(10, "\U0001F3B5\U0001F319", "Over the Bannister"),
    BingoItem(11, "\U0001F3B5\U0001F68B", "The Trolley Song"),
    BingoItem(12, "\U0001F4AC\U0001F52B", "They'll all be safe with me. I've got twelve guns in my room."),
    BingoItem(13, "\U0001F4AC\U0001F608", "You're the most deceitful, horrible, sinful creature I ever saw..."),
    BingoItem(14, "\U0001F4AC\U0001F44A", "If there's anything I hate, loathe, despise, and abominate, it's a bully."),
    BingoItem(15, "\U0001F4AC\U0001F498", "If you're not busy tomorrow night, could you beat me up again?"),
    BingoItem(16, "\U0001F4AC\u26B0\uFE0F", "It'll take me at least a week to dig up all my dolls in the cemetery."),
    BingoItem(17, "\U0001F4AC\U0001F3E2", "Rich people have houses. People like us live in flats..."),
    BingoItem(18, "\U0001F3B5\U0001F694", "Aren't you afraid to stay here alone with a criminal?"),
    BingoItem(19, "\U0001F4AC\U0001F634", "You don't need any beauty sleep."),
    BingoItem(20, "\U0001F4AC\U0001F48B", "I'm going to let John Truett kiss me tonight."),
    BingoItem(21, "\U0001F4AC\U0001F440", "If we're going to wreck Lucille Ballard's evening, we've simply got to be a sensation."),  # noqa: E501
    BingoItem(22, "\U0001F4AC\U0001F338", "Men don't want the bloom rubbed off."),
    BingoItem(23, "\U0001F4AC\U0001F33A", "Personally, I think I have too much bloom. Maybe that's the trouble with me."),  # noqa: E501
    BingoItem(24, "\U0001F4AC\U0001F4B0", "Money! I hate, loathe, despise, and abominate money!"),
    BingoItem(25, "\U0001F4AC\U0001F3B7", "Wasn't I lucky to be born in my favorite city?"),
    BingoItem(26, "\U0001F4AC\U0001F46D", "You and I"),
    BingoItem(27, "\U0001F4AC\U0001F46B", "We could be happy anywhere as long as we're together."),
    BingoItem(28, "\U0001F4AC\u2603\uFE0F", "I'd rather kill them if we can't take them with us."),
    BingoItem(29, "\U0001F3B5\U0001F384", "Have Yourself a Merry Little Christmas"),
    BingoItem(30, "\U0001F4AC\U0001F4A1", "I never dreamed anything could be so beautiful."),
]


# Vintage Christmas Films (1898-1908) bingo items
# 4 silent films: Santa Claus (1898), A Winter Straw Ride (1906),
# The Night Before Christmas (1905), The Christmas Burglars (1908)
# Each film has a consistent first emoji as identifier
VINTAGE_CHRISTMAS_FILMS = [
    # Santa Claus (1898) - George Albert Smith, UK - 8 events
    BingoItem(1, "\U0001F385\U0001F3A5", "Santa Claus (1898) - Film begins"),
    BingoItem(2, "\U0001F385\U0001F6CF", "Children sleeping in bed"),
    BingoItem(3, "\U0001F385\U0001F319", "Santa appears magically"),
    BingoItem(4, "\U0001F385\U0001F381", "Santa fills stockings"),
    BingoItem(5, "\U0001F385\U0001F3E0", "Rooftop scene"),
    BingoItem(6, "\U0001F385\U0001F4A8", "Santa vanishes"),
    BingoItem(7, "\U0001F385\U0001F476", "Children wake up"),
    BingoItem(8, "\U0001F385\U0001F389", "Children discover presents"),
    # A Winter Straw Ride (1906) - American Mutoscope & Biograph - 7 events
    BingoItem(9, "\U0001F3BF\U0001F6F7", "Sleigh ride begins"),
    BingoItem(10, "\U0001F3BF\U0001F3D4", "Winter landscape"),
    BingoItem(11, "\U0001F3BF\U0001F40E", "Horse-drawn sleigh"),
    BingoItem(12, "\U0001F3BF\u2744\uFE0F", "Snowfall scene"),
    BingoItem(13, "\U0001F3BF\U0001F46B", "Couples riding together"),
    BingoItem(14, "\U0001F3BF\U0001F3A4", "Singing/merriment"),
    BingoItem(15, "\U0001F3BF\U0001F3E1", "Arrival at destination"),
    # The Night Before Christmas (1905) - Edwin S. Porter - 8 events
    BingoItem(16, "\U0001F384\U0001F319", "Night scene"),
    BingoItem(17, "\U0001F384\U0001F9E6", "Children hanging stockings"),
    BingoItem(18, "\U0001F384\U0001F6CF", "Children go to bed"),
    BingoItem(19, "\U0001F384\U0001F385", "Santa comes down chimney"),
    BingoItem(20, "\U0001F384\U0001F381", "Santa arranges gifts"),
    BingoItem(21, "\U0001F384\U0001F36A", "Santa eats cookies"),
    BingoItem(22, "\U0001F384\U0001F4A8", "Santa departs"),
    BingoItem(23, "\U0001F384\U0001F389", "Morning excitement"),
    # The Christmas Burglars (1908) - D.W. Griffith - 7 events
    BingoItem(24, "\U0001F3E0\U0001F5DD", "House exterior"),
    BingoItem(25, "\U0001F3E0\U0001F977", "Burglars appear"),
    BingoItem(26, "\U0001F3E0\U0001F440", "Burglars sneak in"),
    BingoItem(27, "\U0001F3E0\U0001F476", "Child discovers burglars"),
    BingoItem(28, "\U0001F3E0\U0001F6A8", "Alarm raised"),
    BingoItem(29, "\U0001F3E0\U0001F46E", "Burglars caught"),
    BingoItem(30, "\U0001F3E0\U0001F384", "Happy Christmas ending"),
]


def get_game_data(name: str = "meet_me_in_st_louis") -> list[BingoItem]:
    """Get bingo items for a specific game.

    Args:
        name: Name of the game/movie.

    Returns:
        List of BingoItem objects.

    Raises:
        ValueError: If game name is not recognized.
    """
    games = {
        "meet_me_in_st_louis": MEET_ME_IN_ST_LOUIS,
        "vintage_christmas_films": VINTAGE_CHRISTMAS_FILMS,
    }
    if name not in games:
        raise ValueError(f"Unknown game: {name}. Available: {list(games.keys())}")
    return games[name]
