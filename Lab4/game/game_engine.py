import math
import random
from array import array

import pygame
from game.color_button import ColorButton


# Playback timing (milliseconds): starts slow and easy to follow, speeds up
# each round, and never goes below the minimums so it stays playable.
BASE_FLASH_MS = 450
BASE_PAUSE_MS = 200
MIN_FLASH_MS = 160
MIN_PAUSE_MS = 70
FLASH_STEP_MS = 20   # flash time removed per round after round 1
PAUSE_STEP_MS = 9    # pause time removed per round after round 1

# One pitch (Hz) per button id: Red, Blue, Green, Yellow (C4, E4, G4, C5).
TONE_FREQUENCIES = [262, 330, 392, 523]
TONE_LENGTH_MS = 200

# Player turn timer (milliseconds): total time allowed to enter the WHOLE pattern.
# Longer patterns get more time: round 1 = 4 s, round 5 = 8 s, round 10 = 13 s.
TIMER_BASE_MS = 3000
TIMER_PER_STEP_MS = 1000

# Short breather before each round's playback so the player's last click (and its
# tone) isn't mixed with the first flash of the new pattern.
ROUND_START_DELAY_MS = 600


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        pad_size = 130
        gap = 24
        start_x = width // 2 - pad_size - (gap // 2)
        start_y = 150

        self.buttons = [
            ColorButton(0, pygame.Rect(start_x, start_y, pad_size, pad_size), (110, 20, 20), (255, 50, 50)),                      # Red
            ColorButton(1, pygame.Rect(start_x + pad_size + gap, start_y, pad_size, pad_size), (15, 60, 150), (40, 170, 255)),   # Blue
            ColorButton(2, pygame.Rect(start_x, start_y + pad_size + gap, pad_size, pad_size), (15, 100, 30), (50, 255, 90)),    # Green
            ColorButton(3, pygame.Rect(start_x + pad_size + gap, start_y + pad_size + gap, pad_size, pad_size), (140, 110, 10), (255, 235, 40)), # Yellow
        ]

        self.sequence = []
        self.player_input = []
        self.score = 0

        self.state = "WATCH"
        self.showing_step = 0
        self.step_start_time = 0
        self.flash_duration = BASE_FLASH_MS
        self.pause_duration = BASE_PAUSE_MS
        self.is_flashing = False

        self.player_lit_button = None
        self.player_lit_start = 0
        self.player_flash_duration = 150

        self.turn_start_time = 0
        self.turn_time_limit = TIMER_BASE_MS
        self.turn_time_left = TIMER_BASE_MS
        self.game_over_reason = ""

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_medium = pygame.font.SysFont(None, 28)

        self.sounds = self.build_sounds()

        self.start_next_round()

    def build_sounds(self):
        """Generate one short sine tone per button (no extra dependencies).
        Returns an empty list if audio is unavailable so the game still runs."""
        try:
            init = pygame.mixer.get_init()
            if init is None or init[1] != -16:
                pygame.mixer.quit()
                pygame.mixer.init(44100, -16, 1)
            sample_rate, _, channels = pygame.mixer.get_init()

            sounds = []
            total = int(sample_rate * TONE_LENGTH_MS / 1000)
            fade = int(sample_rate * 0.015)  # short fade in/out avoids clicks
            for freq in TONE_FREQUENCIES:
                samples = array("h")
                for i in range(total):
                    envelope = min(1.0, i / fade, (total - i) / fade)
                    value = int(9000 * envelope * math.sin(2 * math.pi * freq * i / sample_rate))
                    samples.extend([value] * channels)
                sounds.append(pygame.mixer.Sound(buffer=samples.tobytes()))
            return sounds
        except pygame.error:
            return []

    def play_tone(self, color_id):
        if self.sounds:
            self.sounds[color_id].play()

    def update_playback_speed(self):
        """Shorten flash and pause as the round number (sequence length) grows."""
        rounds_played = len(self.sequence) - 1
        self.flash_duration = max(MIN_FLASH_MS, BASE_FLASH_MS - FLASH_STEP_MS * rounds_played)
        self.pause_duration = max(MIN_PAUSE_MS, BASE_PAUSE_MS - PAUSE_STEP_MS * rounds_played)

    def get_turn_time_limit(self):
        """Time allowed for the player's turn, scaled by the pattern length."""
        return TIMER_BASE_MS + TIMER_PER_STEP_MS * len(self.sequence)

    def check_turn_timeout(self, now):
        """Update the remaining time; end the game if it ran out. True on timeout."""
        elapsed = now - self.turn_start_time
        self.turn_time_left = max(0, self.turn_time_limit - elapsed)
        if self.turn_time_left <= 0:
            self.game_over_reason = "TIME'S UP! GAME OVER"
            self.state = "GAME_OVER"
            return True
        return False

    def start_next_round(self):
        new_color = random.randint(0, 3)

        # self.sequence += self.sequence + [new_color]    # This is the bug for Task 1        
        self.sequence.append(new_color)
        
        self.update_playback_speed()

        self.player_input.clear()
        self.state = "WATCH"
        self.showing_step = -1   # -1 = short delay before the first flash
        self.step_start_time = pygame.time.get_ticks()
        self.is_flashing = False

        # Timer is reset here but only starts counting once the player's turn begins
        self.turn_time_limit = self.get_turn_time_limit()
        self.turn_time_left = self.turn_time_limit

    def update(self):
        now = pygame.time.get_ticks()

        if self.player_lit_button is not None:
            if now - self.player_lit_start >= self.player_flash_duration:
                self.player_lit_button.is_lit = False
                self.player_lit_button = None

        if self.state == "WATCH":
            if self.showing_step < 0:
                if now - self.step_start_time >= ROUND_START_DELAY_MS:
                    self.showing_step = 0
                    first_id = self.sequence[0]
                    self.buttons[first_id].is_lit = True
                    self.play_tone(first_id)
                    self.is_flashing = True
                    self.step_start_time = now
                return

            current_btn_id = self.sequence[self.showing_step]

            if self.is_flashing:
                if now - self.step_start_time >= self.flash_duration:
                    self.buttons[current_btn_id].is_lit = False
                    self.is_flashing = False
                    self.step_start_time = now
            else:
                if now - self.step_start_time >= self.pause_duration:
                    self.showing_step += 1
                    if self.showing_step < len(self.sequence):
                        next_id = self.sequence[self.showing_step]
                        self.buttons[next_id].is_lit = True
                        self.play_tone(next_id)
                        self.is_flashing = True
                        self.step_start_time = now
                    else:
                        self.state = "PLAYER_TURN"
                        self.turn_start_time = now
                        self.turn_time_left = self.turn_time_limit

        elif self.state == "PLAYER_TURN":
            self.check_turn_timeout(now)

    def handle_event(self, event):
        if self.state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if self.state == "PLAYER_TURN" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # A click that arrives after time ran out must not count
            if self.check_turn_timeout(pygame.time.get_ticks()):
                return

            for btn in self.buttons:
                if btn.contains(event.pos):
                    if self.player_lit_button is not None:
                        self.player_lit_button.is_lit = False  # avoid a stuck-lit pad on fast clicks
                    btn.is_lit = True
                    self.player_lit_button = btn
                    self.player_lit_start = pygame.time.get_ticks()
                    self.play_tone(btn.color_id)

                    self.register_player_click(btn.color_id)
                    break

    def register_player_click(self, color_id):
        self.player_input.append(color_id)
        current_idx = len(self.player_input) - 1

        if self.player_input[current_idx] != self.sequence[current_idx]:
            self.game_over_reason = "WRONG PATTERN! GAME OVER"
            self.state = "GAME_OVER"
            return

        if len(self.player_input) == len(self.sequence):
            self.score += 1
            self.start_next_round()

    def reset(self):
        self.sequence.clear()
        self.player_input.clear()
        self.score = 0
        self.game_over_reason = ""
        for btn in self.buttons:
            btn.is_lit = False
        self.player_lit_button = None
        self.start_next_round()

    def render_timer_bar(self, screen):
        left = self.buttons[0].rect.left
        width = self.buttons[1].rect.right - left
        bar = pygame.Rect(left, 125, width, 14)

        ratio = self.turn_time_left / self.turn_time_limit
        if ratio > 0.5:
            fill_color = (80, 240, 130)
        elif ratio > 0.25:
            fill_color = (255, 220, 80)
        else:
            fill_color = (240, 70, 70)

        pygame.draw.rect(screen, (45, 48, 58), bar, border_radius=7)
        fill = bar.copy()
        fill.width = int(bar.width * ratio)
        if fill.width > 0:
            pygame.draw.rect(screen, fill_color, fill, border_radius=7)
        pygame.draw.rect(screen, (70, 75, 85), bar, width=2, border_radius=7)

    def render(self, screen):
        screen.fill((22, 24, 30))

        title_surf = self.font_title.render("Memory Pattern Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 20))

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 60))

        status_text = "Watch the pattern..." if self.state == "WATCH" else "Your turn: Click the pattern!"
        status_color = (190, 195, 205) if self.state == "WATCH" else (80, 240, 130)
        status_surf = self.font_medium.render(status_text, True, status_color)
        screen.blit(status_surf, (self.width // 2 - status_surf.get_width() // 2, 95))

        if self.state == "PLAYER_TURN":
            self.render_timer_bar(screen)

        for btn in self.buttons:
            btn.render(screen)

        if self.state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_title.render(self.game_over_reason, True, (240, 70, 70))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_score_surf = self.font_medium.render(f"Final Score: {self.score}", True, (255, 255, 255))
            screen.blit(final_score_surf, (self.width // 2 - final_score_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_medium.render("Press [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))