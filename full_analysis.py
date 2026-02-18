import json

MY_CHAMPS = ["Camille", "Jax", "Irelia", "Garen", "Ornn", "Gwen", "Illaoi"]

with open("strong_against.json") as f:
    data = json.load(f)

# Build: for each enemy, what WR does each of my champs have?
enemy_matchups = {}  # enemy -> [(my_champ, my_wr)]

for my_champ in MY_CHAMPS:
    champ_data = data[my_champ]
    if "error" in champ_data:
        continue
    all_matchups = champ_data["strong_against"] + champ_data["weak_against"]
    for m in all_matchups:
        enemy = m["champion"]
        wr = m["winrate"]
        enemy_matchups.setdefault(enemy, []).append((my_champ, wr))

# Sort each enemy's options by WR descending (best pick first)
for enemy in enemy_matchups:
    enemy_matchups[enemy].sort(key=lambda x: -x[1])

# ─── Full cheat sheet with REAL winrates ───
print("=" * 80)
print("  COMPLETE MATCHUP CHART — YOUR CHAMP'S WR (not enemy's)")
print("  Pool: Camille, Jax, Irelia, Garen, Ornn, Gwen, Illaoi")
print("=" * 80)
print(f"  {'Enemy':<20} {'Best Pick':<12} {'Your WR':<10} {'Alts (>50% WR)'}")
print(f"  {'-' * 70}")

all_enemies = sorted(enemy_matchups.keys())
covered_50plus = 0
for enemy in all_enemies:
    picks = enemy_matchups[enemy]
    best = picks[0]
    winning_alts = [(c, wr) for c, wr in picks[1:] if wr > 50.0]
    alt_str = ", ".join(f"{c} ({wr}%)" for c, wr in winning_alts[:3])

    marker = ""
    if best[1] < 50.0:
        marker = " ← losing"
    elif best[1] >= 55.0:
        marker = " ★"

    if best[1] > 50.0:
        covered_50plus += 1

    print(f"  {enemy:<20} {best[0]:<12} {best[1]:<10} {alt_str}{marker}")

print(f"\n  Winning matchup (>50% WR) for: {covered_50plus}/{len(all_enemies)} enemies")

# ─── Per champ summary ───
print(f"\n{'=' * 80}")
print(f"  PER-CHAMP STRENGTH SUMMARY")
print(f"{'=' * 80}")
for champ in MY_CHAMPS:
    d = data[champ]
    if "error" in d:
        continue
    strong = d["strong_against"]
    weak = d["weak_against"]
    best3 = strong[:3] if strong else []
    worst3 = weak[:3] if weak else []
    print(f"\n  {champ} — {d['wins']}W / {d['losses']}L matchups")
    print(f"    Best:  {', '.join(f'{m['champion']} ({m['winrate']}%)' for m in best3)}")
    print(f"    Worst: {', '.join(f'{m['champion']} ({m['winrate']}%)' for m in worst3)}")

# ─── Optimal 4-champ pool analysis ───
print(f"\n\n{'=' * 80}")
print(f"  OPTIMAL 4-CHAMP POOL (from your 7, maximizing >50% WR coverage)")
print(f"{'=' * 80}")

from itertools import combinations

best_pool = None
best_count = 0
best_avg = 0

for combo in combinations(MY_CHAMPS, 4):
    pool = set(combo)
    count = 0
    total_wr = 0
    for enemy, picks in enemy_matchups.items():
        pool_picks = [(c, wr) for c, wr in picks if c in pool]
        if pool_picks:
            best_wr = max(wr for _, wr in pool_picks)
            if best_wr > 50.0:
                count += 1
                total_wr += best_wr

    avg = total_wr / count if count else 0
    if count > best_count or (count == best_count and avg > best_avg):
        best_count = count
        best_pool = pool
        best_avg = avg

print(f"\n  Best 4: {', '.join(sorted(best_pool))}")
print(f"  Winning matchups (>50% WR): {best_count}/{len(all_enemies)}")
print(f"  Avg WR in winning matchups: {best_avg:.1f}%")

# Show all combos ranked
print(f"\n  All 4-champ combos ranked:")
results = []
for combo in combinations(MY_CHAMPS, 4):
    pool = set(combo)
    count = 0
    total_wr = 0
    for enemy, picks in enemy_matchups.items():
        pool_picks = [(c, wr) for c, wr in picks if c in pool]
        if pool_picks:
            best_wr = max(wr for _, wr in pool_picks)
            if best_wr > 50.0:
                count += 1
                total_wr += best_wr
    avg = total_wr / count if count else 0
    results.append((pool, count, avg))

results.sort(key=lambda x: (-x[1], -x[2]))
for i, (pool, count, avg) in enumerate(results[:10]):
    marker = " ← BEST" if i == 0 else ""
    print(f"  {i+1:>2}. {', '.join(sorted(pool)):<45} {count}/{len(all_enemies)} winning, avg {avg:.1f}%{marker}")

# ─── Final: best 4 cheat sheet ───
print(f"\n\n{'=' * 80}")
print(f"  CHEAT SHEET FOR BEST 4: {', '.join(sorted(best_pool))}")
print(f"{'=' * 80}")
print(f"  {'Enemy':<20} {'Pick':<12} {'Your WR':<10}")
print(f"  {'-' * 45}")

losing_matchups = []
for enemy in all_enemies:
    picks = enemy_matchups[enemy]
    pool_picks = [(c, wr) for c, wr in picks if c in best_pool]
    if pool_picks:
        pool_picks.sort(key=lambda x: -x[1])
        best = pool_picks[0]
        if best[1] > 50.0:
            print(f"  {enemy:<20} {best[0]:<12} {best[1]}%")
        else:
            print(f"  {enemy:<20} {best[0]:<12} {best[1]}%  ← losing")
            losing_matchups.append((enemy, best[0], best[1]))

if losing_matchups:
    print(f"\n  LOSING MATCHUPS ({len(losing_matchups)}):")
    for enemy, champ, wr in sorted(losing_matchups, key=lambda x: x[2]):
        print(f"    vs {enemy:<20} best option: {champ} ({wr}%)")
