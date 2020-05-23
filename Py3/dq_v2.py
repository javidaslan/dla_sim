import random
import scipy.optimize
import numpy as np
import argparse
import traceback
import time


def calculate_mass_list(agg, rl):
    """Calculate the mass list with given r list."""
    random_coord = random.choice(list(agg.keys()))
    pos = np.array(list(agg.keys()))  # get position of all points
    dist = ((random_coord[0] - pos[:, 0]) ** 2 + (random_coord[1] - pos[:, 1]) ** 2) ** 0.5  # calculate ditance
    dist = dist[dist < rl[-1]]  # ignore what is too far
    closest = dist < rl[0]  # select which are too close
    m0 = np.sum(closest)  # number which are too close
    dist = dist[~closest]  # discard too close (maybe save little time)

    r = np.sort(dist)
    # print(r)
    m = m0 + np.arange(len(r))
    ml = np.interp(rl, r, m)  # calculate mass for all r limits
    return ml


def calculate_Dq_at_q(distance_range, mll, q):
    """Calculate Dq at give q"""
    x = np.log10(distance_range) * (q - 1) # calculate x
    y = np.log10(np.mean(np.power(mll, q - 1), axis=0)) # calculate y
    # fit linear on log log
    (a, b), pcov = scipy.optimize.curve_fit(lambda x, a, b: a * x + b, x, y)
    return a


def calculate_Dq(agg, pivots, q_range, distance_range):
    """Calculate D(q) at a given q."""
    mass_list, Dq = [], []
    while pivots:
        ml = calculate_mass_list(agg, distance_range)
        mass_list.append(ml)
        pivots -= 1

    for q in q_range:
        Dq_at_q = calculate_Dq_at_q(distance_range, mass_list, q)
        Dq.append(Dq_at_q)

    return Dq


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


def save_dq(dq, file='Dq.txt'):
    """
    Save agg to txt
    """
    with open(file, 'w') as f:
        for elm in dq:
            f.write(f"{elm}\n") # x,y,index


def show_progress(current_step, overall):
    """
    Show grow progress in percentage
    """
    perc = (current_step/overall)*100
    print(f"Calculation is in progress...{perc:.2f}%", end="\r")

if __name__=='__main__':
    try:
        argparser = argparse.ArgumentParser()
        argparser.add_argument('-r', '--replications', required=True, type=int, help="Number of replications")
        argparser.add_argument('-p', '--pivots', required=True, type=int, help="Number of pivot points")
        argparser.add_argument('-d', '--distance-range', required=True, type=int, nargs=2, help="Distance range, insert 2 numbers as start and end of range")
        argparser.add_argument('-q', '--q-range', required=True, type=int, nargs=2, help="q range, insert 2 numbers as start and end of range")
        args = argparser.parse_args()

        replications = args.replications
        pivots = args.pivots
        d_range = range(*args.distance_range)
        q_range = range(*args.q_range)

        agg = read_agg()  # read agg
        print()
        Dq = []
        start_time = time.time()
        for i in range(replications):
            Dq_i = calculate_Dq(agg, q_range=q_range, pivots=pivots, distance_range=d_range)
            Dq.append(Dq_i)
            show_progress(i+1, replications)
        save_dq(dq=Dq)  # save results
        print(f"\nCalculation has been completed!\nExecution time: {time.time() - start_time:.2f} seconds")
    except Exception as ex:
        print(traceback.format_exc())
