
#%% 读取IEEE 33配电网数据
# bigM
bigM = 100
basekV = 12.66# 电压基准值为12.66kV
baseMVA = 10 # 功率基准值为10MVA
baseI = 789.89
# 节点数据
T_set = np.arange(24)
dT = 1
B_num = 33
B_set = np.arange(33)
Pc=[80,100,87.5,125]# 充电/放电功率
mu_yiyuan=0.63
sigma_yiyuan=0.26
mu_juming=0.43
sigma_juming=0.18
mu_shangye=0.51
sigma_shangye=0.21
f0 = open("ieee33节点配电系统.txt");
t=33
PQ = np.zeros((t, 2))
A0 = np.zeros((t, t), int)
SB = 10  # 功率基准
fault_branch=[9,25,28]
population_start=[1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,0,0,0,0,0]#故障信息
task_number=37
population_size=50
iteration_number=100
bounds = np.vstack((np.ones(37), np.zeros(37)))
min_max_fit_loss=[0,284.880152]
min_max_fit_switch=[0,7]
C1=0.5
C2=0.5
class TLBO():
    """教学优化算法"""

    def __init__(self, population_x, task_number, population_size, iteration_number,fault_branch):
        self.population_x = population_x  # 初始种群
        self.task_number = task_number  # 开关个数
        self.population_size = population_size  # 种群规模
        self.iteration_number = iteration_number  # 迭代次数
        self.fault_brach = fault_branch #故障支路
    def initialization(self,populathion_x):
        """初始化阶段:根据种群规模，生成相应个数的个体（服务组合解）;
        通过为每个任务随机挑选候选服务来初始化一个组合服务"""
        population = self.population_x  # 种群
        return population
    def teacher_phase(self, population, teacher):
        """教师阶段:所有个体通过老师和个体平均值的差值像老师;
        学习参数是 种群列表 和 候选服务集的上下界列表"""
        Mean = self.get_Mean(population)  # 每个任务的平均值列表
        old_population = copy.deepcopy(population)  # 保存算法开始前的种群
            # 这个循环遍历每个个体
        for i in range(0, self.population_size):
            # TF = round(1 + random.random())  # 教学因素 = round[1 + rand(0, 1)]
                # r = random.random()  # ri=rand(0,1), 学习步长
                # 这个循环与第一个循环一起用来更新每个个体的第j个任务
            for j in range(0, self.task_number):#task_num为个体中有37个开关数
                TF = round(1 + random.random())  # 教学因素 = round[1 + rand(0, 1)]
                r = random.random()  # ri=rand(0,1), 学习步长
                 # 更新第i个解的第j个任务的响应时间
                difference_Res = r * (teacher[j] - TF * Mean[j][0])
                old_population[i][j] += difference_Res
                if old_population[i][j] >= 0.5:
                    old_population[i][j]=1
                else:
                    old_population[i][j]=0
                # 在教师阶段方法内直接调用update方法
        new_population = copy.deepcopy(self.update(population, old_population,teacher))
        return new_population
    def min_max_turnone(self,fitness, min_value, max_value):
        normalized_value = (fitness - min_value) / (max_value - min_value)
        return normalized_value
    def total_fitness(self,fit_loss,fit_switch):
        total_fit=0
        total_fit=C1*self.min_max_turnone(fit_loss,min_max_fit_loss[0],min_max_fit_loss[1])+C2*self.min_max_turnone(fit_switch,min_max_fit_loss[0],min_max_fit_loss[1])
        return total_fit
    def student_phase(self, population,teacher):
        """学生阶段"""
        old_population = copy.deepcopy(population)  # 保存算法开始前的旧种群
        new_population = []  # 初始化新种群
        for i in range(0, self.population_size):
            num_list = self.get_list()  # 获得一个种群大小的数字列表362
            num_list.remove(i)
            index = random.choice(num_list)  # 这两步获得一个除了自身以外的随机索引
            # print("第"+str(i)+"个选择了"+"第"+str(index)+"个")
            X = copy.deepcopy(population[i])
            Y = copy.deepcopy(population[index])  # 被选中与X交叉的个体
            # 如果X支配Y, X比Y好
            if self.total_fitness(fitness_loss(Y),self.fitness_switch(Y))<self.total_fitness(fitness_loss(X),self.fitness_switch(X)):

                r = random.random()  # 学习步长ri=rand(0,1)
                for j in range(0, self.task_number):
                    # 更新第X的第j个任务的响应时间
                    X[j] += r * (X[j] - Y[j])

                    if X[j] >= 0.5:
                        X[j] = 1
                    else:
                        X[j] = 0

            new_population.append(X)

        # 在教师阶段方法内直接调用refine方法
        # new_population = copy.deepcopy(self.refine(population, self.bounds))

            # 在教师阶段方法内直接调用update方法
        new_population = copy.deepcopy(self.update(old_population, new_population,teacher))

        return new_population

    def find_teacher(self, population):
        """找到种群中的老师(Pareto解集)"""

        min = 0
        for i in range(0, self.population_size):
            if self.total_fitness(fitness_loss(population[min]),
                                  self.fitness_switch(population[min])) > self.total_fitness(
                    fitness_loss(population[i]), self.fitness_switch(population[i]))and satisfy_conditions.is_n_equal_to_m_plus_one(population[i]):
                min = i

        return population[min]
    def fitness_switch(self, solution):
        different_count = np.sum(population_start != solution)
        return different_count
    def update(self, old_group, new_group,teacher):
        """这个函数用来更新种群:若新解支配旧解，则替换;否则保留"""

        updated_group = []
        for i in range(self.population_size):
            # 如果新解支配旧解
            if self.total_fitness(fitness_loss(new_group[i]),self.fitness_switch(new_group[i]))<self.total_fitness(fitness_loss(old_group[i]),self.fitness_switch(old_group[i])) and new_group[i][fault_branch[0]]==0and new_group[i][fault_branch[1]]==0and new_group[i][fault_branch[2]]==0 and satisfy_conditions.is_n_equal_to_m_plus_one(new_group[i]):
                updated_group.append(new_group[i])
                continue
            if self.total_fitness(fitness_loss(new_group[i]),self.fitness_switch(new_group[i]))>self.total_fitness(fitness_loss(old_group[i]),self.fitness_switch(old_group[i])):
                updated_group.append(old_group[i])
                continue
            if teacher==old_group[i]:
                updated_group.append(old_group[i])
                continue
            else:
                y=base_on_tulun.recovery_x(new_group[i])
                updated_group.append(y)
        return updated_group
    def get_list(self):
        """"为了学生阶段获得一个种群大小的数字列表"""
        nums_list = []
        for i in range(0, self.population_size):
            nums_list.append(i)
        return nums_list
    def get_Mean(self, population):
        """获得种群中 每个任务 的平均值;
           参数为种群;
           返回值为每个任务平均值的列表
        """
        Mean = []
        #population的每一列i，与每一行
        for i in range(0, self.task_number):

            Sum_Res = np.zeros(37)
            Mean_i = []
            for j in range(0, self.population_size):

                Sum_Res[i] += population[j][i]

            Mean_i.append(Sum_Res[i] / self.population_size)

            Mean.append(Mean_i)

        return Mean
    def run_TLBO(self):
        #初始化种群和参数

        # 初始化种群和参数
        new_population = self.initialization(self.population_x)

        teacher_solution = self.find_teacher(new_population)
        record=[]
        sum_sum = []
        for iteration in range(self.iteration_number):
            sum1 = 0
            # 计算所有解的平均值
            record.append(fitness_loss(teacher_solution) * 10000)
            for i in range(population_size):
                sum1=sum1+fitness_loss(new_population[i])*10000
            sum1=float(sum1/100)
            sum_sum.append(sum1)
            # 教师阶段
            old_population=self.teacher_phase(new_population, teacher_solution)
            # 学生阶段
            new_population=self.student_phase(old_population,teacher_solution)


            # 更新最优解
            teacher_solution = self.find_teacher(new_population)

        # 输出教师作为最终结果
        return teacher_solution,record,new_population,sum_sum

result=TLBO(x_solutions.population,task_number,population_size,iteration_number,fault_branch)
teacher,record,end_pop,sum_sum=result.run_TLBO()
