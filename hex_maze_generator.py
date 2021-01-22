"""
    Autor: Sebastian Krajna
    Data: 13.01.2021 r.
    
    Generowanie labiryntu zlozonego z szesciokatow
    przy wykorzystaniu algorytmu Aldous-Brodera.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

################################################################
# Klasa Point przechowujaca wspolrzedne x,y
################################################################
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


################################################################
# Klasa Line przechowujaca wspolrzedne poczatku i konca linii
################################################################
class Line:
    def __init__(self, xs, xe, ys, ye, i):
        self.lx  = [xs, xe]
        self.ly  = [ys, ye]
        self.num = i
        
    def draw(self):
        return self.lx, self.ly


################################################################
# Klasa Hexagon tworzy punktu dookola x,y, ktore potrzebne sa
# do utworzenia linii ktore zostana wyswietlone.
# Linie przechowywane sa w tablicy, ktore moga zostac usuniete
# przez wewnetrzna metode, aby utworzyc sciezke labiryntu 
################################################################
class Hexagon:
    def __init__(self, x, y, size):
        self.center  = Point(x, y)
        self.size    = size
        self.points  = self.gen_points_around()
        self.lines   = self.gen_lines()
        self.visited = False
        
    def gen_points_around(self):
        pts = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = np.deg2rad(angle_deg)
            p_x = self.center.x + self.size * np.cos(angle_rad)
            p_y = self.center.y + self.size * np.sin(angle_rad)
            pts.append(Point(p_x, p_y))
        return pts
    
    def gen_lines(self):
        return [Line(self.points[i].x, self.points[i+1].x,
                     self.points[i].y, self.points[i+1].y, i+2) for i in range(-1,5)]
    
    def get_center_cord(self):
        return self.center.x, self.center.y
                
    def get_lines(self):
        return self.lines
    
    def delete_line(self, acx, acy):
        xd = self.center.x - acx
        yd = self.center.y - acy
        direction   = 0
        
        if xd < 0 and yd > 0:
            direction = 1
            
        if xd < 0 and yd == 0:
            direction = 2
            
        if xd < 0 and yd < 0:
            direction = 3
            
        if xd > 0 and yd < 0:
            direction = 4             
            
        if xd > 0 and yd == 0:
            direction = 5   
            
        if xd > 0 and yd > 0:
            direction = 6
        
        for l in self.lines:
            if l.num == direction:
                self.lines.remove(l)


################################################################
# Klasa Maze generuje row x col szesciokatow polaczonych ze soba
# o danym rozmiarze. W niej zaimplementowany jest algorytm, 
# ktory usuwa wspolna sciane sasiadow, ktorzy tworza sciezke.
# Za jej pomoca rowniez mozemy wyswietlic dany labirynt. 
################################################################            
class Maze:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.hexs = []
        self.stack = []
        self.hex_lines = []
        
    def gen_hexs(self):
        width_hex  = np.sqrt(3) * self.size
        height_hex = 2 * self.size
        
        w = width_hex
        h = height_hex
        
        for i in range(self.row):
            w = width_hex
            if i%2 == 0:
                w += w/2
                
            for j in range(self.col):
                self.hexs.append(Hexagon(w, h, self.size))
                w += width_hex
            
            h += 3/4*height_hex
        
    def gen_maze(self):
        self.stack.append((self.hexs[0], 0, 0))
        self.hexs[0].visited = True
                
        while self.stack:
            hex_now, xr, yr = self.stack.pop()
            
            neighb_xy = []
            neighb_dir_odd =  [(1,-1),(1,0),(0,1),(-1,0),(-1,-1),(0,-1)]
            neighb_dir_even = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(0,-1)]
            neighb_dir = []
            
            if xr%2 == 0:
                neighb_dir = neighb_dir_even
            else:
                neighb_dir = neighb_dir_odd
                
            for nd in neighb_dir:
                i,j = nd
                nxr = xr + i
                nyr = yr + j
                if (nxr>=0 and nxr<maze_row) and (nyr>=0 and nyr<maze_col):
                    if self.hexs[nxr*maze_row + nyr].visited == False:
                        neighb_xy.append((nxr, nyr))
            
            if neighb_xy:
                self.stack.append((hex_now, xr, yr))
                r = np.random.randint(len(neighb_xy))
                nxr, nyr = neighb_xy[r]
                
                xc,  yc  = self.hexs[xr *maze_row +  yr].get_center_cord()
                nxc, nyc = self.hexs[nxr*maze_row + nyr].get_center_cord()
                
                self.hexs[ xr*maze_row +  yr].delete_line(nxc, nyc)
                self.hexs[nxr*maze_row + nyr].delete_line( xc,  yc)
                
                self.hexs[nxr*maze_row + nyr].visited = True
                self.stack.append((self.hexs[nxr*maze_row + nyr], nxr, nyr))
                
        maze.hexs[0].delete_line(-10,-10)
        maze.hexs[-1].delete_line(self.row*10, self.col*10)
             
    def gen_lines(self):
        for i in range(maze_row):
            for j in range(maze_col):
                self.hex_lines.append(self.hexs[i * maze_row + j].get_lines())               
    
    def print_lines(self):
        for hex_line in self.hex_lines:
            for line in hex_line:
                x, y = line.draw()
                l = Line2D(x, y)
                plt.plot(*l.get_data(), c='k')
                
                
                
if __name__ == "__main__":
    fig = plt.figure()
    
    # rozmiar labiryntu
    maze_row = 10
    maze_col = 10
    
    # rozmiar szesciokatu
    size = 1
    
    maze = Maze(maze_row, maze_col, size)
    maze.gen_hexs()
    maze.gen_maze()
    maze.gen_lines()
    maze.print_lines()
    
    plt.show()