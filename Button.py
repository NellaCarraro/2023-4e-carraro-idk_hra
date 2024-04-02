import pygame


class Button():

    def __init__(self, x, y, text, height, color):
        self.x = x
        self.y = y
        self.text = text
        self.height = height
        self.color = color
        self.text_font = pygame.font.Font('EnchantedSword.ttf', height)
        self.text_image = self.text_font.render(text, False, color)
        self.text_rect = self.text_image.get_rect(center=(x, y))

    def activate(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.text_rect.collidepoint(event.pos):
                return True

    def change_text(self, text):
        self.text = text
        self.text_image = self.text_font.render(text, False, self.color)

    def change_color(self, color):
        self.color = color
        self.text_image = self.text_font.render(self.text, False, color)

    def change_height(self, height):
        self.text_font = pygame.font.Font('EnchantedSword.ttf', height)
        self.text_image = self.text_font.render(self.text, False, self.color)
        self.text_rect = self.text_image.get_rect(center=(self.x, self.y))

    def change_position(self, x, y):
        self.text_rect = self.text_image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.text_image, self.text_rect)

    def create_butt_list(x, y, height, color, text_list, distance_x, distance_y):
        butt_list = []
        for text in text_list:
            butt_list.append(Button(x, y, text, height, color))
            x += distance_x
            y += distance_y
        return butt_list

    def create_level_select_buttons(level_list):
        butt_list = []
        width = (1300)/4
        x = 50 + width/2
        i = 0
        y = 340
        while i < len(level_list):
            butt_list.append(Button(x, y, f'{i+1}', 180, (128, 99, 166)))
            x += width
            i += 1
            if (i) % 4 == 0 and i > 0:
                x = 50 + width/2
                y = y + 290
        butt_list.append(Button(x, y, '+', 180, (128, 99, 166)))
        return butt_list

    def add_level_select_button(butt_list):
        width = (1300)/4
        butt_list.pop()
        x = butt_list[len(butt_list)-1].x
        y = butt_list[len(butt_list)-1].y
        x += width
        if (len(butt_list)) % 4 == 0:
            x = 50 + width/2
            y = y + 290
        butt_list.append(
            Button(x, y, f'{len(butt_list)+1}', 180, (128, 99, 166)))
        x += width
        if (len(butt_list)) % 4 == 0:
            x = 50 + width/2
            y = y + 290
        butt_list.append(Button(x, y, '+', 180, (128, 99, 166)))
        return butt_list
