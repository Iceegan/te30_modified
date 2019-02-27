# Modified TE30 Example

This is a modified version of the TE30 example provided for TESP.
The modifications include these files:
- *testRun.bat*; Windows batch file that runs the modified TEAgent
- *testAgent.py*; Python file with the modified TEAgent for the Example
- *reset.bat*; Windows batch file that deletes all outputs and logs and kills the currently running smiulations.

To run the simulation, TESP must be installed according to the instructions here:
https://github.com/pnnl/tesp/tree/master/examples/te30

The directory of this simulation should be placed in TESP_INSTALL/examples/

The details of the original TE30 example can be found here:
https://github.com/pnnl/tesp/tree/master/examples/te30

## Running Simulations
To run and plot a case with the testAgent, from the Terminal:

1. `python prepare_case.py`
2. `testRun` (Windows)
3. `python plots.py TE_Challenge`

Before restarting a simulation, run *reset.bat* to kill existing processes and clear logs.
