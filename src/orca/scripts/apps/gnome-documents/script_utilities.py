# Orca
#
# Copyright (C) 2013 The Orca Team.
#
# Author: Joanmarie Diggs <jdiggs@igalia.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

__id__ = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2013 The Orca Team."
__license__   = "LGPL"

import orca.script_utilities as script_utilities
import orca.scripts.toolkits.gtk as gtk

class Utilities(gtk.Utilities):

    def __init__(self, script):
        gtk.Utilities.__init__(self, script)

    def isReadOnlyTextArea(self, obj):
        if self.isDocument(obj):
            return False

        return gtk.Utilities.isReadOnlyTextArea(self, obj)

    def isTextArea(self, obj):
        if self.isDocument(obj):
            return True

        return gtk.Utilities.isTextArea(self, obj)
