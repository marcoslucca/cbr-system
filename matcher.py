## -*- coding: utf-8 -*-
##
## matcher.py
##
## Author:   Toke Høiland-Jørgensen (toke@toke.dk)
## Date:     27 April 2012
## Copyright (c) 2012, Toke Høiland-Jørgensen
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

class AdaptationError(RuntimeError):
    pass

class Matcher(object):
    def __init__(self, cases=[]):
        self.cases = cases

    def match(self, query, count):
        similarities = []
        for case in self.cases:
            similarities.append((query.similarity(case), case))
        similarities.sort()
        similarities.reverse()
        return similarities[:count]

    def adapt(self, query, result):
        """Adapt a result to a query, if possible.

        The return value is a tuple ('adapted', case), to conform to
        the format of the return values of match()."""
        if not result:
            raise AdaptationError("Cannot adapt from empty result")
        # result is assumed to be the result of a call to match(), so
        # get the Case element of the best match (i.e. the first
        # element).
        best = result[0][1]

        # The adaptable attributes are all those that are marked as
        # adapted, and that differ in value between the query and the
        # case.
        adaptable = [k for (k,v) in query.items() if v.adaptable and query[k] != best[k]]
        if not adaptable:
            raise AdaptationError("No adaptable values differ")
        return ('adapted', best.adapt(query))
