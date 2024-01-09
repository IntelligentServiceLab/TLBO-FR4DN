
import numpy as np

x=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1]
DG=[80,100,87.5,125]
load=[0 ,0.1 ,0.09,    0.12 ,   0.06 ,   0.06 ,   0.2, 0.2 ,0.06 ,   0.06   , 0.045,   0.06,    0.06 ,   0.12   , 0.06  ,
0.06   , 0.06,    0.09 ,   0.09   , 0.09   , 0.09 ,   0.09  ,  0.09    ,0.42  ,  0.42  ,  0.06   , 0.06    ,0.06    ,0.12   ,
0.2 ,0.15 ,   0.21,    0.06]
#节点全部连接返回T
def is_all_nodes_connected(x):
    graph = np.zeros((33, 33))
    for i in range(37):
        if x[i] == 1:
            if i == 17:
                graph[1][i + 1] = 1
                graph[i + 1][1] = 1
            elif i == 21:
                graph[2][i + 1] = 1
                graph[i + 1][2] = 1
            elif i == 24:
                graph[5][i + 1] = 1
                graph[i + 1][5] = 1
            elif i == 32:
                graph[20][7] = 1
                graph[7][20] = 1
            elif i == 33:
                graph[8][14] = 1
                graph[14][8] = 1
            elif i == 34:
                graph[11][21] = 1
                graph[21][11] = 1
            elif i == 35:
                graph[17][32] = 1
                graph[32][17] = 1
            elif i == 36:
                graph[24][28] = 1
                graph[28][24] = 1
            else:
                graph[i][i + 1] = 1
                graph[i + 1][i] = 1
    # Check if all nodes are connected
    num_nodes = len(graph)
    visited = [0] * num_nodes
    stack = [0]  # 使用深度优先搜索（DFS）算法

    while stack:
        node = stack.pop()
        visited[node] = True

        for neighbor in range(num_nodes):
            if graph[node][neighbor] and not visited[neighbor]:
                stack.append(neighbor)

    return all(visited)
#判断有没有回路，有回路返回T
def has_loop(x):
    graph = np.zeros((33, 33))

    for i in range(37):
        if x[i] == 1:
            if i == 17:
                graph[1][i + 1] = 1
                graph[i + 1][1] = 1
            elif i == 21:
                graph[2][i + 1] = 1
                graph[i + 1][2] = 1
            elif i == 24:
                graph[5][i + 1] = 1
                graph[i + 1][5] = 1
            elif i == 32:
                graph[20][7] = 1
                graph[7][20] = 1
            elif i == 33:
                graph[8][14] = 1
                graph[14][8] = 1
            elif i == 34:
                graph[11][21] = 1
                graph[21][11] = 1
            elif i == 35:
                graph[17][32] = 1
                graph[32][17] = 1
            elif i == 36:
                graph[24][28] = 1
                graph[28][24] = 1
            else:
                graph[i][i + 1] = 1
                graph[i + 1][i] = 1
    def has_cycle(node, parent, visited):
        visited[node] = True
        for i in range(len(graph)):
            if graph[node][i] == 1:
                if not visited[i]:
                    if has_cycle(i, node, visited):
                        return True
                elif i != parent:
                    return True
        return False
#拓扑约束
def is_n_equal_to_m_plus_one(x):
    n=33
    m = 0
    for element in x:
        if element == 1:
            m += 1

    if n == m + 1:
        return True
    else:
        return False
#功率约束
def power_constraint(Peqi, PLit, PlossI):
    sum_PLit = sum(PLit)  # 计算L中所有元素的和
    constraint = Peqi - sum_PLit - PlossI  # 计算功率约束
    return constraint
def check_current_constraint(I_ijx, I_ij_max):
    # 检查电流约束是否满足
    if I_ijx <= I_ij_max:
        return True
    else:
        return False

def check_voltage_constraint(U_i_t, U_i_min, U_i_max):
    # 检查电压约束是否满足
    if U_i_min <= U_i_t <= U_i_max:
        return True
    else:
        return False

