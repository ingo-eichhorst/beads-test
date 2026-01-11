#!/usr/bin/env python3
"""Super Simple ASCII Flight Simulator - Side-scrolling view.

Controls:
    W - Pull up (pitch up)
    S - Push down (pitch down)
    Q - Quit
"""

import curses
import time
import random


class SimplePlane:
    def __init__(self, screen_height):
        self.altitude = screen_height // 2  # Middle of screen
        self.velocity = 0.0  # Vertical velocity
        self.screen_height = screen_height

    def update(self, pitch_input):
        # Simple physics
        gravity = 0.3
        pitch_force = pitch_input * 1.0

        self.velocity += pitch_force - gravity
        self.velocity *= 0.9  # Air resistance

        self.altitude -= self.velocity

        # Keep on screen
        if self.altitude < 2:
            self.altitude = 2
            self.velocity = 0
        if self.altitude > self.screen_height - 3:
            self.altitude = self.screen_height - 3
            self.velocity = 0


class SimpleGround:
    def __init__(self, width):
        self.width = width
        self.heights = [random.randint(3, 8) for _ in range(width)]
        self.offset = 0

    def scroll(self):
        self.offset += 1
        if self.offset >= 2:
            self.offset = 0
            # Add new column, remove old
            self.heights.pop(0)
            self.heights.append(random.randint(3, 8))

    def get_height(self, x):
        if 0 <= x < len(self.heights):
            return self.heights[x]
        return 5


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(50)  # 50ms timeout

    height, width = stdscr.getmaxyx()

    plane = SimplePlane(height)
    ground = SimpleGround(width)

    pitch = 0
    frame = 0
    crashed = False

    while True:
        # Input
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break

        pitch = 0
        if key == ord('w') or key == ord('W'):
            pitch = 1
        elif key == ord('s') or key == ord('S'):
            pitch = -1

        # Update
        if not crashed:
            plane.update(pitch)
            if frame % 2 == 0:  # Scroll slower
                ground.scroll()

        # Collision detection
        if not crashed:
            plane_x = width // 3
            plane_y = int(plane.altitude)
            ground_height = ground.get_height(plane_x)
            ground_top_y = height - ground_height

            # Check if plane hits ground
            if plane_y >= ground_top_y - 1:
                crashed = True

        # Draw
        stdscr.clear()

        # Draw ground
        for x in range(width):
            ground_h = ground.get_height(x)
            for y in range(ground_h):
                try:
                    stdscr.addch(height - 1 - y, x, '#')
                except:
                    pass

        # Draw plane
        plane_x = width // 3
        plane_y = int(plane.altitude)
        try:
            if crashed:
                stdscr.addstr(plane_y, plane_x, 'X*X')
            else:
                stdscr.addstr(plane_y, plane_x, '>-o')
        except:
            pass

        # Draw HUD
        try:
            stdscr.addstr(1, 2, f"Altitude: {int(height - plane.altitude):3d}")
            stdscr.addstr(2, 2, f"Velocity: {plane.velocity:5.1f}")
            stdscr.addstr(height - 2, 2, "W=Up S=Down Q=Quit")

            # Crash message
            if crashed:
                crash_msg = "*** CRASHED! Press Q to quit ***"
                crash_x = (width - len(crash_msg)) // 2
                crash_y = height // 2
                stdscr.addstr(crash_y, crash_x, crash_msg, curses.A_BOLD | curses.A_BLINK)
        except:
            pass

        stdscr.refresh()
        frame += 1


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
