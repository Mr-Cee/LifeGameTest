import pygame


# button class
class Button:
    def __init__(self, surface, x, y, image, size_x, size_y, PlayerCharacter, action, hp_increment, food_increment, sleep_increment, cash_increment):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.action = action
        self.PlayerCharacter = PlayerCharacter
        self.hp_increment = hp_increment
        self.food_increment = food_increment
        self.sleep_increment = sleep_increment
        self.cash_increment = cash_increment

    def draw(self):

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:

                if self.action == "cash":
                    self.PlayerCharacter.cash += self.cash_increment

                
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))


