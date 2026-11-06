# ROS 2 Workspace

Content to add to README.md:
- Building the workspace
- Launching the system



All ROS 2 packages for the vehicle. Built with `colcon` against ROS 2 Jazzy (subject to change).

## Packages

Temporary proposed/example packages
| Package | Purpose |
|---|---|
| `lsev_interfaces` | Shared messages, services, and actions (TBD) |
| `lsev_route_manager` | Some way for the web app to communicate with ROS 2 (TBD), manages route and start/stop/pause |
| `lsev_bringup` | Launch files and configs (TBD) |
| `lsev_vehicle_bridge` | Communication with the microcontroller (TBD) |
| `lsev_localization` | GNSS driver for u-blox receiver, some way to get RTK corrections, sensor fusion (IMU/GNSS, may have library), heading |
| `lsev_path_following` | Fill in purpose (TBD) |
| `lsev_perception` | Fill in purpose (TBD) |
| `example_1` | Fill in purpose |

## Build
```bash
build scripts here
```

## Launch
```bash
launch scripts here
```

## Contributing ROS 2 packages

1. Create a package folder in src (src/lsev_{package_name}/)
2. Create a README.md inside new package folder describing:
    1. What each node does
    2. Its topics, services, and actions (interfaces other packages depend on)
    3. Its main parameters 
3. Develop
