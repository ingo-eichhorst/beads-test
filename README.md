# Simple ASCII Flight Simulator

A minimalist terminal-based side-scrolling flight simulator with simple physics and procedural terrain, rendered in ASCII art.

## Features

- **Simple flight physics**: Gravity, pitch control, air resistance
- **Side-scrolling view**: 2D gameplay with procedural terrain
- **Crash detection**: Game ends when plane hits the ground
- **Real-time HUD**: Displays altitude, velocity, and controls
- **Minimalist ASCII graphics**: Clean terminal rendering using curses

## Requirements

- Python 3.6+
- Terminal with curses support (most Unix/Linux/macOS terminals)
- Minimum terminal size: 80x24 characters

## Installation

No installation required! The simulator uses only Python standard library.

```bash
python3 flight_sim.py
```

Or use the provided shell script:

```bash
./run_simulator.sh
```

## Controls

| Key | Action |
|-----|--------|
| W | Pitch up (pull up) |
| S | Pitch down (push down) |
| Q | Quit |

## How to Play

1. **Start the game**: Run the simulator and you'll see your plane (>-o) flying over terrain
2. **Control altitude**: Use W to climb and S to descend
3. **Avoid crashing**: Don't let your plane hit the ground (#)
4. **Monitor your HUD**: Watch your altitude and velocity in the top-left corner

### Flight Tips

- The plane is affected by gravity - you'll naturally descend if you don't pull up
- Use gentle inputs - the physics includes momentum and air resistance
- Watch the terrain ahead and adjust altitude early
- If you crash (plane shows as X*X), press Q to quit

## How It Works

### Physics Model

The simulator uses simplified physics:

- **Gravity**: Constant downward force (0.3 units)
- **Pitch control**: Player input applies upward/downward force (1.0 units)
- **Air resistance**: Velocity dampened by 10% each frame
- **Vertical velocity**: Integrates pitch force minus gravity

### Collision Detection

The game checks if the plane's altitude intersects with the ground height at its horizontal position. When a collision is detected:
- Game freezes (no more updates to plane or terrain)
- Plane graphic changes to "X*X"
- Bold blinking crash message appears

### Rendering

- **Ground**: Drawn with '#' characters at varying heights
- **Plane**: Shown as '>-o' when flying, 'X*X' when crashed
- **Terrain scrolling**: Ground moves right-to-left to simulate forward motion
- **Procedural generation**: New terrain columns added as old ones scroll off screen

### Terrain Generation

Random terrain heights (3-8 units) are generated for each column, creating varied landscapes to navigate.

## Project Structure

```
.
├── flight_sim.py        # Main simulator code
├── run_simulator.sh     # Helper script to run the simulator
├── README.md           # This file
└── .beads/             # Issue tracking
```

## Code Structure

The simulator consists of three main classes:

- `SimplePlane`: Manages plane state (altitude, velocity) and physics updates
- `SimpleGround`: Handles terrain generation and scrolling
- `main()`: Game loop with input, update, collision detection, and rendering

## Troubleshooting

**Terminal too small**: Resize your terminal to at least 80x24 characters.

**Curses errors**: Make sure you're running on a Unix-like system (Linux, macOS) with curses support.

**Game too easy/hard**: Edit `flight_sim.py` and adjust:
- `gravity = 0.3` - Higher = harder to stay airborne
- `pitch_force = 1.0` - Higher = more responsive controls
- `random.randint(3, 8)` - Terrain height range

## Development

This project uses [beads](https://github.com/beadtime/beads) for issue tracking.

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
```

## License

MIT License - feel free to modify and share!

## Credits

Built with Python and curses. A simple demonstration of ASCII game development and basic flight physics.
