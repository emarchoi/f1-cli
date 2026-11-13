import pytest
from project import simulate_race, get_standings, reset_data
from data_manager import DataManager
from models import Championship, Driver, Constructor, Track

@pytest.fixture
def sample_championship():
    # Setup a small sample championship for testing
    c1 = Constructor("Team A", "Engine A", 90)
    c2 = Constructor("Team B", "Engine B", 80)
    
    d1 = Driver("Driver 1", 90, "Team A")
    d2 = Driver("Driver 2", 80, "Team B")
    d3 = Driver("Driver 3", 70, "Team A")
    
    t1 = Track("Country 1", "Track 1", 50, 90.0)
    t2 = Track("Country 2", "Track 2", 60, 100.0)
    
    return Championship(
        drivers=[d1, d2, d3],
        constructors=[c1, c2],
        tracks=[t1, t2],
        current_round=0
    )

def test_simulate_race(sample_championship):
    initial_round = sample_championship.current_round
    results = simulate_race(sample_championship)
    
    assert len(results) == 3
    assert sample_championship.current_round == initial_round + 1
    
    # Check if points were awarded
    total_points = sum(d.points for d in sample_championship.drivers)
    assert total_points == (25 + 18 + 15) # Top 3 get these points

def test_get_standings(sample_championship):
    sample_championship.drivers[0].points = 100
    sample_championship.drivers[1].points = 200
    sample_championship.drivers[2].points = 50
    
    drivers, constructors = get_standings(sample_championship)
    
    assert drivers[0].name == "Driver 2"
    assert drivers[1].name == "Driver 1"
    assert drivers[2].name == "Driver 3"

def test_reset_data(sample_championship):
    # Simulate a race first
    simulate_race(sample_championship)
    
    assert sample_championship.current_round == 1
    assert any(d.points > 0 for d in sample_championship.drivers)
    
    reset_data(sample_championship)
    
    assert sample_championship.current_round == 0
    assert all(d.points == 0 for d in sample_championship.drivers)
    assert all(c.points == 0 for c in sample_championship.constructors)

def test_simulate_all_races(sample_championship):
    # Simulate both tracks
    simulate_race(sample_championship)
    simulate_race(sample_championship)
    
    assert sample_championship.current_round == 2
    
    # Attempting to simulate again should return empty results
    results = simulate_race(sample_championship)
    assert results == []
    assert sample_championship.current_round == 2
