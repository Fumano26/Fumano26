import pygame
from random import randint

from pygame.constants import K_ESCAPE, K_SPACE, K_a, K_d, K_r
pygame.init()
class visuality:
    def __init__(self,lenght,height,size=1):
        self.lenght = lenght
        self.height = height
        self.size = size
        self.window = pygame.display.set_mode((self.lenght,self.height))
        if self.lenght > self.height:
            self.n = self.height//self.size
        else:
            self.n = self.lenght//self.size
        self.list = self.new_list(self.n)
        self.rect_len = self.lenght // self.n
        self.start_x = (self.lenght - self.rect_len * self.n)//2
        self.start_y = (self.height - self.size * self.n)
        self.sorting = False
        self.speed = 60
        print(self.start_y)
        self.moved_left = []
        self.moved_right = []
    
    def new_list(self,n):
        list = []
        for i in range(1,n+1):
            list += [i]
        new = []
        while len(list) > 0:
            i = randint(0,len(list)-1)
            new += [list[i]]
            list = list[:i] + list[i+1:]
        return new
    
    def draw_list(self):
        for y in range(len(self.list)):
            x_coord = self.start_x + y * self.rect_len
            value = self.list[y]
            y_coord = self.start_y + ( self.n*self.size-value*self.size)
            if y in self.moved_left:
                color = (0,255,0)
            elif y in self.moved_right:
                color = (255,0,0)
            else:
                color = (255,255,255)

            pygame.draw.rect(self.window,color,(x_coord,y_coord,self.rect_len,value*self.size))
        pygame.display.update()
    
    def bubble_sort(self):
        for i in range(self.n-1):
            for j in range(self.n-1):
                if self.list[j] > self.list[j+1]:
                    self.list[j],self.list[j+1] = self.list[j+1],self.list[j]
                    self.moved_left = [j+1]
                    self.moved_right = [j]
                    yield True

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(self.speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type != pygame.KEYDOWN:
                    continue
                if event.key == K_ESCAPE:
                    run = False
                if event.key == K_r and not self.sorting:
                    self.list = self.new_list(self.n)
                if event.key == K_SPACE:
                    self.sorting = True
                if event.key == K_d:
                    if self.speed < 400:
                        self.speed += 10
                if event.key == K_a:
                    if self.speed > 10:
                        self.speed -= 10

            if self.sorting:
                try:
                    next(self.bubble_sort())
                except:
                    self.sorting = False
                    self.moved_left = []
                    self.moved_right = []
            self.window.fill((0,0,0))
            self.draw_list()

window_lenght = 1000
window_height = 800
#the higher the number, the larger the values 
size = 5
visu = visuality(window_lenght,window_height,size)
visu.run()
