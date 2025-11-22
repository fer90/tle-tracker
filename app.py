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

    # Mock data for now
    # In a real app, we would use a library like skyfield or sgp4 here
    
    mock_passes = [
        {
            "rise_time": (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
            "set_time": (datetime.datetime.now() + datetime.timedelta(hours=1, minutes=10)).isoformat(),
            "max_elevation": 45.0
        },
        {
            "rise_time": (datetime.datetime.now() + datetime.timedelta(hours=3)).isoformat(),
            "set_time": (datetime.datetime.now() + datetime.timedelta(hours=3, minutes=12)).isoformat(),
            "max_elevation": 75.5
        }
    ]

    return jsonify({
        "status": "success",
        "params": {
            "tle_line1": tle_line1,
            "tle_line2": tle_line2,
            "latitude": latitude,
            "longitude": longitude,
            "elevation": elevation
        },
        "passes": mock_passes
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
