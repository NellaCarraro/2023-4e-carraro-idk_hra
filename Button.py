import pygame
class Button():
    
    def __init__(self,x,y,text,height,color):
        self.text = text
        test_font = pygame.font.Font('EnchantedSword.ttf',height)
        self.text_image = test_font.render(text,False,color)
        self.text_rect = self.text_image.get_rect(center=(x,y))
        
    def activate(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.text_rect.collidepoint(event.pos):
                return True
            
    def draw(self,screen):
        screen.blit(self.text_image,self.text_rect)
    