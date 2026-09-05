import socket
import time
import pygame
import psycopg2
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker
engine=create_engine('postgresql+psycopg2://postgres:543098@localhost/бактерия')
Session=sessionmaker(engine)
Base=declarative_base()
s=Session()
pygame.init()
WIDTHROOM,HEIGHTROOM=4000,4000
WIDTHSERVER,HEIGHTSERVER=300,300
FPS=100
screen=pygame.display.set_mode((WIDTHSERVER,HEIGHTSERVER))
pygame.display.set_caption('server')
clock=pygame.time.Clock()
class Player(Base):
    __tablename__='gamers'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String)
    addres=Column(String)
    x=Column(Integer,default=500)
    y=Column(Integer,default=500)
    size=Column(Integer,default=50)
    errors=Column(Integer,default=0)
    abs_speed=Column(Integer,default=1)
    speed_x=Column(Integer,default=0)
    speed_y=Column(Integer,default=0)
    def __init__(self,name,address):
        self.name=name
        self.addres=address
Base.metadata.create_all(engine)
class LocalPlayer():
   def __init__(self,id,name,sock,address):
       self.id=id
       self.db=s.get(Player,self.id)
       self.name=name
       self.sock=sock
       self.address=address
       self.x=500
       self.y=500
       self.size=50
       self.errors=0
       self.abs_speed=1
       self.speed_x=0
       self.speed_y=0
   def update(self):
       self.x+=self.speed_x
       self.y+=self.speed_y
   def change_speed(self,vector):
       vector=find(vector)



def find(vector):
    first=vector.find('<')
    second=vector.find('>')
    if first<second and first>=0:
        result=vector[first+1:second]
        result=result.split(',')
        result=list(map(float,result))
        return result
    return''
mainsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mainsocket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
mainsocket.bind(('localhost',10000))
mainsocket.setblocking(False)
mainsocket.listen(5)
players={}
run=True
while run:
    clock.tick(FPS)
    try:
        newsocket,addr=mainsocket.accept()
        print('подключился',addr)
        newsocket.setblocking(False)
        player=Player('name',addr)
        s.merge(player)
        s.commit()
        addr=f'({addr[0]},{addr[1]})'
        data=s.query(Player).filter(Player.addres==addr)
        for user in data:
            localPlayer=LocalPlayer(user.id,'name',newsocket,addr)
            players[user.id]=localPlayer
        print(players)
    except BlockingIOError:
        pass
    except Exception as e:
        print(e)
    for id in list(players):
        try:
            data=players[id].sock.recv(1024).decode()
            players[id].change_speed(data)
            print(data)
        except:
            pass
    for id in list(players):
        try:
            players[id].sock.send('hi'.encode())
        except:
            players[id].sock.close()
            del players[id]
            s.query(Player).filter(Player.id==id).delete()
            s.commit()
            print('игрок отключен')
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    screen.fill('black')
    for id in list(players):
        players[id].update()
    for id in players:
        player=players[id]
        x=player.x*WIDTHSERVER//WIDTHROOM
        y=player.y*HEIGHTSERVER//HEIGHTROOM
        size=player.size*WIDTHSERVER//WIDTHROOM
        pygame.draw.circle(screen,'red',(x,y),size)
    pygame.display.flip()



pygame.quit()
mainsocket.close()
s.query(Player).delete()
s.commit()