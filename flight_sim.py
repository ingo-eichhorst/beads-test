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
import os
import json


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


class ScoreManager:
    def __init__(self, score_file='.flight_sim_highscore.json'):
        self.score_file = score_file
        self.distance = 0
        self.time_survived = 0.0
        self.high_score = self.load_high_score()

    def load_high_score(self):
        """Load high score from file."""
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
            except:
                return 0
        return 0

    def save_high_score(self):
        """Save high score to file."""
        try:
            with open(self.score_file, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass

    def update(self, frame_count):
        """Update distance and time based on frame count."""
        self.distance = frame_count // 2  # Each scroll increment
        self.time_survived = frame_count * 0.05  # 50ms per frame

    def get_score(self):
        """Calculate total score."""
        return int(self.distance + self.time_survived * 10)

    def check_high_score(self):
        """Check if current score is a new high score."""
        current_score = self.get_score()
        if current_score > self.high_score:
            self.high_score = current_score
            self.save_high_score()
            return True
        return False


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(50)  # 50ms timeout

    height, width = stdscr.getmaxyx()

    plane = SimplePlane(height)
    ground = SimpleGround(width)
    score_manager = ScoreManager()

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
            score_manager.update(frame)

        # Collision detection
        if not crashed:
            plane_x = width // 3
            plane_y = int(plane.altitude)
            ground_height = ground.get_height(plane_x)
            ground_top_y = height - ground_height

            # Check if plane hits ground
            if plane_y >= ground_top_y - 1:
                crashed = True
                score_manager.check_high_score()

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
            stdscr.addstr(3, 2, f"Distance: {score_manager.distance:4d}")
            stdscr.addstr(4, 2, f"Time:     {score_manager.time_survived:5.1f}s")
            stdscr.addstr(5, 2, f"Score:    {score_manager.get_score():5d}")
            stdscr.addstr(6, 2, f"High:     {score_manager.high_score:5d}")
            stdscr.addstr(height - 2, 2, "W=Up S=Down Q=Quit")

            # Crash message
            if crashed:
                crash_msg = "*** CRASHED! Press Q to quit ***"
                crash_x = (width - len(crash_msg)) // 2
                crash_y = height // 2
                stdscr.addstr(crash_y, crash_x, crash_msg, curses.A_BOLD | curses.A_BLINK)

                # Show final score
                final_score_msg = f"Final Score: {score_manager.get_score()}"
                if score_manager.get_score() >= score_manager.high_score:
                    final_score_msg += " - NEW HIGH SCORE!"
                final_x = (width - len(final_score_msg)) // 2
                stdscr.addstr(crash_y + 1, final_x, final_score_msg, curses.A_BOLD)
        except:
            pass

        stdscr.refresh()
        frame += 1


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
