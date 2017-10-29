#!/usr/bin/env python3

from prolog import *

X = Symbol('X')
Y = Symbol('Y')
Z = Symbol('Z')

eq = Pred('eq')
eq(X, Y).calls(lambda env: env.unify(env[X], env[Y]))
noteq = Pred('noteq')
noteq(X, Y).calls(lambda env: env[X] != env[Y])
gt = Pred('gt')
gt(X, Y).calls(lambda env: env[X] > env[Y])

write = Pred('write')
write(X).calls(lambda env: (print(env[X], end=''),))
writenl = Pred('writenl')
writenl(X).calls(lambda env: (print(env[X]),))
nl = Pred('nl')
nl().calls(lambda env: (print(),))


father = Pred('father')
mother = Pred('mother')
parent = Pred('parent')
sibling = Pred('sibling')

father("matz", "Ruby") << []
mother("Trude", "Sally") << []
father("Tom", "Sally") << []
father("Tom", "Erica") << []
father("Tom", "Mini") << []
mother("Trude", "Mini") << []
father("Mike", "Tom") << []

parent(X,Y) << father(X,Y)
parent(X,Y) << mother(X,Y)
sibling(X,Y) << [ parent(Z,X), parent(Z,Y), noteq(X,Y) ]


print(query(sibling(X, "Sally")))

move = Pred('move')
mov = Pred('mov')
write_info = Pred('write_info')

M = Symbol('M')
N = Symbol('N')
A = Symbol('A')
B = Symbol('B')
C = Symbol('C')

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
