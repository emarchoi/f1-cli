import json
import os
from models import Driver, Constructor, Track, Championship
from game_resources.drivers import drivers as raw_drivers
from game_resources.constructors import constructors as raw_constructors
from game_resources.tracks import tracks as raw_tracks

class DataManager:
    SAVE_FILE = "season_2026.json"

    @classmethod
    def load_game(cls):
        if os.path.exists(cls.SAVE_FILE):
            try:
                with open(cls.SAVE_FILE, "r") as f:
                    data = json.load(f)
                
                constructors = [Constructor(**c) for c in data["constructors"]]
                drivers = [Driver(**d) for d in data["drivers"]]
                tracks = [Track(**t) for t in data["tracks"]]
                
                return Championship(
                    drivers=drivers,
                    constructors=constructors,
                    tracks=tracks,
                    current_round=data["current_round"]
                )
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading save file: {e}. Seeding new data.")
                return cls.seed_initial_data()
        else:
            return cls.seed_initial_data()

    @classmethod
    def save_game(cls, championship):
        with open(cls.SAVE_FILE, "w") as f:
            json.dump(championship.to_dict(), f, indent=4)

    @classmethod
    def seed_initial_data(cls):
        constructors_list = []
        # Map key to full name for driver initialization
        key_to_name = {}
        
        for key, data in raw_constructors.items():
            c = Constructor(
                name=data["name"],
                engine=data["engine"],
                power=data["power"],
                wcc=data.get("wcc", 0)
            )
            constructors_list.append(c)
            key_to_name[key] = data["name"]

        drivers_list = []
        for team_key, drivers_in_team in raw_drivers.items():
            for d_data in drivers_in_team:
                d = Driver(
                    name=d_data["name"],
                    skill=d_data["skill"],
                    constructor_name=key_to_name[team_key],
                    wdc=d_data.get("wdc", 0)
                )
                drivers_list.append(d)

        tracks_list = []
        # Sort tracks by round key to ensure correct order
        for track_key in sorted(raw_tracks.keys()):
            t_data = raw_tracks[track_key]
            t = Track(
                country=t_data["country"],
                track_name=t_data["track_name"],
                laps=t_data["laps"],
                time=t_data["time"]
            )
            tracks_list.append(t)

        return Championship(
            drivers=drivers_list,
            constructors=constructors_list,
            tracks=tracks_list,
            current_round=0
        )
