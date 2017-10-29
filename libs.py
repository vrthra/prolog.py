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


predicates(['father', 'mother', 'parent', 'sibling', 'mov', 'move', 'write_info'])

father("matz", "Ruby") << []
mother("Trude", "Sally") << []
father("Tom", "Sally") << []
father("Tom", "Erica") << []
father("Tom", "Mini") << []
mother("Trude", "Mini") << []
father("Mike", "Tom") << []

parent(X,Y) << [father(X,Y)]
parent(X,Y) << [mother(X,Y)]
sibling(X,Y) << [parent(Z,X), parent(Z,Y), noteq(X,Y)]


print(query(sibling(X, "Sally")))

print("no cut.")

mov(1,X,Y,Z) << [
    write("move top disc from "),
    write(X),
    write(" to "),
    write(Y),
    nl()
]

mov(N,X,Y,Z) << [
    gt(N, 1),
    is_([M,N], lambda n: n - 1),
    mov(M,X,Z,Y),
    mov(1,X,Y,C),
    mov(M,Z,Y,X)
]

query(mov(3,"left","right","center"))
