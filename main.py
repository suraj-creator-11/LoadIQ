#LoadIQ: Priority-Driven Delivery Load Optimisation



class Parcel:
    def __init__(self, pid, weight, volume, priority):
        self.id, self.w, self.v, self.p = pid, weight, volume, priority


class Van:
    def __init__(self, vid, max_w, max_v):
        self.id, self.max_w, self.max_v = vid, max_w, max_v
        self.used_w = 0.0
        self.used_v = 0.0
        self.loaded = []

    def fits(self, x):
        return self.used_w + x.w <= self.max_w and self.used_v + x.v <= self.max_v

    def load(self, x):
        self.loaded.append(x)
        self.used_w += x.w
        self.used_v += x.v

    def util(self):
        return max(self.used_w / self.max_w, self.used_v / self.max_v)


class Plan:
    def __init__(self, name, vans):
        self.name = name
        self.vans = vans
        self.unloaded = []
        self.reason = {}

    def loaded_count(self):
        return sum(len(v.loaded) for v in self.vans)

    def score(self):
        return sum(x.p for v in self.vans for x in v.loaded)

    def high_left(self):
        return sum(1 for x in self.unloaded if x.p >= 4)

    def avg_util(self):
        return sum(v.util() for v in self.vans) / len(self.vans) * 100

    def spread(self):
        u = [v.util() for v in self.vans]
        return (max(u) - min(u)) * 100


parcels = []
vans = []


# ---------- validated input ----------
def read_positive(msg):
    while True:
        try:
            d = float(input(msg).strip())
            if d > 0:
                return d
            print("  Error: value must be greater than 0.")
        except ValueError:
            print("  Error: enter a valid number.")


def read_int(msg, lo, hi):
    while True:
        try:
            n = int(input(msg).strip())
            if lo <= n <= hi:
                return n
            print(f"  Error: enter a number between {lo} and {hi}.")
        except ValueError:
            print("  Error: enter a whole number.")


def read_id(msg, existing):
    while True:
        s = input(msg).strip()
        if not s:
            print("  Error: ID cannot be empty.")
        elif any(e.id.lower() == s.lower() for e in existing):
            print("  Error: ID already exists.")
        else:
            return s


# ---------- features 1 & 2 ----------
def add_parcel():
    pid = read_id("Parcel ID: ", parcels)
    w = read_positive("Weight (kg): ")
    v = read_positive("Volume (m3): ")
    p = read_int("Priority (1=low ... 5=urgent): ", 1, 5)
    parcels.append(Parcel(pid, w, v, p))
    print(f"Parcel {pid} recorded.")


def add_van():
    vid = read_id("Van ID: ", vans)
    w = read_positive("Weight capacity (kg): ")
    v = read_positive("Volume capacity (m3): ")
    vans.append(Van(vid, w, v))
    print(f"Van {vid} recorded.")


def list_data():
    print(f"\nPARCELS ({len(parcels)})")
    print(f"{'ID':<8} {'Wt(kg)':>8} {'Vol(m3)':>8} {'Pri':>4}")
    for x in parcels:
        print(f"{x.id:<8} {x.w:>8.1f} {x.v:>8.2f} {x.p:>4}")
    print(f"VANS ({len(vans)})")
    print(f"{'ID':<8} {'MaxWt(kg)':>10} {'MaxVol(m3)':>10}")
    for x in vans:
        print(f"{x.id:<8} {x.max_w:>10.1f} {x.max_v:>10.2f}")


# ---------- feature 3: greedy assignment ----------
def explain(x):
    mw = max(v.max_w for v in vans)
    mv = max(v.max_v for v in vans)
    alone = any(x.w <= v.max_w and x.v <= v.max_v for v in vans)
    if x.w > mw:
        return f"Weight {x.w}kg exceeds largest van capacity ({mw}kg)"
    if x.v > mv:
        return f"Volume {x.v}m3 exceeds largest van capacity ({mv}m3)"
    if not alone:
        return "No single van has enough weight AND volume capacity"
    return "All vans that could carry it were already full (not enough remaining capacity)"


def build(name, key, balance=False):
    plan = Plan(name, [Van(v.id, v.max_w, v.max_v) for v in vans])
    for x in sorted(parcels, key=key):
        candidates = [v for v in plan.vans if v.fits(x)]
        if candidates:
            # first-fit, or least-loaded van that fits when balancing
            chosen = min(candidates, key=lambda v: v.util()) if balance else candidates[0]
            chosen.load(x)
        else:
            plan.unloaded.append(x)
            plan.reason[x.id] = explain(x)
    return plan


def by_priority(x):          # high priority first, lighter first on ties
    return (-x.p, x.w)


def by_value_per_weight(x):  # priority points per kg, best first
    return -(x.p / x.w)


# ---------- features 4 & 5 ----------
def print_unloaded(plan):
    print(f"\nUNLOADED PARCELS ({plan.name})")
    if not plan.unloaded:
        print("  None - every parcel was loaded.")
        return
    for x in plan.unloaded:
        print(f"  {x.id:<8} Pri {x.p}, {x.w:.1f}kg, {x.v:.2f}m3 -> {plan.reason[x.id]}")


def print_load_sheets(plan):
    print(f"\n===== LOAD SHEETS: {plan.name} =====")
    for v in plan.vans:
        print(f"\nVan {v.id}")
        print(f"  {'Parcel':<8} {'Wt(kg)':>8} {'Vol(m3)':>8} {'Pri':>4}")
        if not v.loaded:
            print("  (empty)")
        for x in v.loaded:
            print(f"  {x.id:<8} {x.w:>8.1f} {x.v:>8.2f} {x.p:>4}")
        print(f"  Total weight: {v.used_w:.1f} / {v.max_w:.1f} kg ({v.used_w / v.max_w * 100:.0f}%)")
        print(f"  Total volume: {v.used_v:.2f} / {v.max_v:.2f} m3 ({v.used_v / v.max_v * 100:.0f}%)")


def ready():
    if not parcels or not vans:
        print("Add at least one parcel and one van first.")
        return False
    return True


def run_plan(name, key, balance=False):
    if not ready():
        return
    plan = build(name, key, balance)
    print_load_sheets(plan)
    print_unloaded(plan)
    print(f"\nSummary: {plan.loaded_count()}/{len(parcels)} loaded, priority score "
          f"{plan.score()}, high-priority (4-5) left behind: {plan.high_left()}")


# ---------- stretch: comparison ----------
def compare():
    if not ready():
        return
    plans = [build("Priority-first", by_priority),
             build("Value-per-weight", by_value_per_weight),
             build("Priority-first + balanced", by_priority, True)]
    print("\n===== PLAN COMPARISON =====")
    print(f"{'Plan':<27} {'Loaded':>7} {'PriScore':>8} {'HighLeft':>9} {'AvgUtil%':>9} {'Spread%':>9}")
    for p in plans:
        loaded = f"{p.loaded_count()}/{len(parcels)}"
        print(f"{p.name:<27} {loaded:>7} {p.score():>8} {p.high_left():>9} {p.avg_util():>9.1f} {p.spread():>9.1f}")
    print("(Spread = difference between fullest and emptiest van; lower = more even.)")


def demo_data():
    parcels.clear()
    vans.clear()
    data = [("P1", 40, 0.5, 5), ("P2", 25, 0.3, 2), ("P3", 60, 0.9, 4), ("P4", 15, 0.2, 1),
            ("P5", 80, 1.2, 3), ("P6", 30, 0.4, 5), ("P7", 120, 2.5, 4), ("P8", 10, 0.1, 2),
            ("P9", 55, 0.8, 5), ("P10", 45, 0.6, 3)]
    for d in data:
        parcels.append(Parcel(*d))
    vans.append(Van("VAN-A", 150, 3.0))
    vans.append(Van("VAN-B", 120, 2.0))
    print("Demo data loaded: 10 parcels, 2 vans.")


def main():
    print("=== LoadIQ: Priority-Driven Delivery Load Optimisation ===")
    while True:
        print("\n1. Add parcel   2. Add van   3. List data")
        print("4. Run priority-first plan (load sheets + unloaded)")
        print("5. Compare plans   6. Balanced plan   7. Load demo data   0. Exit")
        ch = read_int("Choice: ", 0, 7)
        if ch == 1: add_parcel()
        elif ch == 2: add_van()
        elif ch == 3: list_data()
        elif ch == 4: run_plan("Priority-first", by_priority)
        elif ch == 5: compare()
        elif ch == 6: run_plan("Priority-first + balanced", by_priority, True)
        elif ch == 7: demo_data()
        else:
            print("Goodbye.")
            return


if __name__ == "__main__":
    main()
