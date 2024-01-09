def recovery_x(solution):
    fx_graphs = np.zeros((33, 33))
    iii = 0
    for node_i in solution:
        #print(node_i)
        if node_i == 1:
            fx_graphs[branch_node[iii][0]][branch_node[iii][1]] = 1
            fx_graphs[branch_node[iii][1]][branch_node[iii][0]] = 1  # 一个33节点矩阵图
        iii = iii + 1
    b = []

    for i in range(100):
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
                            if not compare_rows_with_array(x, [a, b]) and len(a)+3==len(b):
                                x.append([a, b])
                                b = []
                                a = []
                        fx_graphs[:]=new_graphs[:]
        else:
            fx_graphs[:] = new_graphs[:]
    for row in x:
        num_ab = get_nesting_depth(row)
        if num_ab == 2:
            for i in range(len(row)):
                for lenth in range(len(branch_node)):
                    # 比较矩阵
                    if branch_node[lenth] == row[i] or reversed_branch_node[lenth] == row[i]:
                        row[i] = lenth
                        # print("找到了匹配的节点:", row)
                        break
        if num_ab == 3:
            for i in range(len(row)):
                for row_row in row:

                    for j in range(len(row_row)):
                        for lenth in range(len(branch_node)):
                            # 比较矩阵
                            if branch_node[lenth] == row_row[j] or reversed_branch_node[lenth] == row_row[j]:
                                row_row[j] = lenth
                                break
    #print("rd",random_element)
    for ii in range(len(x)):
        random_int = np.random.randint(0, len(x))
        random_element = x[random_int]
        num_ab = get_nesting_depth(random_element)
        sl = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0,
              0, 0, 0, 0]
        if num_ab == 1:
            for i in random_element:
                sl[i]=1
        if num_ab==2:
            for i in range(len(random_element)):
                if  isinstance(random_element[i], list):
                    for j in random_element[i]:
                        if i==0:
                            sl[int(j)]=0
                        elif i==1:
                            sl[int(j)]=1
                else:
                    sl[random_element[i]]=0
        if satisfy_conditions.is_n_equal_to_m_plus_one(sl):
            break
    return sl

#判断整个路径是否全部已连接，全部连接返回True
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
#判断有没有回路,有回路返回True
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
#disconnected_matrix,disconnected_path= disconnect_random_branch(graphs)
#print(find_cycle(graphs))
#for row in disconnected_matrix:
#    print(row)
#print("Disconnected Path:", disconnected_path)


#随机闭合一条联络开关支路
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
#print(compare_last_row_with_array(start_graphs,graphs[-1]))
#从x中分离出a_b
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

