import sys
sys.path.insert(0, '.')
from unbeatable_ttt import UnbeatableGame, Player
import random

def test_one_game():
    game = UnbeatableGame()
    game.board = [[Player.EMPTY]*3 for _ in range(3)]
    game.current_player = Player.HUMAN
    game.game_over = False
    moves = []
    while not game.game_over:
        # Human random move
        empty = [(r,c) for r in range(3) for c in range(3) if game.board[r][c]==Player.EMPTY]
        if not empty:
            break
        r,c = random.choice(empty)
        game.board[r][c] = Player.HUMAN
        moves.append(('H', r, c))
        winner, _ = game.check_winner(game.board)
        if winner == Player.HUMAN:
            print("Human won - unexpected")
            return False
        if game.is_board_full(game.board):
            print("Draw")
            return True
        # AI move
        game.ai_move()
        winner, _ = game.check_winner(game.board)
        if winner == Player.AI:
            print("AI won")
            return True
    return True

if __name__ == "__main__":
    for i in range(5):
        if not test_one_game():
            print(f"Game {i} failed")
            sys.exit(1)
    print("All quick tests passed")