#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) [YEAR] [YOUR NAME], [YOUR EMAIL]
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Description of this extension
"""

import inkex

class MakeRedExtension(inkex.EffectExtension):
    """Please rename this class, don't keep it unnamed"""
    def add_arguments(self, pars):
        pars.add_argument("--my_option", type=inkex.Boolean,\
            help="An example option, put your options here")

    def effect(self):
        self.msg("Hi and welcome to my first extension")
        for elem in self.svg.selection:
            elem.style['fill'] = 'red'
            elem.style['fill-opacity'] = 1
            elem.style['opacity'] = 1

if __name__ == '__main__':
    MakeRedExtension().run()
