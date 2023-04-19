
import itertools

ListComb = []
for i in range(10):
    ListComb.append("A"+str(i))

print (ListComb)
########################################################  
# All possible pairs in List
# Using list comprehension + enumerate()
res = [(a, b) for idx, a in enumerate(ListComb) for b in ListComb[idx + 1:]]
print("All possible pairs : " + str(res))


List_A = []
List_B = []

for x , y in res:
    List_A.append(x)
    List_B.append(y)
print(List_A)
print(List_B)