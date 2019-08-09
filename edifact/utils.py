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
from edifact.errors import MissingFieldsError, IncorrectValueForField
from edifact.serializer import Serializer
from decorator import decorator
from builtins import object

NO_ERRORS = None
DO_NOTHING = None


def rewind(rewind_iterator):
    rewind_iterator.rewind()


class RewindIterator(object):
    '''Convert a collection or an iterator into a RewindIterator'''
    def __init__(self, collection):
        self._iter = iter([item for item in collection])
        self._prev = []
        self._next = []

    def __iter__(self):
        return self

    def rewind(self):
        '''Rewinds one position the iterator'''
        if self._prev:
            self._next.append(self._prev.pop())

    def __next__(self):
        next_item = self._next.pop(0) if self._next else next(self._iter)
        self._prev.append(next_item)
        return next_item


def separate_section(iterator, start=None, end=None):
    '''Given an iterator of a message segments and optionally a
    start message tag or an end message tag it extracts a subset
    of segments

    Parameters
    ----------

    iterator : RewindIterator
        The iterator with the message segments to be splitted
    start : Segment
        Start segment of the split
    end  : Segment
        Final segment of the split

    Returns
    -------
    extracted
        Segments extracted
    '''
    if not isinstance(iterator, RewindIterator):
        raise TypeError('Argument iterator must be a RewindIterator.')
    started = False
    extracted = []
    if not start and not end:
        extracted = [segment for segment in iterator]

    for segment in iterator:
        if segment.tag == start:
            started = True
            if extracted:
                yield extracted
            extracted = []
            extracted.append(segment)
        elif segment.tag != end:
            if started:
                extracted.append(segment)
        else:
            started = False
            yield extracted
            rewind(iterator)
            break
    else:
        if extracted:
            yield extracted


def validate_segment(elements, template_segment_elements):
    '''Validate the segment elements against the template'''

    if len(template_segment_elements) > len(elements):
        raise MissingFieldsError
    for index, item in enumerate(template_segment_elements):
        if item == u'!ignore':
            continue
        elif item == u'!value':
            if not elements[index]:
                raise IncorrectValueForField
        elif isinstance(item, list):
            # Recursively checks childs
            validate_segment(elements[index], item)
        elif isinstance(item, tuple):
            if elements[index] not in item:
                raise IncorrectValueForField
        else:
            if elements[index] != item:
                raise IncorrectValueForField


@decorator
def with_segment_check(func, *args):
    '''Decorator wich provides a call to the validation of the segment struc
    against the template.
    '''
    try:
        argv = list(args)
        cls = argv.pop(0)
        segment = argv.pop(0)
        template = argv.pop(0)
        control_chars = argv.pop(0) if argv else None
        serializer = Serializer(control_chars) if control_chars \
            else Serializer()
        validate_segment(segment.elements, template)
    except MissingFieldsError:
        serialized_segment = serializer.serialize([segment])
        msg = u'Some field is missing in segment'
        return DO_NOTHING, [u'{}: {}'.format(msg, serialized_segment)]
    except IncorrectValueForField:
        serialized_segment = serializer.serialize([segment])
        msg = 'Incorrect value for field in segment'
        return DO_NOTHING, [u'{}: {}'.format(msg, unicode(serialized_segment))]
    else:
        return func(*args)
