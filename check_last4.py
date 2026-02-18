import json

POOL = {"Jax", "Camille", "Garen", "Gwen", "Galio"}
ENEMIES = ["Pantheon", "Skarner", "Warwick", "Zac"]

with open("counters_under50.json") as f:
    data = json.load(f)

for enemy in ENEMIES:
    counters = data[enemy]
    print(f"\n{'=' * 60}")
    print(f"  vs {enemy} — full counter list (≤50% WR)")
    print(f"{'=' * 60}")

    for i, entry in enumerate(counters):
        champ = entry["champion"]
        wr = entry["winrate"]
        # Mark if it's in the user's pool
        tag = ""
        if champ in POOL:
            tag = " ← IN YOUR POOL"
        elif champ in {"Jax", "Camille", "Garen", "Gwen", "Galio", "Irelia", "Illaoi"}:
            tag = " ← you play this"
        print(f"  {i+1:>2}. {champ:<20} {wr}%{tag}")
