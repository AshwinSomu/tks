import math

# Initialize the Tic-Tac-Toe board
board = [' ' for _ in range(9)]

def print_board():
    """Prints the current board state."""
    for row in [board[i * 3:(i + 1) * 3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')
    print()

def is_winner(board, player):
    """Checks if a player has won."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]             # diagonals
    ]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

def is_draw(board):
    """Checks if the board is in a draw state."""
    return ' ' not in board

def minimax(board, depth, is_maximizing):
    """The minimax algorithm for optimal decision-making."""
    if is_winner(board, 'O'):
        return 10 - depth
    if is_winner(board, 'X'):
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'  # AI's move
                score = minimax(board, depth + 1, False)
                board[i] = ' '  # Undo move
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'  # Player's move
                score = minimax(board, depth + 1, True)
                board[i] = ' '  # Undo move
                best_score = min(score, best_score)
        return best_score

def best_move():
    """Finds the best move for the AI."""
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'  # AI's move
            score = minimax(board, 0, False)
            board[i] = ' '  # Undo move
            if score > best_score:
                best_score = score
                move = i
    return move

def play_game():
    """Main game loop."""
    print("Welcome to Tic-Tac-Toe!")
    print_board()
    
    while True:
        # Player move
        player_move = int(input("Enter your move (1-9): ")) - 1
        if board[player_move] != ' ':
            print("Invalid move! Try again.")
            continue
        board[player_move] = 'X'
        print_board()

        if is_winner(board, 'X'):
            print("You win!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        # AI move
        print("AI is making a move...")
        ai_move = best_move()
        board[ai_move] = 'O'
        print_board()

        if is_winner(board, 'O'):
            print("AI wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

# Run the game
if __name__ == "__main__":
    play_game()