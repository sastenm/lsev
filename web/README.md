# Web

FastAPI backend and browser frontend for creating, sending, and monitoring vehicle routes. Map files 
are cached offline and served to Leaflet on the frontend. 

The web app never sends steering or throttle commands. It sends routes and high-level commands (start, 
pause, cancel) to the (TBD: route manager? path following?). 

## Run locally

```bash
cd web
finish local scripts
```

## Running on the Jetson

```bash
sudo apt install python3.12-venv
git pull
cd web
python3 -m vevn --system-site-packages .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Check ROS Jazzy is installed
```bash
source /opt/ros/jazzy/setup.bash && python -c "import rclpy; print('rclpy ok')"
```

Run it and test on the Jetson itself
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
curl http://localhost:8000/
```

Turn on the hotspot and connect
```bash
nmcli device | grep wifi                # confirm the name; likely wlP1p1s0
sudo nmcli device wifi hotspot ifname wlP1p1s0 ssid lsev-jetson password <8+ chars>
ip addr show wlP1p1s0                   # note the inet address, usually 10.42.0.1
```

On your laptop:
- Join lsev-jetson and open http://10.42.0.1.8000

## Environment variables (proposed, not implemented)

| Variable | Values | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | SQLite path | `sqlite:///./lsev.db` | Saved routes |
| `MAP_TILES_DIR` | Path | TBD | Offline map tiles |

## Tests

No tests yet

```bash
pytest
```

## TODO
