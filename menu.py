import pygame

from globalSettings import STG_textColor


class Menu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.font = pygame.font.Font(None, 48)
        self.secondFont = pygame.font.Font(None, 32)

        self.background = pygame.image.load('img/mainMenu/background.png')
        self.button_normal = pygame.image.load("img/mainMenu/button.png")
        self.button_selected = pygame.image.load("img/mainMenu/selectedButton.png")

        self.button_text = self.font.render('START', True, (13, 23, 58))
        self.title = self.font.render('GRAVITY RUNNER', True, STG_textColor)
        self.author = self.secondFont.render('Vilcu Virgiliu', True, STG_textColor)

        self.button_rect = self.button_normal.get_rect()
        self.button_rect.topleft = (300, 300)
        self.selected = False
        self.__run_menu()

    def __run_menu(self):
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title, (255, 100))
            self.screen.blit(self.author, (560, 570))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    break
                elif event.type == pygame.MOUSEMOTION:
                    self.check_button_hover(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.selected:
                        running = False

            if self.selected:
                self.screen.blit(self.button_selected, (288, 288))
            else:
                self.screen.blit(self.button_normal, self.button_rect)

            self.screen.blit(self.button_text, (345, 315))

            pygame.display.flip()

    def check_button_hover(self, mouse_pos):
        if self.button_rect.collidepoint(mouse_pos):
            self.selected = True
        else:
            self.selected = False
