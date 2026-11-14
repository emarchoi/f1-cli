import random
import sys
from data_manager import DataManager
from models import Championship

def main():
    championship = DataManager.load_game()
    
    while True:
        print("\n--- F1 2026 Season Simulation ---")
        print(f"Current Progress: Round {championship.current_round}/{len(championship.tracks)}")
        if championship.current_round < len(championship.tracks):
            next_track = championship.tracks[championship.current_round]
            print(f"Next Race: {next_track.track_name}, {next_track.country}")
        else:
            print("Season Finished!")

        print("\n1. View Current Standings")
        print("2. Simulate Next Race")
        print("3. Reset Season")
        print("4. Save and Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == "1":
            display_standings(championship)
        elif choice == "2":
            if championship.current_round < len(championship.tracks):
                results = simulate_race(championship)
                display_race_results(results)

                if championship.current_round == len(championship.tracks):
                    drivers, constructors = get_standings(championship)
                    print(f"\n{drivers[0].name} wins the Drivers' Championship!")
                    print(f"{constructors[0].name} wins the Constructors' Championship!")
            else:
                print("The season is already over!")
        elif choice == "3":
            confirm = input("Are you sure you want to reset the season? (y/n): ")
            if confirm.lower() == "y":
                reset_data(championship)
                print("Season reset successful.")
        elif choice == "4":
            DataManager.save_game(championship)
            print("Game saved. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice, please try again.")

def simulate_race(championship):
    if championship.current_round >= len(championship.tracks):
        return []

    track = championship.tracks[championship.current_round]
    scores = []
    
    for driver in championship.drivers:
        constructor = championship.get_constructor(driver.constructor_name)
        # Performance logic: Driver skill + 0.5 * Constructor power + random factor
        power_bonus = constructor.power * 0.5 if constructor else 0
        variance = random.uniform(-5, 5)
        score = driver.skill + power_bonus + variance
        scores.append((driver, score))
    
    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    
    results = [s[0] for s in scores]
    
    # Award points (standard F1 points system)
    points_map = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    for i in range(min(len(results), len(points_map))):
        driver = results[i]
        pts = points_map[i]
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
            wcc_winner = max(championship.constructor, key=lambda c: c.points)
            wcc_winner.wcc +=1

    return results

def get_standings(championship):
    # Sort drivers and constructors by points
    sorted_drivers = sorted(championship.drivers, key=lambda x: x.points, reverse=True)
    sorted_constructors = sorted(championship.constructors, key=lambda x: x.points, reverse=True)
    return sorted_drivers, sorted_constructors

def reset_data(championship):
    for driver in championship.drivers:
        driver.points = 0
    for constructor in championship.constructors:
        constructor.points = 0
    championship.current_round = 0
    return championship

def display_standings(championship):
    drivers, constructors = get_standings(championship)
    
    print("\n--- Driver Standings ---")
    for i, d in enumerate(drivers, 1):
        print(f"{i}. {d.name:20} | {d.constructor_name:30} | {d.points} pts")
        
    print("\n--- Constructor Standings ---")
    for i, c in enumerate(constructors, 1):
        print(f"{i}. {c.name:30} | {c.points} pts")

def display_race_results(results):

    points_map = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

    print("\n--- Race Results ---")
    for i, driver in enumerate(results[:10], 1):

        pts = points_map[i - 1]
        print(f"{i:2}. {driver.name:20} | +{pts} pts")
    if len(results) > 10:
        for i, driver in enumerate(results[10:], 11):
            print(f"{i:2}. {driver.name:20} | 0 pts")

if __name__ == "__main__":
    main()
