from __future__ import annotations

import math
import random
import sys
from dataclasses import dataclass, field
from enum import IntEnum

import pygame
from pygame import gfxdraw

WIDTH, HEIGHT = 640, 480
FONT_SIZE = 17
TITLE_FONT_SIZE = 26

CHIP_RADIUS = 20
CHIP_SPACING = 60
GROUP_START = (120, 110)
GROUP_ROW_SPACING = 90

BUTTON_RECT = pygame.Rect(240, 380, 160, 50)

# Wooden board / Go-stone palette
WOOD_BASE = (200, 155, 106)
WOOD_GRID = (107, 74, 43)
COLOR_TEXT = (59, 42, 26)
COLOR_TEXT_MUTED = (122, 92, 61)
STONE_BASE = (35, 33, 31)
STONE_EDGE = (15, 14, 13)
STONE_HIGHLIGHT = (98, 92, 87)
STONE_SHADOW = (150, 112, 70)
COLOR_HIGHLIGHT = (217, 79, 48)
COLOR_BUTTON = (107, 74, 43)
COLOR_BUTTON_HOVER = (134, 95, 56)
COLOR_BUTTON_DISABLED = (170, 148, 120)
COLOR_BUTTON_TEXT = (245, 234, 214)
COLOR_WIN = (217, 79, 48)


class Player(IntEnum):
    ONE = 1
    TWO = 2

    @property
    def other(self) -> Player:
        return Player.TWO if self is Player.ONE else Player.ONE


@dataclass
class GameState:
    groups: list[int] = field(default_factory=lambda: [3, 5, 7])
    selected_group: int | None = None
    selected_count: int = 0
    current_player: Player = Player.ONE
    winner: Player | None = None

    def reset_selection(self) -> None:
        self.selected_group = None
        self.selected_count = 0

    def is_over(self) -> bool:
        return sum(self.groups) == 0

    def toggle_selection(self, group_index: int, count: int) -> None:
        if self.selected_group == group_index and self.selected_count == count:
            self.reset_selection()
        else:
            self.selected_group = group_index
            self.selected_count = count

    def can_remove_selected(self) -> bool:
        return self.winner is None and self.selected_group is not None and self.selected_count > 0

    def remove_selected(self) -> None:
        group = self.selected_group
        if group is None or self.selected_count <= 0 or self.winner is not None:
            return
        self.groups[group] = max(0, self.groups[group] - self.selected_count)
        self.reset_selection()
        if self.is_over():
            # Misère rule: whoever takes the last chip loses.
            self.winner = self.current_player.other
        else:
            self.current_player = self.current_player.other


def chip_position(group_index: int, chip_index: int) -> tuple[int, int]:
    x = GROUP_START[0] + chip_index * CHIP_SPACING
    y = GROUP_START[1] + group_index * GROUP_ROW_SPACING
    return x, y


def clicked_chip(state: GameState, pos: tuple[int, int]) -> tuple[int | None, int]:
    mouse_x, mouse_y = pos
    for group_index, count in enumerate(state.groups):
        for chip_index in range(count):
            x, y = chip_position(group_index, chip_index)
            if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= CHIP_RADIUS ** 2:
                return group_index, chip_index + 1
    return None, 0


def build_wood_background(size: tuple[int, int]) -> pygame.Surface:
    """Pre-render a subtle wood-grain board texture once, so it's cheap to blit every frame."""
    surface = pygame.Surface(size)
    surface.fill(WOOD_BASE)
    width, height = size
    rng = random.Random(7)
    for y in range(0, height, 3):
        wobble = int(math.sin(y * 0.08) * 6)
        shade = rng.randint(-12, 8)
        color = tuple(max(0, min(255, c + shade)) for c in WOOD_BASE)
        pygame.draw.line(surface, color, (0, y), (width, y + wobble), 2)
    return surface


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background = build_wood_background(screen.get_size())
        self.font = pygame.font.SysFont("georgia", FONT_SIZE)
        self.title_font = pygame.font.SysFont("georgia", TITLE_FONT_SIZE, bold=True)

    def draw_text(
        self,
        text: str,
        position: tuple[int, int],
        *,
        font: pygame.font.Font | None = None,
        color: tuple[int, int, int] = COLOR_TEXT,
        center: bool = False,
    ) -> None:
        surface = (font or self.font).render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = position
        else:
            rect.topleft = position
        self.screen.blit(surface, rect)

    def draw_chip(self, center: tuple[int, int], *, ring: bool = False) -> None:
        x, y = center
        gfxdraw.filled_circle(self.screen, x + 2, y + 3, CHIP_RADIUS, STONE_SHADOW)
        gfxdraw.filled_circle(self.screen, x, y, CHIP_RADIUS, STONE_BASE)
        gfxdraw.aacircle(self.screen, x, y, CHIP_RADIUS, STONE_EDGE)
        gloss_radius = CHIP_RADIUS // 2
        gloss_x, gloss_y = x - CHIP_RADIUS // 3, y - CHIP_RADIUS // 3
        gfxdraw.filled_circle(self.screen, gloss_x, gloss_y, gloss_radius, STONE_HIGHLIGHT)
        gfxdraw.aacircle(self.screen, gloss_x, gloss_y, gloss_radius, STONE_HIGHLIGHT)
        if ring:
            gfxdraw.aacircle(self.screen, x, y, CHIP_RADIUS + 4, COLOR_HIGHLIGHT)
            gfxdraw.aacircle(self.screen, x, y, CHIP_RADIUS + 5, COLOR_HIGHLIGHT)

    def draw_groups(self, state: GameState) -> None:
        for group_index, count in enumerate(state.groups):
            row_y = GROUP_START[1] + group_index * GROUP_ROW_SPACING
            pygame.draw.line(self.screen, WOOD_GRID, (40, row_y + 35), (WIDTH - 40, row_y + 35), 1)

            selected = state.selected_group == group_index
            for chip_index in range(count):
                pos = chip_position(group_index, chip_index)
                is_selected = selected and chip_index < state.selected_count
                self.draw_chip(pos, ring=is_selected)

    def draw_button(self, *, enabled: bool, hovered: bool) -> None:
        if not enabled:
            color = COLOR_BUTTON_DISABLED
        elif hovered:
            color = COLOR_BUTTON_HOVER
        else:
            color = COLOR_BUTTON
        pygame.draw.rect(self.screen, color, BUTTON_RECT, border_radius=8)
        pygame.draw.rect(self.screen, WOOD_GRID, BUTTON_RECT, 2, border_radius=8)
        self.draw_text("Remove selected", BUTTON_RECT.center, color=COLOR_BUTTON_TEXT, center=True)

    def draw_status(self, state: GameState) -> None:
        self.draw_text(f"Player {state.current_player}'s turn", (WIDTH - 220, 20), color=COLOR_TEXT_MUTED)

        if state.selected_group is not None and state.selected_count > 0:
            message = f"Selected {state.selected_count} chip(s) from group {state.selected_group + 1}"
        else:
            message = "Click a group of chips to select some"
        self.draw_text(message, (40, 340), color=COLOR_TEXT_MUTED)

        if state.winner is not None:
            self.draw_text(
                f"Player {state.winner} wins!",
                (WIDTH // 2, 55),
                font=self.title_font,
                color=COLOR_WIN,
                center=True,
            )
            self.draw_text(
                "Whoever takes the last chip loses.",
                (WIDTH // 2, 90),
                color=COLOR_TEXT_MUTED,
                center=True,
            )

    def render(self, state: GameState, *, button_hovered: bool) -> None:
        self.screen.blit(self.background, (0, 0))
        self.draw_status(state)
        self.draw_groups(state)
        self.draw_button(enabled=state.can_remove_selected(), hovered=button_hovered)
        pygame.display.flip()


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Nim — Misère Rules")

    renderer = Renderer(screen)
    state = GameState()
    clock = pygame.time.Clock()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        button_hovered = BUTTON_RECT.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_hovered and state.can_remove_selected():
                    state.remove_selected()
                elif state.winner is None:
                    group_index, count = clicked_chip(state, mouse_pos)
                    if group_index is not None:
                        state.toggle_selection(group_index, count)

        renderer.render(state, button_hovered=button_hovered)
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
