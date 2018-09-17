
# coding: utf-8

# In[33]:


from __future__ import division # safety with double division
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pprint
Opt = SolverFactory("gurobi")


# # Clustering for Centroids
# In this linear programming optimization, it will be optimizing for the Centroids location relative to the fixed assignments;

# ### M1:
# This LP will fix the assignment of the Centroids and optimize for the Lowest possible distance of $C_i$

# In[2]:


M1 = AbstractModel()
M1.name = "Clustering Centroid-Distance LP"


# ### M2
# This LP will fix the Centroid Locations and redo the assignement.

# In[3]:


M2 = AbstractModel()
M2.name = "Clustering Assignment-LP"


# ## Parameters
# Both LP's have same starting parameter that characterize the problem.
# - **d**: number of dimensions
# - **n**: number of points to cluster
# - **k**: number of clusters to generate

# In[4]:


M1.NumberOfDimensions = Param(within=NonNegativeIntegers)
M1.NumberOfPoints = Param(within=NonNegativeIntegers)
M1.NumberOfClusters = Param(within=NonNegativeIntegers)


# In[5]:


M2.NumberOfDimensions = Param(within=NonNegativeIntegers)
M2.NumberOfPoints = Param(within=NonNegativeIntegers)
M2.NumberOfClusters = Param(within=NonNegativeIntegers)


# ## Set
# - **Dimension Index (D)**: Set consisting of all possible possible dimensions an arbitrary point i.e. $[x_1, x_2, x_3 ... x_d]$
# - **Points (P)**: Set consisting of all indexes for Points in the system. $[p_1, p_2, p_3 ... p_n]$
# - **Cluster Index (C)**: Set consisting of possible ClusterIndex. $[c_1, c_2, c_3 ... c_k]$

# In[6]:


M1.DimensionIndex = RangeSet(1,M1.NumberOfDimensions)
M1.PointsIndex = RangeSet(1,M1.NumberOfPoints)
M1.ClusterIndex = RangeSet(1,M1.NumberOfClusters)


# In[7]:


M2.DimensionIndex = RangeSet(1,M2.NumberOfDimensions)
M2.PointsIndex = RangeSet(1,M2.NumberOfPoints)
M2.ClusterIndex = RangeSet(1,M2.NumberOfClusters)


# ## Inputs
# - **Point**: $P_{i,d}$ where $i$ $\in$ PointsIndex and $j$ $\in$ DimensionIndex

# In[8]:


M1.Point = Param(M1.PointsIndex,M1.DimensionIndex, within=Reals)


# In[9]:


M2.Point = Param(M2.PointsIndex,M2.DimensionIndex, within=Reals)


# ## Possible Variables
# - **Centroid**: $C_{i,d}$ where i $\in$ ClusterIndex and d $\in$ dimensionalIndex
# - **Assignment**: $A_{i,j}$ where i $\in$ pointsIndex and j $\in$ clusteringIndex
# - **Slack Positive**: $S^{+}_{i,j,d}$ where i $\in$ P, j $\in$ C, and d $\in$ D
# - **Slack Negative** $S^{-}_{i,j,d}$ where i $\in$ P, j $\in$ C, and d $\in$ D

# ### M1 Variables
# - **Centroid**: $C_{i,d}$ where i $\in$ ClusterIndex and d $\in$ dimensionalIndex
# - **Slack Positive**: $S^{+}_{i,j,d}$ where i $\in$ P, j $\in$ C, and d $\in$ D
# - **Skack Negative** $S^{-}_{i,j,d}$ where i $\in$ P, j $\in$ C, and d $\in$ D

# In[10]:


M1.Centroid=Var(M1.ClusterIndex, M1.DimensionIndex, within=Reals)
M1.Slack_Plus = Var(M1.PointsIndex,M1.ClusterIndex,M1.DimensionIndex, within=NonNegativeReals)
M1.Slack_Minus = Var(M1.PointsIndex,M1.ClusterIndex,M1.DimensionIndex, within=NonNegativeReals)


# ### M2 Variables
# - **Assignment**: $A_{i,j}$ where i $\in$ pointsIndex and j $\in$ clusteringIndex
# - **Slack Positive**: $S^{+}_{i,j,d}$ where i $\in$ P, j $\in$ C, and d $\in$ D
# - **Skack Negative** $S^{-}_{i,j,d}$ where i $\in$ P, j $\in$ C, and d $\in$ D

# In[11]:


M2.Assignment = Var(M2.PointsIndex, M2.ClusterIndex, within=Binary)
M2.Slack_Plus = Var(M2.PointsIndex,M2.ClusterIndex,M2.DimensionIndex, within=NonNegativeReals)
M2.Slack_Minus = Var(M2.PointsIndex,M2.ClusterIndex,M2.DimensionIndex, within=NonNegativeReals)


# ### M1 Fixed Value

# In[12]:


M1.Assignment=Param(M1.PointsIndex, M1.ClusterIndex, default=0,within=Binary, mutable=True)


# ### M2 Fixed Value

# In[13]:


M2.Centroid=Param(M2.ClusterIndex, M2.DimensionIndex,default=0,within=Reals, mutable=True)


# # Model M1
# ## Objective Function for M1
# $$ \sum_{i \in Points}\sum_{j \in Clusters}\sum_{d \in Dimensions} (S^{+}_{i,j,d}+S^{-}_{i,j,d}) $$

# In[14]:


def ObjectiveFunction(M):
    return sum(               (M.Slack_Plus[i,j,d]+M.Slack_Minus[i,j,d])               for i in M.PointsIndex                for j in M.ClusterIndex                for d in M.DimensionIndex)
M1.Distance = Objective(rule=ObjectiveFunction, sense=minimize)



# ### Constraint 1: Distance Constraint
# Used to convert distance metric into 1-norm
# $$0=A_{i,j}\cdot(P_{i,d}-C_{j,d})+(S^{+}_{i,j,d}-S^{-}_{i,j,d}) \qquad \forall i \in P, j\in C, d \in D $$

# In[15]:


def DistanceConstraint(M,i,j,d):
    return 0 == M.Assignment[i,j]*(M.Point[i,d]-M.Centroid[j,d])+M.Slack_Plus[i,j,d]-M.Slack_Minus[i,j,d]
M1.Norm = Constraint(M1.PointsIndex, M1.ClusterIndex, M1.DimensionIndex, rule = DistanceConstraint)


# # Model M2
# ## Objective Function for M2
# $$ \sum_{i \in Points}\sum_{j \in Clusters}\sum_{d \in Dimensions} (S^{+}_{i,j,d}+S^{-}_{i,j,d}) $$

# In[16]:


def ObjectiveFunction(M):
    return sum(               (M.Slack_Plus[i,j,d]+M.Slack_Minus[i,j,d])               for i in M.PointsIndex                for j in M.ClusterIndex                for d in M.DimensionIndex)
M2.Distance = Objective(rule=ObjectiveFunction, sense=minimize)


# ### Constraint 1: Distance Constraint
# Used to convert distance metric into 1-norm
# $$0=A_{i,j}\cdot(P_{i,d}-C_{j,d})+(S^{+}_{i,j,d}-S^{-}_{i,j,d}) \qquad \forall i \in P, j\in C, d \in D $$

# In[17]:


def DistanceConstraint(M,i,j,d):
    return 0 == M.Assignment[i,j]*(M.Point[i,d]-M.Centroid[j,d])+M.Slack_Plus[i,j,d]-M.Slack_Minus[i,j,d]
M2.Norm = Constraint(M2.PointsIndex, M2.ClusterIndex, M2.DimensionIndex, rule = DistanceConstraint)


# ### Constraint 2: Non-Empty Cluster
# $$ 1\leq \sum_{i \in P} A_{i,j} \qquad \forall j \in C $$

# In[18]:


def NonEmptyCluster(M, j):
    return 1<=sum(M.Assignment[i,j] for i in M.PointsIndex)
M2.NonEmptyBalance = Constraint(M2.ClusterIndex, rule = NonEmptyCluster)


# ### Constraint 3: Singular Assignment
# $$ 1 = \sum_j A_{i,j} \qquad \forall i \in P$$

# In[19]:


def SingularAssignment(M, i):
    return 1==sum(M.Assignment[i,j] for j in M.ClusterIndex)
M2.SingularAssignmentBalance = Constraint(M2.PointsIndex, rule = SingularAssignment)


# ## Create Problem and Solver Instance

# In[34]:


dat_file ="../Data/simpleTest.dat"
original_instance1 = M1.create_instance(dat_file)
original_instance2 = M2.create_instance(dat_file)
clusters = original_instance1.NumberOfClusters.value
points = original_instance1.NumberOfPoints.value
dimensions = original_instance1.NumberOfDimensions.value


# In[35]:


def seeding_A(instance):
    clusters = instance.NumberOfClusters.value
    points = instance.NumberOfPoints.value
    for x in range(1,points+1):
        instance.Assignment[x,((x-1)%clusters)+1]=1


# In[ ]:


past_instance1 = None
current_instance1 = original_instance1.clone()
past_instance2 = None
current_instance2 = original_instance2.clone()
seeding_A(current_instance1)
count=0

def end_condition(count):
    if(count>3 and past_instance1 is not None and past_instance2 is not None):
        if value(past_instance1.Distance)== value(current_instance1.Distance):
            return True
        if value(past_instance2.Distance)== value(current_instance2.Distance):
            return True
    return False

def solve_model_1(count):
    count+=1
    Soln1 = Opt.solve(current_instance1)
    current_instance1.solutions.load_from(Soln1)

    # Print the output
    print("Current_instance 1: ", count)
    print("Termination Condition was "+str(Soln1.Solver.Termination_condition))
    display(current_instance1)

    if end_condition(count):
        return;
    past_instance1 = current_instance1
    current_instance2 = original_instance2.clone()
    for j in range(1,clusters+1):
        for d in range(1,dimensions+1):
            current_instance2.Centroid[j,d]=current_instance1.Centroid[j,d]
    solve_model_2(count)


def solve_model_2(count):
    count+=1
    Soln2 = Opt.solve(current_instance2)
    current_instance2.solutions.load_from(Soln2)


    print("Current_instance 2: ", count)
    print("Termination Condition was "+str(Soln2.Solver.Termination_condition))
    display(current_instance2)
    if end_condition(count):
        return;
    past_instance2 = current_instance2
    current_instance1 = original_instance1.clone()
    for i in range(1,points+1):
            for j in range(1,clusters+1):
                current_instance1.Assignment[i,j]=current_instance2.Assignment[i,j]
    solve_model_1(count)

solve_model_1(count)
