import pygame
import config


class GameObject(object):
    def __init__(self, position, dimensions, color=config.white):
        self.pos = position
        self.dim = dimensions
        self.color = color

        self.rect = pygame.Rect(*self.pos, *self.dim)

    def get_rect(self):
        return self.rect

    def draw(self, screen, color=None):
        color = self.color if color is None else color
        pygame.draw.rect(screen, color, self.rect)


class Space(GameObject):
    def __init__(self, x: int, y: int):
        super().__init__((x, y), config.space_dim)

    def __str__(self):
        return f'({self.pos[0]}, {self.pos[1]})'

    def __repr__(self):
        return self.__str__()


class Board(object):
    def __init__(self, size=config.board_size):
        self._size = size
        self._spaces = tuple(
            tuple(
                Space(x, y)
                for x in range(0, self._size, config.space_dim[0])
            ) for y in range(0, self._size, config.space_dim[1])
        )

    @property
    def width(self):
        return self._size // config.space_dim[0]

    @property
    def length(self):
        return self._size // config.space_dim[1]

    def __getitem__(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            raise IndexError
        return self._spaces[pos[1]][pos[0]]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = ''
        for y in range(self.length):
            for x in range(self.width):
                out += f'{self[x, y]}\t'
            out += '\n'
        return out

    def draw(self, screen):
        for y in range(self.length):
            for x in range(self.width):
                self[x, y].draw(screen)

    def __iter__(self):
        return (
            self[x, y]
            for y in range(len(self._spaces))
            for x in range(len(self._spaces[y]))
        )
