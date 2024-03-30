import pygame
from Button import Button

class Player(pygame.sprite.Sprite):
    def __init__(self,level):
        super().__init__()
        self.player_anim_list = Player.create_anim_list(['Stand/player_stand','Run/player_run','Jump/player_jump','Fall/player_fall'])
        self.image = self.player_anim_list[0][0]
        self.rect = self.image.get_rect(bottomleft=(level.start_x,level.start_y))
        self.level = level
        self.anim_index = 0
        self.anime_list_index = 0
        self.gravity = 0
        self.scene_index = 0
        self.jump = False
        self.double_jump_timer = 30
        self.double_jump = False
        self.death = False
        self.face_side = 'r'

    def create_anim_list(name_list):
        player_anim_list =[]
        for name in name_list:
            i = 1
            anim_list =[]
            while i<5:
                anim_list.append(pygame.image.load(f'Images/Player/{name}_{i}.png'))
                i+=1
            player_anim_list.append(anim_list)
        return player_anim_list
        
        
    def update(self,scene_list): 
        Player.input(self)
        if Player.collisions(self,scene_list[self.scene_index]):
            self.death = True
        Player.animation(self)
        self.next_scene(scene_list)
       
    
        
    def animation(self):
        anim_list = self.player_anim_list[self.anime_list_index]
        self.anim_index +=0.1
        if self.anim_index > len(anim_list):
            self.anim_index = 0
        self.image = anim_list[int(self.anim_index)]

    def flip_image_list(self,player_image_list):#i dont get it it should work the easier way but it doesnt so here we are
        i=0
        while i<len(player_image_list):
            o = 0
            while o< len(player_image_list[i]):
                player_image_list[i][o] = pygame.transform.flip(player_image_list[i][o],True,False)
                o+=1
            i+=1
        return player_image_list
    
    def input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            self.rect.x +=6
            if self.anime_list_index <2:
                self.anime_list_index = 1
            if self.face_side == 'l':
                self.face_side = 'r'
                self.player_anim_list = self.flip_image_list(self.player_anim_list)
        elif key[pygame.K_a]:
            self.rect.x -=6
            if self.anime_list_index <2:
                self.anime_list_index = 1
            if self.face_side == 'r':
                self.face_side = 'l'
                self.player_anim_list = self.flip_image_list(self.player_anim_list)

        else:
            if self.anime_list_index <2:
                self.anime_list_index = 0
        
        if key[pygame.K_SPACE]:
            if  self.jump == False and self.gravity <=0:
                self.gravity = 15
                self.jump = True
                self.double_jump_timer = pygame.time.get_ticks()
                self.anime_list_index = 2
            elif self.double_jump == False and pygame.time.get_ticks()>self.double_jump_timer+300:
                self.gravity =10
                self.double_jump = True
                self.anime_list_index = 2
        if self.gravity <0 and self.jump == True:
            self.anime_list_index = 3

    def next_scene(self,scene_list):
        self.next_scene_left(scene_list)
        self.next_scene_right(scene_list)
        self.next_scene_up_down(scene_list)
        

    def next_scene_right(self,scene_list):
        if self.rect.right-self.rect.width/2 >1400:#pokud se ma menit scena a plati ze dalis scena je rifht nebo predchoyi byla left zmeni ji
            if scene_list[self.scene_index].next_scene_index=='right' and self.scene_index<len(scene_list):
                self.rect.x = -self.rect.width/2
                self.scene_index +=1
            elif scene_list[self.scene_index-1].next_scene_index=='left' and self.scene_index>0:
                self.rect.x = -self.rect.width/2
                self.scene_index -=1
            else:
                self.rect.x = 1400 -self.rect.width/2

    def next_scene_left(self,scene_list):
        if self.rect.right-self.rect.width/2 <0: #changes scene 
            if scene_list[self.scene_index].next_scene_index=='left'and self.scene_index<len(scene_list):
                self.rect.x = 1400 -self.rect.width/2
                self.scene_index +=1
            elif scene_list[self.scene_index-1].next_scene_index=='right' and self.scene_index>0:
                self.rect.x = 1400 -self.rect.width/2
                self.scene_index -=1
            else:
                self.rect.x = 0 -self.rect.width/2

    def next_scene_up_down(self,scene_list):
        if self.rect.bottom <0:
            if scene_list[self.scene_index].next_scene_index=='up' and self.scene_index<len(scene_list):
                self.rect.bottom = 800
                self.scene_index +=1
            elif scene_list[self.scene_index-1].next_scene_index=='down' and self.scene_index>0:
                self.rect.bottom = 800 
                self.scene_index -=1
            else:
                self.rect.bottom = 1
        else:
            self.next_scene_down(scene_list)

    def next_scene_down(self,scene_list):
        if self.rect.bottom >800 and self.gravity <0:
            if scene_list[self.scene_index].next_scene_index=='down'and self.scene_index<len(scene_list):
                self.rect.bottom = 1
                self.scene_index +=1
            elif scene_list[self.scene_index-1].next_scene_index=='up'and self.scene_index>0:
                self.rect.bottom = 1
                self.scene_index -=1
            else:
                self.rect.bottom = 800
    
    def start_position(self,x,y):
        self.x = x
        self.y = y

    def collisions(self,scene):
        self.rect.bottom -= self.gravity
        if self.gravity >-15:
            self.gravity -= 1
        if self.rect.collidelistall(scene.trap_list):
            return True
        if self.rect.collidelistall(scene.rect_list):
            collide_list = self.rect.collidelistall(scene.rect_list)
            for i in collide_list:
                if self.rect.bottom > scene.rect_list[i].top and self.rect.bottom < scene.rect_list[i].top -self.gravity+1  and self.gravity<=0:
                    self.rect.bottom = scene.rect_list[i].top
                    if self.jump == True:
                        self.anime_list_index = 0
                    self.jump = False
                    self.double_jump = False
                    self.gravity=-1  
                if self.rect.top < scene.rect_list[i].bottom and self.rect.top > scene.rect_list[i].bottom -21 and self.gravity>=0:
                    self.rect.top = scene.rect_list[i].bottom
                    self.gravity=0      
            collide_list = self.rect.collidelistall(scene.rect_list)
            for i in collide_list:
                if self.rect.right > scene.rect_list[i].left and self.rect.right < scene.rect_list[i].left+14:
                    self.rect.right = scene.rect_list[i].left
                if self.rect.left < scene.rect_list[i].right and self.rect.left > scene.rect_list[i].right-14:
                    self.rect.left = scene.rect_list[i].right

    def harsh_collisions(self,scene):
        if self.rect.collidelistall(scene.trap_list):
            return 
        Player.collisions(self,scene)
        if self.rect.collidelistall(scene.rect_list):
            return
        return False
    
    def collect_collision(self,collectable):
        if self.rect.colliderect(collectable):
            return True
        return False
    
    def win(self,scene_list):
        if self.rect.colliderect(self.level.win_square) and self.scene_index+1 >= len(scene_list):
            return True
        return False
        
            
            
               

                    
        

    

    
       