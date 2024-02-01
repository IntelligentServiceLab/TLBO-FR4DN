
def fitness_loss(x):
    # 33节点信息
    t = 33
    l = 32
    b=[]
    # 前推回代的潮流

    a=[]
    PQ = np.zeros((t, 2))
    V = np.ones(t, complex)
    RX = np.zeros((l, 4))
    UB = 12.66  # 电压基准
    SB = 10  # 功率基准
    ZB = UB * UB / SB  # 阻抗基准
    A0=np.transpose(A0_)
    A0T=np.transpose(A0)
    switch_line=[[20,7,2,2],
        [8,14,2,2],
        [11,21,2,2],
        [17,32,0.5,0.5],
        [24,28,0.5,0.5]]
    NODE_n = np.concatenate((RX, switch_line), axis=0)
    NODE_COPY_n=NODE_n
    init_Node=NODE_n
    #print(init_Node)
    S = np.zeros(t, complex)
    ZL = np.zeros(t, complex)
    IL = np.zeros(t, complex)
    ZL[0] = 0
    for i in range(t):
        S[i] = complex(-PQ[i][0], -PQ[i][1])  # 复数功率
    for i in range(l):
        ZL[i + 1] = complex(RX[i][2], RX[i][3])
        #print(ZL)
    V[0] = 1
    IL[t - 1] = -np.conjugate(S[t - 1] / V[t - 1])  # 支路电流
    max_error = 1  # 迭代误差
    TempV = V
    Vangle = np.zeros((t, 2))
    # 潮流计算
    # print(FT)
    for i in range(len(x)):
        if x[i]==0:
            NODE_n[i, :] = 0
        elif x[i]==1:
            NODE_n[i,:]=NODE_COPY_n[i,:]
    k = 0
    while max_error > 0.0001:
        k += 1
        IN = np.conjugate(S / V)  # 节点注入电流
        for i in range(l):

            IL[l - i - 1] = A0[l - i - 1, l - i:] @ IL[l - i:] - IN[l - i - 1]  # python的矩阵乘法要换成@号
            #print(IL)
        for j in range(1, t):
                # 电压前推过程
                # print(A0T[i,:i]*V[:i]-ZL[i]*IL[i]);
            V[j] = A0T[j, :j] @ V[:j] - ZL[j] * IL[j]
        max_error = max(abs(V - TempV))
        TempV = V  # 记忆迭代结果
    Vangle[:, 0] = abs(V)
    for i in range(t):
        Vangle[i, 1] = cmath.phase(V[i]) / 3.1415 * 180
        #print(Vangle)  # 节点电压和相角
    sumF_loss=0
        #功率损耗
    #print(NODE_n)
    for n in range(36):
        if np.all(NODE_n[n,:]==0):
            continue
        else:
             F_loss=(Vangle[int(NODE_n[n][1])][0]-Vangle[int(NODE_n[n][0])][0])**2/NODE_n[n][2]
             sumF_loss=sumF_loss+F_loss
    return sumF_loss
    def fitness_switch(self, solution):
        different_count = np.sum(population_start != solution)
        return different_count





