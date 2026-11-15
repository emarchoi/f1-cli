# for helper functions

POINTS_MAP = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

def display_standings(championship):

    drivers = sorted(championship.drivers, key=lambda d: (d.points), reverse=True)
    constructors = sorted(championship.constructors, key=lambda c: (c.points), reverse=True)

    print("\n--- Driver Standings ---")
    for i, d in enumerate(drivers, 1):
        print(f"{i:2}. {d.name:20} | {d.constructor_name:30} | {d.points:3} pts")

    print("\n--- Constructor Standings ---")
    for i, c in enumerate(constructors, 1):
        print(f"{i:2}. {c.name:30} | {c.points:3} pts")