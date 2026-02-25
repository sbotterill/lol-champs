import json

# Load existing data for Orianna, Galio, Irelia (and Ahri for comparison)
with open("mid_matchups.json") as f:
    data = json.load(f)

# Official mid lane champion pool — ONLY these count as enemies
MID_CHAMPS = {
    "Ahri", "Akali", "Akshan", "Anivia", "Annie", "Aurelion Sol", "Aurora",
    "Azir", "Brand", "Cassiopeia", "Corki", "Diana", "Ekko", "Fizz", "Galio",
    "Gragas", "Heimerdinger", "Huck", "Hwei", "Irelia", "Jayce", "Karma",
    "Kassadin", "Katarina", "LeBlanc", "Lissandra", "Lux", "Malphite",
    "Malzahar", "Naafiri", "Neeko", "Orianna", "Pantheon", "Qiyana", "Rumble",
    "Ryze", "Smolder", "Swain", "Sylas", "Syndra", "Taliyah", "Talon", "Taric",
    "Tristana", "Twisted Fate", "Veigar", "Vel'Koz", "Vex", "Viktor",
    "Vladimir", "Xerath", "Yasuo", "Yone", "Zed", "Ziggs", "Zoe"
}

# Diana mid data scraped from lolalytics Emerald+ Feb 2026
diana_data = {
    "strong_against": [
        {"champion": "Smolder", "winrate": 64.94},
        {"champion": "Naafiri", "winrate": 60.14},
        {"champion": "Mel", "winrate": 57.86},
        {"champion": "Neeko", "winrate": 57.41},
        {"champion": "Brand", "winrate": 57.14},
        {"champion": "LeBlanc", "winrate": 56.67},
        {"champion": "Ryze", "winrate": 56.44},
        {"champion": "Azir", "winrate": 56.33},
        {"champion": "Fizz", "winrate": 56.05},
        {"champion": "Orianna", "winrate": 55.66},
        {"champion": "Aurora", "winrate": 55.14},
        {"champion": "Vel'Koz", "winrate": 54.87},
        {"champion": "Cassiopeia", "winrate": 54.74},
        {"champion": "Viktor", "winrate": 54.71},
        {"champion": "Taliyah", "winrate": 54.61},
        {"champion": "Syndra", "winrate": 54.55},
        {"champion": "Vladimir", "winrate": 54.50},
        {"champion": "Qiyana", "winrate": 54.45},
        {"champion": "Vex", "winrate": 54.00},
        {"champion": "Sylas", "winrate": 53.97},
        {"champion": "Veigar", "winrate": 53.93},
        {"champion": "Lissandra", "winrate": 53.88},
        {"champion": "Jayce", "winrate": 53.85},
        {"champion": "Katarina", "winrate": 53.70},
        {"champion": "Irelia", "winrate": 53.61},
        {"champion": "Malzahar", "winrate": 53.52},
        {"champion": "Zed", "winrate": 53.17},
        {"champion": "Twisted Fate", "winrate": 52.99},
        {"champion": "Akali", "winrate": 52.90},
        {"champion": "Yone", "winrate": 52.61},
        {"champion": "Ahri", "winrate": 52.56},
        {"champion": "Annie", "winrate": 52.31},
        {"champion": "Hwei", "winrate": 52.07},
        {"champion": "Anivia", "winrate": 51.86},
        {"champion": "Akshan", "winrate": 51.74},
        {"champion": "Zoe", "winrate": 51.60},
        {"champion": "Ekko", "winrate": 51.16},
        {"champion": "Yasuo", "winrate": 51.42},
        {"champion": "Lux", "winrate": 50.99},
        {"champion": "Kassadin", "winrate": 50.86},
        {"champion": "Galio", "winrate": 50.75},
        {"champion": "Cho'Gath", "winrate": 50.71},
        {"champion": "Xerath", "winrate": 50.66},
        {"champion": "Aurelion Sol", "winrate": 50.24},
        {"champion": "Kog'Maw", "winrate": 50.00},
    ],
    "weak_against": [
        {"champion": "Sion", "winrate": 43.11},
        {"champion": "Kayle", "winrate": 43.88},
        {"champion": "Ziggs", "winrate": 46.76},
        {"champion": "Pantheon", "winrate": 48.47},
        {"champion": "Malphite", "winrate": 49.61},
        {"champion": "Talon", "winrate": 49.66},
        {"champion": "Swain", "winrate": 49.76},
    ],
    "total_matchups": 52,
    "wins": 45,
    "losses": 7
}

# ========== POOL DEFINITIONS ==========
NEW_POOL = ["Diana", "Orianna", "Galio", "Irelia"]
OLD_POOL = ["Ahri", "Orianna", "Galio", "Irelia"]

new_pool_data = {
    "Diana": diana_data,
    "Orianna": data["Orianna"],
    "Galio": data["Galio"],
    "Irelia": data["Irelia"],
}

old_pool_data = {
    "Ahri": data["Ahri"],
    "Orianna": data["Orianna"],
    "Galio": data["Galio"],
    "Irelia": data["Irelia"],
}

def build_matchup_map(pool_data, filter_enemies=None):
    """Build a map of enemy -> [(my_champ, winrate), ...] sorted by WR desc."""
    enemy_matchups = {}
    for my_champ, champ_data in pool_data.items():
        all_matchups = champ_data["strong_against"] + champ_data["weak_against"]
        for m in all_matchups:
            enemy = m["champion"]
            if filter_enemies and enemy not in filter_enemies:
                continue
            # Don't include matchups against yourself
            if enemy in pool_data:
                pass  # still include — you might face mirror or your own pool champ
            wr = m["winrate"]
            enemy_matchups.setdefault(enemy, []).append((my_champ, wr))
    for enemy in enemy_matchups:
        enemy_matchups[enemy].sort(key=lambda x: -x[1])
    return enemy_matchups

new_matchups = build_matchup_map(new_pool_data, MID_CHAMPS)
old_matchups = build_matchup_map(old_pool_data, MID_CHAMPS)

# All mid champ enemies that we have data for
all_enemies = sorted(set(list(new_matchups.keys()) + list(old_matchups.keys())))

# Track mid champs with NO data at all
no_data_old = MID_CHAMPS - set(old_matchups.keys())
no_data_new = MID_CHAMPS - set(new_matchups.keys())

print("=" * 80)
print("  COMPARISON: Ahri/Ori/Galio/Irelia  vs  Diana/Ori/Galio/Irelia")
print("  (Filtered to official mid lane champions only)")
print("=" * 80)

if no_data_old:
    print(f"\n  Mid champs with NO data in OLD pool: {', '.join(sorted(no_data_old))}")
if no_data_new:
    print(f"  Mid champs with NO data in NEW pool: {', '.join(sorted(no_data_new))}")

# Stats for new pool
new_winning = []
new_losing = []
for enemy in sorted(new_matchups.keys()):
    picks = new_matchups[enemy]
    best = picks[0]
    if best[1] > 50.0:
        new_winning.append((enemy, picks))
    else:
        new_losing.append((enemy, picks))

# Stats for old pool
old_winning = []
old_losing = []
for enemy in sorted(old_matchups.keys()):
    picks = old_matchups[enemy]
    best = picks[0]
    if best[1] > 50.0:
        old_winning.append((enemy, picks))
    else:
        old_losing.append((enemy, picks))

old_win_wrs = [picks[0][1] for _, picks in old_winning]
new_win_wrs = [picks[0][1] for _, picks in new_winning]
old_all_wrs = [picks[0][1] for _, picks in old_winning + old_losing]
new_all_wrs = [picks[0][1] for _, picks in new_winning + new_losing]

print(f"\n  OLD POOL (Ahri/Ori/Galio/Irelia):")
print(f"    Coverage: {len(old_winning)}/{len(old_matchups)} mid matchups winning ({len(old_winning)/len(old_matchups)*100:.0f}%)")
print(f"    Avg WR (winning): {sum(old_win_wrs)/len(old_win_wrs):.1f}%")
print(f"    Avg WR (all):     {sum(old_all_wrs)/len(old_all_wrs):.1f}%")
print(f"    Losses: {len(old_losing)}")

print(f"\n  NEW POOL (Diana/Ori/Galio/Irelia):")
print(f"    Coverage: {len(new_winning)}/{len(new_matchups)} mid matchups winning ({len(new_winning)/len(new_matchups)*100:.0f}%)")
print(f"    Avg WR (winning): {sum(new_win_wrs)/len(new_win_wrs):.1f}%")
print(f"    Avg WR (all):     {sum(new_all_wrs)/len(new_all_wrs):.1f}%")
print(f"    Losses: {len(new_losing)}")

# ========== MATCHUP-BY-MATCHUP COMPARISON ==========
print(f"\n{'=' * 80}")
print(f"  MATCHUP-BY-MATCHUP COMPARISON (mid champs only)")
print(f"{'=' * 80}")
print(f"  {'Enemy':<20} {'OLD Best':<18} {'NEW Best':<18} {'Change'}")
print(f"  {'-' * 75}")

improved = []
worsened = []

for enemy in all_enemies:
    old_picks = old_matchups.get(enemy)
    new_picks = new_matchups.get(enemy)

    if old_picks and new_picks:
        old_best = old_picks[0]
        new_best = new_picks[0]
        diff = new_best[1] - old_best[1]

        if abs(diff) >= 0.5 or (old_best[1] <= 50 and new_best[1] > 50) or (old_best[1] > 50 and new_best[1] <= 50):
            marker = ""
            if old_best[1] <= 50 and new_best[1] > 50:
                marker = " *** FIXED ***"
                improved.append((enemy, old_best, new_best))
            elif old_best[1] > 50 and new_best[1] <= 50:
                marker = " *** BROKEN ***"
                worsened.append((enemy, old_best, new_best))
            elif diff > 0:
                improved.append((enemy, old_best, new_best))
                marker = " UP"
            elif diff < 0:
                worsened.append((enemy, old_best, new_best))
                marker = " DOWN"

            print(f"  {enemy:<20} {old_best[0]:<10} {old_best[1]:>5.1f}%  {new_best[0]:<10} {new_best[1]:>5.1f}%  {diff:>+5.1f}%{marker}")

# ========== NEWLY BROKEN MATCHUPS ==========
if worsened:
    print(f"\n{'=' * 80}")
    print(f"  MATCHUPS THAT GOT WORSE (sorted by impact)")
    print(f"{'=' * 80}")
    worsened.sort(key=lambda x: x[1][1] - x[2][1], reverse=True)
    for enemy, old_best, new_best in worsened:
        diff = new_best[1] - old_best[1]
        status = "LOST" if old_best[1] > 50 and new_best[1] <= 50 else "worse"
        print(f"  vs {enemy:<18} {old_best[0]} {old_best[1]:.1f}% -> {new_best[0]} {new_best[1]:.1f}% ({diff:+.1f}%) [{status}]")

# ========== NEWLY IMPROVED ==========
if improved:
    print(f"\n{'=' * 80}")
    print(f"  MATCHUPS THAT IMPROVED (sorted by impact)")
    print(f"{'=' * 80}")
    improved.sort(key=lambda x: x[2][1] - x[1][1], reverse=True)
    for enemy, old_best, new_best in improved:
        diff = new_best[1] - old_best[1]
        status = "FIXED" if old_best[1] <= 50 and new_best[1] > 50 else "better"
        print(f"  vs {enemy:<18} {old_best[0]} {old_best[1]:.1f}% -> {new_best[0]} {new_best[1]:.1f}% ({diff:+.1f}%) [{status}]")

# ========== LOSING MATCHUPS IN NEW POOL ==========
print(f"\n{'=' * 80}")
print(f"  LOSING MATCHUPS IN NEW POOL ({len(new_losing)})")
print(f"{'=' * 80}")
for enemy, picks in sorted(new_losing, key=lambda x: x[1][0][1]):
    all_options = ", ".join([f"{c} ({wr:.1f}%)" for c, wr in picks])
    old_picks = old_matchups.get(enemy)
    old_str = ""
    if old_picks:
        old_best = old_picks[0]
        old_str = f"  [was: {old_best[0]} {old_best[1]:.1f}%]"
    print(f"  vs {enemy:<18} {all_options}{old_str}")

# ========== WORKLOAD PER CHAMP ==========
print(f"\n{'=' * 80}")
print(f"  WORKLOAD BY CHAMP (NEW POOL)")
print(f"{'=' * 80}")

for champ in NEW_POOL:
    best_for = [(e, picks) for e, picks in new_winning + new_losing if picks[0][0] == champ]
    wins = len([e for e, picks in best_for if picks[0][1] > 50.0])
    total = len(best_for)
    print(f"  {champ:<12} best pick for {total:>2} matchups ({wins} winning)")

# ========== OVERLAP ANALYSIS ==========
print(f"\n{'=' * 80}")
print(f"  OVERLAP ANALYSIS — CAN YOU SHRINK THE POOL?")
print(f"{'=' * 80}")

for i, champ_a in enumerate(NEW_POOL):
    for champ_b in NEW_POOL[i+1:]:
        shared_wins = []
        for enemy in sorted(new_matchups.keys()):
            picks = new_matchups[enemy]
            a_wr = None
            b_wr = None
            for c, wr in picks:
                if c == champ_a:
                    a_wr = wr
                if c == champ_b:
                    b_wr = wr
            if a_wr and b_wr and a_wr > 50.0 and b_wr > 50.0:
                shared_wins.append((enemy, champ_a, a_wr, champ_b, b_wr))
        print(f"\n  {champ_a} + {champ_b}: {len(shared_wins)} shared winning matchups")
        if shared_wins:
            for enemy, ca, wa, cb, wb in shared_wins[:8]:
                print(f"    vs {enemy:<18} {ca} {wa:.1f}% / {cb} {wb:.1f}%")
            if len(shared_wins) > 8:
                print(f"    ... and {len(shared_wins) - 8} more")

# ========== UNIQUE CONTRIBUTIONS ==========
print(f"\n{'=' * 80}")
print(f"  UNIQUE CONTRIBUTIONS — WHAT EACH CHAMP EXCLUSIVELY COVERS")
print(f"{'=' * 80}")

for champ in NEW_POOL:
    unique = []
    for enemy in sorted(new_matchups.keys()):
        picks = new_matchups[enemy]
        champ_wr = None
        for c, wr in picks:
            if c == champ:
                champ_wr = wr
                break
        if champ_wr is None or champ_wr <= 50.0:
            continue
        others_win = False
        for c, wr in picks:
            if c != champ and wr > 50.0:
                others_win = True
                break
        if not others_win:
            unique.append((enemy, champ_wr))

    print(f"\n  {champ}: {len(unique)} UNIQUE winning matchups (no other pool champ wins)")
    for enemy, wr in sorted(unique, key=lambda x: -x[1]):
        print(f"    vs {enemy:<18} {wr:.1f}%")

# ========== CAN WE DROP ANYONE? ==========
print(f"\n{'=' * 80}")
print(f"  DROP ANALYSIS — WHAT HAPPENS IF WE REMOVE EACH CHAMP?")
print(f"{'=' * 80}")

for drop_champ in NEW_POOL:
    remaining = [c for c in NEW_POOL if c != drop_champ]
    remaining_data = {c: new_pool_data[c] for c in remaining}
    remaining_matchups = build_matchup_map(remaining_data, MID_CHAMPS)

    r_winning = 0
    r_losing = 0
    losses = []
    for enemy in sorted(remaining_matchups.keys()):
        picks = remaining_matchups[enemy]
        best = picks[0]
        if best[1] > 50.0:
            r_winning += 1
        else:
            r_losing += 1
            losses.append((enemy, best))

    r_all_wrs = [remaining_matchups[e][0][1] for e in remaining_matchups]
    avg_wr = sum(r_all_wrs) / len(r_all_wrs)
    no_data = MID_CHAMPS - set(remaining_matchups.keys())

    print(f"\n  Without {drop_champ}: {r_winning}/{len(remaining_matchups)} winning ({r_winning/len(remaining_matchups)*100:.0f}%), avg {avg_wr:.1f}%")
    if no_data:
        print(f"    No data for: {', '.join(sorted(no_data))}")
    print(f"    Losses ({r_losing}):")
    for enemy, best in sorted(losses, key=lambda x: x[1][1]):
        print(f"      vs {enemy:<18} {best[0]} {best[1]:.1f}%")

# ========== FULL NEW CHEATSHEET TABLE ==========
print(f"\n{'=' * 80}")
print(f"  FULL CHEATSHEET — Diana/Orianna/Galio/Irelia (mid champs only)")
print(f"{'=' * 80}")
print(f"  {'Enemy':<20} {'Pick':<12} {'WR':<10} {'Alts >50%'}")
print(f"  {'-' * 70}")

for enemy in sorted(new_matchups.keys()):
    picks = new_matchups[enemy]
    best = picks[0]
    alts = [f"{c}" for c, wr in picks[1:] if wr > 50.0]
    alt_str = ", ".join(alts[:3])

    marker = ""
    if best[1] <= 50.0:
        marker = " LOSING"

    print(f"  {enemy:<20} {best[0]:<12} {best[1]:<10.2f} {alt_str}{marker}")

# Also run old pool for comparison
print(f"\n{'=' * 80}")
print(f"  FULL CHEATSHEET — Ahri/Orianna/Galio/Irelia (mid champs only)")
print(f"{'=' * 80}")
print(f"  {'Enemy':<20} {'Pick':<12} {'WR':<10} {'Alts >50%'}")
print(f"  {'-' * 70}")

for enemy in sorted(old_matchups.keys()):
    picks = old_matchups[enemy]
    best = picks[0]
    alts = [f"{c}" for c, wr in picks[1:] if wr > 50.0]
    alt_str = ", ".join(alts[:3])

    marker = ""
    if best[1] <= 50.0:
        marker = " LOSING"

    print(f"  {enemy:<20} {best[0]:<12} {best[1]:<10.2f} {alt_str}{marker}")
