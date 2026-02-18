import json

CURRENT_POOL = {"Jax", "Camille", "Garen", "Illaoi"}
NEW_POOL = {"Jax", "Camille", "Garen", "Illaoi", "Irelia"}

with open("counters_under50.json") as f:
    data = json.load(f)

TOP_LANERS = sorted(data.keys())

# Build coverage maps
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

# What does Irelia specifically add?
irelia_adds = set(new_cov.keys()) - set(old_cov.keys())
irelia_overlap = set()
for enemy in new_cov:
    if enemy in old_cov:
        new_champs = {c for c, _ in new_cov[enemy]}
        old_champs = {c for c, _ in old_cov[enemy]}
        if "Irelia" in new_champs - old_champs:
            irelia_overlap.add(enemy)

print("=" * 70)
print(f"  ADDING IRELIA TO YOUR POOL")
print(f"  Old: {len(old_cov)}/60 covered → New: {len(new_cov)}/60 covered")
print(f"  Irelia fills {len(irelia_adds)} NEW gaps")
print("=" * 70)

if irelia_adds:
    print(f"\n  NEW matchups Irelia covers (previously blank):")
    for enemy in sorted(irelia_adds):
        for c, wr in new_cov[enemy]:
            if c == "Irelia":
                print(f"    vs {enemy:<20} Irelia at {wr}% WR")

if irelia_overlap:
    print(f"\n  Matchups where Irelia adds redundancy (already covered):")
    for enemy in sorted(irelia_overlap):
        old_picks = [f"{c} ({wr}%)" for c, wr in old_cov[enemy]]
        for c, wr in new_cov[enemy]:
            if c == "Irelia":
                print(f"    vs {enemy:<20} Irelia ({wr}%) — already had: {', '.join(old_picks)}")

# Print updated full pick sheet
still_blank = set(TOP_LANERS) - set(new_cov.keys())
print(f"\n{'=' * 70}")
print(f"  STILL BLANK ({len(still_blank)} matchups with no counter)")
print(f"{'=' * 70}")
for enemy in sorted(still_blank):
    print(f"  vs {enemy}")
