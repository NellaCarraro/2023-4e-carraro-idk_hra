import os
import pickle
import pygame
from Player import Player
from Button import Button
from Scene import Level, Scene
import time
#display level, display score


class Game:
    clock = pygame.time.Clock()

    def __init__(self):
        pygame.init()
        Game.temp(self)
        self.screen = pygame.display.set_mode((1400,800))
        self.player = pygame.sprite.GroupSingle()#probably can get rid of this
        self.level_list = Game.load(self)
        self.player.add(Player(self.level_list[0]))#and this
        Game.start_screen(self)

    def start_screen(self):
        self.clock.tick(60)
        pygame.display.set_caption('Melinoe')
        icon = pygame.image.load('Images/cat_1.png').convert()
        pygame.display.set_icon(icon)
        start_img = pygame.image.load('Images/Main_menu.png').convert()
        start_menu = pygame.image.load('Images/Title_screen_menu.png').convert_alpha()
        start_butt = Button(1200,530,'Play',150,(143, 120, 173))
        exit_butt = Button(1200,700,'Exit',75,(143, 120, 173))
        save_butt = Button(1200,630,'Save',75,(143, 120, 173))
        start_bool = True
        while start_bool:
            for event in pygame.event.get():
                self.game_quit(event)
                if start_butt.activate(event):
                    start_bool=False
                if exit_butt.activate(event):
                    self.save(self.level_list)
                    pygame.quit()
                    quit()
                if save_butt.activate(event):
                    Game.save(self,self.level_list)
            self.screen.blit(start_img,(0,0))
            self.screen.blit(start_menu,(1020,400))
            start_butt.draw(self.screen)
            exit_butt.draw(self.screen)
            save_butt.draw(self.screen)
            pygame.display.update()
        Game.level_select(self,self.level_list)
        
    def event_loop(self,level_id):
        level = self.level_list[level_id]
        display = pygame.image.load('Images/Main_menu.png').convert()
        pl = Player(level)
        self.player.add(pl)
        self.screen = pygame.display.set_mode((1800,800))

        scene_list =level.scene_list_d1
        self.scene = level.scene_list_d1[0]#doesnt need to be self.scene
        level.set_collectibles(False)
        lab_list = [
                    Button(850,40,level.get_collectibles(),85,(143, 120, 173)),
                    Button(700,40,'0',75,(143, 120, 173)),
                    Button(550,40,f'Level {level_id+1}: ',75,(143, 120, 173))
                     ]
        
        

        scene_index = 0
        self.dimension = False
        dev_state = True
        start_time = time.time()

        while True: 
            for event in pygame.event.get():  
                self.game_quit(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Game.pause_menu(self,level_id)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if self.dimension == False:
                            scene_list = level.scene_list_d2
                            if pl.harsh_collisions(scene_list[scene_index])==False:
                                self.dimension = True
                                scene_list = level.scene_list_d2
                            else:
                                scene_list = level.scene_list_d1
                        else:
                            scene_list = level.scene_list_d1
                            if pl.harsh_collisions(scene_list[scene_index])==False:
                                self.dimension = False
                                scene_list = level.scene_list_d1
                            else:
                                scene_list = level.scene_list_d2
                    if event.key == pygame.K_F12:
                        self.screen = pygame.display.set_mode((1800,800))
                        dev_state = True
            if dev_state:
                Game.dev_menu(self)
            self.scene = scene_list[scene_index]
            if self.dimension:
                level.scene_list_d2[scene_index].collectible_list = pl.collectibles(level.scene_list_d2[scene_index].collectible_list)
                self.screen.blit(display,(0,0))
            else:
                level.scene_list_d1[scene_index].collectible_list = pl.collectibles(level.scene_list_d1[scene_index].collectible_list)
                if pl.win(scene_list):
                    Game.next_level_menu(self,level_id,start_time)
                self.screen.fill((200,160,227,255)) 
            self.player.update(scene_list)
            scene_index = pl.scene_index
            Game.update_score(self,lab_list,start_time,level)
            Game.draw_event_loop(self)
            pygame.draw.rect(self.screen,(100,200,200),level.win_square) #can get rid of this 
            if pl.death:
                Game.death_screen(self,level_id)
            pygame.display.update()
            self.clock.tick(60)

    def update_score(self,lab_list,start_time,level):
        lab_list[0].change_text(level.get_collectibles()) 
        curr_time = time.time()-start_time
        lab_list[1].change_text(f'{int(curr_time/60)}:{int(curr_time%60)}') 
        for lab in lab_list:
            lab.draw(self.screen)
        
    def draw_event_loop(self):
        self.player.draw(self.screen)  
        self.scene.draw(self.screen)

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
        while i<len(level_list):
            if (i)%5 ==0 and i >0:
                x = width
                y = y +200
            butt_list.append(Button(x,y,f'{i+1}',180,(255,255,255)))
            x +=width
            i+=1    
        add = Button(x,y,'+',180,(255,255,255))
        while True:
            for event in pygame.event.get():  
                self.game_quit(event)
                l=0
                while l<len(butt_list):
                    if butt_list[l].activate(event):
                        Game.level_select_menu(self,l)
                    l+=1
                if add.activate(event):
                    Game.add_level(self)
                    Game.level_select(self,level_list)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Game.start_screen(self)
            self.clock.tick(60)
            pygame.display.update()
            self.screen.fill((250,160,227,255)) 
            for butt in butt_list:
                add.draw(self.screen)
                butt.draw(self.screen)

    def level_select_menu(self,level_id):
        level = self.level_list[level_id]
        menu = pygame.image.load('Images/Title_screen_menu.png').convert_alpha()
        label_list = [Button(700,270,f'Level: {level_id+1}',75,(143, 120, 173)),
                      Button(700,380,level.get_collectibles(),50,(143, 120, 173))
                     ]
        
        if level.best_time:
            best_time = f'{int(level.best_time/60)}min {int(level.best_time%60)}sec'
            label_list.append(Button(700,330,best_time,50,(143, 120, 173)))
        else:
            label_list.append(Button(700,330,'-',50,(143, 120, 173)))

        butt_list = []
        if level.level_unlock == False:
            butt_list.append(Button(700,440,'Locked',75,(143, 120, 173)))
        else:
            butt_list.append(Button(700,440,'Play',75,(143, 120, 173)))
        butt_list.append(Button(700,500,'Back',50,(143, 120, 173)))
        while True:
            for event in pygame.event.get():
                self.game_quit(event)
                if butt_list[0].activate(event) and butt_list[0].text == 'Play':
                    Game.event_loop(self,level_id)
                if butt_list[1].activate(event):
                    return
                self.screen.blit(menu,(530,180))
            for butt in butt_list:
                butt.draw(self.screen)
            for label in label_list:
                label.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)
                    


    def pause_menu(self,level_id):
        menu = pygame.image.load('Images/Title_screen_menu.png')
        #menu =pygame.transform.rotozoom(menu,0,1.5)
        butt_list = self.small_menu_buttons()
        butt_list.append(Button(700,270,'Continue',75,(143, 120, 173)))
        while True:
            for event in pygame.event.get():
                if Game.small_menu_ev_loop(self,butt_list,level_id,event):
                    return
            self.screen.blit(menu,(530,180))
            for butt in butt_list:
                butt.draw(self.screen)
            self.clock.tick(60)
            pygame.display.update()
            
    def death_screen(self,level_id):
        menu = pygame.image.load('Images/Title_screen_menu.png').convert_alpha()
        butt_list = self.small_menu_buttons()
        butt_list.append(Button(700,270,'Game Over',75,(143, 120, 173)))
        while True:
            for event in pygame.event.get():
                Game.small_menu_ev_loop(self,butt_list,level_id,event)
            self.screen.blit(menu,(530,180))
            for butt in butt_list:
                butt.draw(self.screen)
            self.clock.tick(60)
            pygame.display.update()
        
    def next_level_menu(self,level_id,start_time):
        if level_id+1< len(self.level_list):
            self.level_list[level_id+1].level_unlock=True
        self.level_list[level_id].best_time= time.time()-start_time
        menu = pygame.image.load('Images/Title_screen_menu.png').convert_alpha()
        butt_list = self.small_menu_buttons()
        if level_id +1<len(self.level_list):
            butt_list.append(Button(700,270,'Next Level',75,(143, 120, 173)))
        else:
            butt_list.append(Button(700,270,'Main menu',75,(143, 120, 173)))
        while True:
            for event in pygame.event.get():
                Game.small_menu_ev_loop(self,butt_list,level_id,event)
            self.screen.blit(menu,(530,180))
            for butt in butt_list:
                butt.draw(self.screen)
            self.clock.tick(60)
            pygame.display.update()

    def small_menu_buttons(self):
        butt_list = [Button(700,340,'Try Again',50,(143, 120, 173)),
                    Button(700,390,'Level select',50,(143, 120, 173)),
                    Button(700,440,'Main menu',50,(143, 120, 173)),
                    Button(700,490,'Exit',50,(143, 120, 173)) ]
        return butt_list
    
    def small_menu_ev_loop(self,butt_list,level_id,event):
        self.game_quit(event)
        if butt_list[4].activate(event):
            if butt_list[4].text == 'Continue':
                return True
            if butt_list[4].text == 'Game Over':
                Game.event_loop(self,level_id)
            if butt_list[4].text == 'Next Level':
                if level_id +1 < len(self.level_list):
                    Game.event_loop(self,level_id+1)
        if butt_list[0].activate(event):
            Game.event_loop(self,level_id)
        if butt_list[1].activate(event):
            Game.level_select(self,self.level_list)
        if butt_list[2].activate(event) or butt_list[4].activate(event):
            Game.start_screen(self)
        if butt_list[3].activate(event):
            self.save(self.level_list)
            pygame.quit()
            exit()

    def temp(self):
        rect_list = [pygame.Rect(0,750,160,100),]
        trap_list = pygame.Rect(200,700,50,50)
        cl = pygame.Rect(200,400,50,50)
        lev = Scene(rect_list,'left')
        lev2 = Scene(rect_list,'')
        lev.trap_list.append(trap_list)
        lev2.collectible_list.append([False,pygame.Rect(50,630,50,50)])
        lev.collectible_list.append([False,pygame.Rect(100,630,50,50)])
        scene_list = [lev,lev2]
        scene_list2 = [lev2]

        level_list = [Level(scene_list,scene_list2,0,0,500,pygame.Rect(1300,750,100,100)),Level(scene_list,scene_list2,0,0,500,pygame.Rect(1300,750,100,100))]
        level_list[0].level_unlock = True
        self.save(level_list)

    def dev_menu(self):
        butt_list =[
            Button(1500,25,'add sc d1',40,(0,0,0)),
            Button(1700,25,'add sc d2',40,(0,0,0)),
                    ]
        for butt in butt_list:
            butt.draw(self.screen)
        return False
    
    def add_level(self):
        rect_list = [pygame.Rect(0,750,160,100),]
        lev = Scene(rect_list,'')
        scene_list = [lev]
        level = Level(scene_list,scene_list,0,0,500,pygame.Rect(1300,750,100,100))
        self.level_list.append(level)

game = Game()

