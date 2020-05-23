import pickle
import random
import math
import datetime
import os


def take_step(x, y):
    """Take random step."""
    random_int = random.randint(0,1)
    random_choice = random.choice([-1,1])
    x, y = (x+random_choice, y) if random_int==0 else (x,y+random_choice)
    return x,y


def walk(agg):
    """Brownian method."""
    (xc,yc),r = seed_circle(agg)
    x,y = get_initial_pos(xc,yc,r)
    while True:
        x,y = take_step(x, y)
        if too_far(x,y,xc,yc,r): break # shouldn't go too far
        # check if new coord is next to agg
        if (((x-1,y) in agg) or ((x+1,y) in agg) or ((x,y-1) in agg) or  ((x,y+1) in agg)):
            agg[(x,y)]=len(agg)
            break
    return agg


def seed_circle(agg):
    """Find seed circle"""
    x_s = [x for x, _ in agg]
    xmin, xmax = min(x_s), max(x_s)
    y_s = [y for _, y in agg]
    ymin, ymax = min(y_s), max(y_s)
    xc, yc = (xmin+xmax)/2, (ymin+ymax)/2 #center
    r = (((xmax-xmin)/2)**2 + ((ymax-ymin)/2)**2)**0.5 # radius
    return (xc,yc),r


def get_initial_pos(xc,yc,r):
    """Select initial coordinate randomly"""
    rand_angle = 2* math.pi * random.random()
    return int(xc + r*math.cos(rand_angle)), int(yc + r*math.sin(rand_angle))


def too_far(x,y,x0,y0,r,d=10):
    """Check if the particle went too far."""
    return ((x-x0)**2 + (y-y0)**2)**0.5 > r+d


def grow(agg=None,npart=10000):
    """Grow initial aggregate"""
    if not agg:
        agg={(0,0):0} # setup initial agg
    for i in range(npart):
        agg = walk(agg) # apply Brownian motion
    return agg


def read_agg(file='agg.txt'):
    """
    Read agg file
    By defaults tries to find agg.txt
    """
    agg = {}
    with open(file) as f:
        for line in f:
            x,y,index = tuple(line.split(',')) # line looks like 0,0:0 ==> x,y:index
            agg[(int(x),int(y))] = int(index.strip())
    return agg

def save_agg(agg, file='agg.txt'):
    """
    Save agg to txt
    """
    with open(file, 'w') as f:
        for coord, index in agg.items():
            f.write(f"{coord[0]},{coord[1]},{index}\n") # x,y,index

def show_progress(current_step, overall):
    """
    SHow grow progress in percentage
    """
    perc = (current_step/overall)*100
    # print()
    print(f"grow in progress...{perc:.2f}%", end="\r")

if __name__=='__main__':
    try:
        M = int(input("Enter number of replications (M): "))
        N = int(input("Enter initial number of particles (N): "))
        print()
        agg = read_agg() if os.path.exists('agg.txt') else grow(npart=N)
        for i in range(M):
            agg = grow(agg,npart=N) # create the aggregate
            show_progress(i + 1, M)
        save_agg(agg)
        print()
        print("Grow finished!")
    except ValueError:
        print("Please enter correct numbers for M and N")