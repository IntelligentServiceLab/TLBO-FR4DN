
fault_branch=[9,25,28]
population_start=[1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,0,0,0,0,0]#故障信息
solution=[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0]
sl=solution
task_number=37
population_size=50
iteration_number=100
bounds = np.vstack((np.ones(37), np.zeros(37)))
min_max_fit_loss=[0,284.880152]
min_max_fit_switch=[0,7]
C1=0.7
C2=0.3
class PSO():
    """粒子群算法"""

    def __init__(self, population_x, task_number, population_size, iteration_number, bounds,fault_branch):

        self.w = 0.7  # w为惯性因子
        self.c1 = 1.5
        self.c2 = 1.5  # c1, c2为学习因子，一般取1.5
        self.bounds = bounds  # 位置的边界
        self.population_x = population_x  # 初始种群
        self.task_number = task_number  # 任务数
        self.population_size = population_size  # 种群规模(粒子数量)
        self.iteration_number = iteration_number  # 迭代次数
        self.fault_brach = fault_branch  # 故障支路
    def initialization(self, populathion_x):
        """初始化阶段:根据种群规模，生成相应个数的个体（服务组合解）;
        通过为每个任务随机挑选候选服务来初始化一个组合服务"""
        population = self.population_x  # 种群
        return population

    def initialization_V(self, Vmin, Vmax):
        """
            初始化解的 速度
        """
        population_V = []  # 速度
        for i in range(0, self.population_size):
            temp = np.zeros(37)

            for j in range(0, self.task_number):
                temp[j] = random.uniform(Vmin[j], Vmax[j])

            population_V.append(temp)

        return population_V

    def get_Vmax(self, bounds):
        """获取速度的上下界"""
        Vmax = []  # 每个任务的速度上界
        # 速度的上界
        for i in range(self.task_number):

            temp = 1 * (bounds[0][i])
            Vmax.append(temp)

        return Vmax

    def get_Vmin(self, bounds):
        """获取速度的上下界"""
        Vmin = []  # 每个任务的速度下界
        for i in range(self.task_number):

            temp = (-1) * (bounds[0][i])
            Vmin.append(temp)
        return Vmin

    def min_max_turnone(self,fitness, min_value, max_value):
        normalized_value = (fitness - min_value) / (max_value - min_value)
        return normalized_value
    def total_fitness(self,fit_loss,fit_switch):
        total_fit=0
        total_fit=C1*self.min_max_turnone(fit_loss,min_max_fit_loss[0],min_max_fit_loss[1])+C2*self.min_max_turnone(fit_switch,min_max_fit_loss[0],min_max_fit_loss[1])
        return total_fit
    def update_X(self, pop_X, pop_V):
        """更新位置pop_X是一个种群，相当于population_x"""

        new_pop_X = []  # 种群更新后的位置
        for i in range(0, self.population_size):
            y=[]
            new_X = np.zeros(37)
            #print(i)
            #print("ppp=",pop_V[i])
            for j in range(0, self.task_number):
                new_X[j] = pop_X[i][j] + pop_V[i][j]

                # 判断是否越上界
                if new_X[j] >= 0.5:
                    new_X[j] = 1

                # 判断是否越下界
                if new_X[j] < 0.5:

                    new_X[j] = 0
            new_pop_X.append(new_X)
            #print("n",new_pop_X)

        return new_pop_X

    def update_V(self, pop_X, pop_V, pbest, gbest, Vmin, Vmax):
        """更新速度"""
        new_pop_V = []  # 种群更新后的速度
        newnew_pop_V=[]
        for i in range(0, self.population_size):
            new_pop_V = []

            for j in range(0, self.task_number):
                r1 = random.random()

                r2 = random.random()
                speed = self.w * pop_V[i][j] + self.c1 * r1 * (pbest[i][j] - pop_X[i][j]) + self.c2 * r2 * (
                        gbest[j] - pop_X[i][j])

                # 判断是否越上界
                if speed > Vmax[j]:
                    speed = Vmax[j]

                # 判断是否越下界
                if speed < Vmin[j]:
                    speed = Vmin[j]


                new_pop_V.append(speed)


            #print("nnnn",new_pop_V)
            newnew_pop_V.append(new_pop_V)
        return newnew_pop_V

    def save_pbest(self, pbest, pop_X,teacher):
        """更新个体历史最优"""
        updated_pbest = []
        for i in range(self.population_size):
            solution = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
                        0, 0, 0, 0, 0]
            # 如果新解支配旧解
            if self.total_fitness(fitness_loss(pop_X[i]),self.fitness_switch(pop_X[i]))<self.total_fitness(fitness_loss(pbest[i]),self.fitness_switch(pbest[i])) and satisfy_conditions.is_n_equal_to_m_plus_one(pop_X[i]):
                updated_pbest.append(pop_X[i])

                continue
            if teacher == pbest[i]:
                updated_pbest.append(pbest[i])
                continue
            if not satisfy_conditions.is_n_equal_to_m_plus_one(pop_X[i]) :
                y=base_on_tulun.recovery_x(pop_X[i])
                updated_pbest.append(y)
                continue
            else:
                y = base_on_tulun.recovery_x(solution)
                updated_pbest.append(y)
        return updated_pbest

    def save_gbest(self, population):
        """更新种群历史最优"""
        min = 0
        for i in range(0, self.population_size):
            if self.total_fitness(fitness_loss(population[min]),
                                  self.fitness_switch(population[min])) > self.total_fitness(
                    fitness_loss(population[i]),
                    self.fitness_switch(population[i])) and satisfy_conditions.is_n_equal_to_m_plus_one(population[i]):
                min = i


        return population[min]

    def sigmoid(self,V):
        return 1 / (1 + np.exp(-V))
    def find_teacher(self, population):
        """找到种群中的老师(Pareto解集)"""

        min = 0
        for i in range(0, self.population_size):
            if self.total_fitness(fitness_loss(population[min]),self.fitness_switch(population[min]))>self.total_fitness(fitness_loss(population[i]),self.fitness_switch(population[i]))and satisfy_conditions.is_n_equal_to_m_plus_one(population[i]):
                min = i


        return population[min]

    def fitness_switch(self, solution):
        different_count = np.sum(population_start != solution)
        return different_count

    def update(self, old_group, new_group):
        """这个函数用来更新种群:若新解支配旧解，则替换;否则保留"""

        updated_group = []
        for i in range(self.population_size):
            # 如果新解支配旧解
            if self.total_fitness(fitness_loss(new_group[i]), self.fitness_switch(new_group[i])) < self.total_fitness(
                    fitness_loss(old_group[i]), self.fitness_switch(old_group[i])) and new_group[i][
                fault_branch[0]] == 0 and new_group[i][fault_branch[1]] == 0 and new_group[i][
                fault_branch[2]] == 0 and satisfy_conditions.is_n_equal_to_m_plus_one(new_group[i]):
                updated_group.append(new_group[i])
                continue
            else:
                updated_group.append(old_group[i])
        return updated_group

    def run_PSO(self):
        #初始化种群和参数
        # 初始化种群和参数
        record=[]
        new_pop_X = self.initialization(self.population_x)
        pbest = self.initialization(self.population_x)
        Vmax = self.get_Vmax(self.bounds)
        Vmin = self.get_Vmin(self.bounds)
        pop_V = self.initialization_V(Vmin,Vmax)
        gbest = self.find_teacher(new_pop_X)
        for iteration in range(self.iteration_number):


            old_pop_X = self.update_X(new_pop_X,pop_V)

            pbest = self.save_pbest(pbest, old_pop_X,gbest)
            new_pop_X=copy.deepcopy(pbest)
            pop_V = self.update_V(new_pop_X, pop_V, pbest, gbest, Vmin, Vmax)


            #pbest = self.save_pbest(pbest,new_pop_X)

            gbest = self.save_gbest(pbest)

        # 输出教师作为最终结果
        return gbest,record,pbest,sum_sum


result = PSO(x_solutions.population,task_number,population_size,iteration_number,bounds,fault_branch)
gbest,record,end_pop,sum_sum = result.run_PSO()


