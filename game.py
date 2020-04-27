import argparse
import logging
import pygame
import random

import config
import board
import player


class Text(object):
    def __init__(self, text, position, **kwargs):
        font_name = kwargs.get('font', 'freesansbold.ttf')
        font_size = kwargs.get('size', 32)
        self.font = pygame.font.Font(font_name, font_size)

        self.text = text
        self.position = position

        self.text_color = kwargs.get('text_color', config.blue)
        self.background = kwargs.get('background', config.white)

    def draw(self, screen):
        text_surface = \
            self.font.render(self.text, True, self.text_color, self.background)

        surface_rect = text_surface.get_rect()
        surface_rect.center = self.position

        screen.blit(text_surface, surface_rect)


def get_score_text(score, **kwargs):
    return Text(str(score), (config.board_size // 2, 20), **kwargs)


def get_gameover_text(text):
    position = (config.board_size // 2, config.board_size // 4)
    text = f'Game Over: {text}'
    return Text(text, position, text_color=config.red)


def draw_path(path, board, screen):
    if path is None or len(path) <= 1:
        return

    points = [board[pos].get_rect().center for pos in path]

    pygame.draw.lines(screen, config.red, False, points)


class Game(object):
    def __init__(self, screen, ai_player=False):
        self.clock = pygame.time.Clock()

        self.screen = screen
        self.running = False
        self.ai_player = ai_player

        self.board = None
        self.player = None
        self.food = None
        self.speed = None

    def start(self):
        # Start Loop
        while self._prompt_newgame():
            logging.info('Starting new game')
            self.board = board.Board(config.board_size)
            if self.ai_player:
                self.player = player.AIPlayer(self.board)
            else:
                self.player = player.HumanPlayer(self.board)
            self.speed = config.speed
            self.reset_food()

            self._loop()
            logging.info('Game Over')

    def _loop(self):

        self.running = True
        while self.running:
            self._key_events()
            self._move()

            # Check for gameover events
            if self.player.is_outside():
                self.running = False
                get_gameover_text('Snake hit a wall!').draw(self.screen)
                continue
            elif self.player.is_overlap():
                get_gameover_text('Snake ate itself!').draw(self.screen)
                self.running = False
                continue

            self.speed = self.get_speed(self.player.get_score())

            if not self.is_food_set():
                self.reset_food()
            self._draw()

            pygame.display.update()
            self.clock.tick(config.speed)

        pygame.display.update()
        self.clock.tick(config.speed)

    def _key_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.running = pause()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                import pdb; pdb.set_trace()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                logging.info('Restarting game')
                self.running = False
                break

            if not self.ai_player:
                self.player.react_to(event=event)

        if self.ai_player:
            self.player.react_to()

    def _move(self):
        self.player.move()

    def _draw(self):
        self.board.draw(self.screen)
        self.player.draw(self.screen)

        if isinstance(self.player, player.AIPlayer):
            draw_path(self.player.path, self.board, self.screen)

        get_score_text(self.player.get_score()).draw(self.screen)

    def _prompt_newgame(self):
        position = (config.board_size // 2, config.board_size // 3)
        Text('Start a New Game? [Y/N]', position).draw(self.screen)
        pygame.display.update()
        self.clock.tick(config.speed)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                    return True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    return False

    def is_food_set(self):
        return self.food not in self.player.get_spaces()

    def reset_food(self):
        if self.food is not None:
            self.food.color = config.background_color

        spaces = [
            s for s in self.board
            if s not in self.player.get_spaces()
        ]
        randint = random.randint(0, len(spaces) - 1)
        self.food = spaces[randint]
        self.food.color = config.food_color

    def get_speed(self, score):
        score_speed_map = {
            (0, 1000): 4,
            (1000, 2000): 5,
            (2000, 3000): 6,
            (3000, 4000): 7,
            (4000, 5000): 8,
            (5000, 6000): 9,
            (6000, 7000): 10,
            (7000, 8000): 11,
            (8000, 9000): 12,
            (9000, 10000): 13,
            (10000, 11000): 14,
        }

        for lb, ub in score_speed_map.keys():
            if lb <= score < ub:
                return score_speed_map[(lb, ub)]

        return 15


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True


def main(ai_player=False):
    pygame.init()
    screen = pygame.display.set_mode((config.board_size, config.board_size))
    pygame.display.set_caption('PySnake')

    g = Game(screen, ai_player)
    g.start()

    pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('py-snake')
    parser.add_argument('--debugging', action='store_true', default=False)
    parser.add_argument('--ai_player', action='store_true', default=False)
    # parser.add_argument('--')
    args = parser.parse_args()

    log_lvl = logging.DEBUG if args.debugging else logging.INFO
    log_fmt = '[%(asctime)s] %(levelname)s> %(message)s'
    logging.basicConfig(format=log_fmt, level=log_lvl)
    main(args.ai_player)
