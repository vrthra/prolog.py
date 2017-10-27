#!/usr/bin/env python3
import itertools

class Pred:
    def __init__(self, _name):
        self.name = _name
        self.defs = []

    def __str__(self): return self.name

    def __repr__(self): return str(self)

    def __getitem__(self, args): # []
        if type(args) is tuple:
            args = list(args)
        else:
            args = [args]
        return Goal(self, args)

class Goal:
    def __init__(self, pred, args):
        self.pred, self.args = pred, args

    def si(self, rhs):
        self.pred.defs.append([self, to_list(rhs)])

    def fact(self):
        return self.si([])

    def __lshift__(self, rhs): # <<
        self.si(rhs if type(rhs) is list else [rhs])

    def calls(self, callback):
        self.pred.defs.append([self, callback])

    def __str__(self): return "%s%s" % (str(self.pred), str(self.args))

    def __repr__(self): return str(self)

class Cons:
    def __init__(self, car, cdr):
      self.car = car
      self.cdr = cdr

    def __str__(self):
       def lst_repr(x):
          if x.cdr is None: return [str(x.car)]
          elif type(x.cdr) is Cons:
              return [str(x.car)] + lst_repr(x.cdr)
          else: return [str(x.car), '.', str(x.cdr)]
       return '(' + ' '.join(lst_repr(self)) + ')'

    def __repr__(self): return str(self)

def counter():
    for i in itertools.count(): yield i

global is_cnt
is_cnt = counter()

def is_(syms, blk):
    global is_cnt
    is_p = Pred('is_%d' % next(is_cnt))
    assert len(syms) > 0 # need at least one symbol needed

    def is_f(env):
        lst =[env[x] for x in syms[1:]]
        value = blk(*lst)
        return env.unify(syms[0], value)

    is_p[syms].calls(is_f)
    return is_p[syms]

def to_list(x):
    y = None
    for e in reversed(x):
        y = cons(e, y)
    return y

def cons(car, cdr):
    return Cons(car, cdr)

class Symbol:
    def __init__(self, name): self.name = name

    def __str__(self): return '$' + self.name

    def __repr__(self): return str(self)

CUT = Symbol('CUT')


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
        if tt is Cons: return cons(env[t.car], env[t.cdr])
        if tt is list: return [env[e] for e in t]
        return t

def _unify(x, x_env, y, y_env, trail, tmp_env):
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
        elif type(y) is Symbol:
            x, x_env, y, y_env = y, y_env, x, x_env
        else: break
    if type(x) is Goal and type(y) is Goal:
       if x.pred != y.pred: return False
       x, y = x.args, y.args
    if type(x) is list and type(y) is list:
       if len(x) != len(y): return False

       for i,v in enumerate(x):
          if not(_unify(x[i], x_env, y[i], y_env, trail, tmp_env)): return False
       return True
    else:
       return x == y

def resolve(goals):
    env = Env()
    for _ in _resolve_body(to_list(goals), env, [False]): # not an error.
        yield env

def _resolve_body(body, env, cut):
    if body is None: yield None
    else:
       goal, rest = body.car, body.cdr
       if goal == CUT:
          for _ in _resolve_body(rest, env, cut): yield None
          cut[0] = True
       else:
          d_env = Env()
          d_cut = [False]
          for d_head, d_body in goal.pred.defs:
             if d_cut[0] or cut[0]: break
             trail = []
             if _unify_(goal, env, d_head, d_env, trail, d_env):
                if callable(d_body):
                    if d_body(CallbackEnv(d_env, trail)):
                        for _ in _resolve_body(rest, env, cut):
                           yield None
                else:
                   for _i in _resolve_body(d_body, d_env, d_cut):
                       for _j in _resolve_body(rest, env, cut):
                           yield None
                       if d_cut[0] is None: d_cut[0] = cut[0]
             for x, x_env in trail:
                 x_env.delete(x)
             d_env.clear()

global d_trace
d_trace = False
def trace(flag):
    global d_trace
    d_trace = flag

def _unify_(x, x_env, y, y_env, trail, tmp_env):
    global d_trace
    if d_trace: lhs, rhs = str(x_env[x]), str(y)
    unified = _unify(x, x_env, y, y_env, trail, tmp_env)
    if d_trace:
        print("\t%s %s %s" % (lhs, ('~' if unified else '!~'), rhs))
    return unified

class CallbackEnv:
    def __init__(self, env, trail):
       self.env, self.trail = env, trail
    def __getitem__(self, t):
       return self.env[t]
    def unify(self, t, u):
       return _unify(t, self.env, u, self.env, self.trail, self.env)

def query(*goals):
   goals = list(goals)
   results =[]
   for env in resolve(goals):
       results.append(env[goals])

   return results

