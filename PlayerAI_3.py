import math
from BaseAI_3 import BaseAI

vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

# the core of the expectimax function
class PlayerAI(BaseAI):
    def getMove(self, grid):
        _, move = self.search(grid, 0, True)
        return move

    def search(self, grid, depth, turn):
        possible_moves = grid.getAvailableMoves()
        available_cells = grid.getAvailableCells()
        # Anything higher than 3 takes more than .2 seconds
        if depth == 3 or not possible_moves:
            return self.get_heuristic(grid), None
        max_score, best_move = -math.inf, None
        # This is max turn
        if turn:
            for move in possible_moves:
                utility, _ = self.search(move[1], depth + 1, False)
                # Grab max
                if utility > max_score:
                    max_score, best_move = utility, move[0]
            return max_score, best_move
        # This is chance turn
        else:
            score = 0
            # Get's the expected value of the child.
            for move in available_cells:
                # Get the expected value of 2
                temp_grid = grid.clone()
                temp_grid.setCellValue(move, 2)
                score_2, child = self.search(temp_grid, depth + 1, True)
                # Get expected value of 4
                temp_grid = grid.clone()
                temp_grid.setCellValue(move, 4)
                score_4, child = self.search(temp_grid, depth + 1, True)
                # Expected score of the children
                score += ((.9 * score_2)/len(available_cells) + (.1 * score_4)/len(available_cells))
            return score, None

    def get_heuristic(self, grid) -> float:
        # Board pattern to maintain the higher number pieces in one corner.
        # Each value in this board represents the weight of each position.
        board_weight = [
            [3, 2, 1, 0],
            [5, 3, 2, 1],
            [15, 5, 3, 2],
            [30, 15, 5, 3]
        ]
        # Snake pattern mentioned in stackoverflow post.
        # board_weight = [
        #     [12, 9, 6, 3],
        #     [24, 21, 18, 15],
        #     [36, 33, 30, 27],
        #     [48, 45, 42, 39]
        # ]
        # 4:1:4 2048 512 2048 2048 512 2048 2048 2048 1024 2048
        # 4:8:4 1024 512 1024 2048 2048 1024 2048 1024 2048 2048
        # 4:.5.4 1024 512 1024 2048 1024 1024 1024 2048 2048 1024
        # snake 4:8:4 2048 2048 2048 1024 1024 1024 2048 1024 1024 1024
        # snake does not care about empty tiles as much
        # snake 4:.5:4 1024 1024 512 2048 1024 1024 2048 1024 512 2048
        # 4:20:4 too much emphasis on empty tiles changes alot 1024 2048 512 2048 1024 1024 1024 512 2048 512

        # Weights for each heuristic
        weight_one = 3
        weight_two = 7
        weight_three = 3
        available_moves = grid.getAvailableCells()
        total_cells = len(available_moves)
        # What the score will be based on: The weight of the board
        board_weight_h = 0
        for i in range(grid.size):
            for j in range(grid.size):
                board_weight_h = board_weight_h + (board_weight[i][j] * grid.map[i][j])
        total = board_weight_h
        # Smoothness. The less smooth the board is, the higher the penalty.
        smoothness = 0
        for i in range(grid.size):
            for j in range(grid.size - 1):
                smoothness += abs(grid.map[i][j] - grid.map[i][j + 1])
        for i in range(grid.size - 1):
            for j in range(grid.size):
                smoothness += abs(grid.map[i][j] - grid.map[i + 1][j])
        # Maintains a decreasing/increasing order rows and cols for a given tile
        monotonic_dirs = self.is_monotonic(grid)
        value = (int(monotonic_dirs[0]) + int(monotonic_dirs[1]) + int(monotonic_dirs[2]) + int(monotonic_dirs[3])) / 2
        if value == 0:
            value = .25
        total = total * (value * weight_one)
        # Last Heuristic used is the amount of empty cells currently available
        total = total * (weight_two * (total_cells / 14))
        total = total - (smoothness * weight_three)
        return total

    # Monotonic and smoothness idea obtained from
    # https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
    # This returns a tuple of size 4 that contains true of false if the grid is monotonic
    def is_monotonic(self, grid):
        return (all(grid.map[i][j] <= grid.map[i][j + 1] for i in range(grid.size) for j in range(grid.size - 1)),
                all(grid.map[i][j] >= grid.map[i][j + 1] for i in range(grid.size) for j in range(grid.size - 1)),
                all(grid.map[i][j] <= grid.map[i + 1][j] for i in range(grid.size - 1) for j in range(grid.size)),
                all(grid.map[i][j] >= grid.map[i + 1][j] for i in range(grid.size - 1) for j in range(grid.size)))
