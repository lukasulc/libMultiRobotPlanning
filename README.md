[![Build](https://github.com/whoenig/libMultiRobotPlanning/actions/workflows/build.yml/badge.svg)](https://github.com/whoenig/libMultiRobotPlanning/actions/workflows/build.yml)

# libMultiRobotPlanning

libMultiRobotPlanning is a library with search algorithms primarily for task and path planning for multi robot/agent systems.
It is written in C++(14), highly templated for good performance, and comes with useful examples.

The following algorithms are currently supported:

* Single-Robot Algorithms
  * A*
  * A* epsilon (also known as focal search)
  * SIPP (Safe Interval Path Planning)

* Multi-Robot Algorithms
  * Conflict-Based Search (CBS)
  * Enhanced Conflict-Based Search (ECBS)
  * Conflict-Based Search with Optimal Task Assignment (CBS-TA)
  * Enhanced Conflict-Based Search with Optimal Task Assignment (ECBS-TA)
  * Prioritized Planning using SIPP (example code for SIPP)

* Assignment Algorithms
  * Minimum sum-of-cost (flow-based; integer costs; any number of agents/tasks)
  * Best Next Assignment (series of optimal solutions)

## Building

Tested on Ubuntu 16.04.

```
mkdir build
cd build
cmake ..
make
```

### Targets

* `make`: Build examples, only
* `make docs`: build doxygen documentation
* `make clang-format`: Re-format all source files
* `make clang-tidy`: Run linter & static code analyzer
* `make run-test`: Run unit-tests

## Run specific tests

```
python3 ../test/test_next_best_assignment.py TestNextBestAssignment.test_1by2
```

## Run example instances

### ECBS

````
./ecbs -i ../benchmark/32x32_obst204/map_32by32_obst204_agents10_ex1.yaml -o output.yaml -w 1.3
python3 ../example/visualize.py ../benchmark/32x32_obst204/map_32by32_obst204_agents10_ex1.yaml output.yaml
````

### Generalized Roadmaps

CBS works on generalized graphs, with a particular focus on optional wait actions (e.g., this can be used with motion primitives as well).
However, the roadmap annotation and visualization step currently assume a 2D Euclidean embedding and straight-line edges.

```
python3 ../tools/annotate_roadmap.py ../test/mapf_simple1_roadmap_to_annotate.yaml mapf_simple1_roadmap_annotated.yaml
./cbs_roadmap -i mapf_simple1_roadmap_annotated.yaml -o output.yaml
python3 ../example/visualize_roadmap.py mapf_simple1_roadmap_annotated.yaml output.yaml
```

## Generate maps

Donwload raw maps from: https://movingai.com/benchmarks/mapf/index.html

### Ex. 1
````
mkdir examples/ground/warehouse-10-20-10-2-1
````

standard_benchmark_converter.py
````
python3 libMultiRobotPlanning/example/standard_benchmark_converter.py ../mapf-scen-random/scen-random/warehouse-10-20-10-2-1-random-1.scen ../mapf-map/warehouse-10-20-10-2-1.map "./examples/ground/warehouse-10-20-10-2-1/random-1/"
````

### Ex. 2
This example takes longer to execute but it generates
more examples.

````
mkdir examples/ground/empty-48-48.map
````

auto_convert_benchmarks.py
````
python3 libMultiRobotPlanning/tools/auto_convert_benchmarks.py --scen ../mapf-scen-even/scen-even/ --map ../mapf-map/empty-48-48.map --output_base "./examples/ground/"
````

### Ex. 3
````
EX_PATH=brc202d
````

````
mkdir examples/ground/$EX_PATH
````

````
python3 libMultiRobotPlanning/tools/auto_convert_benchmarks.py --scen ../mapf-scen-even/scen-even/ --map ../mapf-map/$EX_PATH.map --output_base "./examples/ground/" --count 500
````