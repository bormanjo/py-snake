import logging
from numpy import Inf
import pygame

import config
import snake


def get_inverted_key(key, controls):
    inv_controls = {
        controls['left']: controls['right'],
        controls['right']: controls['left'],
        controls['up']: controls['down'],
        controls['down']: controls['up'],
    }
    return inv_controls[key]


class Player(snake.Snake):
    def __init__(self, board, pos=config.starting_pos):
        self.board = board
        super().__init__(config.starting_pos)

        self.controls = config.control_sets['right']
        self.last_key = None
        self.deactiv_key = None

        # Logging Config
        self.log = logging.getLogger(self.__class__.__name__)
        self.mv_cnt = 0     # Move counter

    def get_spaces(self):
        return [self.board[x, y] for x, y in self.pos]

    def is_outside(self):
        '''
        Check if any positions are outside the board -> will throw IndexError
        '''
        try:
            self.get_spaces()
            return False
        except IndexError:
            self.log.info(f'({self.mv_cnt}) Snake is outside')
            return True

    def is_overlap(self):
        '''Check if any positions are duplicated (snake eats itself)'''
        if len(self.pos) != len(set(self.pos)):
            self.log.info(f'({self.mv_cnt}) Snake ate itself')
            return True
        return False

    def eat_food(self):
        self.log.info(f'({self.mv_cnt}) Eating food')
        self.pos.add_cappacity(1)
        self.board.color = config.background_color

    def slither(self, delta):
        '''
        Slither (delta_x, delta_y) to the next position

        If next position is food, increases position capacity by 1

        Adds the next position
        '''

        head_pos = self.head()
        next_pos = (head_pos[0] + delta[0], head_pos[1] + delta[1])

        self.log.debug(f'({self.mv_cnt}) Moving from {head_pos} to {next_pos}')

        try:
            if self.board[next_pos].color == config.food_color:
                self.eat_food()
        except IndexError:
            pass

        self.pos.add(next_pos)

    def move(self):
        '''
        Map the last_key state to a board movement and slither in that
        direction

        Finally, update the deactivated key (e.g. player can only move forward,
        left or right relative to the snake's head)
        '''

        self.mv_cnt += 1    # increment for logging

        if self.last_key is None:
            return
        elif self.last_key == self.deactiv_key:
            self.last_key = get_inverted_key(self.deactiv_key, self.controls)

        # Map controls to a (position delta, deactive key)
        control_map = {
            self.controls['down']:  ((0, 1), self.controls['up']),
            self.controls['up']:    ((0, -1), self.controls['down']),
            self.controls['left']:  ((-1, 0), self.controls['right']),
            self.controls['right']: ((1, 0), self.controls['left'])
        }

        delta, deactivated_key = control_map[self.last_key]

        self.slither(delta)
        self.deactiv_key = deactivated_key

    def draw(self, screen):
        for pos in self.__iter__():
            color = self.head_color if pos == self.head() else self.color
            self.board[pos].draw(screen, color)

    def get_score(self):
        return self.pos.get_capacity() * 100


class HumanPlayer(Player):
    def react_to(self, **kwargs):
        event = kwargs.get('event', None)

        if event is None:
            self.log.debug(f'({self.mv_cnt}) No events passed to HumanPlayer')
            return

        keypress = event.type == pygame.KEYDOWN
        if keypress and event.key in self.controls.values():
            self.last_key = event.key


class AIPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = None

        self.delta_mapping = {
            (-1, 0): 'left',
            (1, 0): 'right',
            (0, -1): 'up',
            (0, 1): 'down'
        }

        # Map the delta -> key
        self.last_key = self.get_key(
                self.get_delta(self.pos[1], self.pos[0])
        )
        self.path_step = None

    def get_key(self, delta):
        direction = self.delta_mapping[delta]
        return self.controls[direction]

    @staticmethod
    def get_delta(a, b):
        '''Calculate the delta to move from point a to b'''
        return (b[0] - a[0], b[1] - a[1]) 

    def eat_food(self):
        super().eat_food()
        self.log.debug(f'({self.mv_cnt}) Resetting path step')
        self.path_step = None

    def react_to(self, **kwargs):
        self.log.debug(f'({self.mv_cnt}) Current Position: {self.head()}')

        # Path step missing -> find new path
        if self.path_step is None:
            food = self.find_food()
            if food is None:
                self.log.debug(f'({self.mv_cnt}) No food on board')
                return

            self.path = self.find_path(food)
            self.path_step = 0
        else:
            # Otherwise increment path step
            self.path_step += 1

        # Log Current Path
        self.log.debug(f'({self.mv_cnt}) Current Path [{self.path_step}/{len(self.path)}]: {self.path}')

        # If path is missing or no step to take -> report no decision
        if self.path is None or len(self.path) <= 1:
            self.log.debug(f'({self.mv_cnt}) No decision')
            return

        # If still steps to take -> take step
        if self.path_step < len(self.path) - 1:
            i = self.path_step
            delta = self.get_delta(self.path[i], self.path[i+1])
            self.log.debug(f'({self.mv_cnt}) Delta ({self.delta_mapping[delta]}): {delta} = {self.path[i+1]} - {self.path[i]}')
            self.last_key = self.get_key(delta)
        else:
            # Otherwise reset path step -> calculate new step on next loop
            self.log.warn(f'({self.mv_cnt}) No steps left to take')

    def find_path(self, target_node):
        '''
        Finds the shortest path from the head node to the target node
        using Dijkstra's Algorithm
        '''
        starting_node = self.head()

        # Set of all visited nodes
        unvisited = {(x, y) for x in range(self.board.width)
                     for y in range(self.board.length)}

        # Init distances to all nodes as Inf
        distances = {
            (x, y): Inf
            for x in range(self.board.width)
            for y in range(self.board.length)
        }
        # Dict of node previous to key
        prev = {}

        # Init distance to starting node as 0
        distances[starting_node] = 0

        def min_distance_node(unvisited):
            unvis_dist = {k: v for k, v in distances.items() if k in unvisited}
            min_dist_nodes = [
                node for node in unvisited
                if unvis_dist[node] == min(unvis_dist.values())
            ]
            if len(min_dist_nodes) == 0:
                return None
            return min_dist_nodes[0]

        def is_valid(node):
            return 0 <= node[0] < self.board.width \
                and 0 <= node[1] < self.board.length \
                and node not in self.pos

        def get_neighbors(node):
            x, y = node
            nodes = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            return [node
                    for node in nodes
                    if is_valid(node) and node in unvisited]

        path = []

        while len(unvisited) != 0:
            # Visit the unvisted node w/ min distance from source
            node = min_distance_node(unvisited)
            unvisited.remove(node)                  # Mark as visited

            # For each neighbor
            for nb_node in get_neighbors(node):
                new_distance = distances[node] + 1  # Calc dist
                if new_distance < distances[nb_node]:
                    # Update improvements
                    distances[nb_node] = new_distance
                    prev[nb_node] = node

            if node == target_node:
                if prev.get(node, None) is not None:
                    # iterate backwards over nodes for shortest path
                    while node is not None:
                        path = [node] + path
                        node = prev[node]
                        if node == starting_node:
                            path = [node] + path
                            break

        return path

    def find_food(self):
        food = [
            (x, y)
            for x in range(self.board.width)
            for y in range(self.board.length)
            if self.board[x, y].color == config.food_color
        ]
        if len(food) > 0:
            return food[0]
        return None
