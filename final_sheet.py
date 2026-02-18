import json

POOL = {"Jax", "Camille", "Garen", "Gwen"}

# Manual overrides (user-assigned picks regardless of data)
MANUAL_PICKS = {
    "Darius": "Jax",
    "Fiora": "Jax",
    "Kayle": "Jax",
    "Mordekaiser": "Jax",
    "Nasus": "Jax",
    "Renekton": "Jax",
    "Yasuo": "Jax",
    "Vayne": "Jax",
    "Ornn": "Jax",
    "Tryndamere": "Jax",
    "Poppy": "Garen",
    "Shen": "Garen",
    "Sett": "Gwen",
    "Singed": "Camille",
    "Vladimir": "Camille",
}

# Ranged/AP tops that remain — user wants Galio for these
AP_RANGED_COUNTERPICK = {"Akali", "Aurora", "Heimerdinger", "Karma", "Kennen",
                          "Smolder", "Sylas", "Teemo", "Twisted Fate"}

# Remaining blanks that aren't AP/ranged
OTHER_BLANKS = {"Pantheon", "Skarner", "Warwick", "Zac"}

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())

print(f"{'Enemy':<20} {'Pick':<12} {'WR':<10} {'Note'}")
print("=" * 65)

for enemy in TOP_LANERS:
    counters = data[enemy]
    if isinstance(counters, dict) and "error" in counters:
        continue

    # Data-backed picks
    matches = []
    for entry in counters:
        if entry["champion"] in POOL:
            matches.append((entry["champion"], float(entry["winrate"])))
    matches.sort(key=lambda x: x[1])

    if enemy in AP_RANGED_COUNTERPICK:
        # Check if Galio is in counter list
        galio_wr = None
        for entry in counters:
            if entry["champion"] == "Galio":
                galio_wr = entry["winrate"]
                break
        wr_str = f"{galio_wr}%" if galio_wr else ">50%"
        print(f"{enemy:<20} {'Galio':<12} {wr_str:<10} counterpick")
    elif matches:
        best = matches[0]
        print(f"{enemy:<20} {best[0]:<12} {best[1]}%")
    elif enemy in MANUAL_PICKS:
        champ = MANUAL_PICKS[enemy]
        # Find actual WR
        actual_wr = None
        for entry in counters:
            if entry["champion"] == champ:
                actual_wr = entry["winrate"]
                break
        wr_str = f"{actual_wr}%" if actual_wr else ">50%"
        print(f"{enemy:<20} {champ:<12} {wr_str:<10} comfort")
    elif enemy in OTHER_BLANKS:
        print(f"{enemy:<20} {'???':<12} {'---':<10} no assignment")
    else:
        print(f"{enemy:<20}")

# Summary
print(f"\n{'=' * 65}")
print(f"POOL: Camille, Garen, Gwen, Jax + Galio (counterpick)")
print(f"{'=' * 65}")

assigned = 0
unassigned = []
for enemy in TOP_LANERS:
    counters = data[enemy]
    if isinstance(counters, dict) and "error" in counters:
        continue
    matches = [e for e in counters if e["champion"] in POOL]
    if matches or enemy in MANUAL_PICKS or enemy in AP_RANGED_COUNTERPICK:
        assigned += 1
    else:
        unassigned.append(enemy)

print(f"Assigned: {assigned}/60")
if unassigned:
    print(f"Still unassigned ({len(unassigned)}): {', '.join(unassigned)}")
else:
    print(f"Full coverage!")
