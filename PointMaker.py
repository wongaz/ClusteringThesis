
ls_tuples  = [(-2,1),(-2,-1),(2,1),(2,-1)]


for k in range(len(ls_tuples)):
    current = ls_tuples[k]
    for j in range(len(current)):
        print(k+1,j+1,current[j])
