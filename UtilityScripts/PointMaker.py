import sys
import random
import csv

param = "param"
NUMBER_OF_POINTS = "NumberOfPoints"
NUMBER_OF_CLUSTERS = "NumberOfClusters"
NUMBER_OF_DIMENSIONS = "NumberOfDimensions"

assignment = ":="
end =";"

random_points = sys.argv[1]
random_dimensions = sys.argv[2]
random_cluster = sys.argv[3]
upper_bound = sys.argv[4]

if upper_bound.isdigit():
    upper_bound = int(upper_bound)
else:
    upper_bound = 92223720

HEADERS = ['Index']+["X_"+str(d) for d in range(1, int(random_dimensions)+1)]
print(param,NUMBER_OF_CLUSTERS,assignment,random_cluster,end)
print(param,NUMBER_OF_POINTS,assignment,random_points,end)
print(param,NUMBER_OF_DIMENSIONS,assignment,random_dimensions,end)

print(param, "Point",assignment)

with open('temp.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(HEADERS)
    for i in range(1,int(random_points)+1):
        row = [i]
        for d in range(1,int(random_dimensions)+1):
            val = random.randint(0, upper_bound)
            row.append(val)
            print(i, d, val)
        csvwriter.writerow(row)
    print(end)

# for k in range(len(ls_tuples)):
#     current = ls_tuples[k]
#     for j in range(len(current)):
#         print(k+1,j+1,)
