# ASCII Flight Simulator

A terminal-based 3D flight simulator with semi-realistic physics and procedural terrain, rendered entirely in ASCII art.

![Flight Simulator](ascii-flight-sim.png)

## Features

- **Semi-realistic flight physics**: Lift, drag, thrust, and stall behavior
- **3D procedural terrain**: Generated using Perlin noise
- **ASCII raycasting renderer**: Real-time 3D terrain visualization
- **Full flight instruments**: HUD displaying altitude, airspeed, heading, and more
- **Stall warnings**: Realistic stall behavior at high angles of attack

## Requirements

- Python 3.6+
- Terminal with support for cursor control (most modern terminals)
- Minimum terminal size: 80x24 characters

## Installation

No installation required! The simulator uses only Python standard library.

```bash
cd ascii_flight_sim
./main.py
```

Or:

```bash
python3 ascii_flight_sim/main.py
```

## Controls

| Key | Action |
|-----|--------|
| W / S | Pitch up / down |
| A / D | Roll left / right |
| + / - | Increase / decrease throttle |
| R | Reset aircraft |
| P | Pause simulation |
| Q | Quit |

## Flight Tips

1. **Takeoff**: Increase throttle to 75%+, wait for speed to build, then gently pull back (W)
2. **Avoid stalls**: Keep angle of attack below 12 degrees (watch the AoA indicator)
3. **Turning**: Use roll (A/D) to bank, aircraft will turn naturally
4. **Landing**: Reduce throttle, maintain ~50 knots, gentle descent

## How It Works

### Physics Model

The simulator uses simplified aerodynamic equations:

- **Lift**: `L = 0.5 × ρ × V² × S × CL(α)`
- **Drag**: `D = 0.5 × ρ × V² × S × CD(α)`
- **Stall**: Occurs at ~15° angle of attack

Where:
- ρ = air density
- V = airspeed
- S = wing area
- CL, CD = lift/drag coefficients (functions of angle of attack α)

### Rendering

Uses column-based raycasting to render 3D terrain:
1. Cast ray for each screen column
2. March along ray, sampling terrain height
3. Map distance to ASCII character for depth shading
4. Characters: ` .:-=+*#%@` (light to dark)

### Terrain

Generated using multi-octave Perlin noise for realistic, infinite procedural terrain.

## Project Structure

```
ascii_flight_sim/
├── main.py                 # Entry point
├── config.py               # Constants and configuration
├── engine/                 # Game engine
│   ├── display.py          # Curses wrapper
│   ├── game_loop.py        # Main loop
│   └── input_handler.py    # Controls
├── physics/                # Flight physics
│   ├── aircraft.py         # Aircraft state
│   ├── aerodynamics.py     # Force calculations
│   ├── physics_engine.py   # Physics integration
│   └── vector3d.py         # 3D math
├── rendering/              # Graphics
│   ├── camera.py           # Camera system
│   ├── raycaster.py        # 3D renderer
│   ├── ascii_shader.py     # Character mapping
│   └── hud.py              # Instruments
└── world/                  # World generation
    ├── perlin.py           # Noise generator
    └── terrain.py          # Terrain queries
```

## Troubleshooting

**Terminal too small**: Resize your terminal to at least 80x24 characters.

**Colors not working**: Some terminals may not support colors. The simulator will still work in monochrome.

**Slow performance**: Try reducing the terminal size or closing other applications.

## License

MIT License - feel free to modify and share!

## Credits

Built with Python and curses. Inspired by classic ASCII art games and flight simulators.
