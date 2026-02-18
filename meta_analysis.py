import json

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())

# ─── 1) Least counters: which champs have the fewest sub-50% counters ───
champ_counter_counts = []
for enemy in TOP_LANERS:
    counters = data[enemy]
    if isinstance(counters, dict) and "error" in counters:
        continue
    champ_counter_counts.append((enemy, len(counters)))

champ_counter_counts.sort(key=lambda x: x[1])

print("=" * 65)
print("  HARDEST TO COUNTER — fewest sub-50% WR counters")
print("  (fewer = harder to find a winning pick against them)")
print("=" * 65)
for champ, count in champ_counter_counts:
    bar = "█" * count
    print(f"  {champ:<20} {count:>2} counters  {bar}")

# ─── 2) Most listed as counter: which champs appear most in others' counter lists ───
counter_appearances = {}
for enemy in TOP_LANERS:
    counters = data[enemy]
    if isinstance(counters, dict) and "error" in counters:
        continue
    for entry in counters:
        champ = entry["champion"]
        counter_appearances.setdefault(champ, []).append((enemy, float(entry["winrate"])))

# Sort by number of appearances
ranked = sorted(counter_appearances.items(), key=lambda x: -len(x[1]))

print(f"\n{'=' * 65}")
print("  MOST DOMINANT COUNTERS — appear most in other champs' counter lists")
print("  (these champs counter the most top laners)")
print("=" * 65)
for champ, enemies in ranked[:30]:
    # How many of the 60 top laners they counter
    top_lane_enemies = [e for e, _ in enemies if e in set(TOP_LANERS)]
    avg_wr = sum(wr for _, wr in enemies) / len(enemies)
    bar = "█" * len(top_lane_enemies)
    print(f"  {champ:<20} counters {len(top_lane_enemies):>2} top laners (avg {avg_wr:.1f}% WR)  {bar}")

# ─── 3) Top 10 most dominant + least counterable ───
print(f"\n{'=' * 65}")
print("  TOP 10 MOST OPPRESSIVE TOP LANERS")
print("  (fewest counters = hardest to deal with)")
print("=" * 65)
for i, (champ, count) in enumerate(champ_counter_counts[:10], 1):
    print(f"  {i:>2}. {champ:<20} only {count} champs can beat them")

print(f"\n{'=' * 65}")
print("  TOP 10 MOST COUNTERABLE TOP LANERS")
print("  (most counters = easiest to find a pick against)")
print("=" * 65)
for i, (champ, count) in enumerate(champ_counter_counts[-10:], 1):
    print(f"  {i:>2}. {champ:<20} {count} champs can beat them")
