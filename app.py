from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/passes', methods=['GET'])
def get_passes():
    tle_line1 = request.args.get('tle_line1')
    tle_line2 = request.args.get('tle_line2')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    elevation = request.args.get('elevation')

    # Skyfield implementation
    from skyfield.api import load, Topos, EarthSatellite
    
    try:
        ts = load.timescale()
        t0 = ts.now()
        t1 = ts.from_datetime(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7))

        # Load ephemeris data (will download if not present)
        # Note: In a production env, you might want to cache this or handle the download explicitly
        eph = load('de421.bsp')
        
        # Create observer location
        # Latitude and longitude are expected in degrees
        # Elevation in meters
        lat_float = float(latitude)
        lon_float = float(longitude)
        ele_float = float(elevation) if elevation else 0.0
        
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
                current_pass = {"rise_time": ti.utc_datetime().isoformat(), "max_elevation": 0.0}
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

        return jsonify({
            "status": "success",
            "params": {
                "tle_line1": tle_line1,
                "tle_line2": tle_line2,
                "latitude": latitude,
                "longitude": longitude,
                "elevation": elevation
            },
            "passes": passes
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
