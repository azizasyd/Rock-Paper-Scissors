import pygame
from network import Network
from button import Button
pygame.font.init()

# Set up the window dimensions and create a display window
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not(game.connected()):
        # Display text if the game is not connected
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        # Display texts if the game is connected
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        # Get moves of both players
        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        # Display the moves or status based on whether both players have made their moves
        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        # Display the moves on the screen based on player number
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:  # p == 0
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        # Draw the buttons on the screen
        for btn in btns:
            btn.draw(win)

    pygame.display.update()  # Update the display

# buttons for Rock, Scissors, and Paper moves
btns = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)), Button("Paper", 450, 500, (0, 255, 0))]

def main():
    run = True
    clock = pygame.time.Clock()  # control the frame rate
    n = Network()  # handle client-server communication
    player = int(n.getP())  # get the player number from the server
    print("You are player", player)

    while run:
        clock.tick(60)

        try:
            game = n.send("get")  # Send a request to get the current game state
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)

            try:
                game = n.send("reset")  # Send a request to reset the game state
            except:
                run = False
                print("Couldn't get game")
                break

            # Display the result of the game
            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!", 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:
                text = font.render("You lost!", 1, (255, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        # Handle events (game quit and making a move)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)  # Send the move to the server
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)  # Redraw the window with the updated game state

def menu_screen():
    run = True
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        # Handle events (game quit and starting new game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

# Continuously show the menu screen
while True:
    menu_screen()
    break  # Break after showing the menu screen once
