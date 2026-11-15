LoadIQ: Priority-Driven Delivery Load Optimisation Engine
Team

SURAJ B (1AT24AI102)  SWORUP ACHARYA (1AT24AI103) , Python track

How to run

python main.py

(Python 3.8 or newer, no extra libraries needed.)

Features that work

Core

Record parcels with weight, volume and priority (priority 1-5, 5 = urgent; input is validated: no blanks, no duplicate IDs, no zero/negative/non-numeric values)
Record vans with weight and volume capacity
Assign parcels to vans, highest priority first (lighter parcel first on ties), never exceeding weight or volume capacity (greedy first-fit)
List parcels that could not be loaded, with the reason for each
Print a load sheet per van with total weight and volume used (and % of capacity)

Stretch 6. Compare a priority-first plan with a value-per-weight plan (also shows a balanced plan) in one table 7. Balance load across vans as evenly as possible (least-loaded-van-that-fits rule, menu option 6)

Approach

Greedy heuristic: sort parcels by priority, then place each in the first van with enough remaining weight AND volume. This is a 2-constraint knapsack variant (NP-hard), so greedy is fast but not guaranteed optimal.

Sample run
=== LoadIQ: Priority-Driven Delivery Load Optimisation ===

1. Add parcel   2. Add van   3. List data
4. Run priority-first plan (load sheets + unloaded)
5. Compare plans   6. Balanced plan   7. Load demo data   0. Exit
Choice: Demo data loaded: 10 parcels, 2 vans.

1. Add parcel   2. Add van   3. List data
4. Run priority-first plan (load sheets + unloaded)
5. Compare plans   6. Balanced plan   7. Load demo data   0. Exit
Choice: 
===== LOAD SHEETS: Priority-first =====

Van VAN-A
  Parcel     Wt(kg)  Vol(m3)  Pri
  P6           30.0     0.40    5
  P1           40.0     0.50    5
  P9           55.0     0.80    5
  P8           10.0     0.10    2
  P4           15.0     0.20    1
  Total weight: 150.0 / 150.0 kg (100%)
  Total volume: 2.00 / 3.00 m3 (67%)

Van VAN-B
  Parcel     Wt(kg)  Vol(m3)  Pri
  P3           60.0     0.90    4
  P10          45.0     0.60    3
  Total weight: 105.0 / 120.0 kg (88%)
  Total volume: 1.50 / 2.00 m3 (75%)

UNLOADED PARCELS (Priority-first)
  P7       Pri 4, 120.0kg, 2.50m3 -> All vans that could carry it were already full (not enough remaining capacity)
  P5       Pri 3, 80.0kg, 1.20m3 -> All vans that could carry it were already full (not enough remaining capacity)
  P2       Pri 2, 25.0kg, 0.30m3 -> All vans that could carry it were already full (not enough remaining capacity)

Summary: 7/10 loaded, priority score 25, high-priority (4-5) left behind: 1

1. Add parcel   2. Add van   3. List data
4. Run priority-first plan (load sheets + unloaded)
5. Compare plans   6. Balanced plan   7. Load demo data   0. Exit
Choice: 
===== PLAN COMPARISON =====
Plan                         Loaded PriScore  HighLeft  AvgUtil%   Spread%
Priority-first                 7/10       25         1      93.8      12.5
Value-per-weight               7/10       24         1      85.4      29.2
Priority-first + balanced      7/10       25         1      94.2       5.0
(Spread = difference between fullest and emptiest van; lower = more even.)

1. Add parcel   2. Add van   3. List data
4. Run priority-first plan (load sheets + unloaded)
5. Compare plans   6. Balanced plan   7. Load demo data   0. Exit
Choice: Goodbye.
