import json

POOL = {"Jax", "Camille", "Garen", "Gwen"}

# All manual overrides
MANUAL_PICKS = {
    "Darius": ("Jax", "comfort"),
    "Fiora": ("Jax", "comfort"),
    "Kayle": ("Jax", "comfort"),
    "Mordekaiser": ("Jax", "comfort"),
    "Nasus": ("Jax", "comfort"),
    "Renekton": ("Jax", "comfort"),
    "Yasuo": ("Jax", "comfort"),
    "Vayne": ("Jax", "comfort"),
    "Ornn": ("Jax", "comfort"),
    "Tryndamere": ("Jax", "comfort"),
    "Poppy": ("Garen", "comfort"),
    "Shen": ("Garen", "comfort"),
    "Sett": ("Gwen", "comfort"),
    "Singed": ("Camille", "comfort"),
    "Vladimir": ("Camille", "comfort"),
    "Pantheon": ("Garen", "outscale"),
    "Skarner": ("Gwen", "tank shred"),
    "Warwick": ("Jax", "E blocks AAs"),
    "Zac": ("Gwen", "W ignores magic"),
}

# Galio counterpick targets
GALIO_TARGETS = {"Akali", "Aurora", "Heimerdinger", "Karma", "Kennen",
                 "Smolder", "Sylas", "Teemo", "Twisted Fate"}

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())

rows = []
for enemy in TOP_LANERS:
    counters = data[enemy]
    if isinstance(counters, dict) and "error" in counters:
        continue

    # Data-backed picks from pool
    matches = []
    for entry in counters:
        if entry["champion"] in POOL:
            matches.append((entry["champion"], float(entry["winrate"])))
    matches.sort(key=lambda x: x[1])

    if enemy in GALIO_TARGETS:
        galio_wr = None
        for entry in counters:
            if entry["champion"] == "Galio":
                galio_wr = entry["winrate"]
                break
        wr_str = f"{galio_wr}%" if galio_wr else ">50%"
        rows.append((enemy, "Galio", wr_str, "counterpick"))
    elif matches:
        best = matches[0]
        rows.append((enemy, best[0], f"{best[1]}%", "data"))
    elif enemy in MANUAL_PICKS:
        champ, note = MANUAL_PICKS[enemy]
        actual_wr = None
        for entry in counters:
            if entry["champion"] == champ:
                actual_wr = entry["winrate"]
                break
        wr_str = f"{actual_wr}%" if actual_wr else ">50%"
        rows.append((enemy, champ, wr_str, note))

# Print
print(f"{'Enemy':<20} {'Pick':<12} {'WR':<10} {'Note'}")
print("=" * 60)
for enemy, pick, wr, note in rows:
    note_str = "" if note == "data" else note
    print(f"{enemy:<20} {pick:<12} {wr:<10} {note_str}")

# Summary counts per champ
print(f"\n{'=' * 60}")
print("CHAMP POOL: Camille, Garen, Gwen, Jax + Galio (counterpick)")
print(f"TOTAL: {len(rows)}/60 matchups assigned")
print(f"{'=' * 60}")

counts = {}
for _, pick, _, _ in rows:
    counts[pick] = counts.get(pick, 0) + 1
for champ in sorted(counts.keys()):
    print(f"  {champ:<12} assigned to {counts[champ]} matchups")
