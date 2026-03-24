import sys
sys.path.insert(0, '.')
from unbeatable_ttt import UnbeatableGame, Player

def test_minimax():
    game = UnbeatableGame()
    # Test empty board: AI should pick any empty cell (should be a valid move)
    game.board = [[Player.EMPTY]*3 for _ in range(3)]
    game.current_player = Player.AI
    game.ai_move()
    # Count AI moves
    ai_count = sum(1 for row in game.board for cell in row if cell == Player.AI)
    assert ai_count == 1, f"Expected exactly one AI move, got {ai_count}"
    print(f"Test 1 passed: AI placed at {[(r,c) for r in range(3) for c in range(3) if game.board[r][c]==Player.AI]}")
    
    # Test block human win
    game.board = [
        [Player.HUMAN, Player.HUMAN, Player.EMPTY],
        [Player.EMPTY, Player.AI, Player.EMPTY],
        [Player.EMPTY, Player.EMPTY, Player.EMPTY]
    ]
    game.current_player = Player.AI
    game.ai_move()
    # AI should block at (0,2)
    assert game.board[0][2] == Player.AI, f"Expected AI at (0,2) to block, got {game.board}"
    print("Test 2 passed: AI blocks human win")
    
    # Test AI win opportunity
    game.board = [
        [Player.AI, Player.AI, Player.EMPTY],
        [Player.EMPTY, Player.HUMAN, Player.EMPTY],
        [Player.EMPTY, Player.EMPTY, Player.HUMAN]
    ]
    game.current_player = Player.AI
    game.ai_move()
    # AI should win at (0,2)
    assert game.board[0][2] == Player.AI, f"Expected AI at (0,2) to win, got {game.board}"
    print("Test 3 passed: AI chooses winning move")
    
    # Test draw scenario
    game.board = [
        [Player.HUMAN, Player.AI, Player.HUMAN],
        [Player.AI, Player.AI, Player.HUMAN],
        [Player.HUMAN, Player.HUMAN, Player.EMPTY]
    ]
    game.current_player = Player.AI
    game.ai_move()
    # Only empty cell is (2,2), AI should fill it
    assert game.board[2][2] == Player.AI, f"Expected AI at (2,2), got {game.board}"
    print("Test 4 passed: AI fills last empty cell")
    
    # Additional test: AI should never lose (simulate a few random games)
    import random
    for _ in range(10):
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
            # Check if human wins (should not happen with perfect AI)
            winner, _ = game.check_winner(game.board)
            if winner == Player.HUMAN:
                print("ERROR: Human won against AI!")
                print(game.board)
                assert False, "AI lost!"
            if game.is_board_full(game.board):
                break
            # AI move
            game.ai_move()
            winner, _ = game.check_winner(game.board)
            if winner == Player.AI:
                # AI wins, break
                break
        print(".", end="")
    print("\nTest 5 passed: AI never loses in random play")
    
    print("All tests passed!")

if __name__ == "__main__":
    test_minimax()