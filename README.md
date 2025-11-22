# 🛰️ Satellite Tracker

A web application to track satellites in real-time, predict visible passes, and visualize orbits in 3D.

![Satellite Pass Predictor Sneak Peek](SatellitePassPRedictor.jpeg)

## ✨ Features

*   **Pass Prediction**: Calculate future satellite passes for any location on Earth.
*   **3D Visualization**: Interactive 3D globe showing the satellite's orbit and position using **Cesium.js**.
*   **Real-time Data**: Uses **Skyfield** and JPL ephemeris data for high-precision astronomical calculations.
*   **Detailed Metrics**: View rise/set times, max elevation, pass duration, and rise azimuth.
*   **Satellite Presets**: Quick access to popular satellites like the **ISS**, **Hubble Space Telescope**, and **NOAA 19**.

## 🛠️ Technologies Used

*   **Backend**: Python, Flask
*   **Astronomy Engine**: Skyfield, NumPy
*   **Frontend**: HTML5, JavaScript, CSS
*   **3D Engine**: Cesium.js

## 🚀 Getting Started

1.  **Clone the repository**
2.  **Set up the environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
    *(Note: You may need to install `flask` and `skyfield` manually if `requirements.txt` is not present)*
    ```bash
    pip install flask skyfield
    ```
3.  **Run the application**:
    ```bash
    python3 app.py
    ```
4.  **Open in browser**:
    Navigate to `http://localhost:5000`

## 🤖 Credits

This project was built with the assistance of **Google Antigravity**, an advanced AI coding agent.
