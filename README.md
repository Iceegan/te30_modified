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

## TODO: 
Add instructions on how to modify the simulation characteristics,how to run it with different parameters/time steps/lengths of time, and how to use the helper scripts and plotting scripts.