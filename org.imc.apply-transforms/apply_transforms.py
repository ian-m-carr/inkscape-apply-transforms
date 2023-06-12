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
import sys

import inkex
from inkex import Rectangle, FlowRoot, FlowPara, FlowRegion, TextElement, Tspan
from transform_utils import bake_transforms_recursively


class ApplyTransforms(inkex.EffectExtension):
    construction_layer: inkex.Layer

    def add_arguments(self, pars):
        pars.add_argument("--apply-to-paths", type=inkex.Boolean,
                          help="If true transform the path nodes (stroke width is not affected so may appear different!) "
                               "If false then the path will be given an individual transformation matrix.")
        pars.add_argument("--apply-to-shapes", type=inkex.Boolean,
                          help="If true transform substitute shapes with paths then transform the path nodes (stroke width is not affected so may appear different!) "
                               "If false then the path will be given an individual transformation matrix.")

    def effect(self):
        if len(self.svg.selection) == 0:
            inkex.utils.errormsg("Nothing selected!")

        for elem in self.svg.selection:
            # selected elements should be the group containing the profile path and center marker elements as descendants!
            if not isinstance(elem, inkex.Group):
                inkex.utils.errormsg(
                    "selection should contain only group elements! The selected element with eid: {} is a {} skipping".format(elem.eid,
                                                                                                                              elem.typename))
                break

            bake_transforms_recursively(elem, self.options.apply_to_paths, self.options.apply_to_shapes)


# standalone test command line paramenters: test\drawing.svg --output=test\drawing-out.svg --id=path249 --id=path287 --id=rect341 --id=path427
if __name__ == '__main__':
    # inkex.utils.errormsg("Args: {}".format(sys.argv))
    ApplyTransforms().run()
