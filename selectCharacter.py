import pygame


class ExportCharacter:
    selectedCharacter = None

    def __init__(self, screen):
        self.screen = screen

        self.font = pygame.font.Font(None, 48)

        self.background = pygame.image.load('img/mainMenu/background.png')
        self.alien = pygame.image.load('img/player/alien/alienMain.png')
        self.astronaut = pygame.image.load('img/player/astronaut/astronautMain.png')
        self.title = self.font.render('CHOOSE YOUR CHARACTER!', False, 'white')

        self.__run_menu()

    def __run_menu(self):
        running = True

        while running:
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.alien, (150, 200))
            self.screen.blit(self.astronaut, (450, 200))
            self.screen.blit(self.title, (160, 155))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 150 <= mouse_pos[0] <= 150 + self.alien.get_width() and 200 <= mouse_pos[
                        1] <= 200 + self.alien.get_height():
                        self.selectedCharacter = 'Alien'
                        running = False
                    elif 450 <= mouse_pos[0] <= 450 + self.astronaut.get_width() and 200 <= mouse_pos[
                        1] <= 200 + self.astronaut.get_height():
                        self.selectedCharacter = 'Astronaut'
                        running = False
