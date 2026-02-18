import json

POOL = {"Ornn", "Gwen", "Jax", "Camille", "Garen"}

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())

# Build coverage: for each enemy, find pool picks that counter them
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

# ─── Full pick sheet ───
print(f"{'Enemy':<20} {'Best Pick':<12} {'WR':<10} {'Alts'}")
print("=" * 70)
for enemy in TOP_LANERS:
    if enemy in coverage:
        best = coverage[enemy][0]
        alts = [f"{c} ({wr}%)" for c, wr in coverage[enemy][1:]]
        alt_str = ", ".join(alts) if alts else ""
        print(f"{enemy:<20} {best[0]:<12} {best[1]:<10} {alt_str}")
    else:
        print(f"{enemy:<20} {'Ornn':<12} {'safe':<10} blind/safe pick")

# ─── Summary ───
print(f"\n{'=' * 70}")
print(f"  POOL: {', '.join(sorted(POOL))}")
print(f"  Data-backed coverage: {len(coverage)}/{len(TOP_LANERS)}")
print(f"  Ornn safe pick for: {len(not_covered)} matchups")
print(f"{'=' * 70}")

# ─── Per-champ workload ───
print(f"\n  Workload (best pick count):")
for champ in sorted(POOL):
    best_for = [e for e, picks in coverage.items() if picks[0][0] == champ]
    print(f"    {champ:<12} best pick in {len(best_for)} matchups")
print(f"    {'Ornn':<12} safe pick in {len(not_covered)} matchups (no data-backed counter)")

# ─── Weakest matchups: where best pick WR is closest to 50% ───
print(f"\n{'=' * 70}")
print(f"  WEAKEST MATCHUPS (best pick WR closest to 50%)")
print(f"{'=' * 70}")
weak = [(e, picks[0]) for e, picks in coverage.items()]
weak.sort(key=lambda x: -x[1][1])  # highest WR = weakest counter
for enemy, (champ, wr) in weak[:15]:
    print(f"  vs {enemy:<20} {champ} at {wr}% — barely favored")

# ─── Enemies where Ornn is the fallback: are any of them common/dangerous? ───
print(f"\n{'=' * 70}")
print(f"  ORNN SAFE-PICK MATCHUPS ({len(not_covered)} total)")
print(f"  (no pool champ has sub-50% WR against these)")
print(f"{'=' * 70}")

# For Ornn matchups, show what Ornn's own WR is against them if available
for enemy in not_covered:
    # Check if Ornn appears in enemy's counter list at any WR
    counters = data[enemy]
    ornn_wr = None
    for entry in counters:
        if entry["champion"] == "Ornn":
            ornn_wr = float(entry["winrate"])
            break
    # Also check enemy in Ornn's counter list
    ornn_counters = data.get("Ornn", [])
    enemy_vs_ornn = None
    if isinstance(ornn_counters, list):
        for entry in ornn_counters:
            if entry["champion"] == enemy:
                enemy_vs_ornn = float(entry["winrate"])
                break

    if ornn_wr is not None:
        print(f"  vs {enemy:<20} Ornn counters them ({ornn_wr}% WR)")
    elif enemy_vs_ornn is not None:
        print(f"  vs {enemy:<20} ⚠ they counter Ornn ({enemy_vs_ornn}% WR for Ornn)")
    else:
        print(f"  vs {enemy:<20} neutral (no data either way)")

# ─── Hard counter exposure for your pool ───
print(f"\n{'=' * 70}")
print(f"  YOUR CHAMPS' HARD COUNTER EXPOSURE (<49% WR)")
print(f"{'=' * 70}")
for champ in sorted(POOL):
    champ_counters = data.get(champ, [])
    if isinstance(champ_counters, dict) and "error" in champ_counters:
        continue
    hard = [(e["champion"], float(e["winrate"])) for e in champ_counters if float(e["winrate"]) < 49.0]
    hard.sort(key=lambda x: x[1])
    names = ", ".join(f"{c} ({wr}%)" for c, wr in hard[:5])
    extra = f" +{len(hard)-5} more" if len(hard) > 5 else ""
    print(f"  {champ:<12} {len(hard)} hard counters: {names}{extra}")
