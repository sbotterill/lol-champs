import json
from itertools import combinations

with open("counters_under50.json") as f:
    data = json.load(f)

# ─── Build a lookup: for each champion, which enemies do they counter? ───
# Only consider the 60 top-lane enemies from our list
TOP_LANERS = set(data.keys())

# counter_map[champ] = set of enemies they counter (appear in that enemy's sub-50% list)
counter_map = {}
for enemy, counters in data.items():
    if isinstance(counters, dict) and "error" in counters:
        continue
    for entry in counters:
        champ = entry["champion"]
        counter_map.setdefault(champ, set()).add(enemy)

# Filter to only count coverage of our 60 top laners
for champ in counter_map:
    counter_map[champ] = counter_map[champ] & TOP_LANERS

# ─── 1) Best single additions to the existing pool ───
CURRENT_POOL = {"Jax", "Camille", "Garen", "Illaoi"}
current_coverage = set()
for champ in CURRENT_POOL:
    current_coverage |= counter_map.get(champ, set())

uncovered = TOP_LANERS - current_coverage
print("=" * 70)
print(f"  CURRENT POOL: {', '.join(sorted(CURRENT_POOL))}")
print(f"  Currently covers: {len(current_coverage)}/{len(TOP_LANERS)} enemies")
print(f"  Uncovered: {len(uncovered)}")
print("=" * 70)

# Rank every champion by how many uncovered enemies they'd fill
additions = []
for champ, enemies in counter_map.items():
    new_coverage = enemies & uncovered
    if new_coverage:
        additions.append((champ, new_coverage))

additions.sort(key=lambda x: -len(x[1]))

print(f"\n{'=' * 70}")
print(f"  BEST SINGLE ADDITION TO YOUR POOL (top 15)")
print(f"{'=' * 70}")
for champ, new_cov in additions[:15]:
    total_with = len(current_coverage | counter_map.get(champ, set()))
    print(f"  + {champ:<18} fills {len(new_cov):>2} gaps → {total_with}/{len(TOP_LANERS)} total coverage")
    print(f"    Covers: {', '.join(sorted(new_cov))}")

# ─── 2) Optimal pools of size 3, 4, 5 from scratch ───
# Candidates: any champ that counters at least 3 top laners
candidates = {c: e for c, e in counter_map.items() if len(e) >= 3}
candidate_list = list(candidates.keys())

print(f"\n\n{'=' * 70}")
print(f"  OPTIMAL POOLS FROM SCRATCH")
print(f"  (testing all combos of top-coverage champions)")
print(f"{'=' * 70}")

# For efficiency, only use top ~30 candidates (most coverage)
top_candidates = sorted(candidate_list, key=lambda c: -len(candidates[c]))[:30]

for pool_size in [3, 4, 5]:
    best_pool = None
    best_coverage = set()

    for combo in combinations(top_candidates, pool_size):
        cov = set()
        for c in combo:
            cov |= candidates[c]
        if len(cov) > len(best_coverage):
            best_coverage = cov
            best_pool = combo

    uncov = TOP_LANERS - best_coverage
    print(f"\n  ── Best {pool_size}-champ pool ──")
    print(f"  Champions: {', '.join(sorted(best_pool))}")
    print(f"  Coverage:  {len(best_coverage)}/{len(TOP_LANERS)} enemies ({len(best_coverage)/len(TOP_LANERS)*100:.0f}%)")
    if uncov:
        print(f"  Gaps:      {', '.join(sorted(uncov))}")
    else:
        print(f"  Gaps:      NONE — full coverage!")

# ─── 3) Best 4-5 champ pools that INCLUDE the user's current picks ───
print(f"\n\n{'=' * 70}")
print(f"  BEST POOLS KEEPING YOUR CURRENT CHAMPS")
print(f"  (adding 1-2 to Jax, Camille, Garen, Illaoi)")
print(f"{'=' * 70}")

# Best +1
print(f"\n  ── Your pool + 1 champ (best 5) ──")
results_plus1 = []
for champ in top_candidates:
    if champ in CURRENT_POOL:
        continue
    cov = current_coverage | counter_map.get(champ, set())
    results_plus1.append((champ, cov))

results_plus1.sort(key=lambda x: -len(x[1]))
for champ, cov in results_plus1[:5]:
    uncov = TOP_LANERS - cov
    print(f"  + {champ:<18} → {len(cov)}/{len(TOP_LANERS)} covered ({len(cov)/len(TOP_LANERS)*100:.0f}%)")
    if uncov:
        print(f"    Still missing: {', '.join(sorted(uncov))}")

# Best +2
print(f"\n  ── Your pool + 2 champs (best 5) ──")
results_plus2 = []
for c1, c2 in combinations([c for c in top_candidates if c not in CURRENT_POOL], 2):
    cov = current_coverage | counter_map.get(c1, set()) | counter_map.get(c2, set())
    results_plus2.append(((c1, c2), cov))

results_plus2.sort(key=lambda x: -len(x[1]))
for (c1, c2), cov in results_plus2[:5]:
    uncov = TOP_LANERS - cov
    print(f"  + {c1} & {c2:<14} → {len(cov)}/{len(TOP_LANERS)} covered ({len(cov)/len(TOP_LANERS)*100:.0f}%)")
    if uncov:
        print(f"    Still missing: {', '.join(sorted(uncov))}")
