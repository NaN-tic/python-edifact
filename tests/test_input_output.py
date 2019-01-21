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
from __future__ import with_statement
from __future__ import absolute_import
from edifact.message import Message
import unittest
import os
from io import open


class InputOutputTest(unittest.TestCase):

    def setUp(self):
        self.path = os.path.dirname(os.path.realpath(__file__)) + u"/data"
        self.maxDiff = None

    def test1(self):
        self._test_file_read(u"{}/wikipedia.edi".format(self.path))

    def test2(self):
        self._test_file_read(u"{}/order.edi".format(self.path))

    def test_patient1(self):
        self._test_file_read(u"{}/patient1.edi".format(self.path))

    def _test_file_read(self, file_name, encoding=u'iso8859-1'):
        # read in a complete message from a file
        message = Message.from_file(file_name)
        output = message.serialize()
        with open(file_name, encoding=encoding) as fp:
            expected = fp.read()
        self.assertEqual(expected, output)


if __name__ == u'__main__':
    unittest.main()
