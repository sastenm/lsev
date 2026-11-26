# LSEV
2026-2027 LSEV Capstone Project

> **Status: skeleton only.** Nothing here is implemented yet. Folder names, package
> names, and versions below are proposals and will change as the team decides.

## Overview

TODO

## Architecture


## Repository layout

```text
├── deploy/             # Docker Compose and systemd files for the Jetson
├── docs/               # Design notes, test procedures, interfaces, ...
├── firmware/           # Microcontroller code (low-level vehicle controller)
├── ros_ws/             # ROS 2 workspace with ROS packages (no packages yet)
├── tools/              # Scripts for setup, logs, ...
└── web/                # FastAPI backend and frontend
```

## Platform 

| Component | Version | Status |
|---|---|---|
| NVIDIA Jetson | Orin Nano 8 GB | Decided |
| Jetson OS | JetPack 7.2 (Ubuntu 24.04) | Decided |
| ROS 2 | Jazzy | Decided |
| Python | 3.12 (Ships with Ubuntu 24.04) | Decided |
| Python packages | uv (`web/pyproject.toml` + `web/uv.lock`) | Proposed |
| Development | Windows 11 + WSL (Ubuntu 24.04) | TBD |
| Microcontroller or Raspberry Pi | TBD | TBD |
| C++ standard | TBD | TBD |

## Quick start

TODO: nothing to run yet

## Contributing


### Workflow

1. **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name`.
2. **Add new/changed files**: `git add file1.example file2.example`.
3. **Commit your changes** with clear messages: `git commit -m 'Add some feature'`.
4. **Push to the remote branch**: `git push origin feature/your-feature-name`.
5. **Open a pull request** into `main` describing your changes and how to test them. Don't push directly into `main`.
6. **Merge PR** into `main` after someone reviews. **Squash** if too many small commits.

If a generated file shows up in `git status` (build output, logs, databases), add it to `.gitignore` instead of committing it.

### Tests

```bash
# Web app
cd web && uv run pytest

# ROS packages
<insert_testing_commands_here> something like colcon test && colcon test-result --verbose
```

### Code style

TBD

### Commits

TBD: agree upon commit convention

