import json
from itertools import combinations

MY_CHAMPS = ["Camille", "Jax", "Irelia", "Garen", "Ornn", "Gwen", "Illaoi"]

with open("strong_against.json") as f:
    data = json.load(f)

# Build: for each enemy, what WR does each of my champs have?
enemy_matchups = {}
for my_champ in MY_CHAMPS:
    champ_data = data[my_champ]
    if "error" in champ_data:
        continue
    all_matchups = champ_data["strong_against"] + champ_data["weak_against"]
    for m in all_matchups:
        enemy = m["champion"]
        wr = m["winrate"]
        enemy_matchups.setdefault(enemy, []).append((my_champ, wr))

all_enemies = sorted(enemy_matchups.keys())
total_enemies = len(all_enemies)

# Difficulty ratings for context
DIFFICULTY = {
    "Camille": "Hard",
    "Jax": "Medium",
    "Irelia": "Very Hard",
    "Garen": "Easy",
    "Ornn": "Medium",
    "Gwen": "Medium",
    "Illaoi": "Medium",
}

# ─── All 35 combos of 4 ───
print("=" * 85)
print("  ALL 4-CHAMP COMBOS FROM YOUR 7 (ranked by winning matchups)")
print("  Difficulty: Easy / Medium / Hard / Very Hard")
print("=" * 85)

results = []
for combo in combinations(MY_CHAMPS, 4):
    pool = set(combo)
    win_count = 0
    lose_count = 0
    total_wr = 0
    losing = []

    for enemy, picks in enemy_matchups.items():
        pool_picks = [(c, wr) for c, wr in picks if c in pool]
        if pool_picks:
            best_wr = max(wr for _, wr in pool_picks)
            best_champ = [c for c, wr in pool_picks if wr == best_wr][0]
            if best_wr > 50.0:
                win_count += 1
                total_wr += best_wr
            else:
                lose_count += 1
                losing.append((enemy, best_champ, best_wr))

    avg = total_wr / win_count if win_count else 0
    diff_tags = [DIFFICULTY[c] for c in sorted(pool)]
    max_diff = max(diff_tags, key=lambda d: ["Easy", "Medium", "Hard", "Very Hard"].index(d))
    results.append((pool, win_count, lose_count, avg, losing, max_diff, diff_tags))

results.sort(key=lambda x: (-x[1], -x[3]))

for i, (pool, wins, losses, avg, losing, max_diff, diff_tags) in enumerate(results, 1):
    pool_str = ", ".join(sorted(pool))
    diff_str = " / ".join(sorted(diff_tags))
    print(f"\n  {i:>2}. {pool_str}")
    print(f"      Winning: {wins}/{total_enemies}  |  Losing: {losses}  |  Avg WR: {avg:.1f}%  |  Difficulty: {diff_str}")
    if losing:
        lose_strs = [f"{e} ({c} {wr}%)" for e, c, wr in sorted(losing, key=lambda x: x[2])]
        print(f"      Losing matchups: {', '.join(lose_strs)}")
    else:
        print(f"      Losing matchups: NONE")

# ─── Highlight combos without Irelia ───
print(f"\n\n{'=' * 85}")
print(f"  WITHOUT IRELIA — best combos (easier to execute)")
print(f"{'=' * 85}")
no_irelia = [r for r in results if "Irelia" not in r[0]]
for i, (pool, wins, losses, avg, losing, max_diff, diff_tags) in enumerate(no_irelia[:10], 1):
    pool_str = ", ".join(sorted(pool))
    diff_str = " / ".join(sorted(diff_tags))
    print(f"\n  {i:>2}. {pool_str}")
    print(f"      Winning: {wins}/{total_enemies}  |  Losing: {losses}  |  Avg WR: {avg:.1f}%  |  Difficulty: {diff_str}")
    if losing:
        lose_strs = [f"{e} ({c} {wr}%)" for e, c, wr in sorted(losing, key=lambda x: x[2])]
        print(f"      Losing matchups: {', '.join(lose_strs)}")

# ─── Easiest combos (no Hard/Very Hard) ───
print(f"\n\n{'=' * 85}")
print(f"  EASIEST COMBOS (no Hard or Very Hard champs)")
print(f"{'=' * 85}")
easy_combos = [r for r in results if r[5] in ["Easy", "Medium"]]
for i, (pool, wins, losses, avg, losing, max_diff, diff_tags) in enumerate(easy_combos[:10], 1):
    pool_str = ", ".join(sorted(pool))
    diff_str = " / ".join(sorted(diff_tags))
    print(f"\n  {i:>2}. {pool_str}")
    print(f"      Winning: {wins}/{total_enemies}  |  Losing: {losses}  |  Avg WR: {avg:.1f}%  |  Difficulty: {diff_str}")
    if losing:
        lose_strs = [f"{e} ({c} {wr}%)" for e, c, wr in sorted(losing, key=lambda x: x[2])]
        print(f"      Losing matchups: {', '.join(lose_strs)}")
