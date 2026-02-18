import json

POOL = {"Jax", "Camille", "Garen", "Illaoi"}

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())

print(f"{'Enemy':<20} {'Best Pick':<12} {'WR':<10} {'Other Options'}")
print("-" * 70)

for enemy in TOP_LANERS:
    counters = data[enemy]
    if isinstance(counters, dict) and "error" in counters:
        print(f"{enemy:<20}")
        continue

    matches = []
    for entry in counters:
        if entry["champion"] in POOL:
            matches.append((entry["champion"], float(entry["winrate"])))

    # Sort by winrate (lower = stronger counter)
    matches.sort(key=lambda x: x[1])

    if matches:
        best = matches[0]
        others = [f"{c} ({wr}%)" for c, wr in matches[1:]]
        others_str = ", ".join(others) if others else ""
        print(f"{enemy:<20} {best[0]:<12} {best[1]:<10} {others_str}")
    else:
        print(f"{enemy:<20}")
