import json

POOL = {"Ornn", "Gwen", "Camille", "Jax"}

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())

coverage = {}
for enemy in TOP_LANERS:
    counters = data[enemy]
    if isinstance(counters, dict) and "error" in counters:
        continue
    matches = []
    for entry in counters:
        if entry["champion"] in POOL:
            matches.append((entry["champion"], float(entry["winrate"])))
    matches.sort(key=lambda x: x[1])
    if matches:
        coverage[enemy] = matches

not_covered = sorted(set(TOP_LANERS) - set(coverage.keys()))

# ─── What did we lose vs the 5-champ pool? ───
POOL_WITH_GAREN = {"Ornn", "Gwen", "Camille", "Jax", "Garen"}
old_cov = {}
for enemy in TOP_LANERS:
    counters = data[enemy]
    if isinstance(counters, dict) and "error" in counters:
        continue
    matches = []
    for entry in counters:
        if entry["champion"] in POOL_WITH_GAREN:
            matches.append((entry["champion"], float(entry["winrate"])))
    matches.sort(key=lambda x: x[1])
    if matches:
        old_cov[enemy] = matches

lost_matchups = set(old_cov.keys()) - set(coverage.keys())
downgraded = {}
for enemy in coverage:
    if enemy in old_cov:
        old_best = old_cov[enemy][0]
        new_best = coverage[enemy][0]
        if old_best[0] == "Garen" and new_best[0] != "Garen":
            downgraded[enemy] = (old_best, new_best)

print("=" * 70)
print(f"  POOL: {', '.join(sorted(POOL))} (dropped Garen)")
print(f"  Data-backed coverage: {len(coverage)}/60")
print(f"  Ornn safe pick for: {len(not_covered)} matchups")
print("=" * 70)

print(f"\n  Lost vs 5-champ pool ({len(lost_matchups)} matchups now Ornn safe pick):")
for enemy in sorted(lost_matchups):
    old_pick = old_cov[enemy][0]
    print(f"    vs {enemy:<20} was {old_pick[0]} ({old_pick[1]}%) → now Ornn safe pick")

print(f"\n  Downgraded (Garen was best, now fallback):")
for enemy in sorted(downgraded.keys()):
    old, new = downgraded[enemy]
    diff = new[1] - old[1]
    print(f"    vs {enemy:<20} was {old[0]} ({old[1]}%) → now {new[0]} ({new[1]}%)  +{diff:.1f}% WR cost")

# ─── Full pick sheet ───
print(f"\n{'=' * 70}")
print(f"  FULL PICK SHEET")
print(f"{'=' * 70}")
print(f"  {'Enemy':<20} {'Pick':<12} {'WR':<10}")
print(f"  {'-' * 45}")
for enemy in TOP_LANERS:
    if enemy in coverage:
        best = coverage[enemy][0]
        print(f"  {enemy:<20} {best[0]:<12} {best[1]}%")
    else:
        print(f"  {enemy:<20} {'Ornn':<12} safe pick")

# ─── Weakest matchups ───
print(f"\n{'=' * 70}")
print(f"  WEAKEST DATA-BACKED MATCHUPS (WR closest to 50%)")
print(f"{'=' * 70}")
weak = [(e, picks[0]) for e, picks in coverage.items()]
weak.sort(key=lambda x: -x[1][1])
for enemy, (champ, wr) in weak[:10]:
    print(f"  vs {enemy:<20} {champ} at {wr}%")

# ─── Ornn safe picks: check for danger ───
print(f"\n{'=' * 70}")
print(f"  ORNN SAFE-PICK MATCHUPS ({len(not_covered)})")
print(f"  Checking if any of these are BAD for Ornn...")
print(f"{'=' * 70}")

ornn_counters = data.get("Ornn", [])
ornn_danger = []
ornn_neutral = []
for enemy in not_covered:
    # Check if enemy appears in Ornn's own counter list
    enemy_vs_ornn = None
    if isinstance(ornn_counters, list):
        for entry in ornn_counters:
            if entry["champion"] == enemy:
                enemy_vs_ornn = float(entry["winrate"])
                break
    # Check if Ornn appears in enemy's counter list
    enemy_counters = data.get(enemy, [])
    ornn_vs_enemy = None
    if isinstance(enemy_counters, list):
        for entry in enemy_counters:
            if entry["champion"] == "Ornn":
                ornn_vs_enemy = float(entry["winrate"])
                break

    if enemy_vs_ornn is not None and enemy_vs_ornn < 49:
        ornn_danger.append((enemy, enemy_vs_ornn, "they hard counter Ornn"))
    elif ornn_vs_enemy is not None:
        ornn_neutral.append((enemy, ornn_vs_enemy, "Ornn counters them"))
    else:
        ornn_neutral.append((enemy, None, "neutral"))

if ornn_danger:
    print(f"\n  ⚠ DANGER — these hard counter Ornn (<49% WR):")
    for enemy, wr, note in sorted(ornn_danger, key=lambda x: x[1]):
        print(f"    vs {enemy:<20} Ornn at {wr}% — {note}")
        # Suggest alt from pool
        counters = data[enemy]
        alt_matches = []
        for entry in counters:
            if entry["champion"] in POOL and entry["champion"] != "Ornn":
                alt_matches.append((entry["champion"], float(entry["winrate"])))
        if alt_matches:
            alt_matches.sort(key=lambda x: x[1])
            print(f"      Alt: {alt_matches[0][0]} ({alt_matches[0][1]}%)")

print(f"\n  Safe/neutral Ornn matchups:")
for enemy, wr, note in sorted(ornn_neutral):
    if wr:
        print(f"    vs {enemy:<20} Ornn at {wr}% — {note}")
    else:
        print(f"    vs {enemy:<20} {note}")

# ─── Workload ───
print(f"\n{'=' * 70}")
print(f"  WORKLOAD")
print(f"{'=' * 70}")
for champ in sorted(POOL):
    best_for = [e for e, picks in coverage.items() if picks[0][0] == champ]
    print(f"  {champ:<12} best pick in {len(best_for)} matchups")
print(f"  {'Ornn':<12} safe pick in {len(not_covered)} matchups (no data-backed counter)")
