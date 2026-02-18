import json

POOL = {"Jax", "Camille", "Garen", "Illaoi"}

with open("counters_under50.json") as f:
    data = json.load(f)

covered = {}      # enemy -> list of (your_champ, winrate)
not_covered = []  # enemies where none of your pool appears

for enemy, counters in data.items():
    if isinstance(counters, dict) and "error" in counters:
        continue

    matches = []
    for entry in counters:
        if entry["champion"] in POOL:
            matches.append((entry["champion"], float(entry["winrate"])))

    if matches:
        covered[enemy] = matches
    else:
        not_covered.append(enemy)

# --- Print coverage ---
print("=" * 65)
print(f"  YOUR POOL: {', '.join(sorted(POOL))}")
print(f"  DATA: all counters with ≤50% winrate")
print("=" * 65)

print(f"\n{'=' * 65}")
print(f"  COVERED — enemies where your pool has a counter ({len(covered)})")
print(f"{'=' * 65}")
for enemy in sorted(covered.keys()):
    picks = covered[enemy]
    pick_strs = [f"{champ} ({wr}%)" for champ, wr in sorted(picks, key=lambda x: x[1])]
    print(f"  vs {enemy:<20} → {', '.join(pick_strs)}")

print(f"\n{'=' * 65}")
print(f"  NOT COVERED — no pool champ in counter list ({len(not_covered)})")
print(f"{'=' * 65}")
for enemy in sorted(not_covered):
    print(f"  vs {enemy}")

# --- Redundancy ---
print(f"\n{'=' * 65}")
print(f"  REDUNDANCY — enemies covered by 2+ of your champs")
print(f"{'=' * 65}")
for enemy in sorted(covered.keys()):
    if len(covered[enemy]) >= 2:
        picks = covered[enemy]
        pick_strs = [f"{champ} ({wr}%)" for champ, wr in sorted(picks, key=lambda x: x[1])]
        print(f"  vs {enemy:<20} → {', '.join(pick_strs)}")

# --- Per-champ workload ---
print(f"\n{'=' * 65}")
print(f"  PER-CHAMP WORKLOAD — how many enemies each champ covers")
print(f"{'=' * 65}")
for champ in sorted(POOL):
    enemies = [e for e, picks in covered.items() if any(c == champ for c, _ in picks)]
    print(f"  {champ:<12} covers {len(enemies)} enemies: {', '.join(sorted(enemies))}")
