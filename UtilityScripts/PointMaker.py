import sys
import random


param = "param"
NUMBER_OF_POINTS = "NumberOfPoints"
NUMBER_OF_CLUSTERS = "NumberOfClusters"
NUMBER_OF_DIMENSIONS = "NumberOfDimensions"

assignment = ":="
end =";"

random_points = sys.argv[1]
random_dimensions = sys.argv[2]
random_cluster = sys.argv[3]

ls_tuples  = [(-2,1),(-2,-1),(2,1),(2,-1)]

print(param,NUMBER_OF_CLUSTERS,assignment,random_cluster,end)
print(param,NUMBER_OF_POINTS,assignment,random_points,end)
print(param,NUMBER_OF_DIMENSIONS,assignment,random_dimensions,end)

print(param, "Point",assignment)

for i in range(int(random_points)):
    for d in range(int(random_dimensions)):
        val = random.uniform(0,92233720)
        print(i+1, d+1, val)
print(end)

# for k in range(len(ls_tuples)):
#     current = ls_tuples[k]
#     for j in range(len(current)):
#         print(k+1,j+1,)
