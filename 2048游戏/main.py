import pygame
import sys
from configs import settings
import Game2048

white = (255, 255, 255)


# 游戏初始化
class Game:
    def __init__(self):
        pygame.init()
        self.settings = settings()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption(self.settings.caption)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
            """"   
            self.screen.fill(self.settings.color)
            square = self.settings.square
            pygame.draw.rect(self.screen, self.settings.square_color, square)
            x, y = 100, 150
            font = pygame.font.SysFont('幼圆', 25, True)
            rendered_text = font.render("2", True, (0, 0, 0))
            text_rect = rendered_text.get_rect()
            for i in range(4):
                x += self.settings.block_gap
                if i != 0:
                    y = 150
                    x += self.settings.block_size
                for j in range(4):
                    if j != 0:
                        y += self.settings.block_size
                    y += self.settings.block_gap
                    block = pygame.Rect(x, y, self.settings.block_size,self.settings.block_size)
                    text_rect.center = block.center
                    pygame.draw.rect(self.screen, self.settings.block_color, block)
                    self.screen.blit(rendered_text, text_rect)
            pygame.display.flip() """



if __name__ == "__main__":
    ai = Game()
    ai.run_game()


