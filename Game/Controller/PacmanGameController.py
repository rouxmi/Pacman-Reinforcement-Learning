from Game.Model.Pathfinder import Pathfinder
from Game.Model.Ghost import Ghost
from Game.Usefull.Maze_Screen_Translation import translate_screen_to_maze, translate_maze_to_screen
import random

class PacmanGameController:
    def __init__(self):
        self.ascii_maze = [ # Can be change other maze in the layouts folder
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
            "%............%%............%",
            "%.%%%%.%%%%%.%%.%%%%%.%%%%.%",
            "%o%%%%.%%%%%.%%.%%%%%.%%%%o%",
            "%.%%%%.%%%%%.%%.%%%%%.%%%%.%",
            "%..........................%",
            "%.%%%%.%%.%%%%%%%%.%%.%%%%.%",
            "%.%%%%.%%.%%%%%%%%.%%.%%%%.%",
            "%......%%....%%....%%......%",
            "%%%%%%.%%%%% %% %%%%%.%%%%%%",
            "%%%%%%.%%%%% %% %%%%%.%%%%%%",
            "%%%%%%.%            %.%%%%%%",
            "%%%%%%.% %%%%  %%%% %.%%%%%%",
            "........ %G  GG  G%  .......",
            "%%%%%%.% %%%%%%%%%% %.%%%%%%",
            "%%%%%%.%            %.%%%%%%",
            "%%%%%%.% %%%%%%%%%% %.%%%%%%",
            "%............%%............%",
            "%.%%%%.%%%%%.%%.%%%%%.%%%%.%",
            "%.%%%%.%%%%%.%%.%%%%%.%%%%.%",
            "%o..%%.......  .......%%..o%",
            "%%%.%%.%%.%%%%%%%%.%%.%%.%%%",
            "%%%.%%.%%.%%%%%%%%.%%.%%.%%%",
            "%......%%....%%....%%......%",
            "%.%%%%%%%%%%.%%.%%%%%%%%%%.%",
            "%.............P............%",
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        ]

        self.numpy_maze = []
        self.cookie_spaces = []
        self.powerup_spaces = []
        self.reachable_spaces = []
        self.ghost_spawns = []
        self.player_spawn = None
        self.ghost_colors = [
            "images/ghost.png",
            "images/ghost_pink.png",
            "images/ghost_orange.png",
            "images/ghost_blue.png"
        ]
        self.size = (0, 0)
        self.convert_maze_to_numpy()
        self.p = Pathfinder(self.numpy_maze)

    def request_new_random_path(self, in_ghost: Ghost):
        random_space = random.choice(self.reachable_spaces)
        current_maze_coord = translate_screen_to_maze(in_ghost.get_position())

        path = self.p.get_path(current_maze_coord[1], current_maze_coord[0], random_space[1],
                                random_space[0])
        test_path = [translate_maze_to_screen(item) for item in path]
        in_ghost.set_new_path(test_path)

    def convert_maze_to_numpy(self):
        for x, row in enumerate(self.ascii_maze):
            self.size = (len(row), x + 1)
            binary_row = []
            for y, column in enumerate(row):
                if column == "G": # ghost spawn
                    self.ghost_spawns.append((y, x))
                if column == "P": # player spawn
                    self.player_spawn = (y, x)
                if column == "%": # wall
                    binary_row.append(0)
                else:
                    binary_row.append(1)
                    if column == ".":  # cookie
                        self.cookie_spaces.append((y, x))
                    self.reachable_spaces.append((y, x))
                    if column == "o": # powerup
                        self.powerup_spaces.append((y, x))

            self.numpy_maze.append(binary_row)