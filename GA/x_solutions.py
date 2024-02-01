for line in f0.readlines():
    if line[0] == '#':
        continue
    if line[:2] == "-1":
        break
    RX[int(line.split(' ')[0]) - 1][0] = int(line.split(' ')[1]) - 1
    RX[int(line.split(' ')[0]) - 1][1] = int(line.split(' ')[2]) - 1

switch_line=[[20,7],
    [8,14],
    [11,21],
    [17,32],
    [24,28]]
edges = np.concatenate((RX, switch_line), axis=0)
NODE_COPY_n=edges.astype(int)
branch_node=[[ 0 ,1],[ 1 ,2],[ 2 , 3], [ 3, 4], [ 4, 5], [ 5, 6], [ 6, 7], [ 7, 8], [ 8, 9], [ 9,10], [10,11], [11,12],
             [12,13], [13,14], [14,15], [15,16], [16,17], [ 1,18], [18,19], [19,20], [20,21], [ 2,22], [22,23], [23,24],
             [ 5,25],[25,26], [26,27], [27,28], [28,29], [29,30], [30,31],[31,32],[20, 7],[ 8,14],[11,21],[17,32],[24,28]]
reversed_branch_node = [[ 1 , 0], [ 2 , 1], [ 3 , 2], [ 4 , 3], [ 5 , 4], [ 6 , 5], [ 7 , 6], [ 8 , 7], [ 9 , 8], [10 , 9],
                        [11 ,10], [12 ,11], [13 ,12], [14 ,13], [15 ,14], [16 ,15], [17 ,16], [18 , 1], [19 ,18], [20 ,19],
                        [21 ,20], [22 , 2], [23 ,22], [24 ,23], [25 , 5], [26 ,25], [27 ,26], [28 ,27], [29 ,28], [30 ,29],
                        [31 ,30], [32 ,31], [ 7 ,20], [14  ,8], [21 ,11], [32, 17], [28 ,24]]
graphs=[[0] * 33 for _ in range(33)]
for node_i in range(37):
    node1=int(edges[node_i][0])
    node2=int(edges[node_i][1])
    graphs[node1][node2] = 1
    graphs[node2][node1] = 1  #一个33节点矩阵图
graphs[20][7]=0
graphs[7][20]=0
graphs[8][14]=0
graphs[14][8]=0
graphs[11][21]=0
graphs[21][11]=0
graphs[17][32]=0
graphs[32][17]=0
graphs[24][28]=0
graphs[28][24]=0
graphs[9][10]=0
graphs[10][9]=0
graphs[25][26]=0
graphs[26][25]=0
graphs[28][29]=0
graphs[29][28]=0
#for row in graphs:
#    print(row)
start_graphs=copy.deepcopy(graphs)
x=[]
def find_x(fx_graphs):
    b = []
    for i in range(3000):
        a = []
        new_graphs = copy.deepcopy(graphs)
        if not is_all_nodes_connected(fx_graphs):
            c = toggle_switch(switch_line,fx_graphs)
            if not compare_rows_with_array(b,c):
                b.append(c)
            if not is_all_nodes_connected(fx_graphs):
                continue
            else:
                if not has_loop(fx_graphs):
                    if is_all_nodes_connected(fx_graphs):
                        if not compare_rows_with_array(x, b):
                            x.append(b)
                            b = []
                        fx_graphs[:]=new_graphs[:]
                while has_loop(fx_graphs):
                    fx_graphs,d=disconnect_random_branch(fx_graphs)
                    if not compare_rows_with_array(a,d) and any(d):
                        a.append(d)
                    if not has_loop(fx_graphs):
                        if is_all_nodes_connected(fx_graphs):
                            if not compare_rows_with_array(x, [a, b]) and (len(a)+3)==len(b):
                                x.append([a, b])

                                #disconnect_toggle_switch(b,fx_graphs)  # 断开所有闭合的联络开关

                                b = []
                                a = []
                        fx_graphs[:]=new_graphs[:]
        else:
            fx_graphs[:] = new_graphs[:]

    return x

#判断整个路径是否全部已连接
def is_all_nodes_connected(graph):
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
#print(is_all_nodes_connected(graphs))
#判断有没有回路
def has_loop(graphs):
    def has_cycle(node, parent, visited):
        visited[node] = True
        for i in range(len(graphs)):
            if graphs[node][i] == 1:
                if not visited[i]:
                    if has_cycle(i, node, visited):
                        return True
                elif i != parent:
                    return True
        return False

    # 遍历图中的每个节点，看是否存在回路
    n = len(graphs)
    visited = [False] * n

    for i in range(n):
        if not visited[i]:
            if has_cycle(i, -1, visited):
                return True
                break
    else:
        return False
#返回回路中的每一个节点
def find_cycle(adj_matrix):
    n = len(adj_matrix)
    visited = [False] * n
    path = []

    def dfs(node, parent):
        visited[node] = True
        for neighbor in range(n):
            if adj_matrix[node][neighbor]:
                if not visited[neighbor]:
                    if dfs(neighbor, node):
                        # 找到回路了，将当前节点加入到path列表中
                        path.append(node)
                        return True
                elif neighbor != parent:
                    # 找到回路了，将当前节点加入到path列表中
                    path.append(node)
                    return True
        return False

    for i in range(n):
        if not visited[i]:
            if dfs(i, -1):
                break

    return path
#随机选择回路中的一个支路断开
def disconnect_random_branch(adj_matrix):
    cycle = find_cycle(adj_matrix)
    if not cycle:
        return adj_matrix

    # 选择一条路径
    path_index = random.randint(0, len(cycle) - 1)
    disconnect_point = cycle[path_index]
    disconnected_path = []
    # 断开路径的支路
    disconnected_adj_matrix = adj_matrix.copy()
    for i in range(path_index, len(cycle) - 1):
        node = cycle[i]
        next_node = cycle[i+1]
        if node == disconnect_point or next_node == disconnect_point:
            # 断开该点在路径上的边
            disconnected_adj_matrix[node][next_node] = 0
            disconnected_adj_matrix[next_node][node] = 0
            disconnected_path.append(node)
            disconnected_path.append(next_node)
            break
        else:
            # 断开路径中两个节点之间的边
            disconnected_adj_matrix[node][next_node] = 0
            disconnected_adj_matrix[next_node][node] = 0
            disconnected_path.append(node)
    return disconnected_adj_matrix,disconnected_path

def toggle_switch(switch_line,ts_graphs):
    # 随机选择一个连接开关
    selected_switch = random.choice(switch_line)
    #print(selected_switch)

    while True:
        # 切换连接开关的状态
        if ts_graphs[int(selected_switch[0])][int(selected_switch[1])] == 0 and ts_graphs[int(selected_switch[1])][int(selected_switch[0])] == 0:
            ts_graphs[int(selected_switch[0])][int(selected_switch[1])] = 1
            ts_graphs[int(selected_switch[1])][int(selected_switch[0])] = 1
        else:
            break
    return selected_switch
#把随机闭合的联络开关断开
def disconnect_toggle_switch(switch,dts_graphs):
    # 随机选择一个连接开关

    for row in switch:
        # 切换连接开关的状态
        if dts_graphs[int(row[0])][int(row[1])] == 1 and dts_graphs[int(row[1])][int(row[0])] == 1:
            dts_graphs[int(row[0])][int(row[1])] = 0
            dts_graphs[int(row[1])][int(row[0])] = 0
        else:
            break
#用矩阵的最后一行与一个一维列表比较，相同返回True，不同返回False
def compare_rows_with_array(matrix, array):
    num_rows = len(matrix)

    if num_rows == 0:
        return False

    for row in matrix:
        if row == array:
            return True

    return False

def get_nesting_depth(lst):
    if not isinstance(lst, list):
        return 0
    return 1 + max(get_nesting_depth(item) for item in lst)
def separate_a_b(the_x):
    for row in the_x:
        num_ab=get_nesting_depth(row)
        if num_ab==2:
            b=row
        if num_ab==3:
            a=row[0]
            b=row[1]
population=[[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [
                1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [
                1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
             1]
            ]






