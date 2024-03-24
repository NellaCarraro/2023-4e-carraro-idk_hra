from Scene import Scene
import pygame
import pickle
import os

os.remove('level_soubor')
rect_list = [pygame.Rect(1000,550,100,50),
             pygame.Rect(0,701,1400,100),
             pygame.Rect(500,550,100,100),
             pygame.Rect(1300,500,100,300),
             pygame.Rect(800,600,100,100),
             pygame.Rect(1100,350,100,50),
             ]
lev = Scene(rect_list)
rect_list2 = [pygame.Rect(1000,600,75,75),
             pygame.Rect(0,701,1400,100),
             pygame.Rect(500,550,75,100),
             pygame.Rect(1300,500,100,300),
             pygame.Rect(800,500,75,125),
             pygame.Rect(1100,350,100,75),
             ]
lev2 = Scene(rect_list2)
