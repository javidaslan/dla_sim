## DLA for Python3

### Run grow_v2.py

~~~
usage: grow_v2.py [-h] -r REPLICATIONS -p PARTICLES

optional arguments:
  -h, --help            show this help message and exit
  -r REPLICATIONS, --replications REPLICATIONS
                        Number of replications
  -p PARTICLES, --particles PARTICLES
                        Number of pivot points
~~~


### Run dq_v2.py

~~~
usage: dq_v2.py [-h] -r REPLICATIONS -p PIVOTS -d DISTANCE_RANGE DISTANCE_RANGE -q Q_RANGE Q_RANGE

optional arguments:
  -h, --help            show this help message and exit
  -r REPLICATIONS, --replications REPLICATIONS
                        Number of replications
  -p PIVOTS, --pivots PIVOTS
                        Number of pivot points
  -d DISTANCE_RANGE DISTANCE_RANGE, --distance-range DISTANCE_RANGE DISTANCE_RANGE
                        Distance range, insert 2 numbers as start and end of range
  -q Q_RANGE Q_RANGE, --q-range Q_RANGE Q_RANGE
                        q range, insert 2 numbers as start and end of range
~~~