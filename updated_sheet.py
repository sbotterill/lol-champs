import json

POOL = {"Jax", "Camille", "Garen", "Illaoi", "Irelia", "Gwen"}
# Manual overrides — user wants Jax assigned to these regardless of data
MANUAL_PICKS = {
    "Darius": "Jax",
    "Fiora": "Jax",
    "Nasus": "Jax",
    "Mordekaiser": "Jax",
    "Yasuo": "Jax",
    "Kayle": "Jax",
}

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())

# Build full pick sheet
print(f"{'Enemy':<20} {'Best Pick':<12} {'WR':<10} {'Other Options'}")
print("-" * 75)

covered_count = 0
for enemy in TOP_LANERS:
    counters = data[enemy]
    if isinstance(counters, dict) and "error" in counters:
        print(f"{enemy:<20}")
        continue

    # Data-backed picks
    matches = []
    for entry in counters:
        if entry["champion"] in POOL:
            matches.append((entry["champion"], float(entry["winrate"])))
    matches.sort(key=lambda x: x[1])

    # Check manual override
    if enemy in MANUAL_PICKS and not matches:
        champ = MANUAL_PICKS[enemy]
        # Try to find actual WR from full counter list (even if >50%)
        actual_wr = None
        for entry in counters:
            if entry["champion"] == champ:
                actual_wr = entry["winrate"]
                break
        wr_str = f"{actual_wr}%" if actual_wr else ">50%"
        print(f"{enemy:<20} {champ:<12} {wr_str:<10} (manual pick)")
        covered_count += 1
    elif matches:
        best = matches[0]
        others = [f"{c} ({wr}%)" for c, wr in matches[1:]]
        others_str = ", ".join(others) if others else ""
        print(f"{enemy:<20} {best[0]:<12} {best[1]:<10} {others_str}")
        covered_count += 1
    else:
        print(f"{enemy:<20}")

print(f"\nCovered: {covered_count}/60")
blank = [e for e in TOP_LANERS if e not in MANUAL_PICKS and not any(
    entry["champion"] in POOL for entry in data[e] if isinstance(data[e], list)
)]
print(f"Still blank: {len(blank)}")
print(f"\nRemaining blanks:")
for e in sorted(blank):
    print(f"  vs {e}")
