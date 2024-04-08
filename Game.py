import os
import pickle
import pygame
from Player import Player
from Button import Button
from Scene import Level, Scene
import time


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1400, 800))
        self.level_list = Game.load(self)
        self.level_list[0].level_unlock = True
        self.color = (128, 99, 166)
        Game.start_screen(self)

    def start_screen(self):
        background = pygame.image.load(
            'Images/Dimension_1/background.png').convert_alpha()
        pygame.display.set_caption('Melinoe')
        icon = pygame.image.load('Images/cat_1.png').convert_alpha()
        pygame.display.set_icon(icon)
        start_menu = pygame.image.load(
            'Images/Dimension_1/menu_screen.png').convert_alpha()
        butt_list = [Button(1200, 530, 'Play', 150, self.color),
                     Button(1200, 700, 'Exit', 75, self.color),
                     Button(1200, 630, 'Save', 75, self.color)]
        while True:
            for event in pygame.event.get():
                self.game_quit(event)
                if butt_list[0].activate(event):
                    Game.level_select(self, self.level_list)
                if butt_list[1].activate(event):
                    self.save(self.level_list)
                    pygame.quit()
                    quit()
                if butt_list[2].activate(event):
                    Game.save(self, self.level_list)
            self.screen.blit(background, (0, 0))
            self.screen.blit(start_menu, (1020, 400))
            for butt in butt_list:
                butt.draw(self.screen)
            self.update()

    def event_loop(self, level_index):
        level = self.level_list[level_index]
        level.dimension = False
        player_sprite = pygame.sprite.GroupSingle()
        player = Player(level)
        player_sprite.add(player)
        scene_list = level.scene_list_d1
        scene = level.scene_list_d1[0]
        level.set_collectibles(False)
        lab_list = [
            Button(900, 30, level.get_collectibles_string(), 75, self.color),
            Button(740, 30, '0', 75, self.color),
            Button(550, 30, f'Level {level_index+1}: ', 85, self.color)]
        dev_butt_list = Game.dev_menu(self)
        scene_index = 0
        dev_state = False
        score_border = level.get_score_border()
        background = level.get_background(level_index, scene_index)
        start_time = time.time()
        dimension_backround1 = pygame.image.load('Images/Dimension_1/background.png').convert_alpha()
        dimension_backround2 = pygame.image.load('Images/Dimension_2/background.png').convert_alpha()
        dimension_backround = dimension_backround1

        while True:
            for event in pygame.event.get():
                self.game_quit(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Game.pause_menu(self, level_index)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        if level.dimension == False:
                            if player.harsh_collisions(level.scene_list_d2[scene_index]) == False:
                                level.dimension = True
                                scene_list = level.scene_list_d2
                                score_border = level.get_score_border()
                                for label in lab_list:
                                    label.change_color(level.get_color())
                                dimension_backround = dimension_backround2
                                
                        else:
                            if player.harsh_collisions(level.scene_list_d1[scene_index]) == False:
                                level.dimension = False
                                scene_list = level.scene_list_d1
                                score_border = level.get_score_border()
                                for label in lab_list:
                                    label.change_color(level.get_color())
                                dimension_backround = dimension_backround1
                    if event.key == pygame.K_F12:
                        self.screen = pygame.display.set_mode((1800, 800))
                        dev_state = True
                if dev_state:
                    level = Game.dev_event_loop(
                        self, event, dev_butt_list, level, scene, background,dimension_backround)
            self.screen.blit(dimension_backround,(0,0))
            if level.dimension == False and player.win(scene_list):
                Game.next_level_menu(self, level_index, start_time, level)
            scene.check_collectible(player)
            player.update(scene_list)
            scene_index = player.scene_index
            scene = scene_list[scene_index]
            background = level.get_background(level_index, scene_index)
            scene.draw(self.screen, background)
            self.screen.blit(score_border, (0, 0))
            Game.update_score(self, lab_list, start_time, level)
            player_sprite.draw(self.screen)
            Game.draw_dev_menu(self, dev_state, dev_butt_list,level, scene_index, scene)
            if player.death:
                Game.death_screen(self, level_index, level)
            Game.update(self)

    def update(self):
        self.clock.tick(60)
        pygame.display.update()

    def update_score(self, lab_list, start_time, level):
        lab_list[0].change_text(level.get_collectibles_string())
        curr_time = time.time()-start_time
        lab_list[1].change_text(f'{int(curr_time/60)}:{int(curr_time % 60)}')
        for lab in lab_list:
            lab.draw(self.screen)

    def next_scene(self, pl, scene_list):
        pl.next_scene_right(scene_list)
        pl.next_scene_left(scene_list)
        pl.next_scene_up_down(scene_list)

    def game_quit(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    def save(self, level_list):
        file = open('levels', 'wb')
        pickle.dump(level_list, file)
        file.close()

    def load(self):
        if os.path.exists('levels'):
            level_list = open('levels', 'rb')
            return pickle.load(level_list)
        else:
            return ([self.new_level()])

    def level_select(self, level_list):
        self.clock.tick(60)
        background = pygame.image.load(
            'Images/select_screen.png').convert_alpha()
        butt_list = Button.create_level_select_buttons(level_list)
        title_label = Button(700, 100, 'Select a level', 125, self.color)

        while True:
            for event in pygame.event.get():
                self.game_quit(event)
                l = 0
                while l < len(butt_list)-1:
                    if butt_list[l].activate(event):
                        Game.level_select_menu(self, l, butt_list, background)
                    l += 1
                if butt_list[len(butt_list)-1].activate(event):
                    butt_list = Game.add_level(self, butt_list)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    Game.start_screen(self)
            self.screen.blit(background, (0, 0))
            for butt in butt_list:
                butt.draw(self.screen)
            title_label.draw(self.screen)
            self.update()

    def level_select_menu(self, level_index, butt_prev_list, background):
        level = self.level_list[level_index]
        menu = pygame.image.load(
            'Images/Dimension_1/menu_screen.png').convert_alpha()
        butt_list = [Button(700, 270, f'Level: {level_index+1}', 75, self.color),
                     Button(700, 490, 'Back', 60, self.color),
                     Button(700, 430, 'Statistics', 60, self.color)
                     ]
        if level.level_unlock == False:
            butt_list.append(Button(700, 350, 'Locked', 100, self.color))
        else:
            butt_list.append(Button(700, 350, 'Play', 100, self.color))
        while True:
            for event in pygame.event.get():
                self.game_quit(event)
                if butt_list[3].activate(event) and butt_list[3].text == 'Play':
                    Game.event_loop(self, level_index)
                if butt_list[1].activate(event):
                    return
                if butt_list[2].activate(event):
                    level.get_score_list(self.screen)
                    self.screen.blit(background, (0, 0))
                    for butt in butt_prev_list:
                        butt.draw(self.screen)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.screen.blit(menu, (530, 180))
            for butt in butt_list:
                butt.draw(self.screen)
            self.update()

    def pause_menu(self, level_index):
        menu = self.level_list[level_index].get_menu()
        butt_list = self.small_menu_buttons(level_index)
        butt_list.append(Button(700, 270, 'Continue', 75,
                         self.level_list[level_index].get_color()))
        while True:
            for event in pygame.event.get():
                if Game.small_menu_ev_loop(self, butt_list, level_index, event):
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            self.screen.blit(menu, (530, 180))
            for butt in butt_list:
                butt.draw(self.screen)
            self.update()

    def death_screen(self, level_index, level):
        menu = level.get_menu()
        butt_list = self.small_menu_buttons(level_index)
        butt_list.append(Button(700, 270, 'Game Over', 75,
                         self.level_list[level_index].get_color()))
        while True:
            for event in pygame.event.get():
                Game.small_menu_ev_loop(self, butt_list, level_index, event)
            self.screen.blit(menu, (530, 180))
            for butt in butt_list:
                butt.draw(self.screen)
            self.update()

    def next_level_menu(self, level_index, start_time, level):
        if level_index+1 < len(self.level_list):
            self.level_list[level_index+1].level_unlock = True
        collectibles = self.level_list[level_index].get_collectibles()[1]
        self.level_list[level_index].add_score(
            [collectibles, time.time()-start_time])
        menu = level.get_menu()
        butt_list = self.small_menu_buttons(level_index)
        if level_index + 1 < len(self.level_list):
            butt_list.append(Button(700, 270, 'Next Level', 75, self.color))
        else:
            butt_list.append(Button(700, 270, 'Main menu', 75, self.color))
        while True:
            for event in pygame.event.get():
                Game.small_menu_ev_loop(self, butt_list, level_index, event)
            self.screen.blit(menu, (530, 180))
            for butt in butt_list:
                butt.draw(self.screen)
            self.update()

    def small_menu_buttons(self, level_index):
        butt_list = Button.create_butt_list(700, 340, 50, self.level_list[level_index].get_color(), [
                                            'Try Again', 'Level Select', 'Main Menu', 'Exit'], 0, 50)
        return butt_list

    def small_menu_ev_loop(self, butt_list, level_index, event):
        self.game_quit(event)
        if butt_list[4].activate(event):
            if butt_list[4].text == 'Continue':
                return True
            if butt_list[4].text == 'Game Over':
                Game.event_loop(self, level_index)
            if butt_list[4].text == 'Next Level':
                if level_index + 1 < len(self.level_list):
                    Game.event_loop(self, level_index+1)
        if butt_list[0].activate(event):
            Game.event_loop(self, level_index)
        if butt_list[1].activate(event):
            Game.level_select(self, self.level_list)
        if butt_list[2].activate(event) or butt_list[4].activate(event):
            Game.start_screen(self)
        if butt_list[3].activate(event):
            self.save(self.level_list)
            pygame.quit()
            exit()

    def add_level(self, butt_list):
        self.level_list.append(Game.new_level())
        butt_list = Button.add_level_select_button(butt_list)
        return butt_list

    def new_level():
        rect_list1 = [pygame.Rect(30, 750, 100, 100),]
        rect_list2 = [pygame.Rect(30, 750, 100, 100),]
        sce1 = Scene(rect_list1, '')
        sce2 = Scene(rect_list2, '')
        scene_list = [sce1]
        scene_list2 = [sce2]
        return (Level(scene_list, scene_list2, 50, 600, pygame.Rect(1300, 450, 100, 150))
                )

    def dev_menu(self):
        butt_list_label = ['add scene', 'add rectangle',
                           'add collectible', 'edit rectangle']
        butt_list = Button.create_butt_list(
            1520, 25, 40, (255, 255, 255), butt_list_label, 0, 35)
        return butt_list

    def draw_dev_menu(self, dev_state, dev_butt_list, level, scene_index, scene):
        
        if dev_state:
            for butt in dev_butt_list:
                butt.draw(self.screen)
            if scene_index+1 == len(level.scene_list_d1):
                pygame.draw.rect(self.screen, (100, 200, 200),
                                 level.win_square)
            scene.dev_draw(self.screen)
            fps_font = pygame.font.Font('EnchantedSword.ttf', 30)
            fps_text = fps_font.render(str(self.clock.get_fps()), False, (0, 255, 0))
            self.screen.blit(fps_text, (0, 0))

    def dev_event_loop(self, event, dev_butt_list, level, scene, background,dimension_backround):
        if dev_butt_list[0].activate(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_1):
            level.add_scene(self.screen)
        if dev_butt_list[1].activate(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_2):
            scene.add_rectangle_menu(self.screen, background,dimension_backround)
        if dev_butt_list[2].activate(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_3):
            scene.add_collectible(self.screen, background,dimension_backround)
        if dev_butt_list[3].activate(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_4):
            scene.edit_rectangle(self.screen, level, background,dimension_backround)
        return level


game = Game()
