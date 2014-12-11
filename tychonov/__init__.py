#!/usr/bin/env python3

import inspect

def typecheck(func):
  anno = func.__annotations__
  sig = inspect.signature(func)
  def typecheck_wrapper(*args, **kwargs):
    ba = sig.bind(*args, **kwargs)
    # TODO: see <https://docs.python.org/3/library/inspect.html> for proper
    # usage and iteration.
    for name, value in ba.arguments.items():
      if name in anno and not tych_isinstance(value, anno[name]):
        raise TypeError("parameter '{:s}' of function '{:s}' should have type {:s}".format(name, func.__name__, tych_typename(anno[name])))
    ret = func(*args, **kwargs)
    if "return" not in anno and ret is not None:
      raise TypeError("function '{:s}' should return None".format(func.__name__))
    elif "return" in anno and not tych_isinstance(ret, anno["return"]):
      raise TypeError("function '{:s}' should have return type {:s}".format(func.__name__, tych_typename(anno["return"])))
    return ret
  typecheck_wrapper.__name__ = func.__name__
  return typecheck_wrapper

def tych_isinstance(value, ty):
  if isinstance(ty, TychType):
    return ty.inv_isa(value)
  else:
    return isinstance(value, ty)

def tych_typename(ty):
  if isinstance(ty, TychType):
    return str(ty)
  elif isinstance(ty, list):
    return "[" + ", ".join(tych_typename(x) for x in ty) + "]"
  else:
    return ty.__name__

class TychType(object):
  def __str__(self):
    raise NotImplementedError

  def inv_isa(self, value):
    raise NotImplementedError

class OptionTy(TychType):
  def __init__(self, ty):
    super().__init__()
    self._inner = ty

  def __str__(self):
    return "OptionTy({:s})".format(tych_typename(self._inner))

  def inv_isa(self, value):
    return value is None or tych_isinstance(value, self._inner)

class UnionTy(TychType):
  def __init__(self, ty1, *tys):
    super().__init__()
    self._inner = [ty1]
    self._inner.extend(tys)

  def __str__(self):
    #return "UnionTy({:s})".format(repr(self._inner))
    return "UnionTy({:s})".format(tych_typename(self._inner))

  def inv_isa(self, value):
    for ty in self._inner:
      if tych_isinstance(value, ty):
        return True
    return False
