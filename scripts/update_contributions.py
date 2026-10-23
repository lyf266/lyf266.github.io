#!/usr/bin/env python3
"""
scripts/update_contributions.py
Fetch GitHub contribution calendar for lyf266 and save to data/github-contributions.json
Standard library only - zero external dependencies.
"""
import os
import sys
import json
import urllib.request
import urllib.error

USERNAME = "lyf266"
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "github-contributions.json")

GRAPHQL_QUERY = """
query($username: String!) {
  user(login: $username) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
            weekday
          }
        }
      }
    }
  }
}
"""

def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("[ERROR] Neither GH_TOKEN nor GITHUB_TOKEN environment variable is set.", file=sys.stderr)
        sys.exit(1)

    payload = json.dumps({
        "query": GRAPHQL_QUERY,
        "variables": {"username": USERNAME}
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "lyf266-contributions-updater",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP request failed with status {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    if "errors" in data:
        print(f"[ERROR] GraphQL errors: {data['errors']}", file=sys.stderr)
        sys.exit(1)

    try:
        user_data = data.get("data", {}).get("user")
        if not user_data:
            print(f"[ERROR] User '{USERNAME}' not found in GitHub GraphQL API response: {data}", file=sys.stderr)
            sys.exit(1)
        calendar = user_data["contributionsCollection"]["contributionCalendar"]
    except (KeyError, TypeError) as e:
        print(f"[ERROR] Unexpected API response structure: {e}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(calendar, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Updated {OUTPUT_FILE} with {calendar.get('totalContributions', 0)} total contributions.")

if __name__ == "__main__":
    main()
