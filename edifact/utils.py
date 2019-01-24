# encoding: utf8
##############################################################################
#
#    Copyright (C) 2011-2019 NaN Projectes de Programari Lliure, S.L.
#                            http://www.NaN-tic.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from __future__ import absolute_import


def rewind(rewind_iterator):
    rewind_iterator.rewind()


class RewindIterator(object):

    def __init__(self, collection):
        self._iter = iter(collection)
        self._prev = []
        self._next = []

    def __iter__(self):
        return self

    def rewind(self):
        """Rewinds one position the iterator
        """
        if self._prev:
            self._next.append(self._prev.pop())

    def next(self):
        next_item = self._next.pop(0) if self._next else next(self._iter)
        self._prev.append(next_item)
        return next_item

    def __next__(self):
        return self.next()
