# CS2 API Wrapper

A Python wrapper for BO3.gg's Counter-Strike 2 professional match statistics API, providing an alternative to HLTV which blocks automated requests.

[![PyPI Version](https://img.shields.io/pypi/v/cs2api)](https://pypi.org/project/cs2api/)
[![Python Versions](https://img.shields.io/pypi/pyversions/cs2api)](https://pypi.org/project/cs2api/)

[![PyPI Downloads](https://static.pepy.tech/badge/sofascore-wrapper)](https://pepy.tech/projects/cs2api)

## Features

- Real-time CS2 match data from professional tournaments
- Player and team statistics
- Transfer tracking
- Match predictions
- Async/await support
- Automatic rate limiting handling

## Installation

```bash
pip install cs2api
```

## Example Usage

```py
from cs2api import CS2
import asyncio
import json

async def main():
    async with CS2() as cs2:
        # Get live matches
        live_matches = await cs2.get_live_matches()
        print(json.dumps(live_matches, indent=4))
        
        # Get player transfers
        transfers = await cs2.get_player_transfers(31349)
        print(json.dumps(transfers, indent=4))

asyncio.run(main())
```

## API METHODS

**Match Endpoints**

- get_live_matches() - Current live matches

- finished() - Recently finished matches

- get_live_match_snapshot(match_id) - Detailed live match data

- get_todays_matches() - Today's scheduled matches

- get_match_details(slug) - Comprehensive match info

**Team Endpoints**

- search_teams(query) - Search for teams by name

- get_team_matches(team_id) - Team's match history

- get_team_upcoming_matches(team_id) - Team's upcoming matches

- get_team_news(team_slug) - Team-related news

- get_team_stats(team_slug) - Team performance stats

- get_team_data(team_slug) - Basic team info

- get_team_transfers(team_id) - Team transfer history

**Player Endpoints**

- search_players(query) - Search players by name

- get_player_details(slug) - Player profile data

- get_player_stats(slug) - Player performance stats

- get_player_matches(player_id) - Player's match history

- get_player_transfers(player_id) - Player transfer history

## Context Manager (Recommended)

```py
async with CS2() as cs2:
    data = await cs2.get_live_matches()
```

## Manual Session Management

```py
cs2 = CS2()
try:
    data = await cs2.get_live_matches()
finally:
    await cs2.close()
```
