## TLBO-FR4DN
Teaching Learning Based Optimization Algorithm for Fault Recovery of Distribution Network with Distributed Genaration

## [Dataset: IEEE33-node system](IEEE33-node-system.md)
- **Table 1**: IEEE33 node data
- **Table 2**: IEEE33 node voltage
- **Table 3**: IEEE33 node load

<div align=center><img width="513" height="240" src="images/modified IEEE33-node system.png"/> <br> Modified IEEE33-node distribution system</div>  

## [Other Data Description](other-data-description.md)
- **Table 1**: Daily power demand of different types of loads
- **Table 2**: Node load recovery priority factor
- **Table 3**: Distributed DG Power
- **Table 4**: Node load at 13:00 and 19:00
- **Table 5**: Node load type
- **Table 6**: Importance level of node

## Use of Source Code
### [GA](GA)
- island.py
  - Function: This file aims to recover the first phase of power grid restoration strategy, and divide the power grid into islands.
  - Input: Fault network information
  - Output: Power grid after the first phase of restoration

- base_on_tulun.py
  - Function: This file aims to modify and improve an infeasible solution, and output a feasible solution which is called by pso.py.
  - Input: Infeasible solution
  - Output: A feasible solution
  
- fitness.py
  - Function: his file aims to calculate the network loss objective function of the power grid, and output the network loss, which is called by pso.py.
  - Input: Power grid information
  - Output: Objective function

- ga.py
  - Function: This file aims to perform genetic algorithm calculation on the power grid to obtain the optimal solution. It is the main function file that calls other files.
  - Input: Fault network information
  - Output: Feasible solution

- satisfy_condition.py
  - Function: This file aims to impose some constraint conditions on the power grid, and constrain the power grid in terms of current, voltage and topology. It is called by pso.py.
  - Input: Power grid information
  - Output: Returns a boolean value
  
- x_solution.py
  - Function: Calculates the initial population for the fault network and is called by pso.py.
  - Input: Power grid information
  - Output: Produces initial population
  
### PSO
- island.py
  - Function: This file aims to recover the first phase of power grid restoration strategy, and divide the power grid into islands.
  - Input: Fault network information
  - Output: Power grid after the first phase of restoration

base_on_tulun.py
  - Function: This file aims to modify and improve an infeasible solution, and output a feasible solution which is called by pso.py.
  - Input: Infeasible solution
  - Output: A feasible solution
  
- fitness.py
  - Function: This file aims to calculate the network loss objective function of the power grid, and output the network loss, which is called by pso.py.
  - Input: Power grid information
  - Output: Objective function

- pso.py
  - Function: This file aims to perform particle swarm algorithm calculation on the power grid to obtain the optimal solution. It is the main function file that calls other files.
- Input: Fault network information
- Output: Feasible solution

- satisfy_condition.py
  - Function: This file aims to impose some constraint conditions on the power grid, and constrain the power grid in terms of current, voltage and topology. It is called by pso.py.
  - Input: Power grid information
  - Output: Returns a boolean value
  
- x_solution.py
  - Function: Calculates the initial population for the fault network and is called by pso.py.
  - Input: Power grid information
  - Output: Produces initial population
  
### TLBO
- island.py
  - Function: This file aims to recover the first phase of power grid restoration strategy, and divide the power grid into islands.
  - Input: Fault network information
  - Output: Power grid after the first phase of restoration

- base_on_tulun.py
  - Function: This file aims to modify and improve an infeasible solution, and output a feasible solution which is called by pso.py.
  - Input: Infeasible solution
  - Output: A feasible solution
  
- fitness.py
  - Function: This file aims to calculate the network loss objective function of the power grid, and output the network loss, which is called by pso.py.
  - Input: Power grid information
  - Output: Objective function

- main.py
  - Function: This file aims to perform TLBO algorithm calculation on the power grid to obtain the optimal solution. It is the main function file that calls other files.
  - Input: Fault network information
  - Output: Feasible solution
  
- satisfy_condition.py
  - Function: This file aims to impose some constraint conditions on the power grid, and constrain the power grid in terms of current, voltage and topology. It is called by pso.py.
  - Input: Power grid information
  - Output: Returns a boolean value
  
- x_solution.py
  - Function: Calculates the initial population for the fault network and is called by pso.py.
  - Input: Power grid information
  - Output: Produces initial population
  
## Experimental Results
### Island division result at time period 13:00 
<div align=center><img width="513" height="240" src="images/island division at 13.png"/></div>  

### Island division result at time period 19:00 
<div align=center><img width="513" height="240" src="images/island division at 19.png"/></div>  

### Fault recovery scheme at time period 13:00 
<div align=center><img width="513" height="240" src="images/recovery echeme at 13.png"/></div>  

### Fault recovery scheme at time period 19:00 
<div align=center><img width="513" height="240" src="images/recovery echeme at 19.png"/></div>  
