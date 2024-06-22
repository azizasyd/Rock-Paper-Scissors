class Game:
    def __init__(self, id):
        # Initialize game state variables
        self.p1Went = False  # Player 1's move status
        self.p2Went = False  # Player 2's move status
        self.ready = False  # Game readiness status
        self.id = id  # Game ID
        self.moves = [None, None]  # List to store moves of both players
        self.wins = [0, 0]  # List to keep track of wins for both players
        self.ties = 0  # Counter for tie games

    def get_player_move(self, p):
        """
        :param p: Player index [0,1]
        :return: Move of the specified player
        """
        return self.moves[p]

    def play(self, player, move):
        # Record the move of the player
        self.moves[player] = move
        if player == 0:
            self.p1Went = True  # Update Player 1's move status
        else:
            self.p2Went = True  # Update Player 2's move status

    def connected(self):
        # Check if both players are connected and the game is ready
        return self.ready

    def bothWent(self):
        # Check if both players have made their moves
        return self.p1Went and self.p2Went

    def winner(self):
        # Determine the winner
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1  # Tie

        # Determine the winner
        if p1 == "R" and p2 == "S":
            winner = 0  # Rock beats Scissors, Player 1 wins
        elif p1 == "S" and p2 == "R":
            winner = 1  # Scissors loses to Rock, Player 2 wins
        elif p1 == "P" and p2 == "R":
            winner = 0  # Paper beats Rock, Player 1 wins
        elif p1 == "R" and p2 == "P":
            winner = 1  # Rock loses to Paper, Player 2 wins
        elif p1 == "S" and p2 == "P":
            winner = 0  # Scissors beats Paper, Player 1 wins
        elif p1 == "P" and p2 == "S":
            winner = 1  # Paper loses to Scissors, Player 2 wins

        return winner  # Return the winner

    def resetWent(self):
        # Reset the move status for both players
        self.p1Went = False
        self.p2Went = False
