# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added (docs & marketing)
- Three-mode output screenshots in `docs/images/`
- Demo GIF showing single + multi mode usage
- `docs/blog_post.md` — open-source story for cross-posting
- `docs/promo_templates.md` — pre-written templates for Reddit/V2EX/雪球/Twitter
- Codecov badge & GitHub Actions integration
- Visible badges row in README (License/Python/Market/OpenClaw/Tests/Codecov)

### Planned
- Sector comparison mode (auto-detect CPO / Semiconductor / New Energy sectors)
- Historical backtest module (validate stop-loss rules)
- HK & US market support
- Web Dashboard

## [2.2.0] - 2026-05-06

### Added
- 🆕 **Announcement detection module** (`announcements.py`)
  - Auto-pulls recent 14-day announcements via gsk web_search
  - Recognizes HIGH (减持/立案/业绩预减) and MED (解禁/收购/重组) severity
  - Pinned at top of portfolio briefing output
- 🆕 **Profit lock level** in stop-loss algorithm — prevents risk line from being stuck at irrelevant levels for profitable positions
- 🆕 **Risk-based ranking** for portfolio holdings (loss × margin × MA20 break × heavy weight)
- 🆕 **Margin coverage ratio** auto-calculation with 5-level alerting
- 🆕 **Operation priority labels** (P0/P1/P2) on action lists

### Fixed
- Profit % display bug (template variable misalignment)
- Multi-account holdings of same symbol now correctly merged (weighted average cost)
- Stop-loss line for profitable heavy positions (was using cost-15%, now uses MA20)
- Default portfolio path resolution (now: arg > env > cwd)

### Changed
- Default data source priority: Tencent → Sina → AKShare (was AKShare-first)
- AKShare timeout reduced to 15s (was unlimited)

## [2.0.0] - 2026-04-29

### Added
- 🆕 **Three-mode architecture**: Portfolio (P) / Single (S) / Multi (M)
- 🆕 Auto mode detection based on input
- 🆕 Tencent daily-K backup data source
- 🆕 Multi-stock comparison with composite scoring
- 🆕 Single-stock deep-dive with 5 operational levels

### Changed
- Renamed from `premarket-position-brief` to `stock-realtime-brief`
- Expanded scope from "portfolio only" to "any A-share input"

## [1.0.0] - 2026-04-21

### Added
- Initial release as `premarket-position-brief`
- Portfolio-only mode
- 7-step methodology
- Three-tier hard stop loss (Warning / Risk / Cut)
- Position adjustment factors (heavy / margin / loss)
- Tencent + Sina + AKShare data fetcher

[Unreleased]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v2.2.0...HEAD
[2.2.0]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v2.0.0...v2.2.0
[2.0.0]: https://github.com/Michaelliugh/stock-realtime-brief/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/Michaelliugh/stock-realtime-brief/releases/tag/v1.0.0
