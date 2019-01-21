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
from edifact.message import Message
import unittest
import os


class HugeMessageTest(unittest.TestCase):

    def test_huge_message(self):
        u"""tests parsing a huge message"""
        file = os.path.abspath(u'tests/data/huge_file2.edi')
        Message.from_file(file)


if __name__ == u'__main__':
    unittest.main()
