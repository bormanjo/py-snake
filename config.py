import pygame

# colors
white = (255, 255, 255)
green = (66, 245, 84)
dark_green = (26, 92, 44)
blue = (0, 0, 128)
red = (128, 0, 0)
black = (0, 0, 0)

snake_color = green
snake_head_color = dark_green
food_color = black
background_color = white

space_dim = (60, 60)
board_size = 1200

speed = 4   # int from 1 to 10

starting_pos = [(3, 3), (3, 2), (3, 1)]

control_sets = dict(
    left=dict(
        up=pygame.K_w,
        down=pygame.K_s,
        left=pygame.K_a,
        right=pygame.K_d
    ),
    right=dict(
        up=pygame.K_UP,
        down=pygame.K_DOWN,
        left=pygame.K_LEFT,
        right=pygame.K_RIGHT
    )
)