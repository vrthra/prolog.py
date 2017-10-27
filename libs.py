#!/usr/bin/env python3

from prolog import *

X = Symbol('X')
Y = Symbol('Y')
Z = Symbol('Z')

eq = Pred('eq')
eq[X, Y].calls(lambda env: env.unify(env[X], env[Y]))
noteq = Pred('noteq')
noteq[X, Y].calls(lambda env: env[X] != env[Y])
gt = Pred('gt')
gt[X, Y].calls(lambda env: env[X] > env[Y])

def ptrue(var):
    print(var,end='')
    return True

def pnltrue(var):
    print(var)
    return True


write = Pred('write')
write[X].calls(lambda env: ptrue(env[X]))
writenl = Pred('writenl')
writenl[X].calls(lambda env: pnltrue(env[X]))
nl = Pred('nl')
nl[None].calls(lambda env: ptrue("\n"))


father = Pred('father')
mother = Pred('mother')
parent = Pred('parent')
sibling = Pred('sibling')

father["matz", "Ruby"].fact()
mother["Trude", "Sally"].fact()
father["Tom", "Sally"].fact()
father["Tom", "Erica"].fact()
father["Tom", "Mini"].fact()
mother["Trude", "Mini"].fact()
father["Mike", "Tom"].fact()

parent[X,Y] << father[X,Y]
parent[X,Y] << mother[X,Y]
sibling[X,Y] << [ parent[Z,X], parent[Z,Y], noteq[X,Y] ]


print(query(sibling[X, "Sally"]))

move = Pred('move')
mov = Pred('mov')
write_info = Pred('write_info')

M = Symbol('M')
N = Symbol('N')
A = Symbol('A')
B = Symbol('B')
C = Symbol('C')

move[0, X,Y,Z] << CUT
move[N,A,B,C] << [
    is_([M,N], lambda n: n - 1),
    move[M,A,C,B],
    write_info[A,B],
    move[M,C,B,A]
]
write_info[X,Y] << [
    write["move a disc from the "],
    write[X], write[" pole to the "],
    write[Y], writenl[" pole "]
]

query(move[3,"left","right","center"])

print("no cut.")

mov[1,X,Y,Z] << [
    write["move top disc from "],
    write[X],
    write[" to "],
    write[Y],
    nl[None]
]

mov[N,X,Y,Z] << [
    gt[N, 1],
    is_([M,N], lambda n: n - 1),
    move[M,X,Z,Y],
    move[1,X,Y,C],
    move[M,Z,Y,X]
]

query(move[3,"left","right","center"])
