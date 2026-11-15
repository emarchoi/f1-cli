# for helper functions

POINTS_MAP = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

def race_time(seconds):

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

def display_standings(championship):

    drivers = sorted(championship.drivers, key=lambda d: (d.points), reverse=True)
    constructors = sorted(championship.constructors, key=lambda c: (c.points), reverse=True)

    print("\n--- Driver Standings ---")
    for i, d in enumerate(drivers, 1):
        print(f"{i:2}. {d.name:20} | {d.constructor_name:30} | {d.points:3} pts")

    print("\n--- Constructor Standings ---")
    for i, c in enumerate(constructors, 1):
        print(f"{i:2}. {c.name:30} | {c.points:3} pts")

# def display_race_results