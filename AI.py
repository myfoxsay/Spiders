# from numpy import *
#
# random.rand(4,4)
#
# m=mat(random.rand(4,4))
# mi=m.I
# print(m*mi)
# print(m*mi-eye(4))

import kNN

group, labels = kNN.createDataSet()
s=kNN.classify0([1,1.2],group,labels,3)
print(s)