from typing import Literal
import pygame as pg
pg.init()
fps=pg.time.Clock()
f=pg.display.set_mode((500,500),pg.RESIZABLE)
font=pg.font.SysFont('consolas',25)


class wind:
    h=500
    l=500

class dep:
    x=0
    y=0

class Button:
    name='Bouton'
    def __repr__(self):
      return 'B '+str(self.IsOn)+' '+str(self.pos)
    def __init__(self,pos):
        self.pos=(carto(pos[0]),carto(pos[1]))
        self.IsOn=True
        self.pored=False
        self.filed=[]
        self.rect=pg.Rect(0,0,20,20)
    def draw(self):
        if self.IsOn:
            pg.draw.circle(f,0x00aa00,(dep.x+self.pos[0],dep.y+self.pos[1]),10)
        self.rect=pg.draw.circle(f,0xffffff,(dep.x+self.pos[0],dep.y+self.pos[1]),10,1)
        
class Cable:
    name='Cable'
    def __init__(self,pos1,pos2,on=False):
        self.pos1=pos1
        self.pos2=pos2
        self.pos1.filed.append(self)
        self.pos2.filed.append(self)
        self.IsOn=on
    def draw(self):
        self.IsOn=self.pos1.IsOn
        self.pos2.IsOn=self.IsOn
        if self.IsOn:
            c=0x00ff00
        else:
            c=0xffffff
        pg.draw.line(f,c,(dep.x+self.pos1.pos[0],dep.y+self.pos1.pos[1]),(dep.x+self.pos2.pos[0],dep.y+self.pos2.pos[1]),2)
    def __repr__(self)-> str:
      return 'Cable '+str(self.pos1)+' '+str(self.pos2)
    def destroy(self):
        fils.remove(self)
        self.pos1.filed.remove(self)
        self.pos2.filed.remove(self)
   
class Digit:
    name='Digit'
    def __init__(self,pos,nb=3):
        self.pos=(carto(pos[0]),carto(pos[1]))
        self.val=0
        self.entrys=[Button((pos[0],pos[1]+i*50)) for i in range(1,nb+1)]
        for i in self.entrys:
            i.pored=self
            objs[i]=i.rect
    def __repr__(self) -> str:
        return f"D {self.val},{self.pos}"
    def draw(self):
        num=font.render(str(self.val),1,(255,255,255))
        f.blit(num,(dep.x+self.pos[0],dep.y+self.pos[1]))
        self.rect=num.get_rect()
        self.rect.x,self.rect.y=(self.pos[0]+depx,self.pos[1]+depy)
        place=0
        for i in format(self.val,'0'+str(len(self.entrys))+'b')[::-1]:
            self.entrys[place].IsOn=(i =='1')
            place+=1
    def destroy(self):
        global objs
        for but in self.entrys:
          objs.pop(but)
        objs.pop(self)
        
class Port: 
    name='Port'
    def __init__(self,pos):
        '''entry1,entry2,exit'''
        self.pos=(carto(pos[0]),carto(pos[1]))
        self.buts=[Button(self.pos) for _ in range(3)]

        self.positionstudent()
        self.mode='OR'
        for but in self.buts:
          but.pored=self
          objs[but]=but.rect
    def __repr__(self):
      return 'Port'+self.mode
    def draw(self):
        if self.mode=='OR':
            self.buts[2].IsOn=self.buts[0].IsOn or self.buts[1].IsOn
        elif self.mode=='AND':
            self.buts[2].IsOn=self.buts[0].IsOn and self.buts[1].IsOn
            
        des=font.render(self.mode,1,(255,0,255))
        desrect=des.get_rect()
        f.blit(des,(dep.x+self.pos[0]-desrect.width/2,dep.y+self.pos[1]-desrect.height/2))
        
        self.positionstudent()
        for but in self.buts:
          but.draw()
        
        self.rect=desrect
        self.rect.x,self.rect.y=(self.pos[0]-desrect.width/2+depx,self.pos[1]-desrect.height/2+depy)
    def positionstudent(self):
        self.buts[0].pos=(self.pos[0]-50,self.pos[1]-50)
        self.buts[1].pos=(self.pos[0]-50,self.pos[1]+50)
        self.buts[2].pos=(self.pos[0]+50,self.pos[1])
    def destroy(self):
        global objs
        for but in self.buts:
          objs.pop(but)
        objs.pop(self)
 
class Not:
    name='NOT'
    def __init__(self,pos):
        self.pos=(carto(pos[0]),carto(pos[1]))
        self.entry=Button(self.pos)
        self.exit=Button(self.pos)
        self.positionstudent()
        self.entry.pored=self
        self.exit.pored=self
        self.rect=pg.Rect(0,0,0,0)
        objs[self.entry]=self.entry.rect
        objs[self.exit]=self.exit.rect
    def __repr__(self) -> str:
        return f"N {self.pos}"
    def draw(self):
        des=font.render('NOT',1,(255,0,255))
        desrect=des.get_rect()
        f.blit(des,(dep.x+self.pos[0]-desrect.width/2,dep.y+self.pos[1]-desrect.height/2))
        self.exit.IsOn= not self.entry.IsOn 
        self.positionstudent()
        self.entry.draw()
        self.exit.draw()
        self.rect=self.entry.rect
        self.rect.width=100

    def positionstudent(self):
        self.entry.pos=(self.pos[0]-50,self.pos[1])
        self.exit.pos=(self.pos[0]+50,self.pos[1])
    def destroy(self):
        global objs
        objs.pop(self.entry)
        objs.pop(self.exit)
        objs.pop(self)

créable=[Button,Cable,Port,Not,Digit]

def findobj(pos):
    for obj in objs:
        if objs[obj].collidepoint(pos):
            return obj
    return ''


B=1
pushing=0
pos1=0
fils=[]
selection=0
handling=None
objs={}
depy,depx=0,0
obs=Literal['']
carto=lambda val:round(val/50)*50
while B:
    B+=1
    pg.display.flip()
    f.fill(0)
    fps.tick(60)
    mode=créable[selection]
    f.blit(font.render(mode.name,1,(255,255,255)),(0,0))
    dep.x+=(depx-dep.x)/7
    dep.y+=(depy-dep.y)/7
    dep.x,dep.y=round(dep.x),round(dep.y)
    mouse=(carto(pg.mouse.get_pos()[0]),carto(pg.mouse.get_pos()[1]))
    for y in range(-dep.y,wind.h-dep.y,50):
        for x in range(-dep.x,wind.l-dep.x,50):
            pg.draw.circle(f,0x555555,(dep.x+x,dep.y+y),2)
    for fil in fils:
        fil.draw()
    for obj in objs:
        obj.draw()
        #pg.draw.rect(f,0xff00ff,obj.rect)
        objs[obj]=obj.rect
    if pos1:
        pg.draw.line(f,0xffffff,(pos1.pos[0]+dep.x,pos1.pos[1]+dep.y),mouse)
    if handling:
        handling.pos=mouse
        handling.draw()
    mous=pg.mouse.get_pos()
    mouse=(carto(mous[0]),carto(mous[1]))
    obs=findobj(mouse)
    if handling:
        handling.pos=(mouse[0]-depx,mouse[1]-depy)
        handling.draw()
    pg.draw.circle(f,0xff00000,mouse,5)
    f.blit(font.render(str(obs),True,(255,0,0)),mouse)
    for event in pg.event.get():
        if event.type==pg.KEYUP:
            key=event.key
            if key==pg.K_UP:
                depy+=50
            elif key==pg.K_DOWN:
                depy-=50
            elif key==pg.K_LEFT:
                depx+=50
            elif key==pg.K_RIGHT:
                depx-=50
            elif key==pg.K_q:
                pg.quit()
                B=0

            else:
                selection+=1
                selection=selection%len(créable)
           
        elif event.type==pg.MOUSEBUTTONDOWN:
            pushing=event.button
            if pushing==1:
                if mode==Cable:
                    obs=findobj(mouse)
                    if type(obs)==Button:
                        pos1=obs #raacccrocher le début du cable
                else:
                    if obs=='':
                        handling=mode(mouse) # créer un nouvel objet
                    else:
                        handling=obs
            
            
            
        elif event.type==pg.MOUSEBUTTONUP:
            if event.button==1:
                if mode==Button :
                    if obs:
                        obs.IsOn=not obs.IsOn
                    if handling:
                        objs[handling]=handling.rect

                elif mode==Cable:
                    if type(obs)==Button:
                        fils.append(Cable(pos1,obs))
                    pos1=0
                

                else:
                    if handling:
                        objs[handling]=handling.rect
                    if type(obs)==Digit:
                        obs.val+=1
                        obs.val=obs.val%8
                    elif type(obs)==Button:
                        obs.IsOn=not obs.IsOn
            elif event.button==3 and obs:
                if type(obs)==Button:
                    if obs.filed:
                        for i in obs.filed:
                            i.destroy()
                    elif obs.pored:
                        obs.pored.destroy()
                    else:
                        objs.pop(obs)
                elif type(obs)==Port:
                    if obs.mode=='OR':
                        obs.mode='AND'
                    elif obs.mode=='AND':
                        obs.mode='OR'
                elif type(obs)==Digit:
                    obs.val+=1
                    obs.val=obs.val%(2**3)
                else:
                    obs.destroy()
            handling=0

        elif event.type==pg.VIDEORESIZE:
            wind.h=event.h
            wind.l=event.w
            
        elif event.type==pg.QUIT:
            B=0
            pg.quit()


