#匯入pygame
import pygame as pg
#pygame初始化
pg.init()

#設定視窗
width, height = 640, 480                        #遊戲畫面寬和高
screen = pg.display.set_mode((width, height))   #依設定顯示視窗
pg.display.set_caption("Sean's game")           #設定程式標題



#關閉程式的程式碼
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
pg.quit()   