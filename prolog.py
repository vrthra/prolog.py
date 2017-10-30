#!/usr/bin/env python3
import itertools
import inspect

class Pred:
    def __init__(self, name): self.name, self.defs = name, []

    def __str__(self): return self.name

    def __repr__(self): return str(self)

    def __call__(self, *args): # []
        assert type(args) is tuple
        return Goal(self, to_list(args))

class Goal:
    def __init__(self, pred, args): self.pred, self.args = pred, args

    def __lshift__(self, rhs): self.pred.defs.append([self, to_list(rhs)])

    def __str__(self): return "%s%s" % (str(self.pred), str(self.args))

    def __repr__(self): return str(self)

class Cons:
    def __init__(self, car, cdr): self.car, self.cdr = car, cdr

    def __str__(self):
       def lst_repr(x):
          if x.cdr is None: return [str(x.car)]
          elif type(x.cdr) is Cons: return [str(x.car)] + lst_repr(x.cdr)
          else: return [str(x.car), '.', str(x.cdr)]
       return '(' + ' '.join(lst_repr(self)) + ')'

    def __repr__(self): return str(self)

def counter(): yield from itertools.count()

global is_cnt
is_cnt = counter()

def is_(syms, blk):
    global is_cnt
    is_p = Pred('is_%d' % next(is_cnt))

    def is_f(env):
        lst = [env[x] for x in syms[1:]]
        return env.unify(syms[0], blk(*lst))

    is_p(syms) << [is_f]
    return is_p(syms)

def to_list(x, y=None):
    for e in reversed(x):
        if type(e) is list: y = Cons(to_list(e), y)
        elif type(e) is Cons: y = e
        else: y = Cons(e, y)
    return y

class Symbol:
    def __init__(self, name): self.name = name

    def __str__(self): return '$' + self.name

    def __repr__(self): return str(self)

    def __pow__(self, other):
        return Cons(self, other)

class Env:
    def __init__(self): self.table = {}

    def put(self, x, pair): self.table[x] = pair

    def get(self, x): return self.table.get(x)

    def clear(self): self.table = {}

    def __repr__(self): return "env:" + str(self.table)

    def delete(self, x): del self.table[x]

    def __str__(self): return "env:" + str(self.table)

    def dereference(self, t):
        env = self
        while type(t) is Symbol:
            p = env.get(t)
            if p is None: break
            t, env = p
        return [t, env]

    def __getitem__(self, t):
        t, env = self.dereference(t)
        tt = type(t)
        if tt is Goal: return Goal(t.pred, env[t.args])
        if tt is Cons: return Cons(env[t.car], env[t.cdr])
        if tt is list: return [env[e] for e in t]
        return t

def unify(x, x_env, y, y_env, trail, tmp_env):
    while True:
        if type(x) is Symbol:
           xp = x_env.get(x)
           if xp is None:
              y, y_env = y_env.dereference(y)
              if x != y or x_env != y_env:
                  x_env.put(x, [y, y_env])
                  if x_env != tmp_env: trail.append([x, x_env])
              return True
           else:
              x, x_env = xp
              x, x_env = x_env.dereference(x)
        elif type(y) is Symbol: x, x_env, y, y_env = y, y_env, x, x_env
        else: break
    if type(x) is Goal and type(y) is Goal:
       if x.pred != y.pred: return False
       x, y = x.args, y.args
    if type(x) is Cons and type(y) is Cons:
       val = unify(x.car, x_env, y.car, y_env, trail, tmp_env)
       if not val: return False
       x, y = x.cdr, y.cdr
       return unify(x, x_env, y, y_env, trail, tmp_env)
    if type(x) is list and type(y) is list:
       if len(x) != len(y): return False

       return all(unify(a, x_env, b, y_env, trail, tmp_env) for a,b in zip(x,y))
    return x == y

def resolve_body(body, env):
    if body is None: yield None # yield when ever no more goals remain
    else:
       goal, rest = body.car, body.cdr
       for d_head, d_body in goal.pred.defs:
          d_env, trail = Env(), []
          if unify(goal, env, d_head, d_env, trail, d_env):
             if d_body and callable(d_body.car):
                 if d_body.car(CallbackEnv(d_env, trail)):
                     yield from resolve_body(rest, env)
             else:
                for _i in resolve_body(d_body, d_env):
                    yield from resolve_body(rest, env)
          for x, x_env in trail: x_env.delete(x)

def resolve(goals):
    env = Env()
    for _ in resolve_body(to_list(goals), env): # not an error.
        yield env

class CallbackEnv:
    def __init__(self, env, trail): self.env, self.trail = env, trail

    def __getitem__(self, t): return self.env[t]

    def unify(self, t, u): return unify(t, self.env, u, self.env, self.trail, self.env)

def query(*goals):
   goals = list(goals)
   return [env[goals] for env in resolve(goals)]

def symbols(symbols):
    for s in symbols: inspect.currentframe().f_back.f_globals[s] = Symbol(s)
def predicates(predicates):
    for s in predicates: inspect.currentframe().f_back.f_globals[s] = Pred(s)
