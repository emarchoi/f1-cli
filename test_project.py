import pytest
from models import Championship, Constructor, Driver, Track
from project import (
    get_standings,
    reset_data,
    simulate_qualifying,
    simulate_race,
)

@pytest.fixture
def sample_championship():
    constructors = [
        Constructor(name="Mercedes-AMG Petronas F1 Team", engine="Mercedes", power=97, wcc=1, points=0),
        Constructor(name="Oracle Red Bull Racing", engine="Red Bull Ford", power=92, wcc=0, points=0),
        Constructor(name="Scuderia Ferrari HP", engine="Ferrari", power=94, wcc=2, points=0),
    ]
    drivers = [
        Driver(name="George Russell", skill=93, constructor_name="Mercedes-AMG Petronas F1 Team", wdc=0, points=0),
        Driver(name="Max Verstappen", skill=95, constructor_name="Oracle Red Bull Racing", wdc=4, points=0),
        Driver(name="Charles Leclerc", skill=92, constructor_name="Scuderia Ferrari HP", wdc=0, points=0),
    ]
    tracks = [
        Track(country="Australia", track_name="Albert Park Circuit", laps=62, time=80.5),
        Track(country="Japan", track_name="Suzuka Circuit", laps=55, time=91.5),
    ]
    return Championship(
        drivers=drivers,
        constructors=constructors,
        tracks=tracks,
        current_round=0,
    )

def test_simulate_qualifying(sample_championship):
    quali = simulate_qualifying(sample_championship, delay=0)

    assert len(quali) == 3
    assert [entry["grid_pos"] for entry in quali] == [1, 2, 3]
    assert [entry["grid_bonus"] for entry in quali] == [0.50, 0.25, 0.00]
    assert quali[0]["quali_score"] >= quali[1]["quali_score"] >= quali[2]["quali_score"]

    # Finished season returns an empty list
    sample_championship.current_round = len(sample_championship.tracks)
    assert simulate_qualifying(sample_championship, delay=0) == []

def test_simulate_race(sample_championship):
    initial_wdc = {d.name: d.wdc for d in sample_championship.drivers}
    initial_wcc = {c.name: c.wcc for c in sample_championship.constructors}

    # Round 1 = Australia, Albert Park Circuit
    results = simulate_race(sample_championship, delay=0)

    assert sample_championship.current_round == 1
    assert len(results) == 3
    assert [r["driver"].points for r in results] == [25, 18, 15]
    assert results[0]["total_time"] <= results[1]["total_time"] <= results[2]["total_time"]
    assert ":" in results[0]["total_time_display"]

    for r in results:
        constructor = sample_championship.get_constructor(r["driver"].constructor_name)
        assert constructor.points == r["driver"].points

    # Round 2 = Final Round -> also shows WDC AND WCC
    simulate_race(sample_championship, delay=0)
    assert sample_championship.current_round == 2

    wdc_champ = max(sample_championship.drivers, key=lambda d: d.points)
    wcc_champ = max(sample_championship.constructors, key=lambda c: c.points)
    assert wdc_champ.wdc == initial_wdc[wdc_champ.name] + 1
    assert wcc_champ.wcc == initial_wcc[wcc_champ.name] + 1

    assert simulate_race(sample_championship, delay=0) == []