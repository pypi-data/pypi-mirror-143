# -*- coding: utf-8 -*-

from itertools import combinations_with_replacement
from typing import Union, Sequence

import numpy as np

import brainpy.math as bm
from brainpy.nn.base import RecurrentNode
from brainpy.tools.checking import (check_shape_consistency,
                                    check_float,
                                    check_integer,
                                    check_sequence)

__all__ = [
  'NVAR'
]


def _comb(N, k):
  r"""The number of combinations of N things taken k at a time.

  .. math::

     \frac{N!}{(N-k)! k!}

  """
  if N > k:
    val = 1
    for j in range(min(k, N - k)):
      val = (val * (N - j)) // (j + 1)
    return val
  elif N == k:
    return 1
  else:
    return 0


class NVAR(RecurrentNode):
  """Nonlinear vector auto-regression (NVAR) node.

  This class has the following features:

  - it supports batch size,

  Parameters
  ----------
  delay: int
    The number of delay step.
  order: int, sequence of int
    The nonlinear order.
  stride: int
    The stride to sample linear part vector in the delays.
  constant: optional, float
    The constant value.

  References
  ----------
  .. [1] Gauthier, D.J., Bollt, E., Griffith, A. et al. Next generation
         reservoir computing. Nat Commun 12, 5564 (2021).
         https://doi.org/10.1038/s41467-021-25801-2

  """

  def __init__(self,
               delay: int,
               order: Union[int, Sequence[int]],
               stride: int = 1,
               constant: Union[float, int] = None,
               **kwargs):
    super(NVAR, self).__init__(**kwargs)

    if not isinstance(order, (tuple, list)):
      order = [order]
    self.order = order
    check_sequence(order, 'order', elem_type=int, allow_none=False)
    self.delay = delay
    check_integer(delay, 'delay', allow_none=False)
    self.stride = stride
    check_integer(stride, 'stride', allow_none=False)
    self.constant = constant
    check_float(constant, 'constant', allow_none=True, allow_int=True)

    self.comb_ids = []
    # delay variables
    self.num_delay = self.delay * self.stride
    self.idx = bm.Variable(bm.array([0], dtype=bm.uint32))
    self.store = None

  def init_ff_conn(self):
    """Initialize feedforward connections."""
    # input dimension
    batch_size, free_size = check_shape_consistency(self.feedforward_shapes, -1, True)
    self.input_dim = sum(free_size)
    assert batch_size == (None,), f'batch_size must be None, but got {batch_size}'
    # linear dimension
    linear_dim = self.delay * self.input_dim
    # for each monomial created in the non-linear part, indices
    # of the n components involved, n being the order of the
    # monomials. Precompute them to improve efficiency.
    for order in self.order:
      idx = np.array(list(combinations_with_replacement(np.arange(linear_dim), order)))
      self.comb_ids.append(bm.asarray(idx))
    # number of non-linear components is (d + n - 1)! / (d - 1)! n!
    # i.e. number of all unique monomials of order n made from the
    # linear components.
    nonlinear_dim = sum([len(ids) for ids in self.comb_ids])
    # output dimension
    self.output_dim = int(linear_dim + nonlinear_dim)
    if self.constant is not None:
      self.output_dim += 1
    self.set_output_shape((None, self.output_dim))

  def init_state(self, num_batch=1):
    """Initialize the node state which depends on batch size."""
    # To store the last inputs.
    # Note, the batch axis is not in the first dimension, so we
    # manually handle the state of NVAR, rather return it.
    state = bm.zeros((self.num_delay, num_batch, self.input_dim), dtype=bm.float_)
    if self.store is None:
      self.store = bm.Variable(state)
    else:
      self.store.value = state

  def forward(self, ff, fb=None, **shared_kwargs):
    all_parts = []
    # 1. Store the current input
    ff = bm.concatenate(ff, axis=-1)
    self.store[self.idx[0]] = ff
    self.idx.value = (self.idx + 1) % self.num_delay
    # 2. Linear part:
    # select all previous inputs, including the current, with strides
    select_ids = (self.idx[0] + bm.arange(self.num_delay)[::self.stride]) % self.num_delay
    linear_parts = bm.moveaxis(self.store[select_ids], 0, 1)  # (num_batch, num_time, num_feature)
    linear_parts = bm.reshape(linear_parts, (linear_parts.shape[0], -1))
    # 3. constant
    if self.constant is not None:
      constant = bm.broadcast_to(self.constant, linear_parts.shape[:-1] + (1,))
      all_parts.append(constant)
    all_parts.append(linear_parts)
    # 3. Nonlinear part:
    # select monomial terms and compute them
    for ids in self.comb_ids:
      all_parts.append(bm.prod(linear_parts[:, ids], axis=2))
    # 4. Return all parts
    return bm.concatenate(all_parts, axis=-1)

