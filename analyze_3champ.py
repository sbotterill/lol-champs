import json

with open("mid_matchups.json") as f:
    data = json.load(f)

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

def build_matchup_map(pool_data, filter_enemies=None):
    enemy_matchups = {}
    for my_champ, champ_data in pool_data.items():
        all_matchups = champ_data["strong_against"] + champ_data["weak_against"]
        for m in all_matchups:
            enemy = m["champion"]
            if filter_enemies and enemy not in filter_enemies:
                continue
            wr = m["winrate"]
            enemy_matchups.setdefault(enemy, []).append((my_champ, wr))
    for enemy in enemy_matchups:
        enemy_matchups[enemy].sort(key=lambda x: -x[1])
    return enemy_matchups

# ========== Diana / Orianna / Galio (no Irelia) ==========
POOL = ["Diana", "Orianna", "Galio"]
pool_data = {
    "Diana": diana_data,
    "Orianna": data["Orianna"],
    "Galio": data["Galio"],
}

matchups = build_matchup_map(pool_data, MID_CHAMPS)

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
no_data = MID_CHAMPS - set(matchups.keys())

print("=" * 80)
print(f"  POOL: Diana / Orianna / Galio  (3 champs)")
print(f"  Coverage: {len(winning)}/{len(matchups)} mid matchups winning ({len(winning)/len(matchups)*100:.0f}%)")
print(f"  Avg WR (winning): {sum(win_wrs)/len(win_wrs):.1f}%")
print(f"  Avg WR (all):     {sum(all_wrs)/len(all_wrs):.1f}%")
print(f"  Losses: {len(losing)}")
if no_data:
    print(f"  No data for: {', '.join(sorted(no_data))}")
print("=" * 80)

# Workload
print(f"\n  WORKLOAD:")
for champ in POOL:
    best_for = [(e, picks) for e, picks in winning + losing if picks[0][0] == champ]
    wins = len([e for e, picks in best_for if picks[0][1] > 50.0])
    total = len(best_for)
    print(f"    {champ:<12} best pick for {total:>2} matchups ({wins} winning)")

# Losing matchups
print(f"\n  LOSING MATCHUPS ({len(losing)}):")
for enemy, picks in sorted(losing, key=lambda x: x[1][0][1]):
    all_options = ", ".join([f"{c} ({wr:.1f}%)" for c, wr in picks])
    print(f"    vs {enemy:<18} {all_options}")

# Full cheatsheet
print(f"\n{'=' * 80}")
print(f"  FULL CHEATSHEET — Diana / Orianna / Galio")
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

# Compare: what does Irelia add that this pool doesn't cover?
print(f"\n{'=' * 80}")
print(f"  WHAT IRELIA WOULD ADD (matchups where Irelia is strictly better)")
print(f"{'=' * 80}")

irelia_data = data["Irelia"]
irelia_matchups_raw = irelia_data["strong_against"] + irelia_data["weak_against"]
irelia_map = {m["champion"]: m["winrate"] for m in irelia_matchups_raw}

for enemy in sorted(matchups.keys()):
    picks = matchups[enemy]
    best_champ, best_wr = picks[0]
    irelia_wr = irelia_map.get(enemy)
    if irelia_wr and irelia_wr > best_wr and irelia_wr > 50.0:
        diff = irelia_wr - best_wr
        fix = " ** FIXES LOSS **" if best_wr <= 50.0 else ""
        print(f"    vs {enemy:<18} current: {best_champ} {best_wr:.1f}% -> Irelia {irelia_wr:.1f}% (+{diff:.1f}%){fix}")

# Also check enemies Irelia covers but nobody else in this pool has data for
irelia_only = set()
for m in irelia_matchups_raw:
    enemy = m["champion"]
    if enemy in MID_CHAMPS and enemy not in matchups:
        if m["winrate"] > 50.0:
            irelia_only.add((enemy, m["winrate"]))
if irelia_only:
    print(f"\n    Irelia-only coverage (no data from Diana/Ori/Galio):")
    for enemy, wr in sorted(irelia_only, key=lambda x: -x[1]):
        print(f"      vs {enemy:<18} Irelia {wr:.1f}%")
