import tkinter as tk
from time import time, sleep
from random import choice, uniform, randint
from math import sin, cos, radians
from sys import modules
import pyfiglet

GRAVITY = 30  # you can play around with this if you want

class Particle:

    def __init__(self, cv=None, color='white', x=0., y=0.,
                 vx=0., vy=0., lifespan=5.):

        self.cv = cv
        self.cid = None
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.color = color
        self.age, self.lifespan = 0, lifespan

    def update(self, dt):
        """Update position and velocity after dt seconds have passed.

        Args:
            dt (float): the time that has passed after the last update (in s).

        """
        self.age += dt
        if self.alive():
            self.vy += GRAVITY * dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.cv.move(self.cid, self.vx * dt, self.vy * dt)
        elif self.cid is not None:
            cv.delete(self.cid)
            self.cid = None

    def alive(self):
        """Check if particle is still within its lifespan."""
        return self.age <= self.lifespan


class SquareParticle(Particle):
    """A Particle with a quadratic shape"""
    def __init__(self, x=0., y=0., size=2., **kwargs):
        super().__init__(x=x, y=y, **kwargs)
        self.cid = self.cv.create_polygon(
            x - size, y - size, x + size, y - size,
            x + size, y + size, x - size, y + size,
            fill=self.color)


class TriangleParticle(Particle):
    """A Particle with a triangular shape"""
    def __init__(self, x=0., y=0., size=2., **kwargs):
        super().__init__(x=x, y=y, **kwargs)
        self.cid = self.cv.create_polygon(
            x - size, y - size, x + size,
            y - size, x, y + size,
            fill=self.color)


class CircularParticle(Particle):
    """A Particle with a circular shape."""
    def __init__(self, x=0., y=0., size=2., **kwargs):
        super().__init__(x=x, y=y, **kwargs)
        self.cid = self.cv.create_oval(
            x - size, y - size, x + size,
            y + size, fill=self.color)


class Fireworks:

    def __init__(self, cv=None):
        """Init Fireworks objects.

        Args:
            cv (Tk.canvas): the canvas in which the particle is drawn.

        """
        self.cv = cv
        self.age = 0
        self.particles = []

    def update(self, dt):
        """Update the fireworks' particles and remove dead ones.

        Args:
            dt (float): the time that has passed after the last update (in s).

        """
        self.age += dt
        for p in self.particles:
                 p.update(dt)
        for i in range(len(self.particles) - 1, -1, -1):
            if not self.particles[i].alive():
                del self.particles[i]


class Volcano(Fireworks):
    """A volcano that continuously emits colored particles.

    Attributes:
        x (float): x-coordinate of the volcano.
        pps (float): the number of particles to spawn per second.
        colors (list of string): the colors of the particles to spawn."""

    def __init__(self, cv, x, pps, colors):
        """Init Volcano objects.

        Args:
            cv (Tk.canvas): the canvas in which the particle is drawn.
            x (float): x-coordinate of the volcano.
            pps (float): the number of particles to spawn per second.
            colors (list of string): the colors of the particles to spawn.

        """
        super().__init__(cv)
        self.cid = cv.create_polygon(x - 12, 530,  # size and color are fixed
                                     x + 12, 530,  # (can be parametrized)
                                     x, 500,
                                     fill="orange")
        self.x = x
        self.pps = pps
        self.colors = colors
        self._tospawn = 0

    def update(self, dt):
        """Continuously emits new random particles and updates them.

        Args:
            dt (float): the time that has passed after the last update (in s).

        """
        super().update(dt)
        self._tospawn += self.pps * dt
        color = self.colors[int(self.age / 3) % len(self.colors)]
        for i in range(int(self._tospawn)):
            ptype = choice(
                [SquareParticle, TriangleParticle, CircularParticle])
            angle = uniform(-0.25, 0.25)
            speed = -uniform(80.0, 120.0)
            vx = sin(angle) * speed
            vy = cos(angle) * speed
            self.particles.append(
                ptype(cv=self.cv, x=self.x, y=500, color=color, vx=vx, vy=vy))
        self._tospawn -= int(self._tospawn)


class Rocket(Particle, Fireworks):

    def __init__(self, cv, x=0., y=0., size=2., **kwargs):
        super().__init__(cv, x=x, y=y, **kwargs)
        self.cid = self.cv.create_oval(
            x - size, y - size, x + size,
            y + size, fill=self.color)
        self.x = x
        self.pps = 100
        self.colors = ['red']
        self._tospawn = 0
        self.particles = []

    def update(self, dt):
        self.age += dt
        if self.alive():
            self.vy += -GRAVITY * dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.cv.move(self.cid, self.vx * dt, self.vy * dt)
        elif self.cid is not None:
            cv.delete(self.cid)
            self.cid = None
            self._tospawn += 10 * self.pps * dt
        if self.cid is None:
             Fireworks.update(self, dt)
             color = self.colors[int(self.age / 3) % len(self.colors)]
             #self._tospawn += self.pps * dt
             for i in range(int(self._tospawn)):
              ptype = choice(
                [CircularParticle])
              angle = uniform(-100, 100)
              speed = -uniform(80, 120.0)
              vx = sin(angle) * speed
              vy = cos(angle) * speed
              self.particles.append(
                 ptype(cv=self.cv, x=self.x, y=self.y, color=color, vx=vx, vy=vy))
              self._tospawn -= self.pps * dt


def simulate(cv, objects):
    """Fireworks simulation loop.

        Args:
            cv (float): the canvas in which the firework objects are drawn.
            objects (float): the firework objects.

    """
    t = time()
    while running:
        sleep(0.01)
        tnew = time()
        t, dt = tnew, tnew - t
        for o in objects:
            o.update(dt)
        cv.update()


def close(*ignore):
    """Stops simulation loop and closes the window."""
    global running
    running = False
    root.destroy()


if __name__ == '__main__':
    
    name = input("enter your name: ")
    banner1 = pyfiglet.figlet_format("Happy")
    banner2 = pyfiglet.figlet_format("Birthday")
    banner3 = pyfiglet.figlet_format(name)

    x = 10
    root = tk.Tk()
    cv = tk.Canvas(root, height=600, width=800)
    cv.create_rectangle(0, 0, 800, 600, fill="black")  # sky
    cv.create_rectangle(0, 450, 800, 600, fill="gray11")  # ground
    cv.pack()
    #cv.create_text(100, 100, text=banner1, anchor='nw', font='TkMenuFont', fill='red')
    #cv.create_text(300, 100, text=banner2, anchor='nw', font='TkMenuFont', fill='red')
    #cv.create_text(200, 200, text=banner3, anchor='nw', font='TkMenuFont', fill='Green')
    cv.create_text(100, 100, text=banner1, anchor='nw', fill='red')
    cv.create_text(300, 100, text=banner2, anchor='nw', fill='red')
    cv.create_text(200, 200, text=banner3, anchor='nw', fill='Green')
    

    v1 = Volcano(cv, 400, 100, ["red", "green", "gold"])
    ro = Rocket(cv, 600, 500)
    objects = [v1, ro]

    # close with [ESC] or (x) button
    root.bind('<Escape>', close)
    root.protocol("WM_DELETE_WINDOW", close)

    running = True
    root.after(500, simulate, cv, objects)
    if "idlelib" not in modules:
        root.mainloop()