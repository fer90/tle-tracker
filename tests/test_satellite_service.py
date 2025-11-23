import pytest
from services.satellite_service import calculate_passes, calculate_orbit
import datetime

# ISS TLE (Example)
TLE1 = "1 25544U 98067A   24326.50000000  .00016717  00000-0  29673-3 0  9993"
TLE2 = "2 25544  51.6416 209.2207 0005198 100.0000 250.0000 15.49547118483001"

def test_calculate_passes_structure():
    # NYC coordinates
    lat = 40.7128
    lon = -74.0060
    ele = 0
    
    passes = calculate_passes(TLE1, TLE2, lat, lon, ele)
    
    assert isinstance(passes, list)
    if len(passes) > 0:
        p = passes[0]
        assert "rise_time" in p
        assert "set_time" in p
        assert "max_elevation" in p
        assert "duration_seconds" in p
        assert "rise_azimuth" in p
        
        # Check types
        assert isinstance(p["max_elevation"], float)
        assert isinstance(p["duration_seconds"], float)

def test_calculate_orbit_structure():
    start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    end_time = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=90)).isoformat()
    
    points = calculate_orbit(TLE1, TLE2, start_time, end_time)
    
    assert isinstance(points, list)
    assert len(points) == 1000
    
    p = points[0]
    assert "time" in p
    assert "latitude" in p
    assert "longitude" in p
    assert "altitude" in p
    
    assert isinstance(p["latitude"], float)
    assert isinstance(p["longitude"], float)
    assert isinstance(p["altitude"], float)
