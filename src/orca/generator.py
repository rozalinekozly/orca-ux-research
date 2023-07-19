# Orca
#
# Copyright 2009 Sun Microsystems Inc.
# Copyright 2015-2016 Igalia, S.L.
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

"""Superclass of classes used to generate presentations for objects."""

__id__        = "$Id:$"
__version__   = "$Revision:$"
__date__      = "$Date:$"
__copyright__ = "Copyright (c) 2009 Sun Microsystems Inc." \
                "Copyright (c) 2015-2016 Igalia, S.L."
__license__   = "LGPL"

import gi
gi.require_version("Atspi", "2.0")
from gi.repository import Atspi

gi.require_version('Atk', '1.0')
from gi.repository import Atk

import re
import sys
import time
import traceback

from . import braille
from . import debug
from . import messages
from . import object_properties
from . import settings
from . import settings_manager
from .ax_object import AXObject
from .ax_utilities import AXUtilities

# Python 3.10 compatibility:
try:
    import collections.abc as collections_abc
except ImportError:
    import collections as collections_abc

def _formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.args
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)

# [[[WDW - general note -- for all the _generate* methods, it would be great if
# we could return an empty array if we can determine the method does not
# apply to the object.  This would allow us to reduce the number of strings
# needed in formatting.py.]]]

# The prefix to use for the individual generator methods
#
METHOD_PREFIX = "_generate"

_settingsManager = settings_manager.getManager()

class Generator:
    """Takes accessible objects and generates a presentation for those
    objects.  See the generate method, which is the primary entry
    point."""

    # pylint: disable-msg=W0142

    def __init__(self, script, mode):

        # pylint: disable-msg=W0108

        self._mode = mode
        self._script = script
        self._activeProgressBars = {}
        self._methodsDict = {}
        for method in \
            [z for z in [getattr(self, y).__get__(self, self.__class__) for y in [x for x in dir(self) if x.startswith(METHOD_PREFIX)]] if isinstance(z, collections_abc.Callable)]:
            name = method.__name__[len(METHOD_PREFIX):]
            name = name[0].lower() + name[1:]
            self._methodsDict[name] = method
        self._verifyFormatting()

    def _addGlobals(self, globalsDict):
        """Other things to make available from the formatting string.
        """
        globalsDict['obj'] = None
        globalsDict['role'] = None

    def _verifyFormatting(self):

        # Verify the formatting strings are OK.  This is only
        # for verification and does not effect the function of
        # Orca at all.

        # Populate the entire globals with empty arrays
        # for the results of all the legal method names.
        #
        globalsDict = {}
        for key in self._methodsDict.keys():
            globalsDict[key] = []
        self._addGlobals(globalsDict)

        for roleKey in self._script.formatting[self._mode]:
            for key in ["focused", "unfocused"]:
                try:
                    evalString = \
                        self._script.formatting[self._mode][roleKey][key]
                except Exception:
                    continue
                else:
                    if not evalString:
                        # It's legal to have an empty string.
                        #
                        continue
                    while True:
                        try:
                            eval(evalString, globalsDict)
                            break
                        except NameError:
                            info = _formatExceptionInfo()
                            arg = info[1][0]
                            arg = arg.replace("name '", "")
                            arg = arg.replace("' is not defined", "")
                            if arg not in self._methodsDict:
                                debug.printException(debug.LEVEL_SEVERE)
                            globalsDict[arg] = []
                        except Exception:
                            debug.printException(debug.LEVEL_SEVERE)
                            break

    def _overrideRole(self, newRole, args):
        """Convenience method to allow you to temporarily override the role in
        the args dictionary.  This changes the role in args ags
        returns the old role so you can pass it back to _restoreRole.
        """
        oldRole = args.get('role', None)
        args['role'] = newRole
        return oldRole

    def _restoreRole(self, oldRole, args):
        """Convenience method to restore the old role back in the args
        dictionary.  The oldRole should have been obtained from
        _overrideRole.  If oldRole is None, then the 'role' key/value
        pair will be deleted from args.
        """
        if oldRole:
            args['role'] = oldRole
        else:
            del args['role']

    def generateContents(self, contents, **args):
        return []

    def generateContext(self, obj, **args):
        return []

    def generate(self, obj, **args):
        """Returns an array of strings (and possibly voice and audio
        specifications) that represent the complete presentation for the
        object.  The presentation to be generated depends highly upon the
        formatting strings in formatting.py.

        args is a dictionary that may contain any of the following:
        - alreadyFocused: if True, we're getting an object
          that previously had focus
        - priorObj: if set, represents the object that had focus before
          this object
        - includeContext: boolean (default=True) which says whether
          the context for an object should be included as a prefix
          and suffix
        - role: a role to override the object's role
        - formatType: the type of formatting, such as
          'focused', 'basicWhereAmI', etc.
        - forceMnemonic: boolean (default=False) which says if we
          should ignore the settings.enableMnemonicSpeaking setting
        - forceTutorial: boolean (default=False) which says if we
          should force a tutorial to be spoken or not
        """

        if self._script.utilities.isDead(obj):
            msg = 'ERROR: Cannot generate presentation dead obj'
            debug.println(debug.LEVEL_INFO, msg, True)
            return []

        startTime = time.time()
        result = []
        globalsDict = {}
        self._addGlobals(globalsDict)
        globalsDict['obj'] = obj
        try:
            globalsDict['role'] = args.get('role', AXObject.get_role(obj))
        except Exception:
            msg = 'ERROR: Cannot generate presentation for: %s. Aborting' % obj
            debug.println(debug.LEVEL_INFO, msg, True)
            return result
        try:
            # We sometimes want to override the role.  We'll keep the
            # role in the args dictionary as a means to let us do so.
            #
            args['role'] = globalsDict['role']

            # We loop through the format string, catching each error
            # as we go.  Each error should always be a NameError,
            # where the name is the name of one of our generator
            # functions.  When we encounter this, we call the function
            # and get its results, placing them in the globals for the
            # the call to eval.
            #
            args['mode'] = self._mode
            if not args.get('formatType', None):
                if args.get('alreadyFocused', False):
                    args['formatType'] = 'focused'
                else:
                    args['formatType'] = 'unfocused'

            formatting = self._script.formatting.getFormat(**args)

            # Add in the context if this is the first time
            # we've been called.
            #
            if not args.get('recursing', False):
                if args.get('includeContext', True):
                    prefix = self._script.formatting.getPrefix(**args)
                    suffix = self._script.formatting.getSuffix(**args)
                    formatting = '%s + %s + %s' % (prefix, formatting, suffix)
                args['recursing'] = True

            msg = '%s GENERATOR: Starting %s generation for %s (%s)' % \
                (self._mode.upper(), args.get('formatType'), obj, args.get('role'))
            debug.println(debug.LEVEL_INFO, msg, True)

            # Reset 'usedDescriptionFor*' if a previous generator used it.
            self._script.pointOfReference['usedDescriptionForName'] = False
            self._script.pointOfReference['usedDescriptionForUnrelatedLabels'] = False
            self._script.pointOfReference['usedDescriptionForAlert'] = False

            def debuginfo(x):
                return self._resultElementToString(x, False)

            assert(formatting)
            while True:
                currentTime = time.time()
                try:
                    result = eval(formatting, globalsDict)
                    break
                except NameError:
                    result = []
                    info = _formatExceptionInfo()
                    arg = info[1][0]
                    arg = arg.replace("name '", "")
                    arg = arg.replace("' is not defined", "")
                    if arg not in self._methodsDict:
                        debug.printException(debug.LEVEL_SEVERE)
                        break
                    globalsDict[arg] = self._methodsDict[arg](obj, **args)
                    duration = "%.4f" % (time.time() - currentTime)
                    if isinstance(globalsDict[arg], list):
                        stringResult = " ".join(filter(lambda x: x,
                                                        map(debuginfo, globalsDict[arg])))
                        debug.println(debug.LEVEL_ALL,
                                      "%sGENERATION TIME: %s  ---->  %s=[%s]" \
                                      % (" " * 18, duration, arg, stringResult))

        except Exception:
            debug.printException(debug.LEVEL_SEVERE)
            result = []

        duration = "%.4f" % (time.time() - startTime)
        debug.println(debug.LEVEL_ALL, "%sCOMPLETION TIME: %s" % (' ' * 18, duration))
        self._debugResultInfo(result)
        if args.get('isProgressBarUpdate') and result and result[0]:
            self.setProgressBarUpdateTimeAndValue(obj)

        return result

    def _resultElementToString(self, element, includeAll=True):
        if not includeAll:
            return str(element).replace("\n", "\\n")

        return "\n%s'%s'" % (" " * 18, element)

    def _debugResultInfo(self, result):
        if debug.LEVEL_ALL < debug.debugLevel:
            return

        info = "%s%s GENERATOR: Results: " % (" " * 18, self._mode.upper())
        info += "%s" % " ".join(map(self._resultElementToString, result))
        debug.println(debug.LEVEL_ALL, info)

    #####################################################################
    #                                                                   #
    # Name, role, and label information                                 #
    #                                                                   #
    #####################################################################

    def _generateRoleName(self, obj, **args):
        """Returns the role name for the object in an array of strings, with
        the exception that the Atspi.Role.UNKNOWN role will yield an
        empty array.  Note that a 'role' attribute in args will
        override the accessible role of the obj.
        """
        # Subclasses must override this.
        return []

    def _fallBackOnDescriptionForName(self, obj, **args):
        role = args.get('role', AXObject.get_role(obj))
        if role == Atspi.Role.LABEL:
            return False

        return True

    def _generateName(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the name of the object.  If the object is directly
        displaying any text, that text will be treated as the name.
        Otherwise, the accessible name of the object will be used.  If
        there is no accessible name, then the description of the
        object will be used.  This method will return an empty array
        if nothing can be found.  [[[WDW - I wonder if we should just
        have _generateName, _generateDescription,
        _generateDisplayedText, etc., that don't do any fallback.
        Then, we can allow the formatting to do the fallback (e.g.,
        'displayedText or name or description'). [[[JD to WDW - I
        needed a _generateDescription for whereAmI. :-) See below.
        """
        result = []
        self._script.pointOfReference['usedDescriptionForName'] = False
        name = AXObject.get_name(obj)
        role = args.get('role', AXObject.get_role(obj))
        parent = AXObject.get_parent(obj)
        if name:
            result.append(name)
        elif self._fallBackOnDescriptionForName(obj, **args):
            description = AXObject.get_description(obj)
            if description:
                result.append(description)
                self._script.pointOfReference['usedDescriptionForName'] = True
            else:
                link = None
                if role == Atspi.Role.LINK:
                    link = obj
                elif AXUtilities.is_link(parent):
                    link = parent
                if link:
                    basename = self._script.utilities.linkBasenameToName(link)
                    if basename:
                        result.append(basename)
        # To make the unlabeled icons in gnome-panel more accessible.
        if not result and role == Atspi.Role.ICON and AXUtilities.is_panel(parent):
            return self._generateName(parent)

        return result

    def _generatePlaceholderText(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the 'placeholder' text. This is typically text that
        serves as a functional label and is found in a text widget until
        that widget is given focus at which point the text is removed,
        the assumption being that the user was able to see the text prior
        to giving the widget focus.
        """
        attrs = self._script.utilities.objectAttributes(obj)
        placeholder = attrs.get('placeholder-text')
        if placeholder and placeholder != AXObject.get_name(obj):
            return [placeholder]

        placeholder = attrs.get('placeholder')
        if placeholder and placeholder != AXObject.get_name(obj):
            return [placeholder]

        return []

    def _generateLabelAndName(self, obj, **args):
        """Returns the label and the name as an array of strings for speech
        and braille.  The name will only be present if the name is
        different from the label.
        """
        result = []
        label = self._generateLabel(obj, **args)
        name = self._generateName(obj, **args)
        role = args.get('role', AXObject.get_role(obj))
        if not (label or name) and role == Atspi.Role.TABLE_CELL:
            descendant = self._script.utilities.realActiveDescendant(obj)
            name = self._generateName(descendant)

        # If we don't have a label, always use the name.
        if not label:
            return name

        result.extend(label)
        if not name:
            return result

        # Try to eliminate names which are redundant to the label.
        # Convert all non-alphanumeric characters to space and get the words.
        nameWords = re.sub(r"[\W_]", " ", name[0]).split()
        labelWords = re.sub(r"[\W_]", " ", label[0]).split()

        # If all of the words in the name are in the label, the name is redundant.
        if set(nameWords).issubset(set(labelWords)):
            msg = "GENERATOR: name '%s' is redundant to label '%s'" % (name[0], label[0])
            debug.println(debug.LEVEL_INFO, msg, True)
            return result

        result.extend(name)
        return result

    def _generateLabelOrName(self, obj, **args):
        """Returns the label as an array of strings for speech and braille.
        If the label cannot be found, the name will be used instead.
        If the name cannot be found, an empty array will be returned.
        """
        result = self._generateLabel(obj, **args)
        if not result:
            result = self._generateName(obj, **args)

        return result

    def _generateUnrelatedLabelsOrDescription(self, obj, **args):
        result = self._generateUnrelatedLabels(obj, **args)
        if result:
            self._script.pointOfReference['usedDescriptionForUnrelatedLabels'] = False
            return result

        result = self._generateDescription(obj, **args)
        if result:
            self._script.pointOfReference['usedDescriptionForUnrelatedLabels'] = True

        return result

    def _generateDescription(self, obj, **args):
        """Returns an array of strings fo use by speech and braille that
        represent the description of the object, if that description
        is different from that of the name and label.
        """

        if self._script.pointOfReference.get('usedDescriptionForName'):
            return []

        if self._script.pointOfReference.get('usedDescriptionForAlert'):
            return []

        if self._script.pointOfReference.get('usedDescriptionForUnrelatedLabels'):
            return []

        role = args.get('role', AXObject.get_role(obj))

        # Unity Panel Service menubar items are labels which claim focus and
        # have an accessible description of the text + underscore symbol used
        # to create the mnemonic. We'll work around that here for now.
        if role == Atspi.Role.LABEL:
            return []

        name = AXObject.get_name(obj)
        description = AXObject.get_description(obj)

        if role == Atspi.Role.ICON:
            name = self._script.utilities.displayedText(obj) or ""

        result = []
        if description:
            try:
                tokens = self._script.formatting[self._mode][role][args.get('formatType')].split()
                isLabelAndName = 'labelAndName' in tokens
                isLabelOrName = 'labelOrName' in tokens
            except Exception:
                isLabelAndName = False
                isLabelOrName = False

            label = self._script.utilities.displayedLabel(obj) or ""
            desc = description.lower()
            canUse = True
            if isLabelAndName:
                canUse = desc not in name.lower() and desc not in label.lower()
            elif isLabelOrName and label:
                canUse = desc not in label.lower()
            elif isLabelOrName and name:
                canUse = desc not in name.lower()
            if canUse:
                result.append(description)

        if not result:
            desc = self._script.utilities.displayedDescription(obj)
            if desc:
                result.append(desc)

        return result

    def _generateLabel(self, obj, **args):
        """Returns the label for an object as an array of strings for use by
        speech and braille.  The label is determined by the displayedLabel
        method of the script utility, and an empty array will be returned if
        no label can be found.
        """
        result = []
        label = self._script.utilities.displayedLabel(obj)
        if label:
            result.append(label)
        return result

    def generateStatusBar(self, obj, **args):
        """Returns an array of strings that represent a status bar."""

        return self._generateStatusBar(obj, **args)

    def _generateTermValueCount(self, obj, **args):
        return []

    #####################################################################
    #                                                                   #
    # Image information                                                 #
    #                                                                   #
    #####################################################################

    def _generateImageDescription(self, obj, **args ):
        """Returns an array of strings for use by speech and braille that
        represent the description of the image on the object, if it
        exists.  Otherwise, an empty array is returned.
        """
        result = []
        try:
            image = obj.queryImage()
        except NotImplementedError:
            pass
        else:
            description = image.imageDescription
            if description and len(description):
                result.append(description)
        return result

    #####################################################################
    #                                                                   #
    # State information                                                 #
    #                                                                   #
    #####################################################################

    def _generateClickable(self, obj, **args):
        return []

    def _generateHasLongDesc(self, obj, **args):
        return []

    def _generateHasDetails(self, obj, **args):
        return []

    def _generateDetailsFor(self, obj, **args):
        return []

    def _generateAllDetails(self, obj, **args):
        return []

    def _generateHasPopup(self, obj, **args):
        return []

    def _generateAvailability(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the grayed/sensitivity/availability state of the
        object, but only if it is insensitive (i.e., grayed out and
        inactive).  Otherwise, and empty array will be returned.
        """
        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'insensitive'
        if not AXUtilities.is_sensitive(obj):
            result.append(self._script.formatting.getString(**args))
        return result

    def _generateInvalid(self, obj, **args):
        error = self._script.utilities.getError(obj)
        if not error:
            return []

        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'invalid'
        indicators = self._script.formatting.getString(**args)

        if error == 'spelling':
            indicator = indicators[1]
        elif error == 'grammar':
            indicator = indicators[2]
        else:
            indicator = indicators[0]

        errorMessage = self._script.utilities.getErrorMessage(obj)
        if errorMessage:
            result.append("%s: %s" % (indicator, errorMessage))
        else:
            result.append(indicator)

        return result

    def _generateRequired(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the required state of the object, but only if it is
        required (i.e., it is in a dialog requesting input and the
        user must give it a value).  Otherwise, and empty array will
        be returned.
        """
        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'required'
        isRequired = AXUtilities.is_required(obj)
        if not isRequired and AXUtilities.is_radio_button(obj):
            parent = AXObject.get_parent(obj)
            isRequired = AXUtilities.is_required(parent)
        if isRequired:
            result.append(self._script.formatting.getString(**args))
        return result

    def _generateReadOnly(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the read only state of this object, but only if it
        is read only (i.e., it is a text area that cannot be edited).
        """
        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'readonly'
        if AXUtilities.is_read_only(obj) \
           or self._script.utilities.isReadOnlyTextArea(obj):
            result.append(self._script.formatting.getString(**args))
        return result

    def _generateCellCheckedState(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the checked state of the object.  This is typically
        for check boxes that are in a table. An empty array will be
        returned if this is not a checkable cell.
        """
        result = []
        if self._script.utilities.hasMeaningfulToggleAction(obj):
            oldRole = self._overrideRole(Atspi.Role.CHECK_BOX, args)
            result.extend(self.generate(obj, **args))
            self._restoreRole(oldRole, args)

        return result

    def _generateCheckedState(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the checked state of the object.  This is typically
        for check boxes. [[[WDW - should we return an empty array if
        we can guarantee we know this thing is not checkable?]]]
        """
        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'checkbox'
        indicators = self._script.formatting.getString(**args)
        if AXUtilities.is_checked(obj):
            result.append(indicators[1])
        elif AXUtilities.is_indeterminate(obj):
            result.append(indicators[2])
        else:
            result.append(indicators[0])
        return result

    def _generateRadioState(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the checked state of the object.  This is typically
        for check boxes. [[[WDW - should we return an empty array if
        we can guarantee we know this thing is not checkable?]]]
        """
        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'radiobutton'
        indicators = self._script.formatting.getString(**args)
        if AXUtilities.is_checked(obj):
            result.append(indicators[1])
        else:
            result.append(indicators[0])
        return result

    def _generateChildWidget(self, obj, **args):
        widgetRoles = [Atspi.Role.CHECK_BOX,
                       Atspi.Role.COMBO_BOX,
                       Atspi.Role.PUSH_BUTTON,
                       Atspi.Role.RADIO_BUTTON,
                       Atspi.Role.SLIDER,
                       Atspi.Role.TOGGLE_BUTTON]

        def isWidget(x):
            return AXObject.get_role(x) in widgetRoles

        # For GtkListBox, such as those found in the control center
        if AXUtilities.is_list_box(AXObject.get_parent(obj)):
            widget = AXObject.find_descendant(obj, isWidget)
            if widget:
                return self.generate(widget, includeContext=False)

        return []

    def _generateSwitchState(self, obj, **args):
        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'switch'
        indicators = self._script.formatting.getString(**args)
        if AXUtilities.is_checked(obj) or AXUtilities.is_pressed(obj):
            result.append(indicators[1])
        else:
            result.append(indicators[0])
        return result

    def _generateToggleState(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the checked state of the object.  This is typically
        for check boxes. [[[WDW - should we return an empty array if
        we can guarantee we know this thing is not checkable?]]]
        """
        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'togglebutton'
        indicators = self._script.formatting.getString(**args)
        if AXUtilities.is_checked(obj) or AXUtilities.is_pressed(obj):
            result.append(indicators[1])
        else:
            result.append(indicators[0])
        return result

    def _generateCheckedStateIfCheckable(self, obj, **args):
        if AXUtilities.is_checkable(obj) or AXUtilities.is_check_menu_item(obj):
            return self._generateCheckedState(obj, **args)

        if AXUtilities.is_checked(obj):
            return self._generateCheckedState(obj, **args)

        return []

    def _generateMenuItemCheckedState(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the checked state of the menu item, only if it is
        checked. Otherwise, and empty array will be returned.
        """
        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'checkbox'
        indicators = self._script.formatting.getString(**args)
        if AXUtilities.is_checked(obj):
            result.append(indicators[1])
        return result

    def _generateExpandableState(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the expanded/collapsed state of an object, such as a
        tree node. If the object is not expandable, an empty array
        will be returned.
        """
        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'expansion'
        indicators = self._script.formatting.getString(**args)
        if AXUtilities.is_collapsed(obj):
            result.append(indicators[0])
        elif AXUtilities.is_expanded(obj):
            result.append(indicators[1])
        elif AXUtilities.is_expandable(obj):
            result.append(indicators[0])

        return result

    def _generateMultiselectableState(self, obj, **args):
        """Returns an array of strings (and possibly voice and audio
        specifications) that represent the multiselectable state of
        the object.  This is typically for list boxes. If the object
        is not multiselectable, an empty array will be returned.
        """

        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'multiselect'
        if AXUtilities.is_multiselectable(obj) and AXObject.get_child_count(obj):
            result.append(self._script.formatting.getString(**args))
        return result

    #####################################################################
    #                                                                   #
    # Table interface information                                       #
    #                                                                   #
    #####################################################################

    def _generateRowHeader(self, obj, **args):
        """Returns an array of strings to be used in speech and braille that
        represent the row header for an object that is in a table, if
        it exists.  Otherwise, an empty array is returned.
        """

        if args.get('readingRow'):
            return []

        result = []
        header = self._script.utilities.rowHeaderForCell(obj)
        if not header:
            return result

        text = self._script.utilities.displayedText(header)
        if not text:
            return result

        roleString =  self.getLocalizedRoleName(obj, role=Atspi.Role.ROW_HEADER)
        if args.get('mode') == 'speech':
            if settings.speechVerbosityLevel == settings.VERBOSITY_LEVEL_VERBOSE \
               and args.get('formatType') not in ['basicWhereAmI', 'detailedWhereAmI']:
                text = "%s %s" % (text, roleString)
        elif args.get('mode') == 'braille':
            text = "%s %s" % (text, roleString)

        result.append(text)
        return result

    def _generateColumnHeader(self, obj, **args):
        """Returns an array of strings (and possibly voice and audio
        specifications) that represent the column header for an object
        that is in a table, if it exists.  Otherwise, an empty array
        is returned.
        """
        result = []
        header = self._script.utilities.columnHeaderForCell(obj)
        if not header:
            return result

        text = self._script.utilities.displayedText(header)
        if not text:
            return result

        roleString =  self.getLocalizedRoleName(obj, role=Atspi.Role.COLUMN_HEADER)
        if args.get('mode') == 'speech':
            if settings.speechVerbosityLevel == settings.VERBOSITY_LEVEL_VERBOSE \
               and args.get('formatType') not in ['basicWhereAmI', 'detailedWhereAmI']:
                text = "%s %s" % (text, roleString)
        elif args.get('mode') == 'braille':
            text = "%s %s" % (text, roleString)

        result.append(text)
        return result

    def _generateSortOrder(self, obj, **args):
        description = self._script.utilities.getSortOrderDescription(obj)
        if not description:
            return []

        return [description]

    def _generateTableCell2ChildLabel(self, obj, **args):
        """Returns an array of strings for use by speech and braille for the
        label of a toggle in a table cell that has a special 2 child
        pattern that we run into.  Otherwise, an empty array is
        returned.
        """
        result = []

        # If this table cell has 2 children and one of them has a
        # 'toggle' action and the other does not, then present this
        # as a checkbox where:
        # 1) we get the checked state from the cell with the 'toggle' action
        # 2) we get the label from the other cell.
        # See Orca bug #376015 for more details.
        #
        if AXObject.get_child_count(obj) == 2:
            cellOrder = []
            hasToggle = [False, False]
            for i, child in enumerate(obj):
                if self._script.utilities.hasMeaningfulToggleAction(child):
                    hasToggle[i] = True
                    break
            if hasToggle[0] and not hasToggle[1]:
                cellOrder = [ 1, 0 ]
            elif not hasToggle[0] and hasToggle[1]:
                cellOrder = [ 0, 1 ]
            if cellOrder:
                for i in cellOrder:
                    if not hasToggle[i]:
                        result.extend(self.generate(AXObject.get_child(obj, i), **args))
        return result

    def _generateTableCell2ChildToggle(self, obj, **args):
        """Returns an array of strings for use by speech and braille for the
        toggle value of a toggle in a table cell that has a special 2
        child pattern that we run into.  Otherwise, an empty array is
        returned.
        """
        result = []

        # If this table cell has 2 children and one of them has a
        # 'toggle' action and the other does not, then present this
        # as a checkbox where:
        # 1) we get the checked state from the cell with the 'toggle' action
        # 2) we get the label from the other cell.
        # See Orca bug #376015 for more details.
        #
        if AXObject.get_child_count(obj) == 2:
            cellOrder = []
            hasToggle = [False, False]
            for i, child in enumerate(obj):
                if self._script.utilities.hasMeaningfulToggleAction(child):
                    hasToggle[i] = True
                    break
            if hasToggle[0] and not hasToggle[1]:
                cellOrder = [ 1, 0 ]
            elif not hasToggle[0] and hasToggle[1]:
                cellOrder = [ 0, 1 ]
            if cellOrder:
                for i in cellOrder:
                    if hasToggle[i]:
                        result.extend(self.generate(AXObject.get_child(obj, i), **args))
        return result

    def _generateColumnHeaderIfToggleAndNoText(self, obj, **args):
        """If this table cell has a "toggle" action, and doesn't have any
        label associated with it then also speak the table column
        header.  See Orca bug #455230 for more details.
        """
        # If we're reading just a single cell in speech, the new
        # header portion is going to give us this information.
        #
        if args['mode'] == 'speech' and not args.get('readingRow', False):
            return []

        result = []
        descendant = self._script.utilities.realActiveDescendant(obj)
        label = self._script.utilities.displayedText(descendant)
        if not label and self._script.utilities.hasMeaningfulToggleAction(obj):
            accHeader = self._script.utilities.columnHeaderForCell(obj)
            if (accHeader):
                result.append(AXObject.get_name(accHeader))
        return result

    def _generateRealTableCell(self, obj, **args):
        """Orca has a feature to automatically read an entire row of a table
        as the user arrows up/down the roles.  This leads to
        complexity in the code.  This method is used to return an
        array of strings for use by speech and braille for a single
        table cell itself.  The string, 'blank', is added for empty
        cells.
        """
        result = []
        oldRole = self._overrideRole('REAL_ROLE_TABLE_CELL', args)
        result.extend(self.generate(obj, **args))
        self._restoreRole(oldRole, args)
        return result

    def _generateTable(self, obj, **args):
        """Returns an array of strings for use by speech and braille to present
        the size of a table."""

        if self._script.utilities.isLayoutOnly(obj):
            return []

        if self._script.utilities.isSpreadSheetTable(obj):
            return []

        rows, cols = self._script.utilities.rowAndColumnCount(obj)

        # This suggests broken or missing table interface.
        if (rows < 0 or cols < 0) \
           and not self._script.utilities.rowOrColumnCountUnknown(obj):
            return []

        # This can happen if an author uses ARIA incorrectly, e.g. a grid whose
        # immediate child is a gridcell rather than a row. In that case, just
        # announce the role name.
        if rows == 0 and cols == 0:
            return self._generateRoleName(obj, **args)

        return [messages.tableSize(rows, cols)]

    def _generateTableCellRow(self, obj, **args):
        """Orca has a feature to automatically read an entire row of a table
        as the user arrows up/down the roles.  This leads to complexity in
        the code.  This method is used to return an array of strings
        (and possibly voice and audio specifications) for an entire row
        in a table if that's what the user has requested and if the row
        has changed.  Otherwise, it will return an array for just the
        current cell.
        """

        presentAll = args.get('readingRow') is True \
            or args.get('formatType') == 'detailedWhereAmI' \
            or self._mode == 'braille' \
            or self._script.utilities.shouldReadFullRow(obj)

        if not presentAll:
            return self._generateRealTableCell(obj, **args)

        args['readingRow'] = True
        result = []
        cells = self._script.utilities.getShowingCellsInSameRow(obj, forceFullRow=True)

        # Remove any pre-calcuated values which only apply to obj and not row cells.
        doNotInclude = ['startOffset', 'endOffset', 'string']
        otherCellArgs = args.copy()
        for arg in doNotInclude:
            otherCellArgs.pop(arg, None)

        for cell in cells:
            if cell == obj:
                cellResult = self._generateRealTableCell(cell, **args)
            else:
                cellResult = self._generateRealTableCell(cell, **otherCellArgs)
            if cellResult and result and self._mode == 'braille':
                result.append(braille.Region(object_properties.TABLE_CELL_DELIMITER_BRAILLE))
            result.extend(cellResult)

        result.extend(self._generatePositionInList(obj, **args))
        return result

    #####################################################################
    #                                                                   #
    # Text interface information                                        #
    #                                                                   #
    #####################################################################

    def _generateExpandedEOCs(self, obj, **args):
        """Returns the expanded embedded object characters for an object."""
        return []

    def _generateSubstring(self, obj, **args):
        start = args.get('startOffset')
        end = args.get('endOffset')
        if start is None or end is None:
            return []

        substring = args.get('string', self._script.utilities.substring(obj, start, end))
        if substring and self._script.EMBEDDED_OBJECT_CHARACTER not in substring:
            return [substring]

        return []

    def _generateStartOffset(self, obj, **args):
        return args.get('startOffset')

    def _generateEndOffset(self, obj, **args):
        return args.get('endOffset')

    def _generateCurrentLineText(self, obj, **args ):
        """Returns an array of strings for use by speech and braille
        that represents the current line of text, if
        this is a text object.  [[[WDW - consider returning an empty
        array if this is not a text object.]]]
        """
        result = self._generateSubstring(obj, **args)
        if result:
            return result

        [text, caretOffset, startOffset] = self._script.getTextLineAtCaret(obj)
        if text and self._script.EMBEDDED_OBJECT_CHARACTER not in text:
            return [text]

        return []

    def _generateDisplayedText(self, obj, **args ):
        """Returns an array of strings for use by speech and braille that
        represents all the text being displayed by the object.
        """
        result = self._generateSubstring(obj, **args)
        if result:
            return result

        displayedText = self._script.utilities.displayedText(obj)
        if not displayedText:
            return []

        return [displayedText]

    #####################################################################
    #                                                                   #
    # Tree interface information                                        #
    #                                                                   #
    #####################################################################

    def _generateNodeLevel(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represents the tree node level of the object, or an empty
        array if the object is not a tree node.
        """
        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'nodelevel'
        level = self._script.utilities.nodeLevel(obj)
        if level >= 0:
            result.append(self._script.formatting.getString(**args)\
                          % (level + 1))
        return result

    #####################################################################
    #                                                                   #
    # Value interface information                                       #
    #                                                                   #
    #####################################################################

    def _generateValue(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represents the value of the object.  This is typically the
        numerical value, but may also be the text of the 'value'
        attribute if it exists on the object.  [[[WDW - we should
        consider returning an empty array if there is no value.
        """

        role = args.get('role', AXObject.get_role(obj))
        if role == Atspi.Role.COMBO_BOX:
            value = self._script.utilities.getComboBoxValue(obj)
            return [value]

        if role == Atspi.Role.SEPARATOR and not AXUtilities.is_focused(obj):
            return []

        return [self._script.utilities.textForValue(obj)]

    #####################################################################
    #                                                                   #
    # Hierarchy and related dialog information                          #
    #                                                                   #
    #####################################################################

    def _generateApplicationName(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represents the name of the application for the object.
        """
        result = []
        name = AXObject.get_name(AXObject.get_application(obj))
        if name:
            result.append(name)
        return result

    def _generateNestingLevel(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represent the nesting level of an object in a list.
        """
        start = args.get('startOffset')
        end = args.get('endOffset')
        if start is not None and end is not None:
            return []

        result = []
        if not args.get('mode', None):
            args['mode'] = self._mode
        args['stringType'] = 'nestinglevel'
        nestingLevel = self._script.utilities.nestingLevel(obj)
        if nestingLevel:
            result.append(self._script.formatting.getString(**args)\
                          % nestingLevel)
        return result

    def _generateRadioButtonGroup(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represents the radio button group label for the object, or an
        empty array if the object has no such label.
        """
        if not AXUtilities.is_radio_button(obj):
            return []

        radioGroupLabel = None
        relation = AXObject.get_relation(obj, Atspi.RelationType.LABELLED_BY)
        if relation:
            radioGroupLabel = relation.get_target(0)
        if radioGroupLabel:
            return [self._script.utilities.displayedText(radioGroupLabel)]

        parent = AXObject.get_parent_checked(obj)
        while parent:
            if AXUtilities.is_panel(parent) or AXUtilities.is_filler(parent):
                label = self._generateLabelAndName(parent)
                if label:
                    return label
            parent = AXObject.get_parent_checked(parent)
        return []

    def _generateRealActiveDescendantDisplayedText(self, obj, **args ):
        """Objects, such as tables and trees, can represent individual cells
        via a complicated nested hierarchy.  This method returns an
        array of strings for use by speech and braille that represents
        the text actually being painted in the cell, if it can be
        found.  Otherwise, an empty array is returned.
        """
        rad = self._script.utilities.realActiveDescendant(obj)

        if not (AXUtilities.is_table_cell(rad) and AXObject.get_child_count(rad)):
            return self._generateDisplayedText(rad, **args)

        content = set([self._script.utilities.displayedText(x).strip() for x in rad])
        rv = " ".join(filter(lambda x: x, content))
        if not rv:
            return self._generateDisplayedText(rad, **args)
        return [rv]

    def _generateRealActiveDescendantRoleName(self, obj, **args ):
        """Objects, such as tables and trees, can represent individual cells
        via a complicated nested hierarchy.  This method returns an
        array of strings for use by speech and braille that represents
        the role of the object actually being painted in the cell.
        """
        rad = self._script.utilities.realActiveDescendant(obj)
        args['role'] = AXObject.get_role(rad)
        return self._generateRoleName(rad, **args)

    def _generateNamedContainingPanel(self, obj, **args):
        """Returns an array of strings for use by speech and braille that
        represents the nearest ancestor of an object which is a named panel.
        """
        result = []
        parent = AXObject.get_parent_checked(obj)
        while parent:
            if AXUtilities.is_panel(parent):
                label = self._generateLabelAndName(parent)
                if label:
                    result.extend(label)
                    break
            parent = AXObject.get_parent_checked(parent)
        return result

    def _generatePageSummary(self, obj, **args):
        return []

    def _generatePositionInList(self, obj, **args):
        return []

    def _generateProgressBarIndex(self, obj, **args):
        return []

    def _generateProgressBarValue(self, obj, **args):
        return []

    def _getProgressBarUpdateInterval(self):
        return int(_settingsManager.getSetting('progressBarUpdateInterval'))

    def _shouldPresentProgressBarUpdate(self, obj, **args):
        percent = self._script.utilities.getValueAsPercent(obj)
        lastTime, lastValue = self.getProgressBarUpdateTimeAndValue(obj, type=self)
        if percent == lastValue:
            msg = "GENERATOR: Not presenting update for %s. Value still %s" % (obj, percent)
            debug.println(debug.LEVEL_INFO, msg, True)
            return False

        if percent == 100:
            return True

        interval = int(time.time() - lastTime)
        return interval >= self._getProgressBarUpdateInterval()

    def _cleanUpCachedProgressBars(self):
        def isValid(x):
            return not (self._script.utilities.isZombie(x) or self._script.utilities.isDead(x))

        bars = list(filter(isValid, self._activeProgressBars))
        self._activeProgressBars = {x:self._activeProgressBars.get(x) for x in bars}

    def _getMostRecentProgressBarUpdate(self):
        self._cleanUpCachedProgressBars()
        if not self._activeProgressBars.values():
            return None, 0.0, None

        sortedValues = sorted(self._activeProgressBars.values(), key=lambda x: x[0])
        prevTime, prevValue = sortedValues[-1]
        return list(self._activeProgressBars.keys())[-1], prevTime, prevValue

    def getProgressBarNumberAndCount(self, obj):
        self._cleanUpCachedProgressBars()
        if obj not in self._activeProgressBars:
            self._activeProgressBars[obj] = 0.0, None

        thisValue = self.getProgressBarUpdateTimeAndValue(obj)
        index = list(self._activeProgressBars.values()).index(thisValue)
        return index + 1, len(self._activeProgressBars)

    def getProgressBarUpdateTimeAndValue(self, obj, **args):
        if obj not in self._activeProgressBars:
            self._activeProgressBars[obj] = 0.0, None

        return self._activeProgressBars.get(obj)

    def setProgressBarUpdateTimeAndValue(self, obj, lastTime=None, lastValue=None):
        lastTime = lastTime or time.time()
        lastValue = lastValue or self._script.utilities.getValueAsPercent(obj)
        self._activeProgressBars[obj] = lastTime, lastValue

    def _getAlternativeRole(self, obj, **args):
        if self._script.utilities.isMath(obj):
            if self._script.utilities.isMathSubOrSuperScript(obj):
                return 'ROLE_MATH_SCRIPT_SUBSUPER'
            if self._script.utilities.isMathUnderOrOverScript(obj):
                return 'ROLE_MATH_SCRIPT_UNDEROVER'
            if self._script.utilities.isMathMultiScript(obj):
                return 'ROLE_MATH_MULTISCRIPT'
            if self._script.utilities.isMathEnclose(obj):
                return 'ROLE_MATH_ENCLOSED'
            if self._script.utilities.isMathFenced(obj):
                return 'ROLE_MATH_FENCED'
            if self._script.utilities.isMathTable(obj):
                return 'ROLE_MATH_TABLE'
            if self._script.utilities.isMathTableRow(obj):
                return 'ROLE_MATH_TABLE_ROW'
        if self._script.utilities.isDPub(obj):
            if self._script.utilities.isLandmark(obj):
                return 'ROLE_DPUB_LANDMARK'
            if AXUtilities.is_section(obj):
                return 'ROLE_DPUB_SECTION'
        if self._script.utilities.isSwitch(obj):
            return 'ROLE_SWITCH'
        if self._script.utilities.isAnchor(obj):
            return Atspi.Role.STATIC
        if self._script.utilities.isBlockquote(obj):
            return Atspi.Role.BLOCK_QUOTE
        if self._script.utilities.isComment(obj):
            return Atspi.Role.COMMENT
        if self._script.utilities.isContentDeletion(obj):
            return 'ROLE_CONTENT_DELETION'
        if self._script.utilities.isContentError(obj):
            return 'ROLE_CONTENT_ERROR'
        if self._script.utilities.isContentInsertion(obj):
            return 'ROLE_CONTENT_INSERTION'
        if self._script.utilities.isContentMarked(obj):
            return 'ROLE_CONTENT_MARK'
        if self._script.utilities.isContentSuggestion(obj):
            return 'ROLE_CONTENT_SUGGESTION'
        if self._script.utilities.isDescriptionList(obj):
            return Atspi.Role.DESCRIPTION_LIST
        if self._script.utilities.isDescriptionListTerm(obj):
            return Atspi.Role.DESCRIPTION_TERM
        if self._script.utilities.isDescriptionListDescription(obj):
            return Atspi.Role.DESCRIPTION_VALUE
        if self._script.utilities.isFeedArticle(obj):
            return 'ROLE_ARTICLE_IN_FEED'
        if self._script.utilities.isFeed(obj):
            return 'ROLE_FEED'
        if self._script.utilities.isLandmark(obj):
            if self._script.utilities.isLandmarkRegion(obj):
                return 'ROLE_REGION'
            return Atspi.Role.LANDMARK
        if self._script.utilities.isFocusableLabel(obj):
            return Atspi.Role.LIST_ITEM
        if self._script.utilities.isDocument(obj) and AXObject.supports_image(obj):
            return Atspi.Role.IMAGE

        return args.get('role', AXObject.get_role(obj))

    def getLocalizedRoleName(self, obj, **args):
        role = args.get('role', AXObject.get_role(obj))

        if AXObject.supports_value(obj):
            if AXUtilities.is_horizontal_slider(obj):
                return object_properties.ROLE_SLIDER_HORIZONTAL
            if AXUtilities.is_vertical_slider(obj):
                return object_properties.ROLE_SLIDER_VERTICAL
            if AXUtilities.is_horizontal_scrollbar(obj):
                return object_properties.ROLE_SCROLL_BAR_HORIZONTAL
            if AXUtilities.is_vertical_scrollbar(obj):
                return object_properties.ROLE_SCROLL_BAR_VERTICAL
            if AXUtilities.is_horizontal_separator(obj):
                return object_properties.ROLE_SPLITTER_HORIZONTAL
            if AXUtilities.is_vertical_separator(obj):
                return object_properties.ROLE_SPLITTER_VERTICAL
            if AXUtilities.is_split_pane(obj) \
               and (AXUtilities.is_focused(obj) or args.get('alreadyFocused', False)):
                # The splitter has the opposite orientation of the split pane.
                if AXUtilities.is_horizontal(obj):
                    return object_properties.ROLE_SPLITTER_VERTICAL
                if AXUtilities.is_vertical(obj):
                    return object_properties.ROLE_SPLITTER_HORIZONTAL

        if self._script.utilities.isContentSuggestion(obj):
            return object_properties.ROLE_CONTENT_SUGGESTION

        if self._script.utilities.isFeed(obj):
            return object_properties.ROLE_FEED

        if self._script.utilities.isFigure(obj):
            return object_properties.ROLE_FIGURE

        if self._script.utilities.isMenuButton(obj):
            return object_properties.ROLE_MENU_BUTTON

        if self._script.utilities.isSwitch(obj):
            return object_properties.ROLE_SWITCH

        if self._script.utilities.isDPub(obj):
            if self._script.utilities.isLandmark(obj):
                if self._script.utilities.isDPubAcknowledgments(obj):
                    return object_properties.ROLE_ACKNOWLEDGMENTS
                if self._script.utilities.isDPubAfterword(obj):
                    return object_properties.ROLE_AFTERWORD
                if self._script.utilities.isDPubAppendix(obj):
                    return object_properties.ROLE_APPENDIX
                if self._script.utilities.isDPubBibliography(obj):
                    return object_properties.ROLE_BIBLIOGRAPHY
                if self._script.utilities.isDPubChapter(obj):
                    return object_properties.ROLE_CHAPTER
                if self._script.utilities.isDPubConclusion(obj):
                    return object_properties.ROLE_CONCLUSION
                if self._script.utilities.isDPubCredits(obj):
                    return object_properties.ROLE_CREDITS
                if self._script.utilities.isDPubEndnotes(obj):
                    return object_properties.ROLE_ENDNOTES
                if self._script.utilities.isDPubEpilogue(obj):
                    return object_properties.ROLE_EPILOGUE
                if self._script.utilities.isDPubErrata(obj):
                    return object_properties.ROLE_ERRATA
                if self._script.utilities.isDPubForeword(obj):
                    return object_properties.ROLE_FOREWORD
                if self._script.utilities.isDPubGlossary(obj):
                    return object_properties.ROLE_GLOSSARY
                if self._script.utilities.isDPubIndex(obj):
                    return object_properties.ROLE_INDEX
                if self._script.utilities.isDPubIntroduction(obj):
                    return object_properties.ROLE_INTRODUCTION
                if self._script.utilities.isDPubPagelist(obj):
                    return object_properties.ROLE_PAGELIST
                if self._script.utilities.isDPubPart(obj):
                    return object_properties.ROLE_PART
                if self._script.utilities.isDPubPreface(obj):
                    return object_properties.ROLE_PREFACE
                if self._script.utilities.isDPubPrologue(obj):
                    return object_properties.ROLE_PROLOGUE
                if self._script.utilities.isDPubToc(obj):
                    return object_properties.ROLE_TOC
            elif role == "ROLE_DPUB_SECTION":
                if self._script.utilities.isDPubAbstract(obj):
                    return object_properties.ROLE_ABSTRACT
                if self._script.utilities.isDPubColophon(obj):
                    return object_properties.ROLE_COLOPHON
                if self._script.utilities.isDPubCredit(obj):
                    return object_properties.ROLE_CREDIT
                if self._script.utilities.isDPubDedication(obj):
                    return object_properties.ROLE_DEDICATION
                if self._script.utilities.isDPubEpigraph(obj):
                    return object_properties.ROLE_EPIGRAPH
                if self._script.utilities.isDPubExample(obj):
                    return object_properties.ROLE_EXAMPLE
                if self._script.utilities.isDPubPullquote(obj):
                    return object_properties.ROLE_PULLQUOTE
                if self._script.utilities.isDPubQna(obj):
                    return object_properties.ROLE_QNA
            elif role == Atspi.Role.LIST_ITEM:
                if self._script.utilities.isDPubBiblioentry(obj):
                    return object_properties.ROLE_BIBLIOENTRY
                if self._script.utilities.isDPubEndnote(obj):
                    return object_properties.ROLE_ENDNOTE
            else:
                if self._script.utilities.isDPubCover(obj):
                    return object_properties.ROLE_COVER
                if self._script.utilities.isDPubPagebreak(obj):
                    return object_properties.ROLE_PAGEBREAK
                if self._script.utilities.isDPubSubtitle(obj):
                    return object_properties.ROLE_SUBTITLE

        if self._script.utilities.isLandmark(obj):
            if self._script.utilities.isLandmarkWithoutType(obj):
                return ''
            if self._script.utilities.isLandmarkBanner(obj):
                return object_properties.ROLE_LANDMARK_BANNER
            if self._script.utilities.isLandmarkComplementary(obj):
                return object_properties.ROLE_LANDMARK_COMPLEMENTARY
            if self._script.utilities.isLandmarkContentInfo(obj):
                return object_properties.ROLE_LANDMARK_CONTENTINFO
            if self._script.utilities.isLandmarkMain(obj):
                return object_properties.ROLE_LANDMARK_MAIN
            if self._script.utilities.isLandmarkNavigation(obj):
                return object_properties.ROLE_LANDMARK_NAVIGATION
            if self._script.utilities.isLandmarkRegion(obj):
                return object_properties.ROLE_LANDMARK_REGION
            if self._script.utilities.isLandmarkSearch(obj):
                return object_properties.ROLE_LANDMARK_SEARCH
            if self._script.utilities.isLandmarkForm(obj):
                role = Atspi.Role.FORM
        elif self._script.utilities.isComment(obj):
            role = Atspi.Role.COMMENT

        if not isinstance(role, Atspi.Role):
            try:
                return obj.getLocalizedRoleName()
            except Exception:
                return ''

        nonlocalized = Atspi.role_get_name(role)
        atkRole = Atk.role_for_name(nonlocalized)
        if atkRole == Atk.Role.INVALID and role == Atspi.Role.STATUS_BAR:
            atkRole = Atk.role_for_name("statusbar")

        return Atk.role_get_localized_name(atkRole)

    def getStateIndicator(self, obj, **args):
        if self._script.utilities.isSwitch(obj):
            return self._generateSwitchState(obj, **args)

        role = args.get('role', AXObject.get_role(obj))

        if role == Atspi.Role.MENU_ITEM:
            return self._generateMenuItemCheckedState(obj, **args)

        if role in [Atspi.Role.RADIO_BUTTON, Atspi.Role.RADIO_MENU_ITEM]:
            return self._generateRadioState(obj, **args)

        if role in [Atspi.Role.CHECK_BOX, Atspi.Role.CHECK_MENU_ITEM]:
            return self._generateCheckedState(obj, **args)

        if role == Atspi.Role.TOGGLE_BUTTON:
            return self._generateToggleState(obj, **args)

        if role == Atspi.Role.TABLE_CELL:
            return self._generateCellCheckedState(obj, **args)

        return []

    def getValue(self, obj, **args):
        role = args.get('role', AXObject.get_role(obj))

        if role == Atspi.Role.PROGRESS_BAR:
            return self._generateProgressBarValue(obj, **args)

        if role in [Atspi.Role.SCROLL_BAR, Atspi.Role.SLIDER]:
            return self._generatePercentage(obj, **args)

        return []
