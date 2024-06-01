# Import the enum module to create enumerations
import enum

# Define an enumeration for grid positions
class GridPosition(enum.Enum):
    # Define the possible values for grid positions
    EMPTY = 0  # Represents an empty position on the grid
    YELLOW = 1 # Represents a yellow piece on the grid
    RED = 2    # Represents a red piece on the grid

# Define a class for the grid
class Grid:
    # Initialize the grid with the given number of rows and columns
    def __init__(self, rows, columns):
        self._rows = rows         # Store the number of rows
        self._columns = columns   # Store the number of columns
        self._grid = None         # Initialize the grid attribute as None
        self.initGrid()           # Call initGrid method to initialize the grid

    # Initialize the grid with empty positions
    def initGrid(self):
        # Create a 2D list filled with GridPosition.EMPTY
        self._grid = [[GridPosition.EMPTY for _ in range(self._columns)] for _ in range(self._rows)]

    # Return the current state of the grid
    def getGrid(self):
        return self._grid

    # Return the number of columns in the grid
    def getColumnCount(self):
        return self._columns

    # Place a piece in the specified column
    def placePiece(self, column, piece):
        # Check if the column index is out of bounds
        if column < 0 or column >= self._columns:
            raise ValueError('Invalid column')  # Raise an error for invalid column
        # Check if the piece is empty (invalid move)
        if piece == GridPosition.EMPTY:
            raise ValueError('Invalid piece')   # Raise an error for invalid piece
        # Iterate from the bottom row to the top
        for row in range(self._rows-1, -1, -1):
            # Check if the current position is empty
            if self._grid[row][column] == GridPosition.EMPTY:
                # Place the piece at the current position
                self._grid[row][column] = piece
                return row  # Return the row where the piece was placed

    # Check if there's a winning sequence of pieces
    def checkWin(self, connectN, row, col, piece):
        count = 0  # Initialize count for consecutive pieces

        # Check horizontal sequence
        for c in range(self._columns):
            # Check if the current position has the piece
            if self._grid[row][c] == piece:
                count += 1  # Increment the count
            else:
                count = 0  # Reset the count
            if count == connectN:
                return True  # Return True if connectN pieces are found

        # Check vertical sequence
        count = 0  # Reset count for vertical check
        for r in range(self._rows):
            # Check if the current position has the piece
            if self._grid[r][col] == piece:
                count += 1  # Increment the count
            else:
                count = 0  # Reset the count
            if count == connectN:
                return True  # Return True if connectN pieces are found

        # Check diagonal (top-left to bottom-right) sequence
        count = 0  # Reset count for diagonal check
        for r in range(self._rows):
            # Calculate the corresponding column index for the diagonal
            c = row + col - r
            # Check if the current position is within bounds and has the piece
            if c >= 0 and c < self._columns and self._grid[r][c] == piece:
                count += 1  # Increment the count
            else:
                count = 0  # Reset the count
            if count == connectN:
                return True  # Return True if connectN pieces are found

        # Check anti-diagonal (bottom-left to top-right) sequence
        count = 0  # Reset count for anti-diagonal check
        for r in range(self._rows):
            # Calculate the corresponding column index for the anti-diagonal
            c = col - row + r
            # Check if the current position is within bounds and has the piece
            if c >= 0 and c < self._columns and self._grid[r][c] == piece:
                count += 1  # Increment the count
            else:
                count = 0  # Reset the count
            if count == connectN:
                return True  # Return True if connectN pieces are found

        # Return False if no winning sequence was found
        return False

# Define a class for a player
class Player:
    # Initialize the player with a name and piece color
    def __init__(self, name, pieceColor):
        self._name = name           # Store the player's name
        self._pieceColor = pieceColor # Store the player's piece color

    # Return the player's name
    def getName(self):
        return self._name

    # Return the player's piece color
    def getPieceColor(self):
        return self._pieceColor

# Define a class for the game
class Game:
    # Initialize the game with a grid, connectN value, and target score
    def __init__(self, grid, connectN, targetScore):
        self._grid = grid           # Store the game grid
        self._connectN = connectN   # Store the number of pieces needed to win
        self._targetScore = targetScore # Store the target score to win the game

        # Initialize the players with their names and piece colors
        self._players = [
            Player('Player 1', GridPosition.YELLOW),
            Player('Player 2', GridPosition.RED)
        ]

        # Initialize the scores for each player
        self._score = {}
        for player in self._players:
            self._score[player.getName()] = 0

    # Print the current state of the board
    def printBoard(self):
        print('Board:\n')          # Print header for the board
        grid = self._grid.getGrid()  # Get the current grid state
        for i in range(len(grid)):
            row = ''               # Initialize an empty string for the row
            for piece in grid[i]:
                # Add corresponding character for each piece type
                if piece == GridPosition.EMPTY:
                    row += '0 '  # Represent empty position with '0'
                elif piece == GridPosition.YELLOW:
                    row += 'Y '  # Represent yellow piece with 'Y'
                elif piece == GridPosition.RED:
                    row += 'R '  # Represent red piece with 'R'
            print(row)            # Print the row
        print('')                 # Print an empty line after the board

    # Handle a player's move
    def playMove(self, player):
        self.printBoard()  # Print the current board state
        print(f"{player.getName()}'s turn")  # Announce the player's turn
        colCnt = self._grid.getColumnCount()  # Get the number of columns
        # Prompt the player to enter a column index for their move
        moveColumn = int(input(f"Enter column between {0} and {colCnt - 1} to add piece: "))
        # Place the player's piece in the chosen column
        moveRow = self._grid.placePiece(moveColumn, player.getPieceColor())
        return (moveRow, moveColumn)  # Return the position of the placed piece

    # Handle a round of the game
    def playRound(self):
        while True:
            # Iterate over the players in each round
            for player in self._players:
                # Get the move position after the player makes a move
                row, col = self.playMove(player)
                pieceColor = player.getPieceColor()  # Get the player's piece color
                # Check if the player's move resulted in a win
                if self._grid.checkWin(self._connectN, row, col, pieceColor):
                    self._score[player.getName()] += 1  # Increment the player's score
                    return player  # Return the winning player

    # Play the game until a player reaches the target score
    def play(self):
        maxScore = 0  # Initialize the maximum score
        winner = None # Initialize the winner
        # Continue playing rounds until a player reaches the target score
        while maxScore < self._targetScore:
            winner = self.playRound()  # Play a round of the game
            print(f"{winner.getName()} won the round")  # Announce the round winner
            # Update the maximum score
            maxScore = max(self._score[winner.getName()], maxScore)
            self._grid.initGrid()  # Reset the grid for the next round
        print(f"{winner.getName()} won the game")  # Announce the game winner

# Create a grid with 6 rows and 7 columns
grid = Grid(6, 7)
# Create a game with the grid, requiring 4 pieces in a row to win, and a target score of 2
game = Game(grid, 4, 2)
# Start the game
game.play()



