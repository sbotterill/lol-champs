import json

CURRENT_POOL = {"Jax", "Camille", "Garen", "Illaoi", "Irelia"}
NEW_POOL = CURRENT_POOL | {"Gwen"}

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())

def get_coverage(pool):
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

old_cov = get_coverage(CURRENT_POOL)
new_cov = get_coverage(NEW_POOL)

gwen_adds = set(new_cov.keys()) - set(old_cov.keys())
gwen_overlap = set()
for enemy in new_cov:
    if enemy in old_cov:
        new_champs = {c for c, _ in new_cov[enemy]}
        old_champs = {c for c, _ in old_cov[enemy]}
        if "Gwen" in new_champs - old_champs:
            gwen_overlap.add(enemy)

print("=" * 70)
print(f"  ADDING GWEN TO YOUR POOL (Jax, Camille, Garen, Illaoi, Irelia)")
print(f"  Old: {len(old_cov)}/60 covered → New: {len(new_cov)}/60 covered")
print(f"  Gwen fills {len(gwen_adds)} NEW gaps")
print("=" * 70)

if gwen_adds:
    print(f"\n  NEW matchups Gwen covers (previously blank):")
    for enemy in sorted(gwen_adds):
        for c, wr in new_cov[enemy]:
            if c == "Gwen":
                print(f"    vs {enemy:<20} Gwen at {wr}% WR")

if gwen_overlap:
    print(f"\n  Matchups where Gwen adds redundancy (already covered):")
    for enemy in sorted(gwen_overlap):
        old_picks = [f"{c} ({wr}%)" for c, wr in old_cov[enemy]]
        for c, wr in new_cov[enemy]:
            if c == "Gwen":
                # Check if Gwen is actually better than existing best
                old_best_wr = old_cov[enemy][0][1]
                better = " ← UPGRADE" if wr < old_best_wr else ""
                print(f"    vs {enemy:<20} Gwen ({wr}%) — already had: {', '.join(old_picks)}{better}")

still_blank = set(TOP_LANERS) - set(new_cov.keys())
print(f"\n{'=' * 70}")
print(f"  STILL BLANK ({len(still_blank)} matchups with no counter)")
print(f"{'=' * 70}")
for enemy in sorted(still_blank):
    print(f"  vs {enemy}")
