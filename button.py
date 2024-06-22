import pygame

class Button:
    def __init__(self, text, x, y, color):
        # Initialize button with text, position (x, y), and color
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 150
        self.attr = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        # Draw the button on the window
        pygame.draw.rect(win, self.color, self.attr)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        # Center the text on the button and draw it
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        # Check if the button is clicked based on the mouse position
        x1 = pos[0]  # get x of mouse click
        y1 = pos[1]  # get y of mouse click

        # Return True if the click is within the button's rectangle,e
        if (self.x <= x1 <= self.x + self.width) and (self.y <= y1 <= self.y + self.height):
            return True
        else:
            return False
