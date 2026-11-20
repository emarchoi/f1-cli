# F1 CLI-Game Simulator

**F1 CLI-Game Simulator** is a simple and fun command-line Formula 1 championship simulator developed as my final project for CS50's Introduction to Programming with Python (CS50P).

The simulation models the latest Formula 1 season across 24 Grand Prix rounds, 11 constructors, and 22 drivers. This command-line game can simulate full race weekends, complete with a qualifying session that awards starting grid bonuses and a Grand Prix race that computes total race times from track lap counts and base lap times—while tracking World Drivers' Championship (WDC) and World Constructors' Championship (WCC) points and titles across seasons.

#### Development Background:
- I originally developed this project in Java as a practice for Object-Oriented Programming (OOP). The initial implementation used data structures such as Arrays and ArrayLists, along with `.txt` files for data storage. However, the project was never completed, so I eventually decided to refactor it using Python.
- The Python version retains the Object-Oriented Programming (OOP) architecture. However, I switched to `.json` files for data storage to make data insertion and retrieval easier and more efficient. Lastly, I incorporated the `tabulate` library to display cleanly formatted tables.

#### Teck-Stack Used:
1. Python

#### Fun Features:
* **Two-Stage Race Weekend Simulation:**
  * **Qualifying:** Evaluates each driver's skill, constructor power rating, and random variance to set the starting grid (`P1`–`P22`). Higher grid positions earn a tapered race score bonus (`+0.25` per spot ahead of last place).
  * **Grand Prix Race:** Combines driver skill, constructor power, qualifying grid bonus, and race-day variance to calculate each driver's pace relative to the circuit's base lap time (`track.time`) multiplied by total race laps (`track.laps`). Finishers are ranked by total race time (`H:MM:SS.mmm`) and awarded standard F1 points (`25-18-15-12-10-8-6-4-2-1`).
  > **Note:** Pace calculations are just mathematical calculations I came up with.
* **Championship & Title Tracking:** Automatically updates driver and constructor standings after every round and awards WDC and WCC titles once all 24 rounds are finished.
* **Persistent Save State `game_file/f1_cli_data.json`:** Automatically seeds initial season data from static dictionaries on first launch and saves progress, points, and career championship counts to JSON.
* **Formatted Terminal Tables:** Uses `tabulate` to render clean, readable, and properly aligned classification tables.


#### Requirements and Prerequisites:


#### To-do:
- Requirements/Prerequisites
- Play/Contri - Cloning
- Features
- Structure
- Tech-Stack Used
- Intellectual Property