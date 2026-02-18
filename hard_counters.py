import json

HARD_COUNTER_THRESHOLD = 49.0  # below 49% = hard counter

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())

results = []
for champ in TOP_LANERS:
    counters = data[champ]
    if isinstance(counters, dict) and "error" in counters:
        continue

    hard_counters = []
    for entry in counters:
        wr = float(entry["winrate"])
        if wr < 49.0:
            hard_counters.append((entry["champion"], wr))

    hard_counters.sort(key=lambda x: x[1])
    results.append((champ, hard_counters))

results.sort(key=lambda x: len(x[1]))

print("=" * 70)
print(f"  HARD COUNTERS (<49% WR) PER CHAMPION")
print(f"  Sorted by fewest hard counters → most")
print("=" * 70)

for champ, hc_list in results:
    count = len(hc_list)
    bar = "█" * count
    if hc_list:
        worst = hc_list[0]
        names = ", ".join(f"{c} ({wr}%)" for c, wr in hc_list[:5])
        extra = f" +{len(hc_list)-5} more" if len(hc_list) > 5 else ""
        print(f"\n  {champ:<20} {count:>2} hard counters  {bar}")
        print(f"    {names}{extra}")
    else:
        print(f"\n  {champ:<20}  0 hard counters  ★ NO HARD COUNTERS")

# Summary
print(f"\n{'=' * 70}")
print(f"  SAFEST BLIND PICKS (0-3 hard counters)")
print(f"{'=' * 70}")
for champ, hc_list in results:
    if len(hc_list) <= 3:
        names = ", ".join(f"{c} ({wr}%)" for c, wr in hc_list) if hc_list else "none"
        print(f"  {champ:<20} {len(hc_list)} hard counters → {names}")

print(f"\n{'=' * 70}")
print(f"  MOST VULNERABLE (15+ hard counters)")
print(f"{'=' * 70}")
for champ, hc_list in results:
    if len(hc_list) >= 15:
        print(f"  {champ:<20} {len(hc_list)} hard counters")
