# LSEV
2026-2027 LSEV Capstone Project

Content to add to README.md:
- Overview
- Architecture
- Quick start
- Contributing
  - Tests
  - Code style
  - Commits

## Overview


## Architecture


## Repository layout

```text
├── deploy/             # Docker Compose and systemd files for the Jetson
├── docs/               # Design notes, test procedures, ...
├── firmware/           # Microcontroller code
├── ros_ws/             # ROS 2 workspace with all ROS packages
├── tools/              # Scripts for setup, logs, ...
└── web/                # FastAPI backend and frontend
```

## Platform (TBD)

| Component | Version |
|---|---|
| NVIDIA Jetson | Orin Nano 8 GB |
| Jetson OS | JetPack 7.2 (Ubuntu 24.04) |
| ROS 2 | Jazzy or Humble (TBD) |
| Python | 3.12 (maybe? Shipped with Ubuntu and Jazzy) |
| Development | Windows 11 + WSL (Ubuntu 24.04) -- TBD |
| Arduino | TBD |
| C++ | TBD |

## Quick start


## Contributing


### Workflow

1. **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name`.
2. **Add fields to .gitignore** to leave files/folders out of version control.
3. **Add new/changed files**: `git add file1.example file2.example`.
4. **Commit your changes** with clear messages: `git commit -m 'Add some feature'`.
5. **Push to the remote branch**: `git push origin feature/your-feature-name`.
6. **Open a pull request** into `main` describing your changes and how to test them. Don't push directly into `main`.
7. **Merge PR** into `main` after someone reviews. **Squash** if too many small commits.

### Tests

```bash
# Web app
cd web && pytest

# ROS packages
<insert_testing_commands_here> something like colcon test && colcon test-result --verbose
```

### Code style


### Commits
**agree upon commit convention**

