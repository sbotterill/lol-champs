import json
import time
import requests
from lxml import html

# All top lane champions — display name → lolalytics URL slug
CHAMPIONS = {
    "Aatrox": "aatrox",
    "Akali": "akali",
    "Ambessa": "ambessa",
    "Aurora": "aurora",
    "Camille": "camille",
    "Cho'Gath": "chogath",
    "Darius": "darius",
    "Dr. Mundo": "drmundo",
    "Fiora": "fiora",
    "Gangplank": "gangplank",
    "Garen": "garen",
    "Gnar": "gnar",
    "Gragas": "gragas",
    "Gwen": "gwen",
    "Heimerdinger": "heimerdinger",
    "Illaoi": "illaoi",
    "Irelia": "irelia",
    "Jax": "jax",
    "Jayce": "jayce",
    "K'Sante": "ksante",
    "Karma": "karma",
    "Kayle": "kayle",
    "Kennen": "kennen",
    "Kled": "kled",
    "Malphite": "malphite",
    "Mordekaiser": "mordekaiser",
    "Nasus": "nasus",
    "Olaf": "olaf",
    "Ornn": "ornn",
    "Pantheon": "pantheon",
    "Poppy": "poppy",
    "Quinn": "quinn",
    "Renekton": "renekton",
    "Rengar": "rengar",
    "Riven": "riven",
    "Rumble": "rumble",
    "Sett": "sett",
    "Shen": "shen",
    "Singed": "singed",
    "Sion": "sion",
    "Skarner": "skarner",
    "Smolder": "smolder",
    "Sylas": "sylas",
    "Tahm Kench": "tahmkench",
    "Teemo": "teemo",
    "Trundle": "trundle",
    "Tryndamere": "tryndamere",
    "Twisted Fate": "twistedfate",
    "Udyr": "udyr",
    "Urgot": "urgot",
    "Vayne": "vayne",
    "Vladimir": "vladimir",
    "Volibear": "volibear",
    "Warwick": "warwick",
    "Wukong": "wukong",
    "Yasuo": "yasuo",
    "Yone": "yone",
    "Yorick": "yorick",
    "Zaahen": "zaahen",
    "Zac": "zac",
}

MAX_WR = 50.0       # Stop collecting counters once winrate exceeds this
MAX_ENTRIES = 60     # Safety cap so we don't loop forever
OUTPUT_FILE = "counters_under50.json"


def get_counters_under_threshold(slug: str, max_wr: float = MAX_WR) -> list:
    """
    Scrape lolalytics counters page for a champion.
    Keep collecting counters as long as the winrate is <= max_wr.
    Returns a list of {champion, winrate} dicts.
    """
    url = f"https://lolalytics.com/lol/{slug}/counters/"
    resp = requests.get(url)
    tree = html.fromstring(resp.content)
    counters = []

    for i in range(1, MAX_ENTRIES + 1):
        champ_xpath = f'/html/body/main/div[6]/div[1]/div[2]/span[{i}]/div[1]/a/div/div[1]'
        wr_xpath = f'/html/body/main/div[6]/div[1]/div[2]/span[{i}]/div[1]/a/div/div[2]/div'

        try:
            champ_name = tree.xpath(champ_xpath)[0].text_content().strip()
            wr_text = tree.xpath(wr_xpath)[0].text_content().strip()
            winrate = float(wr_text.split('%')[0])
        except (IndexError, ValueError):
            # No more entries on the page
            break

        if winrate > max_wr:
            break

        counters.append({
            "champion": champ_name,
            "winrate": str(winrate)
        })

    return counters


def fetch_all_counters():
    all_counters = {}
    total = len(CHAMPIONS)

    for i, (display_name, slug) in enumerate(CHAMPIONS.items(), 1):
        print(f"[{i}/{total}] Fetching counters for {display_name}...", end=" ", flush=True)
        try:
            entries = get_counters_under_threshold(slug)
            all_counters[display_name] = entries
            print(f"OK — {len(entries)} counters at ≤{MAX_WR}% WR")
        except Exception as e:
            all_counters[display_name] = {"error": str(e)}
            print(f"FAILED — {e}")

        time.sleep(1.5)

    # Save results
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_counters, f, indent=2)

    print(f"\nDone! Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    fetch_all_counters()
