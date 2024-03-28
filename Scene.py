import pygame
import pickle
import os.path

class Scene:
    def __init__(self,rect_list,next_scene_index):
        self.rect_list = rect_list
        self.next_scene_index = next_scene_index
        self.trap_list = []
        self.collectable_list = []
        self.anim_index = 0
        
        
    def draw(self,screen):
        self.anim_index +=0.025
        if self.anim_index>2:
            self.anim_index = 0
        collectable_image = [pygame.image.load('Images/cat_1.png'),
                             pygame.image.load('Images/cat_2.png')]
        for rect in self.rect_list:
            pygame.draw.rect(screen,(178,100,255),rect)
        for rect in self.trap_list:
            pygame.draw.rect(screen,(204,0,100),rect)
        for rect in self.collectable_list:
            if rect[0]==False:
                screen.blit(collectable_image[int(self.anim_index)],rect[1])
        
            
class Level:
    def __init__(self,scene_list_d1,scene_list_d2,level_index,x,y,win_square):
        self.scene_list_d1 = scene_list_d1
        self.scene_list_d2 = scene_list_d2
        self.level_index = level_index
        self.level_unlock = False
        self.start_x = x
        self.start_y = y
        self.win_square = win_square
        self.best_time = None

    def set_spawn(self,x,y):
        self.start_x = x
        self.start_y = y
    
    def add_scene(self,i,rect):
        print('work in progress')
    
    def get_collectibles(self):
        x = 0
        y = 0
        for scene in self.scene_list_d1:
            x += len(scene.collectable_list)
            for collectible in scene.collectable_list:
                if collectible[0]==True:
                    y += 1
        for scene in self.scene_list_d2:
            x+= len(scene.collectable_list)
            for collectible in scene.collectable_list:
                if collectible[0]==True:
                    y += 1
        return f'{y}/{x}'
    
    #def set_collectible(self,scene_id,d):
        
    
    def set_collectibles(self,bool):
        for scene in self.scene_list_d1:
            for collectible in scene.collectable_list:
                collectible[0]= bool
        for scene in self.scene_list_d2:
            for collectible in scene.collectable_list:
                collectible[0] = bool
           
        #start and finish i guess bude tady
        
        
        
        