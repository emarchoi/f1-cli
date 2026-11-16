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
    return "Leader" if diff == 0 else f"+{diff}"

def display_standings(championship):

    drivers = sorted(championship.drivers, key=lambda d: (d.points), reverse=True)
    constructors = sorted(championship.constructors, key=lambda c: (c.points), reverse=True)

    leading_driver = drivers[0].points if drivers else 0
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

    print(f"\n{'+'}{'-' * 76}{'+'}")
    print(f"|{'DRIVERS STANDING':^76}|")
    print(f"{'+'}{'-' * 76}{'+'}")
    print(tabulate(drivers_rows,
                   headers=["POS", "DRIVER", "CONSTRUCTOR", "PTS", "GAP"],
                   tablefmt="grid", stralign="left", numalign="right"))

    leading_constructor = constructors[0].points if constructors else 0
    constructors_rows = [
        [
            i,
            c.name,
            c.engine,
            c.points,
            format_points_diff(c.points, leading_constructor),
        ]
        for i, c in enumerate(constructors, 1)
    ]

    print(f"\n{'+'}{'-' * 72}{'+'}")
    print(f"|{'CONSTRUCTORS STANDING':^72}|")
    print(f"{'+'}{'-' * 72}{'+'}")
    print(tabulate(constructors_rows,
                   headers=["POS", "TEAM", "ENGINE", "PTS", "GAP"],
                   tablefmt="grid", stralign="left", numalign="right"))

def display_qualifying_results(qualifying_results):

    quali = [
        [
            f"P{entry['grid_pos']}",
            entry["driver"].name,
            entry["driver"].constructor_name,
            f"+{entry['grid_bonus']:.2f}",
        ]
        for entry in qualifying_results
    ]

    print("\n===== QUALIFYING CLASSIFICATION =====")
    print(tabulate(quali,
                   headers=["GRID", "DRIVER", "CONSTRUCTOR", "BONUS"],
                   tablefmt="grid", stralign="left", numalign="right"))

def display_race_results(results):

    race = []
    for i, entry in enumerate(results, 1):
  
        grid_pos = entry["grid_pos"]
        driver = entry["driver"]

        pts = POINTS_MAP[i - 1] if i <= len(POINTS_MAP) else 0
        pts_str = f"+{pts} pts" if pts > 0 else "0 pts"

        race.append([
            i,
            f"P{grid_pos}",
            driver.name,
            driver.constructor_name,
            entry["total_time_display"],
            pts_str,
        ])

    print("\n===== RACE CLASSIFICATION =====")
    print(tabulate(race, 
                    headers=["POS", "GRID POS", "DRIVER", "CONSTRUCTOR", "TIME", "POINTS"],
                    tablefmt="grid", stralign="left", numalign="right"))

def display_championships(championship):
    # can add d.points c.points for like "Current Season Points"

    drivers = sorted(championship.drivers, key=lambda d: (d.wdc), reverse=True)
    drivers_row = [
        [
            d.name,
            d.constructor_name,
            d.wdc,
        ]
        for i, d in enumerate(drivers, 1)
    ]
    print("\n===== WORLD DRIVERS' CHAMPIONSHIP (WDC) =====")
    print(tabulate(drivers_row,
                   headers=["DRIVER", "CONSTRUCTOR", "WDC"],
                   tablefmt="grid", stralign="left", numalign="right"))


    constructors = sorted(championship.constructors, key=lambda c: (c.wcc), reverse=True)
    constructors_row = [
        [
            c.name,
            c.engine,
            c.wcc,
        ]
        for i, c in enumerate(constructors, 1)
    ]
    print("\n===== WORLD CONSTRUCTORS' CHAMPIONSHIP (WCC) =====")
    print(tabulate(constructors_row,
                   headers=["CONSTRUCTOR", "ENGINE", "WCC"],
                   tablefmt="grid", stralign="left", numalign="right"))