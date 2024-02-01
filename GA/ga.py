class GA():
    """粒子群算法"""

    def __init__(self, population_x, task_number, population_size, iteration_number, bounds,fault_branch):

        self.cp = 0.5  # cp为交叉率
        self.mp = 0.88  # mp为变异率
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


    def Selection(self, population):
        """选择操作：采用锦标赛选择算法（ps：由于本场景下，个体的适应值越小表示越好，故不宜使用轮盘赌选择算法）"""
        new_population = []
        tournament_size = 2  # 锦标赛规模

        # 锦标赛
        for i in range(0, self.population_size):
            temp = copy.deepcopy(population)  # 临时列表，供锦标赛抽取
            competitor_a = copy.deepcopy(random.choice(temp))  # 随机抽取选手a
            temp.remove(competitor_a)
            competitor_b = copy.deepcopy(random.choice(temp))  # 随机抽取选手b
            temp.remove(competitor_b)

            # 若a支配b
            if (self.total_fitness(fitness_loss(competitor_a),self.fitness_switch(competitor_a))<self.total_fitness(fitness_loss(competitor_b),self.fitness_switch(competitor_b))):
                new_population.append(competitor_a)

            # 若b支配a
            elif (self.total_fitness(fitness_loss(competitor_a),self.fitness_switch(competitor_a))>self.total_fitness(fitness_loss(competitor_b),self.fitness_switch(competitor_b))):

                new_population.append(competitor_b)
            # 若互相不支配
            else:
                new_population.append(population[i])
        return new_population

    def Crossover(self, population):
        """交叉操作"""

        cp = self.cp  # 交叉概率
        new_population = []  # 初始化交叉完毕的种群
        crossover_population = []  # 初始化需要交叉的种群
        # 根据交叉概率选出需要交叉的个体
        for c in population:
            r = random.random()
            if r <= cp:
                crossover_population.append(c)
            else:
                new_population.append(c)

        # 需保证交叉的个体是偶数,若不是偶数，则删掉需交叉列表的最后一个元素
        if len(crossover_population) % 2 != 0:
            new_population.append(crossover_population[len(crossover_population) - 1])
            del crossover_population[len(crossover_population) - 1]

        # crossover——单点交叉
        for i in range(0, len(crossover_population), 2):

            i_solution = crossover_population[i]
            j_solution = crossover_population[i + 1]
            crossover_position = random.randint(1, self.task_number - 2)  # 随机生成一个交叉位
            left_i = copy.deepcopy(i_solution[0:crossover_position])
            right_i = copy.deepcopy(i_solution[crossover_position:self.task_number])
            left_j = copy.deepcopy(j_solution[0:crossover_position])
            right_j = copy.deepcopy(j_solution[crossover_position:self.task_number])
            # 生成新个体
            new_i = copy.deepcopy(left_i + right_j)
            new_j = copy.deepcopy(left_j + right_i)
            new_population.append(new_i)
            new_population.append(new_j)

            if (i + 1) == (len(crossover_population) - 1):
                break

        return new_population

    def Mutation(self, population):
        """变异操作"""
        mp = self.mp  # 变异率
        new_population = []  # 初始化变异后的种群
        for c in population:
            r = random.random()
            copycopy=c
            if r <= mp:
                # mutation——随机选择某个体的一个任务（位置），从对应候选服务集中随机选择某服务替换
                mutation_position = random.randint(0, self.task_number - 1)  # 变异位置
                mutation_pop = generate_pop.generate_x(solution)
                replaced = mutation_pop[mutation_position]
                c[mutation_position] = copy.deepcopy(replaced)
                if satisfy_conditions.is_n_equal_to_m_plus_one(c):

                    new_population.append(c)
                else:
                    new_population.append(copycopy)
            else:
                new_population.append(c)

        # # 调用refine方法，确保不越界
        # new_population = self.refine(new_population, bounds)
        #
        # # 匹配对应任务的候选服务集中的真实服务
        # new_population = self.map_real_service(new_population, candidate_service_list)

        return new_population


    def save_gbest(self, population):
        """更新种群历史最优"""

        min = 0
        for i in range(0, self.population_size):
            if self.total_fitness(fitness_loss(population[min]),
                                  self.fitness_switch(population[min])) > self.total_fitness(
                    fitness_loss(population[i]),
                    self.fitness_switch(population[i])) and satisfy_conditions.is_n_equal_to_m_plus_one(population[i])and satisfy_conditions.is_all_nodes_connected(population[i]):
                min = i
        print(min)

        return population[min]

    def sigmoid(self,V):
        return 1 / (1 + np.exp(-V))
    def min_max_turnone(self,fitness, min_value, max_value):
        normalized_value = (fitness - min_value) / (max_value - min_value)
        return normalized_value
    def total_fitness(self,fit_loss,fit_switch):
        total_fit=0
        total_fit=C1*self.min_max_turnone(fit_loss,min_max_fit_loss[0],min_max_fit_loss[1])+C2*self.min_max_turnone(fit_switch,min_max_fit_loss[0],min_max_fit_loss[1])
        return total_fit

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
                fault_branch[2]] == 0 and satisfy_conditions.is_n_equal_to_m_plus_one(new_group[i])and satisfy_conditions.is_all_nodes_connected(new_group[i]):
                updated_group.append(new_group[i])
                print("n",new_group[i])
                continue
            else:
                updated_group.append(old_group[i])
        return updated_group

    def run_GA(self):
        #初始化种群和参数
        # 初始化种群和参数
        start_time = time.time()
        record=[]
        old_pop = self.initialization(self.population_x)
        gbest = self.find_teacher(old_pop)

        ig=0
        sum_sum=[]
        for iteration in range(self.iteration_number):

            record.append(fitness.fitness_loss(gbest) * 10000)
            numnum=0
            for i in range(population_size):
                if satisfy_conditions.is_n_equal_to_m_plus_one(old_pop[i]):
                    sum1=sum1+fitness.fitness_loss(old_pop[i])*10000
                    numnum+=1
            sum1=float(sum1/numnum)
            sum_sum.append(sum1)

            new_pop = self.Selection(old_pop)
            new_pop = self.Crossover(new_pop)
            new_pop = self.Mutation(new_pop)
            old_pop=self.update(old_pop,new_pop)

            gbest = self.save_gbest(old_pop)

        # 输出教师作为最终结果
        return gbest,record,old_pop,sum_sum


result = GA(x_solutions.population,task_number,population_size,iteration_number,bounds,fault_branch)
gbest,record,end_pop,sum_sum = result.run_GA()



