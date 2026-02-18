import json

POOL = {"Camille", "Gwen", "Jax", "Ornn"}

with open("strong_against.json") as f:
    data = json.load(f)

# Build matchup map
enemy_matchups = {}
for my_champ in POOL:
    champ_data = data[my_champ]
    if "error" in champ_data:
        continue
    all_matchups = champ_data["strong_against"] + champ_data["weak_against"]
    for m in all_matchups:
        enemy = m["champion"]
        wr = m["winrate"]
        enemy_matchups.setdefault(enemy, []).append((my_champ, wr))

for enemy in enemy_matchups:
    enemy_matchups[enemy].sort(key=lambda x: -x[1])

all_enemies = sorted(enemy_matchups.keys())

# Categorize
winning = []    # best pick >50%
losing = []     # best pick <=50%

for enemy in all_enemies:
    picks = enemy_matchups[enemy]
    best = picks[0]
    if best[1] > 50.0:
        winning.append((enemy, picks))
    else:
        losing.append((enemy, picks))

# Stats
all_best_wrs = [picks[0][1] for _, picks in winning + losing]
win_wrs = [picks[0][1] for _, picks in winning]

print("=" * 75)
print(f"  POOL: Camille, Gwen, Jax, Ornn")
print(f"  Total matchups: {len(all_enemies)}")
print(f"  Winning (>50%): {len(winning)}")
print(f"  Losing (≤50%):  {len(losing)}")
print(f"  Win rate:        {len(winning)}/{len(all_enemies)} ({len(winning)/len(all_enemies)*100:.0f}%)")
print(f"  Avg best-pick WR (winning): {sum(win_wrs)/len(win_wrs):.1f}%")
print(f"  Avg best-pick WR (all):     {sum(all_best_wrs)/len(all_best_wrs):.1f}%")
print("=" * 75)

# Per champ workload
print(f"\n  WORKLOAD:")
for champ in sorted(POOL):
    best_for = [(e, picks) for e, picks in winning + losing if picks[0][0] == champ]
    best_wins = [e for e, picks in best_for if picks[0][1] > 50.0]
    champ_data_entry = data[champ]
    print(f"    {champ:<12} best pick for {len(best_for):>2} matchups ({len(best_wins)} winning)")

# Full sheet
print(f"\n{'=' * 75}")
print(f"  {'Enemy':<20} {'Pick':<12} {'Your WR':<10} {'Alts >50%'}")
print(f"  {'-' * 65}")

for enemy in all_enemies:
    picks = enemy_matchups[enemy]
    best = picks[0]
    alts = [f"{c} ({wr}%)" for c, wr in picks[1:] if wr > 50.0]
    alt_str = ", ".join(alts[:3])
    
    marker = ""
    if best[1] >= 55.0:
        marker = " ★"
    elif best[1] <= 50.0:
        marker = " ✗"
    
    print(f"  {enemy:<20} {best[0]:<12} {best[1]:<10} {alt_str}{marker}")

# Losing matchups detail
if losing:
    print(f"\n{'=' * 75}")
    print(f"  LOSING MATCHUPS ({len(losing)})")
    print(f"{'=' * 75}")
    for enemy, picks in sorted(losing, key=lambda x: x[1][0][1]):
        all_options = [f"{c} ({wr}%)" for c, wr in picks]
        print(f"  vs {enemy:<20} {', '.join(all_options)}")

# Strongest matchups
print(f"\n{'=' * 75}")
print(f"  TOP 10 STRONGEST MATCHUPS")
print(f"{'=' * 75}")
all_sorted = sorted(winning, key=lambda x: -x[1][0][1])
for enemy, picks in all_sorted[:10]:
    print(f"  vs {enemy:<20} {picks[0][0]} at {picks[0][1]}%")

# Weakest winning matchups
print(f"\n{'=' * 75}")
print(f"  10 CLOSEST WINNING MATCHUPS (barely favored)")
print(f"{'=' * 75}")
for enemy, picks in all_sorted[-10:]:
    print(f"  vs {enemy:<20} {picks[0][0]} at {picks[0][1]}%")
