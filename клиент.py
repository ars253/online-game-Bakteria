import math
import socket
import time
import pygame
mainsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mainsocket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
mainsocket.connect(('localhost',10000))
pygame.init()
width=800
height=600
СС=(width//2,height//2)
old=[0,0]
radius=50
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('бактерия')
run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if pygame.mouse.get_focused():
            pos=pygame.mouse.get_pos()
            vector=pos[0]-СС[0],pos[1]-СС[1]
            lenv=math.sqrt(vector[0]**2+vector[1]**2)
            vector=vector[0]/lenv,vector[1]/lenv
            if lenv<=radius:
                vector=0,0
            if vector!=old:
                old=vector
                msg=f'<{vector[0]},{vector[1]}>'
                mainsocket.send(msg.encode())
    data=mainsocket.recv(1024).decode()
    print(data)
    screen.fill('white')
    pygame.draw.circle(screen,'green',СС,radius)
    pygame.display.update()
pygame.quit()