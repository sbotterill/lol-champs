import json

with open("strong_against.json") as f:
    data = json.load(f)

POOL = ["Jax", "Garen", "Ornn"]
pool_data = {c: data[c] for c in POOL}

def build_matchup_map(pool_data):
    enemy_matchups = {}
    for my_champ, champ_data in pool_data.items():
        all_matchups = champ_data["strong_against"] + champ_data["weak_against"]
        for m in all_matchups:
            enemy = m["champion"]
            wr = m["winrate"]
            enemy_matchups.setdefault(enemy, []).append((my_champ, wr))
    for enemy in enemy_matchups:
        enemy_matchups[enemy].sort(key=lambda x: -x[1])
    return enemy_matchups

matchups = build_matchup_map(pool_data)

winning = []
losing = []
for enemy in sorted(matchups.keys()):
    picks = matchups[enemy]
    best = picks[0]
    if best[1] > 50.0:
        winning.append((enemy, picks))
    else:
        losing.append((enemy, picks))

win_wrs = [picks[0][1] for _, picks in winning]
all_wrs = [picks[0][1] for _, picks in winning + losing]

print("=" * 80)
print(f"  POOL: Jax / Garen / Ornn")
print(f"  Coverage: {len(winning)}/{len(matchups)} winning ({len(winning)/len(matchups)*100:.0f}%)")
print(f"  Avg WR (winning): {sum(win_wrs)/len(win_wrs):.1f}%")
print(f"  Avg WR (all):     {sum(all_wrs)/len(all_wrs):.1f}%")
print(f"  Losses: {len(losing)}")
print("=" * 80)

# Workload
print(f"\n  WORKLOAD:")
for champ in POOL:
    best_for = [(e, picks) for e, picks in winning + losing if picks[0][0] == champ]
    wins = len([e for e, picks in best_for if picks[0][1] > 50.0])
    total = len(best_for)
    print(f"    {champ:<12} best pick for {total:>2} matchups ({wins} winning)")

# Losing
print(f"\n  LOSING MATCHUPS ({len(losing)}):")
for enemy, picks in sorted(losing, key=lambda x: x[1][0][1]):
    all_options = ", ".join([f"{c} ({wr:.1f}%)" for c, wr in picks])
    print(f"    vs {enemy:<18} {all_options}")

# Full table
print(f"\n{'=' * 80}")
print(f"  FULL CHEATSHEET")
print(f"{'=' * 80}")
print(f"  {'Enemy':<20} {'Pick':<12} {'WR':<10} {'Alts >50%'}")
print(f"  {'-' * 70}")

for enemy in sorted(matchups.keys()):
    picks = matchups[enemy]
    best = picks[0]
    alts = [f"{c}" for c, wr in picks[1:] if wr > 50.0]
    alt_str = ", ".join(alts[:3])
    marker = ""
    if best[1] <= 50.0:
        marker = " LOSING"
    print(f"  {enemy:<20} {best[0]:<12} {best[1]:<10.2f} {alt_str}{marker}")

# Strongest
print(f"\n  TOP STRONGEST:")
for enemy, picks in sorted(winning, key=lambda x: -x[1][0][1])[:10]:
    print(f"    vs {enemy:<18} {picks[0][0]} {picks[0][1]:.1f}%")

# Tightest
print(f"\n  TIGHTEST WINS:")
for enemy, picks in sorted(winning, key=lambda x: x[1][0][1])[:8]:
    print(f"    vs {enemy:<18} {picks[0][0]} {picks[0][1]:.1f}%")
