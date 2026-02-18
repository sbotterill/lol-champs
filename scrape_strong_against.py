import json
import time
import requests
from lxml import html

# User's full champ pool to evaluate
MY_CHAMPS = {
    "Camille": "camille",
    "Jax": "jax",
    "Irelia": "irelia",
    "Garen": "garen",
    "Ornn": "ornn",
    "Gwen": "gwen",
    "Illaoi": "illaoi",
}

MAX_ENTRIES = 60
OUTPUT_FILE = "strong_against.json"


def scrape_all_matchups(slug: str) -> list:
    """
    Scrape ALL matchup entries from a champ's counter page.
    Returns list of {champion, winrate} — winrate is YOUR champ's WR.
    Entries with WR > 50 = you beat them. WR < 50 = they beat you.
    """
    url = f"https://lolalytics.com/lol/{slug}/counters/"
    resp = requests.get(url)
    tree = html.fromstring(resp.content)
    matchups = []

    for i in range(1, MAX_ENTRIES + 1):
        champ_xpath = f'/html/body/main/div[6]/div[1]/div[2]/span[{i}]/div[1]/a/div/div[1]'
        wr_xpath = f'/html/body/main/div[6]/div[1]/div[2]/span[{i}]/div[1]/a/div/div[2]/div'

        try:
            champ_name = tree.xpath(champ_xpath)[0].text_content().strip()
            wr_text = tree.xpath(wr_xpath)[0].text_content().strip()
            winrate = float(wr_text.split('%')[0])
        except (IndexError, ValueError):
            break

        matchups.append({
            "champion": champ_name,
            "winrate": winrate
        })

    return matchups


def main():
    all_data = {}
    total = len(MY_CHAMPS)

    for i, (display_name, slug) in enumerate(MY_CHAMPS.items(), 1):
        print(f"[{i}/{total}] Scraping all matchups for {display_name}...", end=" ", flush=True)
        try:
            matchups = scrape_all_matchups(slug)
            # Split into "strong against" (>50%) and "weak against" (<50%)
            strong = [m for m in matchups if m["winrate"] > 50.0]
            weak = [m for m in matchups if m["winrate"] <= 50.0]
            all_data[display_name] = {
                "strong_against": sorted(strong, key=lambda x: -x["winrate"]),
                "weak_against": sorted(weak, key=lambda x: x["winrate"]),
                "total_matchups": len(matchups),
                "wins": len(strong),
                "losses": len(weak)
            }
            print(f"OK — {len(strong)} winning, {len(weak)} losing matchups")
        except Exception as e:
            all_data[display_name] = {"error": str(e)}
            print(f"FAILED — {e}")

        time.sleep(1.5)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

    print(f"\nDone! Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
