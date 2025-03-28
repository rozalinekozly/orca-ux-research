# Orca
#
# Copyright 2006-2009 Sun Microsystems Inc.
# Copyright 2010 Joanmarie Diggs
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

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2005-2009 Sun Microsystems Inc., "  \
                "Copyright (c) 2010 Joanmarie Diggs"
__license__   = "LGPL"

from orca import focus_manager
from orca import input_event_manager
from orca.scripts import default
from orca.ax_object import AXObject
from orca.ax_selection import AXSelection
from orca.ax_utilities import AXUtilities

from .script_utilities import Utilities
from .speech_generator import SpeechGenerator

class Script(default.Script):


    def get_speech_generator(self):
        """Returns the speech generator for this script."""
        return SpeechGenerator(self)

    def get_utilities(self):
        """Returns the utilities for this script."""
        return Utilities(self)

    def on_caret_moved(self, event):
        """Callback for object:text-caret-moved accessibility events."""

        # Java's SpinButtons are the most caret movement happy thing
        # I've seen to date.  If you Up or Down on the keyboard to
        # change the value, they typically emit three caret movement
        # events, first to the beginning, then to the end, and then
        # back to the beginning.  It's a very excitable little widget.
        # Luckily, it only issues one value changed event.  So, we'll
        # ignore caret movement events caused by value changes and
        # just process the single value changed event.
        if AXObject.find_ancestor(event.source, AXUtilities.is_spin_button):
            manager = input_event_manager.get_manager()
            if manager.last_event_was_up_or_down() or manager.last_event_was_mouse_button():
                return

        default.Script.on_caret_moved(self, event)

    def on_selection_changed(self, event):
        """Callback for object:selection-changed accessibility events."""

        # We treat selected children as the locus of focus. When the
        # selection changes in a list we want to update the locus of
        # focus. If there is no selection, we default the locus of
        # focus to the containing object.
        #
        if (AXUtilities.is_list(event.source) \
           or AXUtilities.is_page_tab_list(event.source) \
           or AXUtilities.is_tree(event.source)) \
           and AXUtilities.is_focused(event.source):
            new_focus = AXSelection.get_selected_child(event.source, 0) or event.source
            focus_manager.get_manager().set_locus_of_focus(event, new_focus)
        else:
            default.Script.on_selection_changed(self, event)

    def on_focused_changed(self, event):
        """Callback for object:state-changed:focused accessibility events."""

        if not event.detail1:
            return

        # Accessibility support for menus in Java is badly broken: Missing
        # events, missing states, bogus events from other objects, etc.
        # Therefore if we get an event, however broken, for menus or their
        # their items that suggests they are selected, we'll just cross our
        # fingers and hope that's true.
        if AXUtilities.is_menu_related(event.source) \
           or AXUtilities.is_menu_related(AXObject.get_parent(event.source)):
            focus_manager.get_manager().set_locus_of_focus(event, event.source)
            return

        if AXUtilities.is_root_pane(event.source) \
           and AXUtilities.is_menu_related(focus_manager.get_manager().get_locus_of_focus()):
            return

        default.Script.on_focused_changed(self, event)

    def on_value_changed(self, event):
        """Callback for object:property-change:accessible-value accessibility events."""

        # We'll ignore value changed events for Java's toggle buttons since
        # they also send a redundant object:state-changed:checked event.
        if AXUtilities.is_toggle_button(event.source) \
           or AXUtilities.is_radio_button(event.source) \
           or AXUtilities.is_check_box(event.source):
            return

        # Java's SpinButtons are the most caret movement happy thing
        # I've seen to date.  If you Up or Down on the keyboard to
        # change the value, they typically emit three caret movement
        # events, first to the beginning, then to the end, and then
        # back to the beginning.  It's a very excitable little widget.
        # Luckily, it only issues one value changed event.  So, we'll
        # ignore caret movement events caused by value changes and
        # just process the single value changed event.
        #
        if AXUtilities.is_spin_button(event.source):
            focus = focus_manager.get_manager().get_locus_of_focus()
            parent = AXObject.get_parent(focus)
            grandparent = AXObject.get_parent(parent)
            if grandparent == event.source:
                self._presentTextAtNewCaretPosition(event, otherObj=focus)
                return

        default.Script.on_value_changed(self, event)
