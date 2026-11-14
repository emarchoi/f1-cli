class Constructor:
    def __init__(self, name, engine, power, wcc=0, points=0):
        self.name = name
        self.engine = engine
        self.power = power
        self.wcc = wcc
        self.points = points

    def __str__(self):
        return f"{self.name} ({self.engine}) - {self.points} pts"

    def to_dict(self):
        return {
            "name": self.name,
            "engine": self.engine,
            "power": self.power,
            "wcc": self.wcc,
            "points": self.points
        }


class Driver:
    def __init__(self, name, skill, constructor_name, wdc=0, points=0):
        self.name = name
        self.skill = skill
        self.constructor_name = constructor_name
        self.wdc = wdc
        self.points = points

    def __str__(self):
        return f"{self.name} [{self.constructor_name}] - {self.points} pts"

    def to_dict(self):
        return {
            "name": self.name,
            "skill": self.skill,
            "constructor_name": self.constructor_name,
            "wdc": self.wdc,
            "points": self.points
        }


class Track:
    def __init__(self, country, track_name, laps, time):
        self.country = country
        self.track_name = track_name
        self.laps = laps
        self.time = time

    def __str__(self):
        return f"{self.track_name}, {self.country} ({self.laps} laps)"

    def to_dict(self):
        return {
            "country": self.country,
            "track_name": self.track_name,
            "laps": self.laps,
            "time": self.time
        }


class Championship:
    def __init__(self, drivers=None, constructors=None, tracks=None, current_round=0, season_count=0):
        self.drivers = drivers if drivers else []
        self.constructors = constructors if constructors else []
        self.tracks = tracks if tracks else []
        self.current_round = current_round
        self.season_count = season_count

    def get_constructor(self, name):
        for constructor in self.constructors:
            if constructor.name == name:
                return constructor
        return None

    def to_dict(self):
        return {
            "drivers": [d.to_dict() for d in self.drivers],
            "constructors": [c.to_dict() for c in self.constructors],
            "tracks": [t.to_dict() for t in self.tracks],
            "current_round": self.current_round
        }
