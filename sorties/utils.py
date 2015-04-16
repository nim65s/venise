#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division

from math import copysign


class BoundedVar(object):
    def __init__(self, name, maxi=1, mini=None, val=0, circular=False):
        if mini is None:
            mini = -maxi
        if val is None:
            val = 0  # random() * (maxi - mini) - mini
        assert mini <= val <= maxi
        self._val, self._min, self._max, self._cir = val, mini, maxi, circular
        self._mini = self._val
        self._maxi = self._val
        self.name = name

    def __get__(self, obj, objtype):
        return self._val

    def __set__(self, obj, val):
        self._val = val % self._max if self._cir else min(max(val, self._min), self._max)
        self._post_set(obj)

    def _post_set(self, obj):
        obj.__dict__[self.name] = self._val
        if self.name + '_min' not in obj.__dict__:
            obj.__dict__[self.name + '_min'] = self._val
        if self.name + '_max' not in obj.__dict__:
            obj.__dict__[self.name + '_max'] = self._val
        if self._val < self._mini:
            self._mini = self._val
            obj.__dict__[self.name + '_min'] = self._mini
        elif self._val > self._maxi:
            self._maxi = self._val
            obj.__dict__[self.name + '_max'] = self._maxi


class CheckedVar(BoundedVar):
    def __init__(self, name, diff_max, max=1, min=None, val=0, circular=False):
        self.diff_max = diff_max
        return super().__init__(name, max, min, val, circular)

    def __set__(self, obj, val):
        if self._val is None:
            self._val = val
        elif -self.diff_max <= val - self._val <= self.diff_max:
            self._val = val % self._max if self._cir else min(max(val, self._min), self._max)
        else:
            err_txt = 'Dépassement de limite de %s: %.3f < %.3f (%.3f - %.3f) < %.3f'
            raise ValueError(err_txt % (self.name, -self.diff_max, val - self._val, val, self._val, self.diff_max))
            self._val += copysign(self.diff_max, val - self._val)
        self._post_set(obj)
