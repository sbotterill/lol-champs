import json

POOL = {"Ornn", "Gwen", "Jax", "Camille", "Garen"}

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())


def get_coverage(pool):
    covered = {}
    for enemy in TOP_LANERS:
        counters = data[enemy]
        if isinstance(counters, dict) and "error" in counters:
            continue
        matches = []
        for entry in counters:
            if entry["champion"] in pool:
                matches.append((entry["champion"], float(entry["winrate"])))
        if matches:
            matches.sort(key=lambda x: x[1])
            covered[enemy] = matches
    return covered


full_cov = get_coverage(POOL)
full_count = len(full_cov)

print("=" * 70)
print(f"  CURRENT POOL: {', '.join(sorted(POOL))}")
print(f"  Data-backed coverage: {full_count}/60")
print("=" * 70)

for drop in sorted(POOL):
    reduced_pool = POOL - {drop}
    reduced_cov = get_coverage(reduced_pool)
    reduced_count = len(reduced_cov)
    lost = full_count - reduced_count

    # Sole coverage: only this champ counters that enemy
    sole_coverage = []
    for enemy, picks in full_cov.items():
        champs_covering = [c for c, _ in picks]
        if drop in champs_covering and len(champs_covering) == 1:
            wr = [w for c, w in picks if c == drop][0]
            sole_coverage.append((enemy, wr))

    # Where this champ is the BEST pick but others exist
    best_but_backed = []
    for enemy, picks in full_cov.items():
        champs_covering = [c for c, _ in picks]
        if drop in champs_covering and len(champs_covering) > 1 and picks[0][0] == drop:
            next_best = [(c, w) for c, w in picks if c != drop][0]
            drop_wr = [w for c, w in picks if c == drop][0]
            diff = next_best[1] - drop_wr
            best_but_backed.append((enemy, drop_wr, next_best[0], next_best[1], diff))

    total_appearances = sum(1 for enemy, picks in full_cov.items() if drop in [c for c, _ in picks])

    print(f"\n  ── Drop {drop}? ──")
    print(f"  Coverage: {full_count} → {reduced_count}  (lose {lost} data-backed matchup{'s' if lost != 1 else ''})")
    print(f"  Appears in {total_appearances} matchups, {len(sole_coverage)} as sole counter")

    if sole_coverage:
        print(f"  Would go to Ornn safe pick:")
        for enemy, wr in sorted(sole_coverage, key=lambda x: x[1]):
            print(f"    vs {enemy:<20} (was {drop} at {wr}%)")

    if best_but_backed:
        print(f"  Best pick but has backup (WR cost to drop):")
        for enemy, drop_wr, backup, backup_wr, diff in sorted(best_but_backed, key=lambda x: -x[4]):
            print(f"    vs {enemy:<20} {drop} ({drop_wr}%) → {backup} ({backup_wr}%)  +{diff:.1f}% WR cost")

    if lost == 0:
        verdict = "FREE DROP — no unique coverage lost"
    elif lost <= 2:
        verdict = "LOW IMPACT — minimal loss, Ornn covers"
    elif lost <= 4:
        verdict = "MODERATE — some matchups go to Ornn"
    else:
        verdict = "HIGH IMPACT — significant coverage loss"
    print(f"  → {verdict}")
