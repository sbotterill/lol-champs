import json

FULL_POOL = {"Jax", "Camille", "Garen", "Illaoi", "Irelia", "Gwen"}

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())


def get_coverage(pool):
    """Returns dict: enemy -> list of (champ, wr) sorted by wr."""
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


full_cov = get_coverage(FULL_POOL)
full_count = len(full_cov)

print("=" * 70)
print(f"  CURRENT POOL: {', '.join(sorted(FULL_POOL))}")
print(f"  Total coverage: {full_count}/60")
print("=" * 70)

for drop in sorted(FULL_POOL):
    reduced_pool = FULL_POOL - {drop}
    reduced_cov = get_coverage(reduced_pool)
    reduced_count = len(reduced_cov)
    lost = full_count - reduced_count

    # Which enemies are ONLY covered by this champ (sole coverage)?
    sole_coverage = []
    for enemy, picks in full_cov.items():
        champs_covering = [c for c, _ in picks]
        if drop in champs_covering and len(champs_covering) == 1:
            wr = [w for c, w in picks if c == drop][0]
            sole_coverage.append((enemy, wr))

    # Where this champ is the BEST pick but others exist
    best_but_redundant = []
    for enemy, picks in full_cov.items():
        champs_covering = [c for c, _ in picks]
        if drop in champs_covering and len(champs_covering) > 1:
            drop_wr = [w for c, w in picks if c == drop][0]
            is_best = picks[0][0] == drop
            next_best = [(c, w) for c, w in picks if c != drop][0]
            if is_best:
                best_but_redundant.append((enemy, drop_wr, next_best[0], next_best[1]))

    # Total matchups this champ appears in
    total_appearances = sum(1 for enemy, picks in full_cov.items() if drop in [c for c, _ in picks])

    print(f"\n  ── Drop {drop}? ──")
    print(f"  Coverage: {full_count} → {reduced_count}  (lose {lost} matchup{'s' if lost != 1 else ''})")
    print(f"  Appears in {total_appearances} matchups total, {len(sole_coverage)} as SOLE counter")

    if sole_coverage:
        print(f"  SOLE counter for (would go blank):")
        for enemy, wr in sorted(sole_coverage):
            print(f"    vs {enemy:<20} ({wr}%)")

    if best_but_redundant:
        print(f"  Best pick but backed up by another:")
        for enemy, drop_wr, backup, backup_wr in sorted(best_but_redundant):
            print(f"    vs {enemy:<20} {drop} ({drop_wr}%) → fallback: {backup} ({backup_wr}%)")

    print(f"  {'⚠️  HIGH IMPACT — would lose unique matchups' if lost >= 3 else '✓  Low impact — most matchups have backups' if lost <= 1 else '~  Moderate impact'}")
