# Modified TE30 Simulation for use with TRANSAX
This is a Gridlab-D simulation based on a modified version of PNNL's [TE30 model](https://github.com/pnnl/tesp/tree/master/examples/te30) to simulate a small distribution network as a proof of concept for the TRANSAX system. The simulation can run on its own with a generic control strategy, or it can be connected to a RIAPS system in real-time using the FNCS framework.

# Installation Instructions
1. Install [FNCS](https://github.com/FNCS/fncs) and [Gridlab-D](http://gridlab-d.shoutwiki.com/wiki/Installation_Guide)
    * The [FNCS Tutorial](https://github.com/FNCS/FNCS-Tutorial/tree/master/demo-gld-ns3) offers instructions on how to install the two programs together
1. Update `env.sh`
    * Update `FNCS_INSTALL` (line 4) to point to the location where FNCS was installed
    * Make sure that the `GLPATH` and `GRIDLABD` variables are correct (lines 23 and 24) 

# Running the Simulation
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
* To Do

# Modifying the Simulation Parameters
The simulation has 3 major parts.
1. `TE_Challenge.glm`, which describes the underlying GridLAB-D model
1. FNCS, which coordinates communication and time synchronization between the Python agent, the GridLAB-D model, and RIAPS
1. `Agent.py`, which runs the main loop of program iteration and data processing.

### GridLAB-D Simulation
The simulated microgrid is described in the GridLAB-D File `TE_Challenge.glm`. The file is organized into sections that describe the feeders, lines, and loads. More information on `glm` files can be found on the [GridLAB-D Website](https://www.gridlabd.org/) or the [GridLAB-D GitHub](https://github.com/gridlab-d).

The helper scripts `generate_batt.py` and `generate_lines.py` can be used to generate the text for any changes to be made to all the batteries or all the overhead lines. Individual changes must be made in `TE_Challenge.glm`.

Changing the length of time for running the simulation requires changes to two parameters.
1. In `TE_Challenge.glm`, the clock object must be modified to the desired start and stop time
1. In `env.sh`, the `hours` variable (line 26) must be modified to be equal to the time difference between start and stop time.

### FNCS Modifications
The FNCS parameters are dictated by two files.
1.  `TE_Challenge_agent.yaml`
    * This describes the GridLAB-D values that can published and subscribed to through FNCS
    * As written, the Python Agent requires values for solar power output, battery power output, and battery charge level to communicate with RIAPS.
1. `TE_Challenge_FNCS_Config.txt`
    * This file defines the publish/subscribe relationships for variables over FNCS

Any modifications to the topology of the circuit in `TE_Challenge.glm` will require changes in the FNCS values and subscriptions. More information on how FNCS works can be found in the [FNCS Tutorial](https://github.com/FNCS/FNCS-Tutorial/tree/master/demo-gld-ns3).

### Python Agent Modifications


## TODO: 
Add instructions on how to modify the simulation characteristics,how to run it with different parameters/time steps/lengths of time, and how to use the helper scripts and plotting scripts.