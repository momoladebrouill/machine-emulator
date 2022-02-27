import pygame as pg
from sys import exit
pg.init()
fps=pg.time.Clock()
f=pg.display.set_mode((500,500),pg.RESIZABLE)
font=pg.font.SysFont('consolas',25)
pg.display.set_caption('Sytem calculation')

class wind:
    h=500
    l=500

class dep:
    fkx=25
    fky=25
    rlx=25
    rly=25

class Button:
    name='Bouton'
    def __repr__(self):return f'B {self.IsOn}'
    def __init__(self,pos):
        self.pos=(carto(pos[0]),carto(pos[1]))
        self.IsOn=True
        self.pored=False
        self.filed=[]
        self.rect=pg.Rect(0,0,20,20)
    def draw(self):
        if self.IsOn:
            pg.draw.circle(f,0x00aa00,(dep.fkx+self.pos[0],dep.fky+self.pos[1]),10)
        self.rect=pg.draw.circle(f,0xffffff,(dep.fkx+self.pos[0],dep.fky+self.pos[1]),10,1)
        
class Cable:
    name='Cable'
    def __repr__(self)-> str:return f'Cable {self.pos1} {self.pos2}'
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
        pg.draw.line(f,c,(dep.fkx+self.pos1.pos[0],dep.fky+self.pos1.pos[1]),(dep.fkx+self.pos2.pos[0],dep.fky+self.pos2.pos[1]),2)
   
    def destroy(self):
        fils.remove(self)
        self.pos1.filed.remove(self)
        self.pos2.filed.remove(self)
   
class Digit:
    name='Digit'
    def __repr__(self):return f"D {self.val}"
    def __init__(self,pos,nb=3):
        self.pos=(carto(pos[0]),carto(pos[1]))
        self.val=0
        self.entrys=[Button((pos[0],pos[1]+i*50)) for i in range(3)]
        for i in self.entrys:
            i.pored=self
            objs[i]=i.rect
    
    def draw(self):
        num=font.render(str(self.val),1,(255,255,255))
        f.blit(num,(dep.fkx+self.pos[0],dep.fky+self.pos[1]))
        self.rect=num.get_rect()
        self.rect.x,self.rect.y=(self.pos[0]+dep.rlx,self.pos[1]+dep.rly)
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
    def __repr__(self):return 'Port '+self.mode
    def __init__(self,pos):
        '''entry1,entry2,exit'''
        self.pos=(carto(pos[0]),carto(pos[1]))
        self.buts=[Button(self.pos) for _ in range(3)]
        self.positionstudent()
        self.mode='OR'
        for but in self.buts:
          but.pored=self
          objs[but]=but.rect
    
    def draw(self):
        if self.mode=='OR':
            self.buts[2].IsOn=self.buts[0].IsOn or self.buts[1].IsOn
        elif self.mode=='AND':
            self.buts[2].IsOn=self.buts[0].IsOn and self.buts[1].IsOn
            
        des=font.render(self.mode,1,(255,0,255))
        desrect=des.get_rect()
        f.blit(des,(dep.fkx+self.pos[0]-desrect.width/2,dep.fky+self.pos[1]-desrect.height/2))
        
        self.positionstudent()
        for but in self.buts:
          but.draw()
        
        self.rect=desrect
        self.rect.x,self.rect.y=(self.pos[0]-desrect.width/2+dep.rlx,self.pos[1]-desrect.height/2+dep.rly)
    
    def destroy(self):
        global objs
        for but in self.buts:
          objs.pop(but)
        objs.pop(self)
        
    def positionstudent(self):
        self.buts[0].pos=(self.pos[0]-50,self.pos[1]-50)
        self.buts[1].pos=(self.pos[0]-50,self.pos[1]+50)
        self.buts[2].pos=(self.pos[0]+50,self.pos[1])
 
class Not:
    name='NOT'
    def __repr__(self):return f"N {self.entry.IsOn}"
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
    
    def draw(self):
        des=font.render('NOT',1,(255,0,255))
        desrect=des.get_rect()
        f.blit(des,(dep.fkx+self.pos[0]-desrect.width/2,dep.fky+self.pos[1]-desrect.height/2))
        self.exit.IsOn= not self.entry.IsOn 
        self.positionstudent()
        self.entry.draw()
        self.exit.draw()
        self.rect=self.entry.rect
        self.rect.width=100

    def destroy(self):
        global objs
        objs.pop(self.entry)
        objs.pop(self.exit)
        objs.pop(self)
    def positionstudent(self):
        self.entry.pos=(self.pos[0]-50,self.pos[1])
        self.exit.pos=(self.pos[0]+50,self.pos[1])
        
carto=lambda val:round(val/50)*50
def findobj(pos):
    for obj in objs:
        if objs[obj].collidepoint(pos):
            return obj
    return ''

créable=[Button,Cable,Port,Not,Digit]
B=1
pushing=0
pos1=0
fils=[]
selection=0
handling=None
objs={}
dep.rly,dep.rlx=0,0
obs=''
mouse=(0,0)

while B:
    B+=1
    pg.display.flip()
    f.fill(0)
    mode=créable[selection]
    f.blit(font.render(mode.name,1,(255,255,255)),(0,0))
    dep.fkx+=(dep.rlx-dep.fkx)/7
    dep.fky+=(dep.rly-dep.fky)/7
    dep.fkx,dep.fky=round(dep.fkx),round(dep.fky)

    
    for y in range(-dep.rly,wind.h-dep.fky,50):
        for x in range(-dep.rlx,wind.l-dep.fkx,50):
            pg.draw.circle(f,0x555555,(dep.fkx+x,dep.fky+y),2)
    pg.draw.line(f,0xffffff,(dep.fkx+5,dep.fky),(dep.fkx-5,dep.fky))
    pg.draw.line(f,0xffffff,(dep.fkx,dep.fky+5),(dep.fkx,dep.fky-5))
    for fil in fils:
        fil.draw()
    for obj in objs:
        obj.draw()
        objs[obj]=obj.rect
        
    if pos1:
        pg.draw.line(f,0xffffff,(pos1.pos[0]+dep.fkx,pos1.pos[1]+dep.fky),mous)
    if handling:
        handling.pos=mouse
        handling.draw()
        
    mous=pg.mouse.get_pos()
    mouse=(carto(mous[0]),carto(mous[1]))
    obs=findobj(mouse)
    
    if handling:
        handling.pos=(mouse[0]-dep.rlx,mouse[1]-dep.rly)
        handling.draw()

    f.blit(font.render(str(obs),True,(255,0,0)),mouse)
    for event in pg.event.get():
        if event.type==pg.KEYUP:
            key=event.key
            if key==pg.K_UP:
                dep.rly+=50
            elif key==pg.K_DOWN:
                dep.rly-=50
            elif key==pg.K_LEFT:
                dep.rlx+=50
            elif key==pg.K_RIGHT:
                dep.rlx-=50
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
                        pos1=obs #racccrocher le début du cable
                else:
                    if obs=='':
                        handling=mode(mouse) # créer un nouvel objet
                    else:
                        handling=obs
            
        elif event.type==pg.MOUSEBUTTONUP:
            if event.button==1:
                if mode==Button :
                    if type(obs)==Button:
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
            exit()
    fps.tick(60)
        

