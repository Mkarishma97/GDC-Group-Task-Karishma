from playwright.sync_api import sync_playwright
from src.classes.models import Match
from src.classes.utils import parse_datetime


def fetch_games_via_browser():
    """
    Fetch games from HotStreak web API using correct web headers.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            extra_http_headers={
                "accept": "application/graphql-response+json, application/json",
                "accept-language": "en-US,en;q=0.9",
                "origin": "https://hs3.hotstreak.gg",
                "referer": "https://hs3.hotstreak.gg/",
                "x-hs3-version": "2",
                "x-requested-with": "web",
                "user-agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/141.0.0.0 Safari/537.36"
                ),
            }
        )

        page = context.new_page()

        query_url = (
            "https://api3.hotstreak.gg/graphql?"
            "query=query+games+%7B+games+%7B+__typename+id+cacheDebug+createdAt+"
            "generatedAt+scheduledAt+status+updatedAt+league+%7B+name+%7D+"
            "opponents+%7B+designation+team+%7B+name+%7D+%7D+%7D+%7D&operationName=games"
        )

        print("Fetching games from HotStreak web API...")
        response = page.request.get(query_url)
        print(f"Response status: {response.status}")

        if response.status != 200:
            print("Non-200 response. Body preview:")
            print(response.text()[:500])
            browser.close()
            return []

        try:
            data = response.json()
        except Exception:
            print("Could not parse JSON. Raw preview:")
            print(response.text()[:500])
            browser.close()
            return []

        games = data.get("data", {}).get("games", [])
        if not games:
            print("No games returned. Full response:")
            print(data)
            browser.close()
            return []

        matches = []
        for g in games:
            league = g.get("league", {}).get("name", "Unknown")
            opponents = g.get("opponents", [])
            home_team = next((o["team"]["name"] for o in opponents if o["designation"] == "home"), "Unknown")
            away_team = next((o["team"]["name"] for o in opponents if o["designation"] == "away"), "Unknown")

            matches.append(
                Match(
                    id=g["id"],
                    home_team=home_team,
                    away_team=away_team,
                    start_time=parse_datetime(g.get("scheduledAt", "")),
                    league=league,
                    odds=[],
                )
            )

        browser.close()
        return matches
