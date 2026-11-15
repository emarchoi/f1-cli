import random
import sys
from data_manager import DataManager
from helper import (
    POINTS_MAP,
    display_championships,
    display_race_results,
    display_standings,
    race_time,
)

def main():
    championship = DataManager.load_game()

    ''' To-do: 1. Add Qualifying + Bonus
               2. Add Lap Times from tracks[laps] and tracks[time] make it like f1 time 
               3. Table formatting'''
    
    while True:

        print(f"\n--- F1 2026 Season {championship.season_count + 1} Simulation ---")
        print(f"Current Progress: Round {championship.current_round}/{len(championship.tracks)}")
        if championship.current_round < len(championship.tracks):
            next_track = championship.tracks[championship.current_round]
            print(f"Next Race: {next_track.track_name}, {next_track.country}")
        else:
            print("Season Finished!")

        print("\n1. View Current Standings")
        print("2. View WDC and WCC Count")

        if championship.current_round == len(championship.tracks):
            print("3. Start Next Season")
        else:
            print("3. Simulate Next Race")

        print("---------------------------")
        print("4. Reset Season")
        print("5. Reset Game Data")
        print("6. Save and Exit")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == "1":
            display_standings(championship)

        if choice == "2":
            display_championships(championship)

        elif choice == "3":
            if championship.current_round < len(championship.tracks):

                results = simulate_race(championship)
                display_race_results(results)

                if championship.current_round == len(championship.tracks):
                    drivers, constructors = get_standings(championship)
                    print(f"\n{drivers[0].name} wins the Drivers' Championship!")
                    print(f"{constructors[0].name} wins the Constructors' Championship!")

                    next_season(championship)

            else:
                print("The season is already over!")

                next_season(championship)

        elif choice == "4":
            confirm = input("Are you sure you want to reset the season? (y/n): ")
            if confirm.lower() == "y":
                reset_season(championship)
                print("Season reset successful.")
        elif choice == "5":
            confirm = input("Reset game whole data? (y/n): ")
            if confirm.lower() == "y":
                reset_data(championship)
                DataManager.save_game(championship)
                print("Game data reset successful.")
                sys.exit()
        elif choice == "6":
            DataManager.save_game(championship)
            print("Game saved. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice, please try again.")

def simulate_race(championship):
    if championship.current_round >= len(championship.tracks):
        return []

    track = championship.tracks[championship.current_round]
    race_entries = []
    
    for driver in championship.drivers:
        constructor = championship.get_constructor(driver.constructor_name)
        power_bonus = constructor.power * 0.5 if constructor else 0
        variance = random.uniform(-5, 5)
        score = driver.skill + power_bonus + variance

        pace = max(1.0, track.time + (145 - score) * 0.03)
        total_time = pace * track.laps

        race_entries.append({
            "driver": driver,
            "total_time": total_time,
            "total_time_display": race_time(total_time),
        })
    
    race_entries.sort(key=lambda :x x["total_time"])
    
    for i in range(min(len(race_entries), len(POINTS_MAP))):
        
        driver = race_entries[i]["driver"]
        pts = POINTS_MAP[i]
        driver.points += pts
        
        constructor = championship.get_constructor(driver.constructor_name)
        if constructor:
            constructor.points += pts
            
    championship.current_round += 1

    if championship.current_round == len(championship.tracks):
        if championship.drivers:
            wdc_winner = max(championship.drivers, key=lambda d: d.points)
            wdc_winner.wdc += 1

        if championship.constructors:
            wcc_winner = max(championship.constructors, key=lambda c: c.points)
            wcc_winner.wcc +=1

    return race_entries

def get_standings(championship):

    sorted_drivers = sorted(championship.drivers, key=lambda x: x.points, reverse=True)
    sorted_constructors = sorted(championship.constructors, key=lambda x: x.points, reverse=True)
    return sorted_drivers, sorted_constructors

def reset_season(championship):
    for driver in championship.drivers:
        driver.points = 0
    for constructor in championship.constructors:
        constructor.points = 0
    championship.current_round = 0
    return championship

def next_season(championship):
    next_season = input("Start next season? (y/n): ").strip()

    if next_season.lower() == "y":
        reset_season(championship)
        championship.season_count += 1


def reset_data(championship):
    for driver in championship.drivers:
        driver.points = 0
        driver.wdc = 0
    for constructor in championship.constructors:
        constructor.points = 0
        constructor.wcc = 0
    championship.current_round = 0
    championship.season_count = 0
    return championship

# def display_standings(championship):
#     drivers, constructors = get_standings(championship)
    
#     print("\n--- Driver Standings ---")
#     for i, d in enumerate(drivers, 1):
#         print(f"{i}. {d.name:20} | {d.constructor_name:30} | {d.points} pts")
        
#     print("\n--- Constructor Standings ---")
#     for i, c in enumerate(constructors, 1):
#         print(f"{i}. {c.name:30} | {c.points} pts")

# def display_wcc_wdc(championship):
#     # can add d.points c.points for like "Current Season Points"

#     sorted_drivers = sorted(championship.drivers, key=lambda d: (d.wdc), reverse=True)
#     sorted_constructors = sorted(championship.constructors, key=lambda c: (c.wcc), reverse=True)

#     print("\n--- World Drivers' Championship (WDC) Counts ---")
#     for i, d in enumerate(sorted_drivers, 1):
#         print(f"{i:2}. {d.name:20} | {d.constructor_name:30} | {d.wdc} WDC")

#     print("\n--- World Constructors' Championship (WCC) Counts ---")
#     for i, c in enumerate(sorted_constructors, 1):
#         print(f"{i:2}. {c.name:30} | {c.wcc} WCC")

# def display_race_results(results):

#     points_map = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

#     print("\n--- Race Results ---")
#     for i, driver in enumerate(results[:10], 1):

#         pts = points_map[i - 1]
#         print(f"{i:2}. {driver.name:20} | +{pts} pts")
#     if len(results) > 10:
#         for i, driver in enumerate(results[10:], 11):
#             print(f"{i:2}. {driver.name:20} | 0 pts")

if __name__ == "__main__":
    main()
