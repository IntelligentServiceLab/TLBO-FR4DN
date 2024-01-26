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
### GA
- Input:
- Output:
### PSO
- Input:
- Output:
### TLBO
- Input:
- Output:
## Experimental Results
### Island division result at time period 13:00 
<div align=center><img width="513" height="240" src="images/island division at 13.png"/></div>  

### Island division result at time period 19:00 
<div align=center><img width="513" height="240" src="images/island division at 19.png"/></div>  

### Fault recovery scheme at time period 13:00 
<div align=center><img width="513" height="240" src="images/recovery echeme at 13.png"/></div>  

### Fault recovery scheme at time period 19:00 
<div align=center><img width="513" height="240" src="images/recovery echeme at 19.png"/></div>  

## TLBO文件说明

island:该文件旨在对电网恢复策略第一阶段进行恢复，对电网进行孤岛划分;

base_on_tulun:该文件旨在对无法实施的解决方案进行修正和改进，输出一个可行解，被pso.py所引用;

fitness.py:该文件旨在对电网的网络损耗目标函数进行计算，输出网络损耗，被pso.py锁引用;

main:该文件旨在对电网进行TLBO算法计算，得出最优解，主函数文件，调用其他文件;

satisfy_condition:该文件旨在对电网进行一些约束条件，在电流电压和拓扑方面对电网进行约束，被pso.py锁引用;

x_solution:对故障电网计算，产生初始种群被pso.py锁引用;

## PSO文件说明

island:该文件旨在对电网恢复策略第一阶段进行恢复，对电网进行孤岛划分;

base_on_tulun:该文件旨在对无法实施的解决方案进行修正和改进，输出一个可行解，被pso.py所引用;

fitness.py:该文件旨在对电网的网络损耗目标函数进行计算，输出网络损耗，被pso.py锁引用;

pso:该文件旨在对电网进行粒子群算法计算，得出最优解，主函数文件，调用其他文件;

satisfy_condition:该文件旨在对电网进行一些约束条件，在电流电压和拓扑方面对电网进行约束，被pso.py锁引用;

x_solution:对故障电网计算，产生初始种群被pso.py锁引用;
