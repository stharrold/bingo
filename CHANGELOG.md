# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-07

### Added
- **Vintage Christmas Films game**: New bingo game featuring 4 silent films (1898-1909)
  - Santa Claus (1898) - 2 events
  - A Winter Straw Ride (1906) - 6 events
  - The Night Before Christmas (1905) - 8 events
  - A Trap for Santa Claus (1909) - 14 events
- **Festive HTML cards**: `bingo festive` command generates styled HTML cards with:
  - Google Fonts (Mountains of Christmas)
  - Christmas color scheme (red, green, gold)
  - Decorative borders and corner icons
  - Single-page cheat sheet with all events
- **PDF export**: `--pdf` flag converts HTML to PDF via Playwright
- **Cross-platform font support**: NotoSans font lookup for macOS, Linux, Windows
- **Game selection**: `-g/--game` flag to choose between games
- Comprehensive test coverage for new features

### Changed
- CLI now defaults to `output/` directory for festive cards
- Improved exception handling with proper chaining in VCS adapters
- Optimized Containerfile for better layer caching

### Fixed
- Font path now cross-platform (was macOS-specific)
