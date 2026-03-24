import sys
sys.path.insert(0, '.')
from unbeatable_ttt import UnbeatableGame, Player
import random

def simulate_games(num_games=50):
    """Simulate random games where human plays randomly, AI plays optimally.
    Ensure AI never loses."""
    wins = 0
    draws = 0
    losses = 0
    for game_num in range(num_games):
        game = UnbeatableGame()
        game.board = [[Player.EMPTY]*3 for _ in range(3)]
        game.current_player = Player.HUMAN
        game.game_over = False
        while not game.game_over:
            # Human random move
            empty = [(r,c) for r in range(3) for c in range(3) if game.board[r][c]==Player.EMPTY]
            if not empty:
                break
            r,c = random.choice(empty)
            game.board[r][c] = Player.HUMAN
            # Check if human wins (should not happen)
            winner, _ = game.check_winner(game.board)
            if winner == Player.HUMAN:
                losses += 1
                print(f"Game {game_num}: Human won! Board:")
                print_board(game.board)
                return False
            if game.is_board_full(game.board):
                draws += 1
                break
            # AI move
            game.ai_move()
            winner, _ = game.check_winner(game.board)
            if winner == Player.AI:
                wins += 1
                break
        # after loop
        if game_num % 10 == 0:
            print(f"Completed {game_num} games...")
    print(f"Results: {wins} AI wins, {draws} draws, {losses} losses")
    if losses == 0:
        print("SUCCESS: AI never lost!")
        return True
    else:
        print("FAILURE: AI lost at least once.")
        return False

def print_board(board):
    for row in board:
        print(' '.join('.' if c==Player.EMPTY else ('X' if c==Player.HUMAN else 'O') for c in row))

if __name__ == "__main__":
    success = simulate_games(100)
    sys.exit(0 if success else 1)