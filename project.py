import random
import sys
from data_manager import DataManager
from helper import (
    POINTS_MAP,
    display_championships,
    display_qualifying_results,
    display_race_results,
    display_standings,
    format_race_time,
    tabulate,
    countdown,
)

def main():
    championship = DataManager.load_game()

    ''' To-do: 1. Adding like thread sleep, eg. pause for 5secs for quali and race
               2. Reset data specific (revert to original/reset all to 0) in the future
               3. Double check spacing, for feedbacks etc.'''
    
    while True:

        title = f"F1 SEASON {championship.season_count + 1} SIMULATION"
        print(f"\n{'+'}{'-' * 70}{'+'}")
        print(f"|{title:^70}|")
        print(f"{'+'}{'-' * 70}{'+'}")

        if championship.current_round < len(championship.tracks):
            next_track = championship.tracks[championship.current_round]
            next_race = f"R{championship.current_round + 1} - {next_track.track_name}, {next_track.country}"
            option_3 = "Simulate Next Race"
        else:
            next_race = "Season Finished"
            option_3 = "Start Next Season"

        season_data = [
            ["Current Progress", f"Round {championship.current_round}/{len(championship.tracks)}"],
            ["Next Race", next_race],
            ["", ""],
            [1, "View Current Standings"],
            [2, "View Championship Titles"],
            [3, option_3],
            [4, "Reset Season"],
            [5, "Reset Game Data"],
            [6, "Save and Exit"],
        ]

        print(tabulate(season_data, tablefmt="grid"))
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            display_standings(championship)

        elif choice == "2":
            display_championships(championship)

        elif choice == "3":
            if championship.current_round < len(championship.tracks):

                qualifying_results = simulate_qualifying(championship)
                display_qualifying_results(qualifying_results)

                results = simulate_race(championship, qualifying_results)
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

def simulate_qualifying(championship, delay=5):
    if championship.current_round >= len(championship.tracks):
        return []

    track = championship.tracks[championship.current_round]
    print(f"\n+{'-' * 70}+")
    print(f"| {'Simulating Qualifying at: ' + track.track_name:^68} |")
    print(f"+{'-' * 70}+") 
    if delay > 0:
        countdown("Simulating Qualifying", delay)

    qualifying = []
    for driver in championship.drivers:
        constructor = championship.get_constructor(driver.constructor_name)
        power_bonus = constructor.power * 0.5 if constructor else 0
        variance = random.uniform(-4, 4)
        quali_score = driver.skill + power_bonus + variance
        qualifying.append({
            "driver": driver,
            "quali_score": quali_score,
        })

    qualifying.sort(key=lambda x: x["quali_score"], reverse=True)

    total_drivers = len(qualifying)
    for grid_pos, entry in enumerate(qualifying, 1):
        entry["grid_pos"] = grid_pos
        entry["grid_bonus"] = round((total_drivers - grid_pos) * 0.25, 2)

    return qualifying

def simulate_race(championship, quali_results=None, delay=5):
    if championship.current_round >= len(championship.tracks):
        return []

    if quali_results is None:
        quali_results = simulate_qualifying(championship)

    quali_dict = {
        entry["driver"].name: (entry["grid_pos"], entry["grid_bonus"])
        for entry in quali_results
    }

    track = championship.tracks[championship.current_round]
    race_entries = []
    
    for driver in championship.drivers:
        constructor = championship.get_constructor(driver.constructor_name)
        power_bonus = constructor.power * 0.5 if constructor else 0
        grid_pos, grid_bonus = quali_dict.get(driver.name, (len(championship.drivers), 0.0))
        variance = random.uniform(-5, 5)

        score = driver.skill + power_bonus + grid_bonus + variance
        pace = max(1.0, track.time + (145 - score) * 0.03)
        total_time = pace * track.laps

        race_entries.append({
            "driver": driver,
            "grid_pos": grid_pos,
            "grid_bonus": grid_bonus,
            "total_time": total_time,
            "total_time_display": format_race_time(total_time),
        })
    
    race_entries.sort(key=lambda x: x["total_time"])
    
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

if __name__ == "__main__":
    main()
