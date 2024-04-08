import pygame
from Button import Button
import os


class Scene:
    def __init__(self, rect_list, next_scene_index):
        self.rect_list = rect_list
        self.next_scene_index = next_scene_index
        self.trap_list = []
        self.collectible_list = []
        self.anim_index = 0

    def draw(self, screen, background):
        screen.blit(background, (0, 0))
        self.anim_index += 0.025
        if self.anim_index > 2:
            self.anim_index = 0
        collectible_image = [pygame.image.load('Images/cat_1.png'),
                             pygame.image.load('Images/cat_2.png')]
        for rect in self.collectible_list:
            if rect[0] == False:
                screen.blit(collectible_image[int(self.anim_index)], rect[1])

    def dev_draw(self, screen):
        for rect in self.rect_list:
            pygame.draw.rect(screen, (178, 100, 255), rect)
        for rect in self.trap_list:
            pygame.draw.rect(screen, (204, 0, 100), rect)

    def check_collectible(self, player):
        for collectible in self.collectible_list:
            if collectible[0] == False and collectible[1].colliderect(player):
                collectible[0] = True

    def add_rectangle(self, screen, background,dimension_backround):
        clock = pygame.time.Clock()
        click = 0
        position1 = (0, 0)
        rect = pygame.Rect(0, 0, 0, 0)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if click == 0:
                        position1 = pygame.mouse.get_pos()
                        click = 1
                    elif click == 1:
                        return pygame.Rect(position1, (pygame.mouse.get_pos()[0]-position1[0], pygame.mouse.get_pos()[1]-position1[1]))
                if event.type == pygame.MOUSEMOTION:
                    if click == 1:
                        rect = pygame.Rect(position1, (pygame.mouse.get_pos()[
                                           0]-position1[0], pygame.mouse.get_pos()[1]-position1[1]))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            screen.blit(dimension_backround,(0,0))
            self.draw(screen, background)
            self.dev_draw(screen)
            pygame.draw.rect(screen, (255, 0, 0), rect)
            clock.tick(60)
            pygame.display.update()

    def add_rectangle_menu(self, screen, background,dimension_backround):
        clock = pygame.time.Clock()
        label_list = ['add platform', 'add trap']
        butt_list = Button.create_butt_list(
            500, 200, 50, (0, 0, 0), label_list, 300, 0)
        while True:
            for event in pygame.event.get():
                for butt in butt_list:
                    if butt.activate(event):
                        rect = self.add_rectangle(screen, background,dimension_backround)
                        if rect != None:
                            if butt.text == 'add platform':
                                self.rect_list.append(rect)
                            if butt.text == 'add trap':
                                self.trap_list.append(rect)
                        return
                    if event.type == pygame.KEYDOWN:
                        rect = self.add_rectangle(screen, background,dimension_backround)
                        if rect != None:
                            if event.key == pygame.K_ESCAPE:
                                if event.key == pygame.K_q:
                                    self.rect_list.append(rect)
                                    return
                                if event.key == pygame.K_e:
                                    self.trap_list.append(rect)
                                    return
            for butt in butt_list:
                butt.draw(screen)
            clock.tick(60)
            pygame.display.update()

    def add_collectible(self, screen, background,dimension_backround):
        clock = pygame.time.Clock()
        rect = pygame.Rect(0, 0, 64, 64)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    rect = pygame.Rect(pygame.mouse.get_pos(), (64, 64))
                    rect.center = pygame.mouse.get_pos()
                    self.collectible_list.append([False, rect])
                if event.type == pygame.MOUSEMOTION:
                    rect = pygame.Rect(pygame.mouse.get_pos(), (64, 64))
                    rect.center = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            screen.blit(dimension_backround,(0,0))
            self.draw(screen, background)
            pygame.draw.rect(screen, (255, 0, 0), rect)
            clock.tick(60)
            pygame.display.update()

    def edit_rectangle(self, screen, level, background,dimension_backround):
        clock = pygame.time.Clock()
        rect_list = []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect in self.rect_list:
                        if rect.collidepoint(pygame.mouse.get_pos()):
                            rect_list.append(rect)
                    for trap in self.trap_list:
                        if trap.collidepoint(pygame.mouse.get_pos()):
                            rect_list.append(trap)
                    for collect in self.collectible_list:
                        if collect[1].collidepoint(pygame.mouse.get_pos()):
                            rect_list.append(collect[1])
                    if level.win_square.collidepoint(pygame.mouse.get_pos()):
                        rect_list.append(level.win_square)
                    if rect_list:
                        delete_list = self.place_rectangle(
                            screen, background, rect_list,dimension_backround)
                        self.delete_rectangle(delete_list)
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            clock.tick(60)
            pygame.display.update()

    def place_rectangle(self, screen, background, rect_list,dimension_backround):
        clock = pygame.time.Clock()
        i = 0
        position = rect_list[i].center
        delete_list = []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    rect_list[i].center = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if i+1 < len(rect_list):
                        position = rect_list[i].center
                        i = +1
                    else:
                        return delete_list
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        rect_list[i].center = position
                        if i+1 < len(rect_list):
                            position = rect_list[i].center
                            i = +1
                        else:
                            return delete_list
                    if event.key == pygame.K_DELETE:
                        delete_list.append(rect_list[i])
                        rect_list.pop(i)
                        if i+1 < len(rect_list):
                            i += 1
                        else:
                            return delete_list
            screen.blit(dimension_backround,(0,0))
            self.draw(screen, background)
            self.dev_draw(screen)
            pygame.draw.rect(screen, (255, 0, 0), rect_list[i])
            clock.tick(60)
            pygame.display.update()

    def delete_rectangle(self, delete_list):
        if delete_list:
            for rect in delete_list:
                if rect in self.rect_list:
                    self.rect_list.remove(rect)
                if rect in self.trap_list:
                    self.trap_list.remove(rect)
                if [False, rect] in self.collectible_list:
                    self.collectible_list.remove([False, rect])


class Level:
    def __init__(self, scene_list_d1, scene_list_d2, x, y, win_square):
        self.scene_list_d1 = scene_list_d1
        self.scene_list_d2 = scene_list_d2
        self.level_unlock = False
        self.dimension = False
        self.start_x = x
        self.start_y = y
        self.win_square = win_square
        self.score_list = [[0, 0]]

    def get_score_list(self, screen):
        clock = pygame.time.Clock()
        stat_menu = pygame.image.load(
            'Images/stat_screen_menu.png').convert_alpha()
        butt_list = []
        if self.score_list[0][1] != 0:
            collectibles_list = []
            time_list = []
            y = self.get_collectibles()[0]
            for score in self.score_list:
                collectibles_list.append(f'{score[0]}/{y}')
                time_list.append(
                    f'{int(score[1]/60)} min {int(score[1] % 60)} sec')
            collectibles_list = Button.create_butt_list(
                820, 205, 35, (143, 120, 173), collectibles_list, 0, 40)
            time_list = Button.create_butt_list(
                620, 205, 35, (143, 120, 173), time_list, 0, 40)
            butt_list = collectibles_list+time_list
        else:
            butt_list.append(Button(620, 205, 'None', 35, (143, 120, 173)))
            butt_list.append(Button(820, 205, 'None', 35, (143, 120, 173)))
        butt_list.append(Button(820, 160, 'Collectibles', 55, (143, 120, 173)))
        butt_list.append(Button(620, 160, 'Time', 55, (143, 120, 173)))
        butt_list.append(Button(710, 605, 'Back', 60, (143, 120, 173)))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if butt_list[len(butt_list)-1].activate(event):
                    return
            screen.blit(stat_menu, (420, 50))
            for butt in butt_list:
                butt.draw(screen)
            clock.tick(60)
            pygame.display.update()

    def add_score(self, new_score):
        if self.score_list[0][1] != 0:
            self.score_list.append(new_score)
            self.score_list = sorted(self.score_list, key=lambda x: x[1])
            self.score_list = sorted(
                self.score_list, key=lambda x: x[0], reverse=True)
            if len(self.score_list) > 10:
                self.score_list.pop()
        else:
            self.score_list.pop()
            self.score_list.append(new_score)

    def get_collectibles(self):
        x = 0
        y = 0
        for scene in self.scene_list_d1:
            x += len(scene.collectible_list)
            for collectible in scene.collectible_list:
                if collectible[0] == True:
                    y += 1
        for scene in self.scene_list_d2:
            x += len(scene.collectible_list)
            for collectible in scene.collectible_list:
                if collectible[0] == True:
                    y += 1
        return [x, y]

    def get_collectibles_string(self):
        list = self.get_collectibles()
        return f'{list[1]}/{list[0]}'

    def set_collectibles(self, bool):
        for scene in self.scene_list_d1:
            for collectible in scene.collectible_list:
                collectible[0] = bool
        for scene in self.scene_list_d2:
            for collectible in scene.collectible_list:
                collectible[0] = bool

    def add_scene(self, screen):
        clock = pygame.time.Clock()
        label_list = ['right', 'left', 'up', 'down']
        next_scene_index = 'none'
        butt_list = Button.create_butt_list(
            400, 300, 75, (0, 0, 0), label_list, 150, 0)
        add_button = Button(700, 400, 'Add scene', 75, (255, 0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                for butt in butt_list:
                    if butt.activate(event):
                        butt.change_color((255, 0, 0))
                        next_scene_index = butt.text
                    else:
                        butt.change_color((0, 0, 0))
                if add_button.activate(event):
                    self.scene_list_d2[len(
                        self.scene_list_d1)-1].next_scene_index = next_scene_index
                    self.scene_list_d2.append(Scene([], 'none'))
                    self.scene_list_d1[len(
                        self.scene_list_d1)-1].next_scene_index = next_scene_index
                    self.scene_list_d1.append(Scene([], 'none'))

                    return
            for butt in butt_list:
                butt.draw(screen)
                add_button.draw(screen)
            clock.tick(60)
            pygame.display.update()

    def get_background(self, level_id, scene_index):
        if self.dimension:
            if os.path.exists(f'Images/Dimension_2/Level_{level_id+1}/scene_{scene_index+1}.png'):
                background = pygame.image.load(
                    f'Images/Dimension_2/Level_{level_id+1}/scene_{scene_index+1}.png').convert_alpha()
            else:
                background = pygame.image.load(
                    'Images/Dimension_2/background.png').convert_alpha()
        elif os.path.exists(f'Images/Dimension_1/Level_{level_id+1}/scene_{scene_index+1}.png'):
            background = pygame.image.load(
                f'Images/Dimension_1/Level_{level_id+1}/scene_{scene_index+1}.png').convert_alpha()
        else:
            background = pygame.image.load(
                'Images/Dimension_1/background.png').convert_alpha()
        return background

    def get_score_border(self):
        if self.dimension:
            return pygame.image.load('Images/Dimension_2/score_border.png').convert_alpha()
        else:
            return pygame.image.load('Images/Dimension_1/score_border.png').convert_alpha()

    def get_menu(self):
        if self.dimension:
            return pygame.image.load('Images/Dimension_2/menu_screen.png').convert_alpha()
        else:
            return pygame.image.load('Images/Dimension_1/menu_screen.png').convert_alpha()

    def get_color(self):
        if self.dimension:
            return (252, 121, 121)
        else:
            return (128, 99, 166)
