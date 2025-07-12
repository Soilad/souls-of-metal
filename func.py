import pygame
import pygame.gfxdraw
from math import cos, sin

def clamp(value, a, b):
    return max(min(value, b), a)

def pichart(screen, pos, radius, percentages):
    start_angle = 0
    for percent in percentages.values():
        for i in range(1, 2 * radius):
            for j in ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                pygame.gfxdraw.pie(
                    screen,
                    pos[0] + j[0],
                    pos[1] + j[1],
                    i,
                    int(start_angle * 360),
                    int(percent[1] * 360),
                    percent[0],
                )

        start_angle = percent[1] + 1


def compass(screen, pos, line_colour, point_colour, compass_axis, tick, country_ideology):
    country_ideology /= 100
    x_right = pygame.math.Vector2(cos(tick), -sin(tick) / (2**0.5)) * 100 + pos
    x_left = pygame.math.Vector2(-cos(tick), sin(tick) / (2**0.5)) * 100 + pos
    y_right = pygame.math.Vector2(-sin(tick), -cos(tick) / (2**0.5)) * 100 + pos
    y_left = pygame.math.Vector2(sin(tick), cos(tick) / (2**0.5)) * 100 + pos
    z_right = pygame.math.Vector2(0, 1 / (2**0.5)) * 100 + pos
    z_left = pygame.math.Vector2(0, -1 / (2**0.5)) * 100 + pos
    projected_pos = (
        pygame.math.Vector2(
            country_ideology[0] * cos(tick) - country_ideology[1] * sin(tick),
            -1
            / (2**0.5)
            * (
                (country_ideology[1] * cos(tick))
                + (country_ideology[0] * sin(tick))
                - country_ideology[2]
            ),
        )
        * 100
        + pos
    )
    pygame.draw.aaline(screen, line_colour, x_right, x_left)
    pygame.draw.aaline(screen, line_colour, y_right, y_left)
    pygame.draw.aaline(screen, line_colour, z_right, z_left)
    pygame.draw.circle(screen, point_colour, projected_pos, 5)
    screen.blit(compass_axis[0], x_right + (2, 0))
    screen.blit(compass_axis[1], x_left + (2, 0))
    screen.blit(compass_axis[2], y_right + (2, 0))
    screen.blit(compass_axis[3], y_left + (2, 0))
    screen.blit(compass_axis[4], z_right + (2, 6))
    screen.blit(compass_axis[5], z_left + (2, -24))


def lerp(v0, v1, t):
    return v0 * (1 - t) + v1 * t

def truncate(text, trunc_length):
    return text if len(text) < trunc_length else text[:trunc_length:] + "..."

def outline(surface, thicc, color):
    convolution_mask = pygame.mask.Mask((thicc, thicc), fill=True)
    convolution_mask.set_at((0, 0), value=0)
    convolution_mask.set_at((thicc - 1, 0), value=0)
    convolution_mask.set_at((0, thicc - 1), value=0)
    convolution_mask.set_at((thicc - 1, thicc - 1), value=0)
    mask = pygame.mask.from_surface(surface)
    outline_surface = mask.convolve(convolution_mask).to_surface(
        setcolor=color, unsetcolor=surface.get_colorkey()
    )
    outline_surface.blit(surface, (thicc // 2, thicc // 2))
    return outline_surface


def round_corners(surface, radius):
    radius *= 3
    # Create a new surface with the same size as the input surface, but with an alpha channel
    rounded_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

    pygame.draw.rect(
        rounded_surface,
        (255, 255, 255),
        (0, 0, surface.get_width(), surface.get_height()),
        border_radius=radius,
    )

    # Use the mask to combine the original surface with the new surface with rounded corners
    surface.blit(rounded_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    return surface
