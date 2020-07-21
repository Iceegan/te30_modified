# Modified TE30 Simulation for use with TRANSAX
This is a Gridlab-D simulation based on a modified version of PNNL's [TE30 model](https://github.com/pnnl/tesp/tree/master/examples/te30) to simulate a small distribution network as a proof of concept for the TRANSAX system. The simulation can run on its own with a generic control strategy, or it can be connected to a RIAPS system in real-time using the FNCS framework.

## Table of Contents

- [Installation Instructions](#installation-instructions)
    - [Requirements](#requirements)
    - [Software and Dependencies](#software-and-dependencies)
        - [ZeroMQ Installation](#zeromq-installation)
        - [CZMQ Installation](#czmq-installation)
        - [FNCS Installation](#fncs-installation)
        - [Xerces-C++ Installation](#xerces-c-installation)
        - [GridLAB-D Installation](#gridlab-d-installation)
        - [ns-3 Installation](#ns-3-installation)
        - [Python and Python Dependencies](#python-and-python-dependencies)
        - [Environment Variables](#environment-variables)
- [Running the Simulation](#running-the-simulation)
- [Installing and Connecting with RIAPS](#installing-and-connecting-with-RIAPS)
- [Modifying the Simulation Parameters](#modifying-the-simulation-parameters)
    - [GridLAB-D Simulation](#gridlab-d-simulation)
    - [FNCS Modifications](#fncs-modifications)
    - [Python Agent Modifications](#python-agent-modifications)


# Installation Instructions
[back to contents](#table-of-contents)

## Requirements
This project was tested and verified in a virtual machine with 64-bit Ubuntu 18.0.4.

## Software and Dependencies
[back to contents](#table-of-contents)

These instructions are a modified version of the instructions provided in the [FNCS Tutorial](https://github.com/FNCS/FNCS-Tutorial/tree/master/demo-gld-ns3) on FNCS with GridLAB-D.

`git` and `build-essential` will need to be installed to perform the following software installations.

```
sudo apt install git

sudo apt install build-essential
```

The following software will need to be installed:

- FNCS
  - ZeroMQ (3.2.x)
  - CZMQ (3.0.x)
- GridLAB-D (ticket 797)
  - Xerces (3.2.3)
  - autoconf (2.63 or better)
  - automake (1.11 or better)
  - libtool (2.2.6b or better)
  - FNCS
- ns-3 (FNCS version based on 3.26)
  - Python (for the waf installer)
  - FNCS

It will be assumed that you will be installing all software into
$HOME/FNCS-install. Doing so will greatly simplify the steps of this
tutorial since we can set $LD_LIBRARY_PATH and $PATH accordingly, as
well as any other needed installation paths while building many of the
involved software packages. In fact, now would be a good time to set a
shortcut environment variable, like so:

```
export FNCS_INSTALL="$HOME/FNCS-install"
```

NOTE: You could, in theory, change this to point to wherever you wish to
install FNCS and all related software packages.

It is also assumed that you are using a Bourne shell; all of the
step-by-step instructions (like the one above) that appear in this
tutorial  will assume a Bourne shell. If you are using a C shell, we
hope you can adapt the steps as needed, mostly in how environment
variables are set.

## ZeroMQ Installation
[back to contents](#table-of-contents)

http://zeromq.org/

Get the ZeroMQ software and install it using the following steps:

```
# we are doing everything from your $HOME directory
cd $HOME

# download zeromq
wget http://download.zeromq.org/zeromq-3.2.4.tar.gz
# if you do not have wget, use
# curl -O http://download.zeromq.org/zeromq-3.2.4.tar.gz

# unpack zeromq, change to its directory
tar -xzf zeromq-3.2.4.tar.gz
cd zeromq-3.2.4

# configure, make, and make install
./configure --prefix=$FNCS_INSTALL
make
make install
```

Congratulations, you have now installed ZeroMQ.

### CZMQ Installation
[back to contents](#table-of-contents)

http://czmq.zeromq.org/

Installing CZMQ is like any other software using configure and make.
The main challenge is specifying the installation location (--prefix)
for CZMQ as well as the location where ZeroMQ was installed.  If you
installed ZeroMQ as written above, the following will work for you.

```
# we are doing everything from your $HOME directory
cd $HOME

# download czmq
wget http://download.zeromq.org/czmq-3.0.0-rc1.tar.gz
# if you do not have wget, use
# curl -O http://download.zeromq.org/czmq-3.0.0-rc1.tar.gz

# unpack czmq, change to its directory
tar -xzf czmq-3.0.0-rc1.tar.gz
cd czmq-3.0.0

# configure, make, and make install
./configure --prefix=$FNCS_INSTALL --with-libzmq=$FNCS_INSTALL

make
make install
```
If the `make` step is producing warnings, you can remove the -werror flags in the makefile so that it will still build even with warnings.

Congratulations, you have now installed CZMQ.

## FNCS Installation
[back to contents](#table-of-contents)

https://github.com/FNCS/fncs

The FNCS software will build and install the FNCS library, the various
FNCS header files, as well as the broker application. The FNCS broker
represents the central server that all other simulator clients will
connect to in order to synchronize in time and exchange messages with
other simulators. The FNCS library and header represent the needed API
for communicating with the broker using the sync and messaging function
calls.

We will need the most recent develop branch of FNCS to work with the Python publishers and subscribers. Get the FNCS software and install it using the following steps:

```
# we are doing everything from your $HOME directory
cd $HOME

# download FNCS
git clone https://github.com/FNCS/fncs

# change to FNCS directory
cd fncs

# checkout the develop branch
git checkout develop

# configure, make, and make install
./configure --prefix=$FNCS_INSTALL --with-zmq=$FNCS_INSTALL
make
make install
```

Congratulations, you have now installed FNCS.

## Xerces-C++ Installation
[back to contents](#table-of-contents)

http://xerces.apache.org/xerces-c/

```
# we are doing everything from your $HOME directory
cd $HOME

# download Xerces-C++ 3.2.3 source code
wget http://apache.mirrors.pair.com//xerces/c/3/sources/xerces-c-3.2.3.tar.gz
# if you do not have wget, use
# curl -O http://apache.mirrors.pair.com//xerces/c/3/sources/xerces-c-3.2.3.tar.gz

# unpack xerces, change to its directory
tar -xzf xerces-c-3.2.3.tar.gz
cd xerces-c-3.2.3

# configure, make, and make install
./configure --prefix=$FNCS_INSTALL
make
make install
```

Congratulations, you have now installed Xerces-C++ and are ready to
install GridLAB-D.

## GridLAB-D Installation
[back to contents](#table-of-contents)

http://www.gridlabd.org/

GridLAB-D is a power distribution system simulator and analysis tool.
Please see its website for complete details.

Currently the only version of GridLAB-D that will compile with FNCS is the develop branch of GridLAB-D on github. https://github.com/gridlab-d/gridlab-d.git.

Get the FNCS version of the GridLAB-D software and install it using the
following steps:

```
# we are doing everything from your $HOME directory
cd $HOME

# download our FNCS-capable version of GridLAB-D
git clone https://github.com/gridlab-d/gridlab-d

# change to FNCS-gridlab-d directory
cd gridlab-d

# checkout the develop branch
git checkout -b develop origin/develop

# run to autotools to generate the configure script and Makefile.in
# templates
# minimum required versions:
# autoconf 2.63
# automake 1.11
# libtool 2.2.6b
autoreconf -fi

# configure, make, and make install
./configure --prefix=$FNCS_INSTALL --with-xerces=$FNCS_INSTALL --with-fncs=$FNCS_INSTALL --enable-silent-rules 'CFLAGS=-g -O0 -w' 'CXXFLAGS=-g -O0 -w' 'LDFLAGS=-g -O0 -w'
make
make install
```

Congratulations, you have now installed GridLAB-D ticket 797.

## ns-3 Installation
[back to contents](#table-of-contents)

http://www.nsnam.org/

ns-3 is a discrete-event network simulator for Internet systems. Please
see their website for complete details.

FNCS added an "application" as a patch to ns-3.26. The application
receives FNCS messages from GridLAB-D and injects them into the network,
and once through the network (if not dropped), sends the FNCS message on
to its intended recipient.

Get the FNCS version of the ns-3 software and install it using the following
steps:

```
# we are doing everything from your $HOME directory
cd $HOME

# download our FNCS version of ns-3
git clone https://github.com/FNCS/ns-3.26

# change to ns-3.26 directory
cd ns-3.26

# the ns-3 install typically uses the compiler flag for
# warnings-as-errors which often broke our ability to build and install
# it, so we recommend the following configure of ns-3
CFLAGS="-g -O2" CXXFLAGS="-g -O2" ./waf configure --prefix=$FNCS_INSTALL --with-fncs=$FNCS_INSTALL --with-zmq=$FNCS_INSTALL --disable-python

# 'make'
./waf build

# install
./waf install
```

Congratulations, you have now installed ns-3.

## Python and Python Dependencies
[back to contents](#table-of-contents)

The `Agent.py` python file was written and works with the following python dependencies:

* Python 3.7.3
* numpy 1.16.4
* pyzmq 18.0.0

## Command Line Utilities
[back to contents](#table-of-contents)

The `run.sh` file uses tmux for easy monitoring of all logs during simulation runtime. To install tmux:
```
sudo apt install tmux
```

## Environment Variables
[back to contents](#table-of-contents)

Several environment variables need to be set for the bash scripts to work properly. Make sure these are correct in `env.sh`:
* Update `FNCS_INSTALL` (line 4) to point to the location where FNCS was installed. This should be the same as the `FNCS_INSTALL` variable set at the beginning of this guide.
* Make sure that the `GLPATH` and `GRIDLABD` variables are correct (lines 23 and 24). They should not need to be changed if the instructions above were followed for installation.

# Running the Simulation
[back to contents](#table-of-contents)

The simulation can be run either with or without RIAPS communication. Recommended to try running without RIAPS to verify correct installation.
### Without RIAPS
1. Set RIAPS=False in `env.sh` (line 29)
2. `cd` to TE30 Directory
1. `./run.sh`

### With RIAPS
1. Set RIAPS=True in `env.sh` (line 29)
1. Run the RIAPS server on port 5555
1. `cd` to TE30 Directory
1. `./run.sh`

# Installing and Connecting with RIAPS
[back to contents](#table-of-contents)
* To Do

# Modifying the Simulation Parameters
[back to contents](#table-of-contents)

The simulation has 3 major parts.
1. `TE_Challenge.glm`, which describes the underlying GridLAB-D model
1. FNCS, which coordinates communication and time synchronization between the Python agent, the GridLAB-D model, and RIAPS
1. `Agent.py`, which runs the main loop of program iteration and data processing.

### GridLAB-D Simulation
[back to contents](#table-of-contents)

The simulated microgrid is described in the GridLAB-D File `TE_Challenge.glm`. The file is organized into sections that describe the feeders, lines, and loads. More information on `glm` files can be found on the [GridLAB-D Website](https://www.gridlabd.org/) or the [GridLAB-D GitHub](https://github.com/gridlab-d).

The helper scripts `generate_batt.py` and `generate_lines.py` can be used to generate the text for any changes to be made to all the batteries or all the overhead lines. Individual changes must be made in `TE_Challenge.glm`.

Changing the length of time for running the simulation requires changes to two parameters.
1. In `TE_Challenge.glm`, the clock object must be modified to the desired start and stop time
1. In `env.sh`, the `hours` variable (line 26) must be modified to be equal to the time difference between start and stop time.

### FNCS Modifications
[back to contents](#table-of-contents)

The FNCS parameters are dictated by two files.
1.  `TE_Challenge_agent.yaml`
    * This describes the GridLAB-D values that can published and subscribed to through FNCS
    * As written, the Python Agent requires values for solar power output, battery power output, and battery charge level to communicate with RIAPS.
1. `TE_Challenge_FNCS_Config.txt`
    * This file defines the publish/subscribe relationships for variables over FNCS

Any modifications to the topology of the circuit in `TE_Challenge.glm` will require changes in the FNCS values and subscriptions. More information on how FNCS works can be found in the [FNCS Tutorial](https://github.com/FNCS/FNCS-Tutorial/tree/master/demo-gld-ns3).

### Python Agent Modifications
[back to contents](#table-of-contents)

The Python Agent, `Agent.py`, contains the application logic for progressing the simulation and, when connected to RIAPS, communicating the simulation state to RIAPS. The `mainLoop` function controls this process. The loop works by repeatedly performing FNCS time requests until the desired simulation time is reached. 

If the simulation is run without RIAPS, the Agent will step through each simulated time step without modifying any parameters. The result of this will depend only on the parameters described in the `TE_Challenge.glm` file.

When run with RIAPS, the agent controls the interface between GridLAB-D and RIAPS. For each loop, the following actions are taken:
1. Collect all events from FNCS and update the battery charge levels, battery power output, and solar panel power output.
1. Check for a 'step' event. Step events are defined by `step.player`, and are what tell the simulation to hold until it communicates with RIAPS. The simulation is by default set to have a step every 15 minutes of simulation time to align with the trading period of the TRANSAX system. The simulation can be paused at a different frequency by modifying `step.player`.
  * If there is a step event, call the `chargeResp` and `tradeResp` functions to communicate with RIAPS before continuing the simulation.
  * If there is not a request, the simulation will continue until it reaches a step event to wait for commands from RIAPS.

# Plotting Tools
The `Plotting_Scripts/` directory contains 3 Python scripts that are useful for visualizing the general results of each simulation. These tools require `matplotlib` for Python.
1. `Plot_Batt_Charge.py`: this script will plot the average battery charge over the time of the simulation. It is useful to show how the batteries are being utilized by the simulation control parameters. It takes an argument to the directory with the battery charge output csv.
  * ex. `python3 Plotting_Scripts/Plott_Batt_Charge.py Results`
1. `Plot_Sub_Load_.py`: this script will plot the load on the substation over the time of the simulation. It is useful to show the net load on the grid during the simulation. It takes an argument to the directory with the power output csv.
  * ex. `python3 Plotting_Scripts/Plott_Sub_Load.py Results`
1. `Sub_Load_Comparison.py`: this script plots the substation load for two runs of the simulation. It is useful for comparing how different control parameters result in different amounts of grid load, or in comparing how the simulation responds with and without TRANSAX control. To use this script, the simulation must be run twice. After running the first simulation, copy the results into a saved directory since the files in `Results/` will be overwritten when the simulation is re-run. It takes an argument to the two directories with results. By default the first argument is labeled "Traditional" and the second is labeled "With Transax". These labels can be changed on line 30.
  * ex. `python3 Plotting_Scripts/Sub_Load_Comparison.py Experiment1_Results Experiment2_Results`


<!---
# Helper Scripts
There are several helper scripts that make it easier to set up and run this simulation, located in the `Helper Scripts/` Directory. These files are for quickly generating the required text for the simulation network, however fine tuning differences between each modeled house, battery, solar panel, and overhead line will require manual modification of the helper script outputs.
1. `create_events.py`: This script will create the `step.player` file. `step_size` and `final_step` can be modified to change how long the simulation runs and how frequently it pauses for communication with RIAPS.
1. `generate_batt.py`and `generate_lines.py`: these scripts will generate text files that can be copied and pasted into `TE_Challenge.glm`. They are useful for quickly modifying the names, power ratings, and phases of the overhead lines and batteries between houses in the simulation.
1. `generate_FNCS.py`: this file can be quickly used to generate the FNCS publishers and subscribers. The output text file can be copied into
-->