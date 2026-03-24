import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import time
import threading
from enum import Enum


class Player(Enum):
    EMPTY = 0
    HUMAN = 1
    AI = 2


class UnbeatableGame:
    """Cyber-Intelligence Tic Tac Toe with unbeatable AI using Minimax."""
    
    def __init__(self):
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("Cyber-Intelligence Tic Tac Toe")
        self.root.geometry("600x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Bring window to front and focus
        self.root.lift()
        self.root.focus_force()
        self.root.after(100, lambda: self.root.focus_force())
        
        print("Cyber-Intelligence Tic Tac Toe starting...")
        print("Close this window to exit.")
        
        # Game state
        self.board = [[Player.EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = Player.HUMAN
        self.game_over = False
        self.winning_line = None
        
        # UI elements
        self.status_label = None
        self.confidence_label = None
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.reset_button = None
        
        self.create_widgets()
        self.update_status()
        
    def create_widgets(self):
        """Create all UI widgets."""
        # Title
        title = ctk.CTkLabel(self.root, text="CYBER-INTELLIGENCE TIC TAC TOE",
                             font=("Consolas", 24, "bold"))
        title.pack(pady=10)
        
        # Status frame
        status_frame = ctk.CTkFrame(self.root)
        status_frame.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(status_frame, text="", font=("Segoe UI", 16))
        self.status_label.pack(side="left", padx=10)
        
        self.confidence_label = ctk.CTkLabel(status_frame, text="AI Certainty: 100%",
                                             font=("Segoe UI", 14), text_color="cyan")
        self.confidence_label.pack(side="left", padx=10)
        
        # Game grid frame
        grid_frame = ctk.CTkFrame(self.root)
        grid_frame.pack(pady=20)
        
        # Create 3x3 grid of buttons
        for row in range(3):
            for col in range(3):
                btn = ctk.CTkButton(
                    grid_frame,
                    text="",
                    width=120,
                    height=120,
                    font=("Arial", 36, "bold"),
                    corner_radius=20,
                    command=lambda r=row, c=col: self.on_button_click(r, c)
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[row][col] = btn
        
        # Reset button
        self.reset_button = ctk.CTkButton(
            self.root,
            text="Reset Game",
            font=("Segoe UI", 18),
            width=200,
            height=40,
            command=self.reset_game
        )
        self.reset_button.pack(pady=20)
        
        # Footer
        footer = ctk.CTkLabel(self.root, text="AI Engine: Minimax Algorithm | 100% Unbeatable",
                              font=("Consolas", 12))
        footer.pack(pady=10)
    
    def on_button_click(self, row, col):
        """Handle human player's move."""
        if self.game_over or self.current_player != Player.HUMAN:
            return
        if self.board[row][col] != Player.EMPTY:
            return
        
        self.make_move(row, col, Player.HUMAN)
        self.update_status()
        
        # Check if game continues
        if not self.game_over:
            self.current_player = Player.AI
            self.status_label.configure(text="AI Thinking...")
            # Schedule AI move after 0.5 seconds
            self.root.after(500, self.ai_move)
    
    def make_move(self, row, col, player):
        """Place a move on the board and update button."""
        self.board[row][col] = player
        symbol = "X" if player == Player.HUMAN else "O"
        color = "lime" if player == Player.HUMAN else "red"
        self.buttons[row][col].configure(text=symbol, text_color=color, state="disabled")
        
        # Check for win/draw
        self.check_game_state()
    
    def check_game_state(self):
        """Check for win, lose, or draw."""
        winner, line = self.check_winner()
        if winner != Player.EMPTY:
            self.game_over = True
            self.winning_line = line
            self.highlight_winning_line(line)
            message = "You Win!" if winner == Player.HUMAN else "AI Wins!"
            self.status_label.configure(text=message)
            messagebox.showinfo("Game Over", message)
            return
        
        if self.is_board_full():
            self.game_over = True
            self.status_label.configure(text="Draw!")
            messagebox.showinfo("Game Over", "It's a Draw!")
            return
    
    def check_winner(self, board=None):
        """Return (winner, winning_line) if any, else (Player.EMPTY, None).
        If board is provided, use that board instead of self.board."""
        if board is None:
            board = self.board
        # Rows
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] != Player.EMPTY:
                return board[row][0], [(row, 0), (row, 1), (row, 2)]
        # Columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != Player.EMPTY:
                return board[0][col], [(0, col), (1, col), (2, col)]
        # Diagonals
        if board[0][0] == board[1][1] == board[2][2] != Player.EMPTY:
            return board[0][0], [(0, 0), (1, 1), (2, 2)]
        if board[0][2] == board[1][1] == board[2][0] != Player.EMPTY:
            return board[0][2], [(0, 2), (1, 1), (2, 0)]
        return Player.EMPTY, None
    
    def is_board_full(self, board=None):
        """Return True if no empty cells left.
        If board is provided, use that board instead of self.board."""
        if board is None:
            board = self.board
        for row in range(3):
            for col in range(3):
                if board[row][col] == Player.EMPTY:
                    return False
        return True
    
    def highlight_winning_line(self, line):
        """Change appearance of winning line buttons with a glowing effect."""
        if line is None:
            return
        for (row, col) in line:
            self.buttons[row][col].configure(
                fg_color="#00ffff",          # bright cyan
                hover_color="#00aaaa",
                border_color="#ffffff",
                border_width=3,
                text_color="black"           # make text stand out
            )
    
    def ai_move(self):
        """AI chooses best move using Minimax."""
        if self.game_over:
            return
        
        # Calculate best move
        best_score = -float('inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == Player.EMPTY:
                    self.board[row][col] = Player.AI
                    score = self.minimax(self.board, 0, False)
                    self.board[row][col] = Player.EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        # Make the move
        if best_move:
            row, col = best_move
            self.make_move(row, col, Player.AI)
            self.current_player = Player.HUMAN
            self.update_status()
    
    def minimax(self, board, depth, is_maximizing):
        """Minimax algorithm with depth limited to 9."""
        winner, _ = self.check_winner(board)
        if winner == Player.AI:
            return 10 - depth
        elif winner == Player.HUMAN:
            return depth - 10
        elif self.is_board_full(board):
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == Player.EMPTY:
                        board[row][col] = Player.AI
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = Player.EMPTY
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == Player.EMPTY:
                        board[row][col] = Player.HUMAN
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = Player.EMPTY
                        best_score = min(score, best_score)
            return best_score
    
    def update_status(self):
        """Update status label and confidence."""
        if self.game_over:
            return
        if self.current_player == Player.HUMAN:
            self.status_label.configure(text="Your Turn (X)")
        else:
            self.status_label.configure(text="AI Thinking...")
        # Confidence calculation (simplified)
        confidence = self.calculate_confidence()
        self.confidence_label.configure(text=f"AI Certainty: {confidence}%")
    
    def calculate_confidence(self):
        """Calculate AI's confidence based on board state."""
        # Simple heuristic: if AI is about to win, confidence high
        winner, _ = self.check_winner()
        if winner == Player.AI:
            return 100
        # Count empty cells
        empty = sum(1 for row in self.board for cell in row if cell == Player.EMPTY)
        if empty == 0:
            return 0
        # More empty cells -> lower confidence (just for show)
        return min(100, 100 - (empty * 10))
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = [[Player.EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = Player.HUMAN
        self.game_over = False
        self.winning_line = None
        
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].configure(
                    text="",
                    state="normal",
                    fg_color=["#3a7ebf", "#1f538d"],  # default
                    hover_color=["#325882", "#14375e"],
                    border_width=0,
                    border_color="",
                    text_color="white"
                )
        self.update_status()
    
    def run(self):
        """Start the main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    game = UnbeatableGame()
    game.run()