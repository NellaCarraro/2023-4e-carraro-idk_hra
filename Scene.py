import pygame
import pickle
import os.path

class Scene:
    def __init__(self,rect_list,next_scene_index):
        self.rect_list = rect_list
        self.next_scene_index = next_scene_index
 
            
    def open_level(self,lel_number):
        print(f'level: {lel_number}')
        
    def draw(self,screen):
        i = 0
        while i <len(self.rect_list):
            pygame.draw.rect(screen,(255,255,255),self.rect_list[i])
            i +=1
            
class Level:
    def __init__(self,scene_list_d1,scene_list_d2,level_index,x,y,rect):
        self.scene_list_d1 = scene_list_d1
        self.scene_list_d2 = scene_list_d2
        self.level_index = level_index
        self.level_unlock = False
        self.start_x = x
        self.start_y = y
        self.win_square = rect
    def set_spawn(self,x,y):
        self.start_x = x
        self.start_y = y

        #start and finish i guess bude tady
        
        
        
        