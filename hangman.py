"""
Enhanced Pygame Hangman game with difficulty levels, hints, and scoring.

The GUI depends on ``pygame`` but core logic is importable without it, making
it safe to run unit tests in environments where the graphical dependencies are
missing. When executed as a script, the program will warn and exit if ``pygame``
can't be imported.
"""

from __future__ import annotations

import random
import sys
from typing import TYPE_CHECKING

try:  # Optional import so test environments without pygame still work.
    import pygame

    PYGAME_AVAILABLE = True
except ImportError:  # pragma: no cover - guarded by optional dependency
    pygame = None  # type: ignore[assignment]
    PYGAME_AVAILABLE = False
    print("Warning: pygame not available. Install with: pip install pygame", file=sys.stderr)

try:
    import nltk
    from nltk.corpus import words as nltk_words

    NLTK_AVAILABLE = True
except ImportError:  # pragma: no cover - environment specific
    nltk = None  # type: ignore[assignment]
    nltk_words = None  # type: ignore[assignment]
    NLTK_AVAILABLE = False
    print(
        "Warning: NLTK not available. Install with: pip install nltk",
        file=sys.stderr,
    )
    print(
        "Then run: python -c 'import nltk; nltk.download(\"words\")'",
        file=sys.stderr,
    )

if TYPE_CHECKING:  # pragma: no cover - typing helpers
    import pygame as _pygame

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 120, 220)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "EASY": {"min_length": 4, "max_length": 6, "max_attempts": 8, "hint_cost": 1},
    "MEDIUM": {
        "min_length": 6,
        "max_length": 9,
        "max_attempts": 7,
        "hint_cost": 2,
    },
    "HARD": {"min_length": 9, "max_length": 15, "max_attempts": 6, "hint_cost": 3},
}

# Default word list (fallback if NLTK unavailable)
DEFAULT_WORDS = [
    "python",
    "programming",
    "algorithm",
    "developer",
    "function",
    "variable",
    "computer",
    "keyboard",
    "software",
    "hardware",
    "internet",
    "database",
    "security",
    "network",
    "terminal",
    "compiler",
    "debugging",
    "framework",
    "repository",
    "authentication",
    "encryption",
    "bandwidth",
    "firewall",
]


class WordManager:
    """Manages word selection with difficulty levels."""

    def __init__(self):
        self.word_cache = {"EASY": [], "MEDIUM": [], "HARD": []}
        self._initialize_words()

    def _initialize_words(self) -> None:
        """Load and categorize words by difficulty."""

        if NLTK_AVAILABLE:
            try:
                all_words = [
                    word.lower()
                    for word in nltk_words.words()
                    if word.isalpha() and len(word) >= 4
                ]
            except LookupError:
                print("Downloading NLTK words corpus...")
                nltk.download("words", quiet=True)
                all_words = [
                    word.lower()
                    for word in nltk_words.words()
                    if word.isalpha() and len(word) >= 4
                ]
        else:
            all_words = DEFAULT_WORDS

        for difficulty, settings in DIFFICULTY_SETTINGS.items():
            min_len = settings["min_length"]
            max_len = settings["max_length"]
            self.word_cache[difficulty] = [
                word for word in all_words if min_len <= len(word) <= max_len
            ]

        for difficulty, words in self.word_cache.items():
            if not words:
                self.word_cache[difficulty] = DEFAULT_WORDS

    def available_difficulties(self) -> tuple[str, ...]:
        """Return the configured difficulty levels."""

        return tuple(self.word_cache.keys())

    def get_word(self, difficulty: str = "MEDIUM") -> str:
        """Get a random word for the specified difficulty."""

        words = self.word_cache.get(difficulty, self.word_cache["MEDIUM"])
        return random.choice(words)


class HangmanGame:
    """Core game logic for Hangman."""

    def __init__(self, secret_word: str, difficulty: str = "MEDIUM"):
        if not secret_word.isalpha():
            raise ValueError("Secret word must contain only alphabetic characters.")

        if difficulty not in DIFFICULTY_SETTINGS:
            raise ValueError(f"Unknown difficulty '{difficulty}'.")

        self.secret_word = secret_word.lower()
        self.difficulty = difficulty
        self.max_attempts = DIFFICULTY_SETTINGS[difficulty]["max_attempts"]

        self.guessed_letters: set[str] = set()
        self.wrong_guesses: set[str] = set()
        self.hints_used = 0
        self.revealed_hints: set[int] = set()

    @property
    def remaining_attempts(self) -> int:
        """Return remaining attempts."""

        return self.max_attempts - len(self.wrong_guesses)

    @property
    def score(self) -> int:
        """Calculate score based on performance."""

        base_score = len(self.secret_word) * 10
        attempts_bonus = self.remaining_attempts * 5
        hint_penalty = self.hints_used * 10
        difficulty_multiplier = {"EASY": 1, "MEDIUM": 1.5, "HARD": 2}[self.difficulty]
        return int((base_score + attempts_bonus - hint_penalty) * difficulty_multiplier)

    def masked_word(self) -> list[str]:
        """Return the word as a list with unguessed letters masked."""

        return [
            letter
            if (letter in self.guessed_letters or i in self.revealed_hints)
            else "_"
            for i, letter in enumerate(self.secret_word)
        ]

    def guess(self, letter: str) -> bool:
        """Process a guess. Returns True if correct."""

        letter = letter.lower()

        if not letter.isalpha() or len(letter) != 1:
            return False

        if letter in self.guessed_letters or letter in self.wrong_guesses:
            return False

        if letter in self.secret_word:
            self.guessed_letters.add(letter)
            return True

        self.wrong_guesses.add(letter)
        return False

    def get_hint(self) -> bool:
        """Reveal a random unguessed letter. Returns True if hint was given."""

        if self.hints_used >= 3:
            return False

        unrevealed = [
            i
            for i, letter in enumerate(self.secret_word)
            if letter not in self.guessed_letters and i not in self.revealed_hints
        ]

        if unrevealed:
            hint_index = random.choice(unrevealed)
            self.revealed_hints.add(hint_index)
            self.guessed_letters.add(self.secret_word[hint_index])
            self.hints_used += 1
            return True
        return False

    def is_won(self) -> bool:
        """Check if player has won."""

        return all(letter in self.guessed_letters for letter in set(self.secret_word))

    def is_lost(self) -> bool:
        """Check if player has lost."""

        return self.remaining_attempts <= 0

    def game_over(self) -> bool:
        """Check if game is over."""

        return self.is_won() or self.is_lost()


class Button:
    """Simple button class for pygame."""

    def __init__(
        self, pos: tuple[int, int], size: tuple[int, int], text: str, color: tuple
    ) -> None:
        if not PYGAME_AVAILABLE:  # pragma: no cover - GUI guard
            raise RuntimeError("pygame is required to create buttons")

        self.rect = pygame.Rect(*pos, *size)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(c + 30, 255) for c in color)
        self.is_hovered = False

    def draw(self, screen: "_pygame.Surface", font: "_pygame.font.Font") -> None:
        """Draw the button."""

        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event: "_pygame.event.Event") -> bool:
        """Handle mouse events. Returns True if clicked."""

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class LetterButton(Button):
    """Button for letter selection."""

    def __init__(self, x: int, y: int, letter: str):
        super().__init__((x, y), (50, 50), letter.upper(), BLUE)
        self.letter = letter
        self.disabled = False

    def draw(self, screen: "_pygame.Surface", font: "_pygame.font.Font") -> None:
        """Draw letter button."""

        if self.disabled:
            pygame.draw.rect(screen, LIGHT_GRAY, self.rect, border_radius=5)
            pygame.draw.rect(screen, GRAY, self.rect, 2, border_radius=5)
            text_color = GRAY
        else:
            color = self.hover_color if self.is_hovered else self.color
            pygame.draw.rect(screen, color, self.rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
            text_color = WHITE

        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event: "_pygame.event.Event") -> bool:
        """Handle events, but only if not disabled."""

        if self.disabled:
            return False
        return super().handle_event(event)


class HangmanDrawing:
    """Draws the hangman figure."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def set_position(self, x: int, y: int) -> None:
        """Move the drawing origin to a new coordinate."""

        self.x = x
        self.y = y

    def draw(self, screen: "_pygame.Surface", wrong_count: int) -> None:
        """Draw hangman based on wrong guess count."""

        pygame.draw.line(
            screen, BLACK, (self.x, self.y + 200), (self.x + 100, self.y + 200), 5
        )  # Base
        pygame.draw.line(
            screen, BLACK, (self.x + 20, self.y + 200), (self.x + 20, self.y), 5
        )  # Pole
        pygame.draw.line(
            screen, BLACK, (self.x + 20, self.y), (self.x + 100, self.y), 5
        )
        pygame.draw.line(
            screen, BLACK, (self.x + 100, self.y), (self.x + 100, self.y + 30), 3
        )

        if wrong_count >= 1:  # Head
            pygame.draw.circle(screen, RED, (self.x + 100, self.y + 50), 20, 3)

        if wrong_count >= 2:  # Body
            pygame.draw.line(
                screen, RED, (self.x + 100, self.y + 70), (self.x + 100, self.y + 130), 3
            )

        if wrong_count >= 3:  # Left arm
            pygame.draw.line(
                screen, RED, (self.x + 100, self.y + 85), (self.x + 70, self.y + 105), 3
            )

        if wrong_count >= 4:  # Right arm
            pygame.draw.line(
                screen, RED, (self.x + 100, self.y + 85), (self.x + 130, self.y + 105), 3
            )

        if wrong_count >= 5:  # Left leg
            pygame.draw.line(
                screen, RED, (self.x + 100, self.y + 130), (self.x + 75, self.y + 170), 3
            )

        if wrong_count >= 6:  # Right leg
            pygame.draw.line(
                screen, RED, (self.x + 100, self.y + 130), (self.x + 125, self.y + 170), 3
            )


class HangmanGUI:  # pylint: disable=too-many-instance-attributes
    """Main GUI for the Hangman game."""

    def __init__(self):
        if not PYGAME_AVAILABLE:
            raise RuntimeError("pygame is required to run the GUI.")

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hangman Game")
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.Font(None, 60)
        self.large_font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.tiny_font = pygame.font.Font(None, 22)

        self.word_manager = WordManager()
        self.game: HangmanGame | None = None
        self.difficulty = "MEDIUM"
        self.total_score = 0
        self.games_played = 0

        self.hangman_drawing = HangmanDrawing(150, 120)
        self.letter_buttons: list[LetterButton] = []
        self._create_letter_buttons()

        self.state = "MENU"  # MENU, PLAYING, GAME_OVER

    def _create_letter_buttons(self) -> None:
        """Create keyboard letter buttons."""

        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        start_x = 100
        start_y = 500
        spacing = 60

        for i, letter in enumerate(letters):
            row = i // 13
            col = i % 13
            x = start_x + (col * spacing)
            y = start_y + (row * spacing)
            self.letter_buttons.append(LetterButton(x, y, letter))

    def start_new_game(self) -> None:
        """Start a new game."""

        word = self.word_manager.get_word(self.difficulty)
        self.game = HangmanGame(word, self.difficulty)
        self.state = "PLAYING"

        for button in self.letter_buttons:
            button.disabled = False

    def draw_menu(self) -> bool:  # pylint: disable=too-many-locals
        """Draw the main menu."""

        self.screen.fill(WHITE)

        title = self.title_font.render("HANGMAN", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        if NLTK_AVAILABLE:
            word_count = len(self.word_manager.word_cache[self.difficulty])
            subtitle = self.tiny_font.render(
                f"Powered by NLTK - {word_count} words available",
                True,
                GRAY,
            )
        else:
            subtitle = self.tiny_font.render(
                "Using default word list - Install NLTK for more words!", True, ORANGE
            )
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle, subtitle_rect)

        diff_text = self.medium_font.render("Select Difficulty:", True, BLACK)
        diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(diff_text, diff_rect)

        difficulties = ["EASY", "MEDIUM", "HARD"]
        colors = [GREEN, YELLOW, RED]
        y_pos = 280

        diff_buttons = []
        for i, (diff, color) in enumerate(zip(difficulties, colors)):
            btn_pos = (SCREEN_WIDTH // 2 - 150, y_pos + i * 80)
            btn = Button(btn_pos, (300, 60), diff, color)

            if diff == self.difficulty:
                pygame.draw.rect(
                    self.screen, ORANGE, btn.rect.inflate(10, 10), 4, border_radius=10
                )

            btn.draw(self.screen, self.medium_font)
            diff_buttons.append((btn, diff))

            settings = DIFFICULTY_SETTINGS[diff]
            info = self.tiny_font.render(
                f"Words: {settings['min_length']}-{settings['max_length']} letters | "
                f"Attempts: {settings['max_attempts']} | Hint cost: {settings['hint_cost']}",
                True,
                DARK_GRAY,
            )
            center_y = y_pos + i * 80 + 75
            info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, center_y))
            self.screen.blit(info, info_rect)

        start_btn = Button((SCREEN_WIDTH // 2 - 100, 580), (200, 60), "START GAME", BLUE)
        start_btn.draw(self.screen, self.large_font)

        if self.games_played > 0:
            stats = self.small_font.render(
                f"Games Played: {self.games_played} | Total Score: {self.total_score}",
                True,
                DARK_GRAY,
            )
            stats_rect = stats.get_rect(center=(SCREEN_WIDTH // 2, 665))
            self.screen.blit(stats, stats_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            for btn, diff in diff_buttons:
                if btn.handle_event(event):
                    self.difficulty = diff

            if start_btn.handle_event(event):
                self.start_new_game()

        return True

    def draw_game(self) -> bool:  # pylint: disable=too-many-locals,too-many-branches
        """Draw the active game."""

        if not self.game:
            return True

        self.screen.fill(WHITE)

        self.hangman_drawing.draw(self.screen, len(self.game.wrong_guesses))

        masked = self.game.masked_word()
        word_display = " ".join(masked)
        word_surf = self.large_font.render(word_display, True, BLACK)
        word_rect = word_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(word_surf, word_rect)

        info_y = 270
        attempts_text = f"Attempts: {self.game.remaining_attempts}/{self.game.max_attempts}"
        attempts_surf = self.medium_font.render(attempts_text, True, DARK_GRAY)
        attempts_rect = attempts_surf.get_rect(center=(SCREEN_WIDTH // 2, info_y))
        self.screen.blit(attempts_surf, attempts_rect)

        if self.game.wrong_guesses:
            wrong = ", ".join(sorted(self.game.wrong_guesses, key=str.upper))
            wrong_text = f"Wrong: {wrong}"
            wrong_surf = self.small_font.render(wrong_text, True, RED)
            wrong_rect = wrong_surf.get_rect(center=(SCREEN_WIDTH // 2, info_y + 40))
            self.screen.blit(wrong_surf, wrong_rect)

        diff_surf = self.tiny_font.render(f"Difficulty: {self.game.difficulty}", True, GRAY)
        self.screen.blit(diff_surf, (10, 10))

        score_surf = self.tiny_font.render(f"Current Score: {self.game.score}", True, GRAY)
        self.screen.blit(score_surf, (SCREEN_WIDTH - 200, 10))

        hint_btn = Button(
            (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 70),
            (130, 50),
            f"HINT ({3 - self.game.hints_used})",
            ORANGE,
        )
        if self.game.hints_used >= 3:
            hint_btn.color = GRAY
            hint_btn.hover_color = GRAY
        hint_btn.draw(self.screen, self.small_font)

        for button in self.letter_buttons:
            button.draw(self.screen, self.small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    self._handle_guess(event.unicode.lower())

            if hint_btn.handle_event(event):
                if self.game.get_hint():
                    for button in self.letter_buttons:
                        if button.letter.lower() in self.game.guessed_letters:
                            button.disabled = True

            for button in self.letter_buttons:
                if button.handle_event(event):
                    self._handle_guess(button.letter.lower())

        if self.game.game_over():
            self.state = "GAME_OVER"
            if self.game.is_won():
                self.total_score += self.game.score
            self.games_played += 1

        return True

    def _handle_guess(self, letter: str) -> None:
        """Handle a letter guess."""

        if not self.game or self.game.game_over():
            return

        if letter in self.game.guessed_letters or letter in self.game.wrong_guesses:
            return

        self.game.guess(letter)

        for button in self.letter_buttons:
            if button.letter.lower() == letter:
                button.disabled = True
                break

    def draw_game_over(self) -> bool:  # pylint: disable=too-many-locals
        """Draw game over screen."""

        if not self.game:
            return True

        self.screen.fill(WHITE)

        self.hangman_drawing.draw(self.screen, len(self.game.wrong_guesses))

        if self.game.is_won():
            result_text = "CONGRATULATIONS!"
            result_color = GREEN
            message = "You guessed the word!"
        else:
            result_text = "GAME OVER"
            result_color = RED
            message = "Better luck next time!"

        result_surf = self.title_font.render(result_text, True, result_color)
        result_rect = result_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(result_surf, result_rect)

        message_surf = self.medium_font.render(message, True, BLACK)
        message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 2, 260))
        self.screen.blit(message_surf, message_rect)

        word_text = f"The word was: {self.game.secret_word.upper()}"
        word_surf = self.large_font.render(word_text, True, BLUE)
        word_rect = word_surf.get_rect(center=(SCREEN_WIDTH // 2, 330))
        self.screen.blit(word_surf, word_rect)

        if self.game.is_won():
            score_text = f"Score: {self.game.score}"
            score_surf = self.medium_font.render(score_text, True, ORANGE)
            score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 390))
            self.screen.blit(score_surf, score_rect)

        stats_text = f"Total Score: {self.total_score} | Games: {self.games_played}"
        stats_surf = self.small_font.render(stats_text, True, DARK_GRAY)
        stats_rect = stats_surf.get_rect(center=(SCREEN_WIDTH // 2, 440))
        self.screen.blit(stats_surf, stats_rect)

        play_again_btn = Button((SCREEN_WIDTH // 2 - 250, 520), (200, 60), "PLAY AGAIN", GREEN)
        menu_btn = Button((SCREEN_WIDTH // 2 + 50, 520), (200, 60), "MAIN MENU", BLUE)

        play_again_btn.draw(self.screen, self.medium_font)
        menu_btn.draw(self.screen, self.medium_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if play_again_btn.handle_event(event):
                self.start_new_game()

            if menu_btn.handle_event(event):
                self.state = "MENU"

        return True

    def run(self) -> None:
        """Main game loop."""

        running = True
        while running:
            if self.state == "MENU":
                running = self.draw_menu()
            elif self.state == "PLAYING":
                running = self.draw_game()
            elif self.state == "GAME_OVER":
                running = self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


def main() -> None:
    """Entry point for the game."""

    if not PYGAME_AVAILABLE:
        raise SystemExit(
            "pygame is required to run the GUI. Install it with 'pip install pygame'."
        )

    game = HangmanGUI()
    game.run()


if __name__ == "__main__":
    main()
