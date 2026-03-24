import sys
sys.path.insert(0, '.')
from unbeatable_ttt import UnbeatableGame, Player

game = UnbeatableGame()
game.board = [
    [Player.HUMAN, Player.AI, Player.HUMAN],
    [Player.AI, Player.AI, Player.HUMAN],
    [Player.HUMAN, Player.HUMAN, Player.EMPTY]
]
game.current_player = Player.AI
game.game_over = False

print("Board before AI move:")
for row in game.board:
    print(row)
print("Empty cells:", [(r,c) for r in range(3) for c in range(3) if game.board[r][c]==Player.EMPTY])

# Call ai_move
game.ai_move()

print("Board after AI move:")
for row in game.board:
    print(row)
print("Empty cells:", [(r,c) for r in range(3) for c in range(3) if game.board[r][c]==Player.EMPTY])

# Check if move was made
if game.board[2][2] == Player.AI:
    print("SUCCESS: AI placed at (2,2)")
else:
    print("FAIL: AI did not place at (2,2)")