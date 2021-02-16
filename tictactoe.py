# Author: Rachel Traina-Grandon

import random

def show_instructions():
    """Displays instructions for playing the game."""

    print "Welcome to Tic-Tac-Toe!"
    print "You will play as 'X' against the computer ('O'). When it is your turn, choose the number of the space you would like to occupy. This is our gameboard:\n"
    
    # Init game board with numbers to show possible moves to player
    show_curr_board([2,3,4,5,6,7,8,9,10])


def show_curr_board(board):
    """Displays current board positions."""

    # Display current positions, defined as 0 for computer and 1 for user
    for i in range(3):
        print " ",
        for j in range(3):
            if board[i * 3 + j] == 1:
                print 'X',
            elif board[i * 3 + j] == 0:
                print 'O',  
            elif board[i * 3 + j] != -1:
                print board[i * 3 + j] - 1,
            else:
                print ' ',
            
            # Print delimeters/lines between position values
            if j != 2:
                print " | ",
        print
        
        # Print lines between rows
        if i != 2:
            print "-----------------"
        else: 
            print 

    print "- - - - - - - - - - - - - - - - -\n"


def get_user_position(turn):
    """Gets user's desired game position."""

    valid = False
    while not valid:
        try:
            user = int(raw_input("Where to place your " + turn + " (1-9)?  "))
            if user >= 1 and user <= 9:
                return user - 1
            else:
                print "That's not a valid move. :( Please try again.\n"
                show_instructions()
        except:
            pass
 
     
def get_win_status(board):
    """Checks for current winner status after 4 moves in game."""

    win_combos = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]

    for combo in win_combos:
        try:
            if board[combo[0] - 1] == 1 and board[combo[1] - 1] == 1 and board[combo[2] - 1] == 1:
                # User has won!
                return 1
            elif board[combo[0] - 1] == 0 and board[combo[1] - 1] == 0 and board[combo[2] - 1] == 0:
                # Computer has won!
                return 0
        except:
            pass
    # Return -1 for logic in main()
    return -1


def main():
    """Main app function to begin Tic-Tac-Toe. 

    Initiates gameboard with instructions, monitors game progress, and closes 
    once winner found or no moves remain."""
    
    # Get instructions at the beginning of the game
    show_instructions()

    # Start with empty board and append -1 for logic in show_curr_board()
    board = []
    for i in range(9):
        board.append(-1)

    # Init variables to look at current game conditions
    win = False
    move = 0

    #While there is no winner
    while not win:
        # Display the board
        show_curr_board(board)
        print "Turn #%s" %(move+1)
        if move % 2 == 0:
            turn = 'X'
        else:
            turn = 'O'

        # Get player input for next turn
        if turn == 'X':
            user = get_user_position(turn)
            # While space is occupied
            while board[user] != -1:
                print "Oh no -- That tac has been ticked! Try again.\n"
                user = get_user_position(turn)
            board[user] = 1

        # Get computer input for next turn
        else:
            try:
                computer = random.randrange(10)
                # While space is occupied
                while board[computer] != -1:
                    computer = random.randrange(10)
                board[computer] = 0
                print "The computer has moved.\n"
            except:
                pass

        # Increment move and check if a winner has been declared once enough moves have been made
        move += 1
        if move > 4:
            winner = get_win_status(board)

            # If there is a valid winner before 9th move
            if winner != -1:
                if winner == 1:
                    print "You won!"
                elif winner == 0:
                    print "The computer is too smart for you!"
                win = True
                quit()

            elif move == 9 and not win:
                print "No winner this round. :( "
                quit()


# Helper function to get app started
if __name__ == "__main__":
    main()
    
