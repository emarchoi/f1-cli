# for helper functions
from tabulate import tabulate

POINTS_MAP = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

def format_race_time(seconds):

    total_ms = round(seconds * 1000)
    hours = total_ms // 3_600_000
    rem = total_ms % 3_600_000
    minutes = rem // 60_000
    rem = rem % 60_000
    secs = rem // 1000
    ms = rem % 1000

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}:{ms:03d}"
    return f"{minutes}:{secs:02d}:{ms:03d}"

def format_points_diff(points, leader_points):
    diff = leader_points - points
    return "Leader" if diff == 0 else str(diff)

def display_standings(championship):

    drivers = sorted(championship.drivers, key=lambda d: (d.points), reverse=True)
    constructors = sorted(championship.constructors, key=lambda c: (c.points), reverse=True)

    leading_driver = drivers[0].points if drivers else 9
    drivers_rows = [
        [
            i,
            d.name,
            d.constructor_name,
            d.points,
            format_points_diff(d.points, leading_driver),
        ]
        for i, d in enumerate(drivers, 1)
    ]

    print("===== DRIVER STANDINGS =====")
    print(tabulate(drivers_rows,
                   headers=["POS", "DRIVER", "CONSTRUCTOR", "PTS", "DIFF"],
                   tablefmt="grid", stralign="left", numalign="right"))

    leading_constructor = constructors[0].points if constructors else 0
    constructors_rows = [
        [
            i,
            c.name,
            c.engine,
            c.points,
            format_points_diff(c.points, leading_constructor)
        ]
        for i, c in enumerate(constructors, 1)
    ]

    print("\n===== CONSTRUCTORS STANDINGS =====")
    print(tabulate(constructors_rows,
                   headers=["POS", "TEAM", "ENGINE", "PTS", "DIFF"],
                   tablefmt="grid", stralign="left", numalign="right"))

def display_qualifying_results(qualifying_results):

    print("\n--- Qualifying Grid ---")
    print(f"{'Grid':<5} {'Driver':<20} {'Constructor':<30} {'Race Bonus'}")
    print("-" * 69)
    for entry in qualifying_results:
        driver = entry["driver"]
        print(
            f"P{entry['grid_pos']:<4} {driver.name:<20} "
            f"{driver.constructor_name:<30} +{entry['grid_bonus']:.2f}"
        )

def display_race_results(results):

    print("\n--- Race Results ---")
    print(f"{'Pos':<4} {'Driver':<20} {'Total Time':<14} {'Points'}")
    print("-" * 48)
    for i, entry in enumerate(results, 1):
        driver = entry["driver"]
        pts = POINTS_MAP[i - 1] if i <= len(POINTS_MAP) else 0
        pts_str = f"+{pts} pts" if pts > 0 else "0 pts"
        print(f"{i:2}.  {driver.name:<20} {entry['total_time_display']:<14} {pts_str}")

def display_championships(championship):
    # can add d.points c.points for like "Current Season Points"

    sorted_drivers = sorted(championship.drivers, key=lambda d: (d.wdc), reverse=True)
    sorted_constructors = sorted(championship.constructors, key=lambda c: (c.wcc), reverse=True)

    print("\n--- World Drivers' Championship (WDC) Counts ---")
    for i, d in enumerate(sorted_drivers, 1):
        print(f"{i:2}. {d.name:20} | {d.constructor_name:30} | {d.wdc} WDC")

    print("\n--- World Constructors' Championship (WCC) Counts ---")
    for i, c in enumerate(sorted_constructors, 1):
        print(f"{i:2}. {c.name:30} | {c.wcc} WCC")