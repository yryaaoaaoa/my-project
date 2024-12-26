import numpy as np
from configs import settings as st
import pygame
import sys
class Game2048:
    def __init__(self): #初始化数组
        self.nums = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.score = 0
        with open('最高分数.txt', 'r') as best_score:
            self.best_score = int(best_score.read())
        self.st = st()
        for _ in range(2):
            self.create_nums()
        print(self.nums) # 测试
    def run_game(self):
        """开始游戏的主循环"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.st.width, self.st.height))
        pygame.display.set_caption(self.st.caption)
        self.scores()
        self.Paint()
        while True:
            for event in pygame.event.get():
                num1 = self.nums.copy()
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move('up')
                        self.Paint()
                    elif event.key == pygame.K_DOWN:
                        self.move('down')
                        self.Paint()
                    elif event.key == pygame.K_LEFT:
                        self.move('left')
                        self.Paint()
                    elif event.key == pygame.K_RIGHT:
                        self.move('right')
                        self.Paint()
                for i in range(4): #检查当前操作是否有效，若有效才执行create_nums，否则不执行
                    a = 0
                    for j in range(4):
                        if num1[i][j] != self.nums[i][j]:
                            self.create_nums()
                            self.scores()
                            self.Paint()
                            a += 1
                            break
                    if a == 1:
                        break
    def create_nums(self): # 向矩阵里添加数字
        list1 = [[i, j] for i in range(4) for j in range(4) if self.nums[i][j] == 0]  # 为空的位置
        if list1:
            a = list1.pop(np.random.randint(0, len(list1)))
            self.nums[a[0]][a[1]] = np.random.choice([2, 4, 2, 2])
    def read(self):
        print(self.nums) # 测试
    def move(self,direction): # 数组的移动逻辑，包括上左下右4个
        nums = self.nums
        if direction == 'up' or direction == 'down': # 这里我们只写左右的逻辑，用旋转矩阵后执行左右再转回来的方法实现上下移动的逻辑
            nums = np.rot90(self.nums)
        for i in range(4):
            k = 0
            res = [i for i in nums[i] if i != 0]
            while k < len(res) - 1:
                if k < len(res) - 1 and res[k] == res[k + 1]:
                    res.pop(k)
                    res[k] *= 2
                k += 1
            if direction == 'left' or direction == 'up':
                res += (4 - len(res)) * [0]
            elif direction == 'right' or direction == 'down':
                res = (4 - len(res)) * [0] + res
            nums[i] = res
        if direction == 'up' or direction == 'down':
            self.nums = np.rot90(nums,k=-1)
        elif direction == 'right' or direction == 'left':
            self.nums = nums
    def Gameover(self):
        if [1 for i in self.nums if 0 in i]: # 判断是否有0(即空位置)，若有则说明游戏未结束，直接返回False
            for i in range(3):
                for j in range(3):
                    if self.nums[i][j] == self.nums[i][j + 1]:
                        return False
                    if self.nums[i][j] == self.nums[i + 1][j]:
                        return False
            return True
        return False
    def Paint(self): # 绘制图形,包括矩形和方块等等
        font = pygame.font.SysFont('幼圆', 25, True)
        for i in range(4):
            for j in range(4):
                self.screen.fill(self.st.color)
                square = self.st.square
                pygame.draw.rect(self.screen, self.st.square_color, square)
                x, y = 100, 150
                for i in range(4):
                    text_color = (0,0,0)
                    x += self.st.block_gap
                    if i != 0:
                        y = 150
                        x += self.st.block_size
                    for j in range(4):
                        if self.nums[j][i] > 4:
                            text_color = (255,255,255)
                        else:
                            text_color = (0, 0, 0)
                        block_render = font.render(str(self.nums[j][i]), True, text_color)
                        text_rect = block_render.get_rect()
                        if j != 0:
                            y += self.st.block_size
                        y += self.st.block_gap
                        block = pygame.Rect(x, y, self.st.block_size, self.st.block_size)
                        text_rect.center = block.center
                        pygame.draw.rect(self.screen, self.st.block_color[self.nums[j][i]], block)
                        if self.nums[j][i] != 0:
                            self.screen.blit(block_render, text_rect)
        score_render = font.render(str(self.score), True, (255, 255, 255))  # 渲染分数文本
        score_text_render = font.render('SCORE', True, (240, 228, 216))  # 渲染Score文本
        score_render_rect = score_render.get_rect()  # 获取分数文本的矩形
        score_text_render_rect = score_text_render.get_rect()  # 获取Score的矩形
        score = pygame.Rect(50, 20, 100, 60)  # 创建分数矩形
        score_text_render_rect.center = (
            score.midbottom[0], score.midleft[1] - 60 / 4)  # 设置Score矩形的中心为分数矩形下半部分的中心
        score_render_rect.center = (score.midbottom[0], score.midleft[1] + 60 / 4)  # 设置分数文字矩形的中心为分数矩形上半部分的中心
        pygame.draw.rect(self.screen, (187, 173, 160), score)  # 在屏幕上绘制分数矩形
        self.screen.blit(score_render, score_render_rect)  # 将渲染的文本绘制到屏幕上，位于矩形的中间
        self.screen.blit(score_text_render, score_text_render_rect)
        # 最高分数
        best_score_render = font.render(str(self.best_score), True, (255, 255, 255))
        best_score_text_render = font.render('BEST', True, (240, 228, 216))
        best_score_render_rect = best_score_render.get_rect()
        best_score_text_render_rect = best_score_text_render.get_rect()
        best_score = pygame.Rect(160, 20, 100, 60)
        best_score_text_render_rect.center = (best_score.midbottom[0], score.midleft[1] - 60 / 4)
        best_score_render_rect.center = (best_score.midbottom[0], score.midleft[1] + 60 / 4)
        pygame.draw.rect(self.screen, (187, 173, 160), best_score)
        self.screen.blit(best_score_render, best_score_render_rect)
        self.screen.blit(best_score_text_render, best_score_text_render_rect)
        # 开始新游戏
        new_game_rect = pygame.Rect(400,80,150,60)
        pygame.draw.rect(self.screen,(143,120,102),new_game_rect)
        pygame.display.flip()
        # 开始新游戏

    def scores(self):
        self.score = np.sum(self.nums)
        filename = '最高分数.txt'
        try:
            # 尝试打开文件读取最佳分数
            with open(filename, 'r') as a:
                best_score = int(a.read().strip() or 0)  # 如果文件为空，则默认为0
        except FileNotFoundError:
            # 如果文件不存在，则设置初始最佳分数为0
            best_score = 0
        if best_score < self.score:
            # 更新最高分数
            with open(filename, 'w') as a:
                a.write(str(self.score))
            self.best_score = self.score
    def Newgame(self):
        pygame.draw.rect(self.screen, (143,120,102), ())
        # 渲染文本
        text_surface = self.font.render(self.text, True, self.text_color)
        # 获取文本的矩形
        text_rect = text_surface.get_rect(center=self.rect.center)
        # 绘制文本
        self.screen.blit(text_surface, text_rect)
x = Game2048()
x.run_game()









