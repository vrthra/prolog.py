#!/usr/bin/env python3

from prolog import *

symbols([chr(x) for x in range(ord('A'),ord('Z')+1)])
predicates(['eq', 'noteq', 'gt', 'write', 'writenl', 'nl'])

eq(X, Y) << [lambda env: env.unify(env[X], env[Y])]
noteq(X, Y) << [lambda env: env[X] != env[Y]]
gt(X, Y) << [lambda env: env[X] > env[Y]]

write(X) << [lambda env: (print(env[X], end=''),)]
writenl(X) << [lambda env: (print(env[X]),)]
nl() << [lambda env: (print(),)]


predicates(['car', 'cdr', 'cons', 'member', 'append', 'reverse', 'takeout', 'perm', 'subset'])

car([X|Y],X) << []
cdr([X|Y],Y) << []
cons(X,R,[X|R]) << []
member(X,[X|R]) << []
member(X,[Y|R]) << [member(X,R)]

#print(to_list([1,2,3]))
#print(query(member(1,to_list([1,2,3]))))
#print(query(member(3,to_list([1,2,3]))))
#print(query(member(10,to_list([1,2,3]))))


append([],X,X) << []
#print(query(append([],[1,2],A)))
append([X|Y],Z,[X|W]) << [append(Y,Z,W)]
print(query(append([1,2,3],[4],B)))
print(query(append([1,2,3],[4,5],[1,2,3,4,5])))
print(query(append([1,2,3],W,[1,2,3,4,5])))

reverse([X|Y],Z,W) << [reverse(Y,[X|Z],W)]
reverse([],X,X) << []
reverse(A,R) << [reverse(A,[],R)]

print(query(reverse([1,2,3,4,5],X)))


takeout(X,[X|R],R) << []
takeout(X,[F|R],[F|S]) << [takeout(X,R,S)]

print(query(takeout(X,[1,2,3],L)))

perm([X|Y],Z) << [perm(Y,W), takeout(X,Z,W)]
perm([],[]) << []

#print(query(perm(P,[1,2])))

subset([X|R],S) << [member(X,S), subset(R,S)]
subset([],X) << []

print(query(subset([4,3],[2,3,5,4])))
#print(query(subset([A],[2,3,5,4])))
