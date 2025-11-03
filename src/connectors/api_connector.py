import httpx
from src.classes.models import Match, Odd
from src.classes.utils import parse_datetime


class HotstreakAPI:
    """Handles API requests to HotStreak GraphQL endpoint with HTTP/2 support."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {
            "authority": "api3.hotstreak.gg",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://hs3.hotstreak.gg",
            "referer": "https://hs3.hotstreak.gg/",
            "sec-ch-ua": '"Google Chrome";v="141", "Not A(Brand";v="8", "Chromium";v="141"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/141.0.0.0 Safari/537.36"
            ),
        }

    def fetch_games(self):
        """Fetch all available games using HTTP/2 GET."""
        query = (
            "query games { games { __typename id cacheDebug createdAt generatedAt "
            "scheduledAt status updatedAt league { name } opponents { designation team { name } } } }"
        )

        params = {"query": query, "operationName": "games"}

        with httpx.Client(http2=True, headers=self.headers, timeout=20) as client:
            response = client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

        if "data" not in data or not data["data"].get("games"):
            print("No data returned.")
            return []

        return data["data"]["games"]

    def parse_games(self, games: list):
        """Convert raw API game data into Match objects."""
        matches = []
        for g in games:
            league = g.get("league", {}).get("name", "Unknown")
            opponents = g.get("opponents", [])
            home_team = next(
                (o["team"]["name"] for o in opponents if o["designation"] == "home"), "Unknown"
            )
            away_team = next(
                (o["team"]["name"] for o in opponents if o["designation"] == "away"), "Unknown"
            )

            match = Match(
                id=g["id"],
                home_team=home_team,
                away_team=away_team,
                start_time=parse_datetime(g.get("scheduledAt", "")),
                league=league,
                odds=[],
            )
            matches.append(match)
        return matches

    def fetch_odds(self, match_id: str):
        """Fetch odds for a given match using HTTP/2."""
        query = (
            "query markets($gameId: ID!) { markets(gameId: $gameId) { id marketType "
            "outcomes { id playerName price } } }"
        )

        params = {
            "query": query,
            "variables": f'{{"gameId":"{match_id}"}}',
            "operationName": "markets",
        }

        with httpx.Client(http2=True, headers=self.headers, timeout=20) as client:
            try:
                response = client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

                markets = data.get("data", {}).get("markets", [])
                odds_list = []
                for m in markets:
                    for o in m.get("outcomes", []):
                        odds_list.append(
                            Odd(
                                id=o["id"],
                                market=m["marketType"],
                                player_name=o.get("playerName"),
                                decimal_odds=o.get("price", 0.0),
                            )
                        )
                return odds_list
            except Exception as e:
                print(f"Error fetching odds for {match_id}: {e}")
                return []
