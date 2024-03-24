import pygame
class Player(pygame.sprite.Sprite):
    #incializani metoda
    def __init__(self,level):
        super().__init__()
        x = level.start_x
        y = level.start_y
        self.player_field = [pygame.image.load('Images/char1.png')
                             ,pygame.image.load('Images/char2.png')]
        self.image = self.player_field[0]
        self.rect = self.image.get_rect(bottomleft=(x,y))
        self.anim_index = 0
        self.gravity = 0
        self.jump = False
        self.scene_index = 0
        self.level = level

    def update(self,scene_index):
        Player.input(self)
        Player.animation_standing(self)
        print(self.scene_index)
        Player.collisions(self,self.level.scene_list[self.scene_index])
    def animation_standing(self):
        self.anim_index +=0.1
        if self.anim_index > len(self.player_field):
            self.anim_index = 0
        self.image = self.player_field[int(self.anim_index)]

    def input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            self.rect.x +=7
            self.next_scene_right()
        if key[pygame.K_a]:
            self.rect.x -=7#moves player
            self.next_scene_left()
        if key[pygame.K_SPACE]:
            if  self.jump == False:
                self.gravity = 20
                self.jump = True
        self.next_scene_up_down()
        

    def next_scene_right(self):
        scene_list = self.level.scene_list
        if self.rect.right-self.rect.width/2 >1400:#pokud se ma menit scena a plati ze dalis scena je rifht nebo predchoyi byla left zmeni ji
            if scene_list[self.scene_index].next_scene_index=='right' and self.scene_index<len(self.level.scene_list):
                self.rect.x = -self.rect.width/2
                self.scene_index +=1
            elif scene_list[self.scene_index-1].next_scene_index=='left' and self.scene_index>0:
                self.rect.x = -self.rect.width/2
                self.scene_index -=1
            else:
                self.rect.x = 1400 -self.rect.width/2

    def next_scene_left(self):
        scene_list = self.level.scene_list
        if self.rect.right-self.rect.width/2 <0: #changes scene 
            if scene_list[self.scene_index].next_scene_index=='left'and self.scene_index<len(self.level.scene_list):
                self.rect.x = 1400 -self.rect.width/2
                self.scene_index +=1
            elif scene_list[self.scene_index-1].next_scene_index=='right' and self.scene_index>0:
                self.rect.x = 1400 -self.rect.width/2
                self.scene_index -=1
            else:
                self.rect.x = 0 -self.rect.width/2
    def next_scene_up_down(self):
        scene_list = self.level.scene_list
        if self.rect.top + self.rect.height <0:
            if scene_list[self.scene_index].next_scene_index=='up' and self.scene_index<len(self.level.scene_list):
                self.rect.top = 800-self.rect.width/2
                self.scene_index +=1
            elif scene_list[self.scene_index-1].next_scene_index=='down' and self.scene_index>0:
                self.rect.top = 800-self.rect.width/2
                self.scene_index -=1
            else:
                self.rect.x = -self.rect.height/2
        else:
            self.next_scene_down()
    def next_scene_down(self):
        if self.rect.top + self.rect.height >800 and self.gravity <0:
            if self.level.scene_list[self.scene_index].next_scene_index=='down'and self.scene_index<len(self.level.scene_list):
                self.rect.top = -self.rect.width/2
                self.scene_index +=1
            elif self.level.scene_list[self.scene_index].next_scene_index=='up'and self.scene_index>0:
                self.rect.top = -self.rect.width/2
                self.scene_index -=1
            else:
                self.rect.x = 800-self.rect.width/2
    
    def start_position(self,x,y):
        self.x = x
        self.y = y
    def collisions(self,scene):
        self.rect.bottom -= self.gravity
        if self.gravity >-20:
            self.gravity -= 1
            
        if self.rect.collidelistall(scene.rect_list):
            collide_list = self.rect.collidelistall(scene.rect_list)
            for i in collide_list:
                if self.rect.bottom > scene.rect_list[i].top and self.rect.bottom < scene.rect_list[i].top +21 and self.gravity<=0:
                    self.rect.bottom = scene.rect_list[i].top
                    self.jump = False
                    self.gravity=-1  
                if self.rect.top < scene.rect_list[i].bottom and self.rect.top > scene.rect_list[i].bottom -21 and self.gravity>=0:
                    self.rect.top = scene.rect_list[i].bottom
                    self.gravity=0      
            collide_list = self.rect.collidelistall(scene.rect_list)
            for i in collide_list:
                if self.rect.right > scene.rect_list[i].left and self.rect.right < scene.rect_list[i].right-scene.rect_list[i].width/2:
                    self.rect.right = scene.rect_list[i].left
                if self.rect.left < scene.rect_list[i].right and self.rect.left > scene.rect_list[i].right-scene.rect_list[i].width/2:
                    self.rect.left = scene.rect_list[i].right
               

                    
        

    

    
       