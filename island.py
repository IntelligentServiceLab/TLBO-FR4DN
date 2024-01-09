def get_matching_indexes(list1, list2):
    matching_indexes = []
    for i, element in enumerate(list2):
        if element in list1:
            matching_indexes.append(i)
    return matching_indexes
def bfs_search(matrix, visited, start_node):
    # 定义搜索队列
    search_queue = deque()

    # 将起点加入搜索队列
    search_queue.append(start_node)
    visited[start_node] = True

    # 定义孤岛范围列表
    island_range = [start_node]

    # 开始搜索
    while search_queue:
        # 弹出队首节点
        current_node = search_queue.popleft()

        # 遍历所有相邻节点
        for i in range(len(matrix[current_node])):
            if matrix[current_node][i] != 0 and not visited[i]:
                # 如果相邻节点未被访问过且有连边，则将其加入搜索队列
                search_queue.append(i)
                visited[i] = True

                # 将相邻节点加入孤岛范围列表
                island_range.append(i)

    return island_range

def get_islands(matrix, root_nodes):
    # 初始化visited数组
    visited = [False] * len(matrix)

    # 定义孤岛列表
    islands = []

    # 遍历所有根节点
    for root_node in root_nodes:
        # 如果该节点未被访问过，则进行BFS搜索
        if not visited[root_node]:
            island_range = bfs_search(matrix, visited, root_node)
            islands.append(island_range)

    return islands
def get_leaf_nodes(matrix, start_node):
    # 定义搜索队列和访问数组
    search_queue = deque()
    visited = [False] * len(matrix)

    # 将起点加入搜索队列和访问数组
    search_queue.append(start_node)
    visited[start_node] = True

    # 定义末端节点列表
    leaf_nodes = []

    # 开始搜索
    while search_queue:
        # 弹出队首节点
        current_node = search_queue.popleft()

        # 判断当前节点是否为末端节点
        is_leaf_node = True
        for i in range(len(matrix[current_node])):
            if matrix[current_node][i] != 0 and not visited[i]:
                # 如果相邻节点未被访问过且有连边，则将其加入搜索队列和访问数组
                search_queue.append(i)
                visited[i] = True
                is_leaf_node = False

        # 如果当前节点是末端节点，则将其加入末端节点列表
        if is_leaf_node:
            leaf_nodes.append(current_node)

    return leaf_nodes
def dfs_traverse(matrix, visited, current_node, target_value, node_data, current_sum, path):
    path.append(current_node)

    if current_sum <= target_value:
        visited[current_node] = True
        if current_sum == target_value:
            return True

        for i in range(len(matrix[current_node])):
            if matrix[current_node][i] != 0 and not visited[i]:
                if dfs_traverse(matrix, visited, i, target_value, node_data, current_sum, path):
                    return True

        visited[current_node] = False


    return False


def find_target_value(matrix, node_data, target_value, root):
    num_nodes = len(matrix)
    visited = [False] * num_nodes
    path = []

    if dfs_traverse(matrix, visited, root, target_value, node_data, 0, path):
        return True, path

    return False, path
def calculate_f1(L, lambdas, P, y):
    f1 = 0
    for i in L:
        t = i.t
        f1 += lambdas[t] * P[L] * y[L][t]
    return f1
def cut_node(graphs,root_node):

    result = get_islands(graphs, root_node)
    for i in range(len(result)):
        sum_node = 0

        for j in range(len(result[i])):
            sum_node=sum_node+load2[result[i][j]]
        DG_node=get_matching_indexes(result[i],root_node)

        sum_DG=0
        for node in range(len(get_matching_indexes(result[i],root_node))):

            sum_DG=sum_DG+DG[DG_node[node]]

        while sum_DG<sum_node:

            leaf_node=get_leaf_nodes(graphs,root_node[DG_node[0]])
            if 0 in leaf_node:
                leaf_node.remove(0)
            min_node=leaf_node[0]

            min_value=lambs2[leaf_node[0]]

            for node in range(len(leaf_node)):
                if lambs2[leaf_node[node]] < min_value:
                    min_value = lambs2[leaf_node[node]]
                    min_node=leaf_node[node]

            print("min",min_node)
            if min_node<root_node[DG_node[0]]:
                graphs[min_node][min_node+1]=0
                graphs[min_node+1][min_node] = 0
            else:
                graphs[min_node][min_node-1]=0
                graphs[min_node-1][min_node] = 0

            sum_node=sum_node-load2[min_node]
            if sum_DG>=sum_node:
                break

    return get_islands(graphs,root_node)

island = cut_node(graphs,root_node)
