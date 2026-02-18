import json
from itertools import combinations

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())
TOTAL = len(TOP_LANERS)

# Build counter_map: for each champ, which top laners do they counter (sub-50%)?
counter_map = {}
for enemy in TOP_LANERS:
    counters = data[enemy]
    if isinstance(counters, dict) and "error" in counters:
        continue
    for entry in counters:
        champ = entry["champion"]
        wr = float(entry["winrate"])
        counter_map.setdefault(champ, {})[enemy] = wr


def coverage_details(pool):
    """Returns (covered_set, detailed_picks) for a pool."""
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


def print_pool_summary(pool, label):
    cov = coverage_details(pool)
    uncov = sorted(set(TOP_LANERS) - set(cov.keys()))
    avg_wrs = []
    for enemy, picks in cov.items():
        avg_wrs.append(picks[0][1])  # best pick WR
    avg_wr = sum(avg_wrs) / len(avg_wrs) if avg_wrs else 0

    print(f"\n{'=' * 70}")
    print(f"  {label}")
    print(f"  Pool: {', '.join(sorted(pool))}")
    print(f"  Coverage: {len(cov)}/{TOTAL} ({len(cov)/TOTAL*100:.0f}%)")
    print(f"  Avg best-pick WR: {avg_wr:.1f}%")
    print(f"{'=' * 70}")

    # Per-champ breakdown
    print(f"\n  Per-champ workload:")
    for champ in sorted(pool):
        # Count where this champ is the BEST pick
        best_for = [e for e, picks in cov.items() if picks[0][0] == champ]
        print(f"    {champ:<12} best pick in {len(best_for)} matchups")

    print(f"\n  {'Enemy':<20} {'Best Pick':<12} {'WR':<10}")
    print(f"  {'-' * 45}")
    for enemy in TOP_LANERS:
        if enemy in cov:
            best = cov[enemy][0]
            print(f"  {enemy:<20} {best[0]:<12} {best[1]}%")
        else:
            print(f"  {enemy:<20}")

    print(f"\n  Uncovered ({len(uncov)}): {', '.join(uncov)}")


# ═══════════════════════════════════════════════════════════════════
# 1) BEST 4 FROM USER'S CHAMP POOL
# ═══════════════════════════════════════════════════════════════════
USER_CHAMPS = ["Jax", "Camille", "Garen", "Illaoi", "Irelia", "Gwen"]

print("\n" + "#" * 70)
print("#  PART 1: BEST 4 FROM YOUR 6 CHAMPS")
print("#" * 70)

best_user_pool = None
best_user_count = 0
best_user_avg = 100

for combo in combinations(USER_CHAMPS, 4):
    pool = set(combo)
    cov = coverage_details(pool)
    if len(cov) > best_user_count:
        best_user_count = len(cov)
        best_user_pool = pool
        # Track avg WR for tiebreak
        wrs = [picks[0][1] for picks in cov.values()]
        best_user_avg = sum(wrs) / len(wrs)
    elif len(cov) == best_user_count:
        wrs = [picks[0][1] for picks in cov.values()]
        avg = sum(wrs) / len(wrs)
        if avg < best_user_avg:
            best_user_avg = avg
            best_user_pool = pool

# Show top 5 combos
print(f"\n  All 4-champ combos from your pool, ranked:")
results = []
for combo in combinations(USER_CHAMPS, 4):
    pool = set(combo)
    cov = coverage_details(pool)
    wrs = [picks[0][1] for picks in cov.values()]
    avg = sum(wrs) / len(wrs) if wrs else 100
    results.append((pool, len(cov), avg))

results.sort(key=lambda x: (-x[1], x[2]))
for i, (pool, count, avg) in enumerate(results):
    marker = " ← BEST" if i == 0 else ""
    print(f"  {i+1}. {', '.join(sorted(pool)):<45} {count}/{TOTAL} covered, avg WR {avg:.1f}%{marker}")

print_pool_summary(best_user_pool, "RECOMMENDED 4 FROM YOUR CHAMPS")


# ═══════════════════════════════════════════════════════════════════
# 2) BEST 4 FROM ALL CHAMPIONS (pure data)
# ═══════════════════════════════════════════════════════════════════
print("\n\n" + "#" * 70)
print("#  PART 2: BEST 4 FROM ALL CHAMPIONS (pure winrate optimization)")
print("#" * 70)

# Use top 25 candidates by coverage count for combinatorial search
all_candidates = sorted(counter_map.keys(), key=lambda c: -len(counter_map[c]))[:25]

best_data_pool = None
best_data_count = 0
best_data_avg = 100

for combo in combinations(all_candidates, 4):
    pool = set(combo)
    cov = coverage_details(pool)
    if len(cov) > best_data_count:
        best_data_count = len(cov)
        best_data_pool = pool
        wrs = [picks[0][1] for picks in cov.values()]
        best_data_avg = sum(wrs) / len(wrs)
    elif len(cov) == best_data_count:
        wrs = [picks[0][1] for picks in cov.values()]
        avg = sum(wrs) / len(wrs)
        if avg < best_data_avg:
            best_data_avg = avg
            best_data_pool = pool

print_pool_summary(best_data_pool, "BEST 4 BY PURE DATA (any champions)")
