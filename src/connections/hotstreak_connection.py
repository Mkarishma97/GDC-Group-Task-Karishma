import json
from src.connectors.browser_api_connector import fetch_games_via_browser
from src.classes.models import Match, Odd


class HotstreakConnection:
    """Main orchestrator that uses the browser connector for fetching matches."""

    def __init__(self, output_path: str):
        self.output_path = output_path

    def run(self):
        print("Fetching matches through browser...")
        matches = fetch_games_via_browser()

        if not matches:
            print("No matches found. Check if the page or API changed.")
            return

        print(f"Fetched {len(matches)} matches.")
        self.save_to_json(matches)

    def save_to_json(self, matches):
        data = [self.serialize_match(m) for m in matches]

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)

        print(f"Data saved to {self.output_path}")

    def serialize_match(self, match: Match):
        """Convert Match object into JSON-serializable dict."""
        return {
            "id": match.id,
            "home_team": match.home_team,
            "away_team": match.away_team,
            "start_time": str(match.start_time),
            "league": match.league,
            "odds": [self.serialize_odd(o) for o in match.odds],
        }

    def serialize_odd(self, odd: Odd):
        """Convert Odd object into JSON-serializable dict."""
        return {
            "id": odd.id,
            "market": odd.market,
            "player_name": odd.player_name,
            "decimal_odds": odd.decimal_odds,
        }
