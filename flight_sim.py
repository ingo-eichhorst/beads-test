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
        self.collectibles = 0
        self.bonus_points = 0

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

    def add_collectible(self, points=50):
        """Add points for collecting an item."""
        self.collectibles += 1
        self.bonus_points += points

    def get_score(self):
        """Calculate total score."""
        return int(self.distance + self.time_survived * 10 + self.bonus_points)

    def check_high_score(self):
        """Check if current score is a new high score."""
        current_score = self.get_score()
        if current_score > self.high_score:
            self.high_score = current_score
            self.save_high_score()
            return True
        return False


class Collectible:
    def __init__(self, x, y, value=50):
        self.x = x
        self.y = y
        self.value = value
        self.char = '*'
        self.active = True

    def scroll(self):
        """Move collectible left as terrain scrolls."""
        self.x -= 1

    def is_off_screen(self):
        """Check if collectible has scrolled off screen."""
        return self.x < 0


class CollectibleManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.collectibles = []
        self.spawn_interval = 100  # Frames between spawns
        self.last_spawn = 0

    def update(self, frame_count):
        """Update all collectibles and spawn new ones."""
        # Scroll existing collectibles
        for item in self.collectibles:
            item.scroll()

        # Remove off-screen collectibles
        self.collectibles = [item for item in self.collectibles if not item.is_off_screen() and item.active]

        # Spawn new collectibles
        if frame_count - self.last_spawn >= self.spawn_interval:
            self.spawn()
            self.last_spawn = frame_count

    def spawn(self):
        """Spawn a new collectible at random altitude."""
        # Spawn at right edge of screen, random altitude (avoid ground and ceiling)
        y = random.randint(5, self.height - 10)
        x = self.width - 1
        self.collectibles.append(Collectible(x, y))

    def check_collision(self, plane_x, plane_y):
        """Check if plane collided with any collectibles."""
        for item in self.collectibles:
            if item.active:
                # Check if plane position overlaps with collectible
                if abs(item.x - plane_x) <= 2 and abs(item.y - plane_y) <= 1:
                    item.active = False
                    return item.value
        return 0

    def draw(self, stdscr):
        """Draw all active collectibles."""
        for item in self.collectibles:
            if item.active:
                try:
                    stdscr.addstr(int(item.y), int(item.x), item.char, curses.A_BOLD)
                except:
                    pass


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(50)  # 50ms timeout

    height, width = stdscr.getmaxyx()

    plane = SimplePlane(height)
    ground = SimpleGround(width)
    score_manager = ScoreManager()
    collectible_manager = CollectibleManager(width, height)

    pitch = 0
    frame = 0
    crashed = False
    last_collect_frame = -10  # For visual feedback

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
            collectible_manager.update(frame)

        # Collision detection
        if not crashed:
            plane_x = width // 3
            plane_y = int(plane.altitude)
            ground_height = ground.get_height(plane_x)
            ground_top_y = height - ground_height

            # Check collectible collision
            points = collectible_manager.check_collision(plane_x, plane_y)
            if points > 0:
                score_manager.add_collectible(points)
                last_collect_frame = frame

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

        # Draw collectibles
        collectible_manager.draw(stdscr)

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
            stdscr.addstr(5, 2, f"Stars:    {score_manager.collectibles:3d}")
            stdscr.addstr(6, 2, f"Score:    {score_manager.get_score():5d}")
            stdscr.addstr(7, 2, f"High:     {score_manager.high_score:5d}")
            stdscr.addstr(height - 2, 2, "W=Up S=Down Q=Quit")

            # Collection feedback
            if frame - last_collect_frame < 10:
                collect_msg = "+50!"
                try:
                    stdscr.addstr(plane_y - 2, plane_x + 4, collect_msg, curses.A_BOLD)
                except:
                    pass

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
