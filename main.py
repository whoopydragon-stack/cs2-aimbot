import tkinter as tk
import random, math

W, H = 1100, 700

class Bot:
    def __init__(self):
        self.x = random.randint(80, W-80)
        self.y = random.randint(100, H-80)
        self.vx = random.choice([-1,1]) * random.uniform(1.0, 3.0)
        self.vy = random.choice([-1,1]) * random.uniform(0.6, 2.2)
        self.r = random.randint(16, 24)
        self.alive = True
        self.respawn = 0
    def update(self):
        if not self.alive:
            self.respawn -= 1
            if self.respawn <= 0: self.__init__()
            return
        self.x += self.vx; self.y += self.vy
        if self.x < 55 or self.x > W-55: self.vx *= -1
        if self.y < 80 or self.y > H-45: self.vy *= -1

class App:
    def __init__(self, root):
        self.root=root; root.title("CS2 Bot Aim Sandbox"); root.resizable(False,False)
        self.c=tk.Canvas(root,width=W,height=H,bg="#101318",highlightthickness=0); self.c.pack()
        self.bots=[Bot() for _ in range(10)]
        self.esp=True; self.aim=True; self.fov=150; self.score=0; self.shots=0; self.hits=0
        self.mx=W//2; self.my=H//2; self.locked=None
        self.c.bind("<Motion>",self.mouse); self.c.bind("<Button-1>",self.shoot)
        root.bind("<e>",lambda e:self.toggle("esp")); root.bind("<a>",lambda e:self.toggle("aim"))
        root.bind("<r>",lambda e:self.reset()); root.bind("<Escape>",lambda e:root.destroy())
        self.loop()
    def mouse(self,e): self.mx,self.my=e.x,e.y
    def toggle(self,w):
        if w=="esp": self.esp=not self.esp
        else: self.aim=not self.aim
    def best_target(self):
        best=None; bd=self.fov
        for b in self.bots:
            if b.alive:
                d=math.hypot(b.x-self.mx,b.y-self.my)
                if d<bd: best,bd=b,d
        return best
    def shoot(self,_=None):
        self.shots+=1
        t=self.locked if self.aim and self.locked and self.locked.alive else self.best_target()
        if t and math.hypot(t.x-self.mx,t.y-self.my)<t.r+18:
            self.hits+=1; self.score+=100; t.alive=False; t.respawn=45
        else: self.score=max(0,self.score-10)
    def reset(self):
        self.score=self.shots=self.hits=0; self.bots=[Bot() for _ in range(10)]
    def draw(self):
        self.c.delete("all"); cx,cy=self.mx,self.my
        self.c.create_oval(cx-self.fov,cy-self.fov,cx+self.fov,cy+self.fov,outline="#505866")
        self.c.create_line(cx-10,cy,cx+10,cy,fill="white"); self.c.create_line(cx,cy-10,cx,cy+10,fill="white")
        self.locked=self.best_target() if self.aim else None
        for i,b in enumerate(self.bots):
            b.update()
            if not b.alive: continue
            x,y,r=b.x,b.y,b.r
            self.c.create_oval(x-r,y-r,x+r,y+r,fill="#c43d48",outline="")
            self.c.create_rectangle(x-r-4,y-r-12,x+r+4,y+r+18,outline="#dfe5ef")
            if self.esp:
                self.c.create_rectangle(x-r-10,y-r-22,x+r+10,y+r+28,outline="#55e6ff",width=2)
                self.c.create_text(x,y-r-34,text=f"BOT {i+1}",fill="#55e6ff",font=("Segoe UI",9,"bold"))
            if b is self.locked:
                self.c.create_oval(x-r-14,y-r-14,x+r+14,y+r+14,outline="#ffd34d",width=3)
                self.c.create_line(cx,cy,x,y,fill="#ffd34d",width=2)
        self.c.create_rectangle(15,15,330,68,fill="#171b22",outline="#303744")
        self.c.create_text(28,30,anchor="w",text=f"SCORE  {self.score}    HITS  {self.hits}/{self.shots}",fill="white",font=("Segoe UI",13,"bold"))
        self.c.create_text(28,52,anchor="w",text=f"[E] ESP: {'ON' if self.esp else 'OFF'}   [A] Aim: {'ON' if self.aim else 'OFF'}   [R] Reset",fill="#aeb7c5",font=("Segoe UI",9))
        self.c.create_text(W-18,24,anchor="e",text="STANDALONE BOT SANDBOX",fill="#697384",font=("Segoe UI",9,"bold"))
        self.c.create_text(W-18,46,anchor="e",text="No CS2 process / memory / injection access",fill="#697384",font=("Segoe UI",8))
    def loop(self):
        self.draw(); self.root.after(16,self.loop)

root=tk.Tk(); App(root); root.mainloop()
