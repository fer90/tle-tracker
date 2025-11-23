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

    try:
        from services.satellite_service import calculate_passes, calculate_orbit

        passes = calculate_passes(tle_line1, tle_line2, latitude, longitude, elevation)

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

@app.route('/api/orbit', methods=['GET'])
def get_orbit():
    tle_line1 = request.args.get('tle_line1')
    tle_line2 = request.args.get('tle_line2')
    start_time_utc = request.args.get('start_time_utc')
    end_time_utc = request.args.get('end_time_utc')

    if not all([tle_line1, tle_line2, start_time_utc, end_time_utc]):
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

    try:
        from services.satellite_service import calculate_orbit
        
        points = calculate_orbit(tle_line1, tle_line2, start_time_utc, end_time_utc)
            
        return jsonify({
            "status": "success",
            "points": points
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
