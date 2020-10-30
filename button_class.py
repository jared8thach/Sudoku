import pygame
from settings import*

class Button():

    def __init__(self, x, y, width, height,
                 color=GREY,
                 hoverColor=LIGHTGREY,
                 text=None,
                 fontSize=FONTSIZE,
                 function=None,
                 params=None):
        self.coor = (x, y)
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coor
        self.color = color
        self.hoverColor = hoverColor
        self.text = text
        self.fontSize = fontSize
        self.function = function
        self.params = params
        self.hovered = False

    def update(self, mouseCoor):
        if self.rect.collidepoint(mouseCoor):
            self.hovered = True
        else:
            self.hovered = False

    def draw(self, window):
        if self.hovered:
            self.image.fill(self.hoverColor)
        else:
            self.image.fill(self.color)

        if self.text:
            fontObj = pygame.font.SysFont(FONT, self.fontSize, bold=1)
            textSurface = fontObj.render(self.text, False, WHITE)
            width, height = textSurface.get_size()
            x = (self.width-width)//2
            y = (self.height-height)//2
            self.image.blit(textSurface, (x, y))

        window.blit(self.image, self.coor)

    def click(self):
        if self.params:
            self.function(self.params)
        else:
            self.function()
