import os
import pickle
import pygame
from Player import Player
from Button import Button
from Scene import Level, Scene


class Game:
    clock = pygame.time.Clock()
    def __init__(self):
        pygame.init()
        self.temp()
        self.screen = pygame.display.set_mode((1400,800))
        self.player = pygame.sprite.GroupSingle()
        self.level_list = Game.load(self)
        self.player.add(Player(self.level_list[0]))
        Game.start_screen(self)

    def start_screen(self):
        self.clock.tick(60)
        start_img = pygame.image.load('Images/Main_menu.png')
        start_butt = Button(600,300,'Start a game',160,(255,180,220))
        exit_butt = Button(600,650,'Exit',100,(255,180,220))
        start_bool = True
        while start_bool:
            self.screen.blit(start_img,(0,0))
            for event in pygame.event.get():
                self.game_quit(event)
                if start_butt.activate(event):
                    start_bool=False
                if exit_butt.activate(event):
                    self.save(self.level_list)
                    pygame.quit()
                    quit()
            start_butt.draw(self.screen)
            exit_butt.draw(self.screen)
            pygame.display.update()
        Game.level_select(self,self.level_list)
        
    def event_loop(self,level):#asi by melo dostat parametr ktery level to ma byt nebo ktera scena
        self.screen = pygame.display.set_mode((1400,800))
        pl = Player(level)
        dimension = False
        self.player.add(pl)
        scene_index = 0
        self.scene = level.scene_list_d1[0]
        add_butt = Button(50,40,'add',40,'red')
        scene_list =level.scene_list_d1
        while True: 
            for event in pygame.event.get():  
                self.game_quit(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Game.pause_menu(self,level)
                if add_butt.activate(event):
                    Game.add_rect(self)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if dimension == False:
                            scene_list = level.scene_list_d2
                            if pl.harsh_collisions(scene_list[scene_index])==False:
                                dimension = True
                                scene_list = level.scene_list_d2
                            else:
                                scene_list = level.scene_list_d1
                        else:
                            scene_list = level.scene_list_d1
                            if pl.harsh_collisions(scene_list[scene_index])==False:
                                dimension = False
                                scene_list = level.scene_list_d1
                            else:
                                scene_list = level.scene_list_d2
                            
            self.clock.tick(60)
            pygame.display.update()
            self.scene = scene_list[scene_index]
            if dimension:
                self.screen.fill((250,160,250,255)) 
                scene_list = level.scene_list_d2
            else:
                self.screen.fill((200,160,227,255)) 
            self.player.update(scene_list)
            scene_index = pl.scene_index
            self.player.draw(self.screen)  
            self.scene.draw(self.screen)
            add_butt.draw(self.screen)
            if pl.death:
                Game.death_screen(self,level)

    def next_scene(self,pl,scene_list):
        pl.next_scene_right(scene_list)
        pl.next_scene_left(scene_list)
        pl.next_scene_up_down(scene_list)
    def game_quit(self,event):
            if event.type == pygame.QUIT:
                pygame.quit() 
                exit()
                
    def save(self,level_list):
        file = open('levels','wb')
        pickle.dump(level_list,file)
        file.close()
        
    def load(self):
        if os.path.exists('levels'):
            level_list = open('levels','rb')
            return pickle.load(level_list) 
        else:
            print('chybicka se vloudila')
            
    def level_select(self,level_list):
        width = (1400-250)/5
        x = width
        i=0
        y = 225
        butt_list=[]
        add_butt = Button(50,40,'add',40,'red')
        while i<len(level_list):
            if (i)%5 ==0 and i >0:
                x = width
                y = y +200
            butt_list.append(Button(x,y,f'{i+1}',180,(255,255,255)))
            x +=width
            i+=1
        while True:
            for event in pygame.event.get():  
                self.game_quit(event)
                l=0
                if add_butt.activate(event):
                    Game.add_level_menu(self)
                while l<len(butt_list):
                    if butt_list[l].activate(event):
                        Game.event_loop(self,level_list[l])
                    l+=1
            self.clock.tick(60)
            pygame.display.update()
            self.screen.fill((250,160,227,255)) 
            for butt in butt_list:
                butt.draw(self.screen)
                
    def pause_menu(self,level):
        rect = pygame.Rect(450,100,500,500)
        butt_list = self.small_menu_buttons()
        butt_list.append(Button(700,200,'Continue',100,(0,0,0)))
        while True:
            if Game.small_menu_ev_loop(self,butt_list,level):
                return
            self.clock.tick(60)
            pygame.draw.rect(self.screen,(255,255,255),rect)
            for butt in butt_list:
                butt.draw(self.screen)
            pygame.display.update()
            
    def death_screen(self,level):
        rect = pygame.Rect(450,100,500,500)
        butt_list = self.small_menu_buttons()
        butt_list.append(Button(700,200,'Game Over',100,(0,0,0)))
        while True:
            Game.small_menu_ev_loop(self,butt_list,level)
            self.clock.tick(60)
            pygame.draw.rect(self.screen,(255,255,255),rect)
            for butt in butt_list:
                butt.draw(self.screen)
            pygame.display.update()
        
    def small_menu_buttons(self):
        butt_list = [Button(700,300,'Level select',75,(0,0,0)),
                    Button(700,400,'Main menu',75,(0,0,0)),
                    Button(700,500,'Exit',75,(0,0,0)) ]
        return butt_list

    def small_menu_ev_loop(self,butt_list,level):
            for event in pygame.event.get():
                self.game_quit(event)
                if butt_list[3].activate(event):
                    if butt_list[3].text == 'Continue':
                        return True
                    if butt_list[3].text == 'Game Over':
                        Game.event_loop(self,level)
                if butt_list[0].activate(event):
                    Game.level_select(self,self.level_list)
                if butt_list[1].activate(event):
                    Game.start_screen(self)
                if butt_list[2].activate(event):
                    self.save(self.level_list)
                    pygame.quit()
                    exit()
    
    def temp(self):
        rect_list = [pygame.Rect(-100,701,1600,100),]
        trap_list = pygame.Rect(600,0,50,50)
        lev = Scene(rect_list,'right')
        lev.trap_list.append(trap_list)
        rect_list2 = [pygame.Rect(1000,300,75,75),
             pygame.Rect(-100,701,1600,100),
             pygame.Rect(500,550,75,100),
             pygame.Rect(1300,50,100,300),
             pygame.Rect(800,400,75,125),
             pygame.Rect(1100,150,100,75),
             ]
        rect_list3 = [pygame.Rect(-400,781,1600,100),]
        lev2 = Scene(rect_list2,'up')
        lev2.trap_list.append(trap_list)
        lev3 = Scene(rect_list3,'left')
        scene_list = [lev,lev2,lev3,lev3]
        scene_list2 = [lev2,lev3,lev,lev]
        i = 0
        level_list = [Level(scene_list,scene_list2,0,0,500,pygame.Rect(1400,800,100,100))]
        
        while i<=13:
            i+=1
            lev = Level(scene_list,scene_list2,0,100,500,pygame.Rect(1400,800,100,100))
            level_list.append(lev)
        self.save(level_list)
    def add_rect(self):
        print('uwu')
    def add_level_menu():
        add_butt = Button(50,40,'add',40,'red')
        
        
        
game = Game()

