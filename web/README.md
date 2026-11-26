# Web

FastAPI backend and browser frontend for creating, sending, and monitoring vehicle routes. Map files 
are cached offline and served to Leaflet on the frontend. 

The web app never sends steering or throttle commands. It sends routes and high-level commands (load, 
start, pause, resume, cancel) to the path following. 

## Run locally

Python packages are managed with [uv](https://docs.astral.sh/uv/). `pyproject.toml` lists the direct dependencies and `uv.lock` pins every package, so every machine gets the same versions.

```bash
# In WSL (Ubuntu 24.04), once
curl -LsSf https://astral.sh/uv/install.sh | sh     # installs uv to ~/.local/bin
source $HOME/.local/bin/env
cd ~ && git clone https://github.com/sastenm/lsev.git && cd lsev/web

# Create the venv with the system Python 3.12 (the one ROS uses), then install from the lockfile
uv venv --python /usr/bin/python3.12 --system-site-packages
uv sync --locked

uv run pytest
uv run uvicorn backend.main:app --port 8000 --workers 1
```

Adding or changing a dependency: `uv add <package>==<version>` (or `uv add --dev ...` for test-only tools). This updates `pyproject.toml` and `uv.lock`

## Running on the Jetson

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh 
source $HOME/.local/bin/env
git pull 
cd web
uv venv --python /usr/bin/python3.12 --system-site-packages   # if .venv doesn't exist yet
uv sync --locked
```

Check ROS Jazzy is installed and visible from venv
```bash
source /opt/ros/jazzy/setup.bash && uv run python -c "import rclpy; print('rclpy ok')"
```

Run it and test on the Jetson itself
```bash
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 1
curl http://localhost:8000/
```

Turn on the hotspot and connect
```bash
nmcli device | grep wifi                # confirm the name; likely wlP1p1s0
sudo nmcli device wifi hotspot ifname wlP1p1s0 ssid lsev-jetson password <8+ chars>
ip addr show wlP1p1s0                   # note the inet address, usually 10.42.0.1
```

On your laptop:
- Join lsev-jetson and open http://10.42.0.1:8000

## Environment variables (proposed, not implemented)

| Variable | Values | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | SQLite path | `sqlite:///./lsev.db` | Saved routes |
| `MAP_TILES_DIR` | Path | TBD | Offline map tiles |

## Tests

```bash
uv run pytest
```

## TODO
