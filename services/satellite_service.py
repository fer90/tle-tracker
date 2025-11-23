import datetime
from skyfield.api import load, Topos, EarthSatellite

def calculate_passes(tle_line1, tle_line2, lat, lon, ele):
    """
    Calculates satellite passes for a given location.
    """
    ts = load.timescale()
    t0 = ts.now()
    t1 = ts.from_datetime(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7))

    # Load ephemeris data
    eph = load('de421.bsp')
    
    # Create observer location
    lat_float = float(lat)
    lon_float = float(lon)
    ele_float = float(ele) if ele else 0.0
    
    observer = Topos(latitude_degrees=lat_float, longitude_degrees=lon_float, elevation_m=ele_float)
    
    # Create satellite object
    satellite = EarthSatellite(tle_line1, tle_line2, 'Target', ts)
    
    # Calculate difference (satellite - observer)
    difference = satellite - observer
    
    # Find events above 10 degrees elevation
    times, events = satellite.find_events(observer, t0, t1, altitude_degrees=10.0)
    
    passes = []
    current_pass = {}
    
    for ti, event in zip(times, events):
        # 0: rise, 1: culminate, 2: set
        name = ('rise', 'culminate', 'set')[event]
        
        if name == 'rise':
            alt, az, distance = difference.at(ti).altaz()
            current_pass = {
                "rise_time": ti.utc_datetime().isoformat(), 
                "max_elevation": 0.0,
                "rise_azimuth": az.degrees
            }
        elif name == 'culminate':
            # Calculate elevation at culmination
            alt, az, distance = difference.at(ti).altaz()
            current_pass["max_elevation"] = alt.degrees
        elif name == 'set':
            if "rise_time" in current_pass: # Ensure we have a matching rise
                current_pass["set_time"] = ti.utc_datetime().isoformat()
                
                # Calculate duration
                rise_dt = datetime.datetime.fromisoformat(current_pass["rise_time"])
                set_dt = ti.utc_datetime()
                duration = (set_dt - rise_dt).total_seconds()
                current_pass["duration_seconds"] = duration
                
                passes.append(current_pass)
                current_pass = {}

    return passes

def calculate_orbit(tle_line1, tle_line2, start_time_utc, end_time_utc):
    """
    Calculates satellite orbit points between two times.
    """
    ts = load.timescale()
    
    # Parse times
    t_start = ts.from_datetime(datetime.datetime.fromisoformat(start_time_utc))
    t_end = ts.from_datetime(datetime.datetime.fromisoformat(end_time_utc))
    
    # Calculate total duration in days
    duration_days = t_end.tt - t_start.tt
    
    # Generate 1000 time points
    times = ts.tt_jd(
        [t_start.tt + i * (duration_days / 999.0) for i in range(1000)]
    )
    
    satellite = EarthSatellite(tle_line1, tle_line2, 'Target', ts)
    
    # Calculate positions (Geocentric)
    geocentric = satellite.at(times)
    
    # Convert to Lat/Lon/Alt (subpoint)
    subpoint = geocentric.subpoint()
    
    points = []
    for i in range(1000):
        points.append({
            "time": times[i].utc_datetime().isoformat(),
            "latitude": subpoint.latitude.degrees[i],
            "longitude": subpoint.longitude.degrees[i],
            "altitude": subpoint.elevation.m[i]
        })
        
    return points
