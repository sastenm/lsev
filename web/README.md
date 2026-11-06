# Web

Content to add to README.md:
- Running the app (locally and on Jetson)
- Environment variables



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
add scripts to run from the Jetson
```

## Environment variables

| Variable | Values | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | SQLite path | `sqlite:///./lsev.db` | Saved routes |
| `MAP_TILES_DIR` | Path | TBD | Offline map tiles |

## Tests

```bash
pytest
```

## TODO

- API endpoints for routes
- WebSocket for live vehicle status
- Map view with offline tiles
- Authentication
