#!/usr/bin/python

"""Test of line navigation."""

from macaroon.playback import *
import utils

sequence = MacroSequence()

sequence.append(PauseAction(3000))
sequence.append(KeyComboAction("<Control>End"))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "1. Line Up",
    ["BRAILLE LINE:  'separator'",
     "     VISIBLE:  'separator', cursor=0",
     "SPEECH OUTPUT: 'separator'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "2. Line Up",
    ["BRAILLE LINE:  'And push button Add another boolean chart push button'",
     "     VISIBLE:  'And push button Add another bool', cursor=1",
     "SPEECH OUTPUT: 'And'",
     "SPEECH OUTPUT: 'push button'",
     "SPEECH OUTPUT: 'Add another boolean chart'",
     "SPEECH OUTPUT: 'push button'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "3. Line Up",
    ["BRAILLE LINE:  '--- combo box --- combo box $l Or push button'",
     "     VISIBLE:  '--- combo box --- combo box $l O', cursor=0",
     "SPEECH OUTPUT: '---'",
     "SPEECH OUTPUT: 'combo box'",
     "SPEECH OUTPUT: '---'",
     "SPEECH OUTPUT: 'combo box'",
     "SPEECH OUTPUT: 'entry'",
     "SPEECH OUTPUT: 'Or'",
     "SPEECH OUTPUT: 'push button'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "4. Line Up",
    ["BRAILLE LINE:  '< > check box Not (negate this whole chart)'",
     "     VISIBLE:  '< > check box Not \(negate this w', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'not checked'",
     "SPEECH OUTPUT: ' Not (negate this whole chart) '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "5. Line Up",
    ["BRAILLE LINE:  'Advanced Searching Using Boolean Charts:'",
     "     VISIBLE:  'Advanced Searching Using Boolean', cursor=1",
     "SPEECH OUTPUT: 'Advanced Searching Using Boolean Charts: '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "6. Line Up",
    ["BRAILLE LINE:  'separator'",
     "     VISIBLE:  'separator', cursor=0",
     "SPEECH OUTPUT: 'separator'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "7. Line Up",
    ["BRAILLE LINE:  '< > check box and remember these as my default search options'",
     "     VISIBLE:  '< > check box and remember these', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'not checked'",
     "SPEECH OUTPUT: ' and remember these as my default search options '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "8. Line Up",
    ["BRAILLE LINE:  'Search push button'",
     "     VISIBLE:  'Search push button', cursor=1",
     "SPEECH OUTPUT: 'Search'",
     "SPEECH OUTPUT: 'push button'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "9. Line Up",
    ["BRAILLE LINE:  'Sort results by: Reuse same sort as last time combo box'",
     "     VISIBLE:  'Sort results by: Reuse same sort', cursor=1",
     "SPEECH OUTPUT: 'Sort results by: '",
     "SPEECH OUTPUT: 'Reuse same sort as last time'",
     "SPEECH OUTPUT: 'combo box'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "10. Line Up",
    ["BRAILLE LINE:  'Unspecified list box'",
     "     VISIBLE:  'Unspecified list box', cursor=0",
     "SPEECH OUTPUT: 'GNOME target:'",
     "SPEECH OUTPUT: 'Unspecified'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 12 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "11. Line Up",
    ["BRAILLE LINE:  'GNOME target:'",
     "     VISIBLE:  'GNOME target:', cursor=1",
     "SPEECH OUTPUT: 'GNOME target:'",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "12. Line Up",
    ["BRAILLE LINE:  'Unspecified list box'",
     "     VISIBLE:  'Unspecified list box', cursor=0",
     "SPEECH OUTPUT: 'GNOME version:'",
     "SPEECH OUTPUT: 'Unspecified'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 14 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "13. Line Up",
    ["BRAILLE LINE:  'GNOME version:'",
     "     VISIBLE:  'GNOME version:', cursor=1",
     "SPEECH OUTPUT: 'GNOME version:'",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "14. Line Up",
    ["BRAILLE LINE:  ' $l'",
     "     VISIBLE:  ' $l', cursor=0",
     "SPEECH OUTPUT: 'entry'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "15. Line Up",
    ["BRAILLE LINE:  'and the new value was:'",
     "     VISIBLE:  'and the new value was:', cursor=1",
     "SPEECH OUTPUT: 'and the new value was:'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "16. Line Up",
    ["BRAILLE LINE:  '[Bug creation] list box'",
     "     VISIBLE:  '[Bug creation] list box', cursor=0",
     "SPEECH OUTPUT: 'where one or more of the following changed:'",
     "SPEECH OUTPUT: '[Bug creation]'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 26 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "17. Line Up",
    ["BRAILLE LINE:  'where one or more of the following changed:'",
     "     VISIBLE:  'where one or more of the followi', cursor=1",
     "SPEECH OUTPUT: 'where one or more of the following changed:'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "18. Line Up",
    ["BRAILLE LINE:  '(YYYY-MM-DD or relative dates)'",
     "     VISIBLE:  '(YYYY-MM-DD or relative dates)', cursor=1",
     "SPEECH OUTPUT: '(YYYY-MM-DD or relative dates) '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "19. Line Up",
    ["BRAILLE LINE:  ' $l and'",
     "     VISIBLE:  ' $l and', cursor=0",
     "SPEECH OUTPUT: 'entry'",
     "SPEECH OUTPUT: 'and '",
     "SPEECH OUTPUT: 'entry'",
     "SPEECH OUTPUT: 'Now'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "20. Line Up",
    ["BRAILLE LINE:  'Only bugs changed between:'",
     "     VISIBLE:  'Only bugs changed between:', cursor=1",
     "SPEECH OUTPUT: 'Only bugs changed between:'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "21. Line Up",
    ["BRAILLE LINE:  'Bug Changes'",
     "     VISIBLE:  'Bug Changes', cursor=1",
     "SPEECH OUTPUT: 'Bug Changes'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "22. Line Up",
    ["BRAILLE LINE:  '(comma-separated list)'",
     "     VISIBLE:  '(comma-separated list)', cursor=0",
     "SPEECH OUTPUT: '(comma-separated list)'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "23. Line Up",
    ["BRAILLE LINE:  'Only include combo box bugs numbered:  $l'",
     "     VISIBLE:  'Only include combo box bugs numb', cursor=0",
     "SPEECH OUTPUT: 'Only include'",
     "SPEECH OUTPUT: 'combo box'",
     "SPEECH OUTPUT: 'bugs numbered: '",
     "SPEECH OUTPUT: 'entry'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "24. Line Up",
    ["BRAILLE LINE:  'separator'",
     "     VISIBLE:  'separator', cursor=0",
     "SPEECH OUTPUT: 'separator'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "25. Line Up",
    ["BRAILLE LINE:  ' $l'",
     "     VISIBLE:  ' $l', cursor=0",
     "SPEECH OUTPUT: 'entry'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "26. Line Up",
    ["BRAILLE LINE:  'contains combo box'",
     "     VISIBLE:  'contains combo box', cursor=0",
     "SPEECH OUTPUT: 'contains'",
     "SPEECH OUTPUT: 'combo box'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "27. Line Up",
    ["BRAILLE LINE:  '< > check box a commenter'",
     "     VISIBLE:  '< > check box a commenter', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'not checked'",
     "SPEECH OUTPUT: 'a commenter '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "28. Line Up",
    ["BRAILLE LINE:  '<x> check box a CC list member'",
     "     VISIBLE:  '<x> check box a CC list member', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'checked'",
     "SPEECH OUTPUT: ' a CC list member '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "29. Line Up",
    ["BRAILLE LINE:  '<x> check box the QA contact'",
     "     VISIBLE:  '<x> check box the QA contact', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'checked'",
     "SPEECH OUTPUT: ' the QA contact '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "30. Line Up",
    ["BRAILLE LINE:  '<x> check box the reporter'",
     "     VISIBLE:  '<x> check box the reporter', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'checked'",
     "SPEECH OUTPUT: ' the reporter '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "31. Line Up",
    ["BRAILLE LINE:  '<x> check box the bug assignee'",
     "     VISIBLE:  '<x> check box the bug assignee', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'checked'",
     "SPEECH OUTPUT: ' the bug assignee '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "32. Line Up",
    ["BRAILLE LINE:  'Any one of:'",
     "     VISIBLE:  'Any one of:', cursor=1",
     "SPEECH OUTPUT: 'Any one of: '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "33. Line Up",
    ["BRAILLE LINE:  ' $l'",
     "     VISIBLE:  ' $l', cursor=0",
     "SPEECH OUTPUT: 'entry'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "34. Line Up",
    ["BRAILLE LINE:  'contains combo box'",
     "     VISIBLE:  'contains combo box', cursor=0",
     "SPEECH OUTPUT: 'contains'",
     "SPEECH OUTPUT: 'combo box'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "35. Line Up",
    ["BRAILLE LINE:  '< > check box a commenter'",
     "     VISIBLE:  '< > check box a commenter', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'not checked'",
     "SPEECH OUTPUT: 'a commenter '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "36. Line Up",
    ["BRAILLE LINE:  '< > check box a CC list member'",
     "     VISIBLE:  '< > check box a CC list member', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'not checked'",
     "SPEECH OUTPUT: ' a CC list member '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "37. Line Up",
    ["BRAILLE LINE:  '< > check box the QA contact'",
     "     VISIBLE:  '< > check box the QA contact', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'not checked'",
     "SPEECH OUTPUT: ' the QA contact '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "38. Line Up",
    ["BRAILLE LINE:  '< > check box the reporter'",
     "     VISIBLE:  '< > check box the reporter', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'not checked'",
     "SPEECH OUTPUT: ' the reporter '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "39. Line Up",
    ["BRAILLE LINE:  '<x> check box the bug assignee'",
     "     VISIBLE:  '<x> check box the bug assignee', cursor=0",
     "SPEECH OUTPUT: 'check box'",
     "SPEECH OUTPUT: 'checked'",
     "SPEECH OUTPUT: ' the bug assignee '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "40. Line Up",
    ["BRAILLE LINE:  'Any one of:'",
     "     VISIBLE:  'Any one of:', cursor=1",
     "SPEECH OUTPUT: 'Any one of: '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "41. Line Up",
    ["BRAILLE LINE:  'Email and Numbering'",
     "     VISIBLE:  'Email and Numbering', cursor=1",
     "SPEECH OUTPUT: 'Email and Numbering '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "42. Line Up",
    ["BRAILLE LINE:  'All list box'",
     "     VISIBLE:  'All list box', cursor=0",
     "SPEECH OUTPUT: 'OS:'",
     "SPEECH OUTPUT: 'All'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 21 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "43. Line Up",
    ["BRAILLE LINE:  'OS:'",
     "     VISIBLE:  'OS:', cursor=1",
     "SPEECH OUTPUT: 'OS:'",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "44. Line Up",
    ["BRAILLE LINE:  'Immediate list box'",
     "     VISIBLE:  'Immediate list box', cursor=0",
     "SPEECH OUTPUT: 'Priority:'",
     "SPEECH OUTPUT: 'Immediate'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 5 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "45. Line Up",
    ["BRAILLE LINE:  'Priority:'",
     "     VISIBLE:  'Priority:', cursor=1",
     "SPEECH OUTPUT: 'Priority:'",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "46. Line Up",
    ["BRAILLE LINE:  'blocker list box'",
     "     VISIBLE:  'blocker list box', cursor=0",
     "SPEECH OUTPUT: 'Severity:'",
     "SPEECH OUTPUT: 'blocker'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 7 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "47. Line Up",
    ["BRAILLE LINE:  'Severity:'",
     "     VISIBLE:  'Severity:', cursor=1",
     "SPEECH OUTPUT: 'Severity:'",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "48. Line Up",
    ["BRAILLE LINE:  'FIXED list box'",
     "     VISIBLE:  'FIXED list box', cursor=0",
     "SPEECH OUTPUT: 'Resolution:'",
     "SPEECH OUTPUT: 'FIXED'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 12 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "49. Line Up",
    ["BRAILLE LINE:  'Resolution:'",
     "     VISIBLE:  'Resolution:', cursor=1",
     "SPEECH OUTPUT: 'Resolution: '",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "50. Line Up",
    ["BRAILLE LINE:  'UNCONFIRMED NEW ASSIGNED REOPENED NEEDINFO list box'",
     "     VISIBLE:  'UNCONFIRMED NEW ASSIGNED REOPENE', cursor=0",
     "SPEECH OUTPUT: 'Status:'",
     "SPEECH OUTPUT: 'UNCONFIRMED'",
     "SPEECH OUTPUT: 'NEW'",
     "SPEECH OUTPUT: 'ASSIGNED'",
     "SPEECH OUTPUT: 'REOPENED'",
     "SPEECH OUTPUT: 'NEEDINFO'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 8 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "51. Line Up",
    ["BRAILLE LINE:  'Status:'",
     "     VISIBLE:  'Status:', cursor=1",
     "SPEECH OUTPUT: 'Status:'",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "52. Line Up",
    ["BRAILLE LINE:  'separator'",
     "     VISIBLE:  'separator', cursor=0",
     "SPEECH OUTPUT: 'separator'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "53. Line Up",
    ["BRAILLE LINE:  'Keywords: contains all of the keywords combo box $l'",
     "     VISIBLE:  'Keywords: contains all of the ke', cursor=1",
     "SPEECH OUTPUT: 'Keywords'",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: ': '",
     "SPEECH OUTPUT: 'row header'",
     "SPEECH OUTPUT: 'contains all of the keywords'",
     "SPEECH OUTPUT: 'combo box'",
     "SPEECH OUTPUT: 'entry'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "54. Line Up",
    ["BRAILLE LINE:  'Whiteboard: contains all of the words/strings combo box $l'",
     "     VISIBLE:  'Whiteboard: contains all of the ', cursor=1",
     "SPEECH OUTPUT: 'Whiteboard:'",
     "SPEECH OUTPUT: 'row header'",
     "SPEECH OUTPUT: 'contains all of the words/strings'",
     "SPEECH OUTPUT: 'combo box'",
     "SPEECH OUTPUT: 'entry'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "55. Line Up",
    ["BRAILLE LINE:  'A Comment: contains the string combo box $l'",
     "     VISIBLE:  'A Comment: contains the string c', cursor=1",
     "SPEECH OUTPUT: 'A Comment:'",
     "SPEECH OUTPUT: 'row header'",
     "SPEECH OUTPUT: 'contains the string'",
     "SPEECH OUTPUT: 'combo box'",
     "SPEECH OUTPUT: 'entry'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "56. Line Up",
    ["BRAILLE LINE:  '--- list box'",
     "     VISIBLE:  '--- list box', cursor=0",
     "SPEECH OUTPUT: 'Target Milestone:'",
     "SPEECH OUTPUT: '---'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 555 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "57. Line Up",
    ["BRAILLE LINE:  'Target Milestone:'",
     "     VISIBLE:  'Target Milestone:', cursor=1",
     "SPEECH OUTPUT: 'Target Milestone:'",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "58. Line Up",
    ["BRAILLE LINE:  '0.0.1 list box'",
     "     VISIBLE:  '0.0.1 list box', cursor=0",
     "SPEECH OUTPUT: 'Version:'",
     "SPEECH OUTPUT: '0.0.1'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 857 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "59. Line Up",
    ["BRAILLE LINE:  'Version:'",
     "     VISIBLE:  'Version:', cursor=1",
     "SPEECH OUTPUT: 'Version:'",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "60. Line Up",
    ["BRAILLE LINE:  'abiscan list box'",
     "     VISIBLE:  'abiscan list box', cursor=0",
     "SPEECH OUTPUT: 'Component:'",
     "SPEECH OUTPUT: 'abiscan'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 1248 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "61. Line Up",
    ["BRAILLE LINE:  'Component:'",
     "     VISIBLE:  'Component:', cursor=1",
     "SPEECH OUTPUT: 'Component'",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: ': '",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "62. Line Up",
    ["BRAILLE LINE:  'accerciser list box'",
     "     VISIBLE:  'accerciser list box', cursor=0",
     "SPEECH OUTPUT: 'Product:'",
     "SPEECH OUTPUT: 'accerciser'",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 379 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "63. Line Up",
    ["BRAILLE LINE:  'Product:'",
     "     VISIBLE:  'Product:', cursor=1",
     "SPEECH OUTPUT: 'Product:'",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "64. Line Up",
    ["BRAILLE LINE:  'Admin  list box'",
     "     VISIBLE:  'Admin  list box', cursor=0",
     "SPEECH OUTPUT: 'Classification:'",
     "SPEECH OUTPUT: 'Admin '",
     "SPEECH OUTPUT: 'multi-select'",
     "SPEECH OUTPUT: 'List with 8 items'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "65. Line Up",
    ["BRAILLE LINE:  'Classification:'",
     "     VISIBLE:  'Classification:', cursor=1",
     "SPEECH OUTPUT: 'Classification:'",
     "SPEECH OUTPUT: 'column header'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "66. Line Up",
    ["BRAILLE LINE:  'Summary: contains all of the words/strings combo box $l Search push button'",
     "     VISIBLE:  'Summary: contains all of the wor', cursor=1",
     "SPEECH OUTPUT: 'Summary:'",
     "SPEECH OUTPUT: 'row header'",
     "SPEECH OUTPUT: 'contains all of the words/strings'",
     "SPEECH OUTPUT: 'combo box'",
     "SPEECH OUTPUT: 'entry'",
     "SPEECH OUTPUT: 'Search'",
     "SPEECH OUTPUT: 'push button'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "67. Line Up",
    ["BRAILLE LINE:  'Give me some help (reloads page.)'",
     "     VISIBLE:  'Give me some help (reloads page.', cursor=1",
     "SPEECH OUTPUT: 'Give me some help'",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: ' (reloads page.)'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "68. Line Up",
    ["BRAILLE LINE:  'Short Bug Search Form Complicated Bug Search Form'",
     "     VISIBLE:  'Short Bug Search Form Complicate', cursor=0",
     "SPEECH OUTPUT: 'Short Bug Search Form '",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: 'Complicated Bug Search Form '"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Up"))
sequence.append(utils.AssertPresentationAction(
    "69. Line Up",
    ["BRAILLE LINE:  'New bug · Browse · Search · Reports · Account · Admin · Help Logged In joanmarie.diggs@gmail.com | Log Out'",
     "     VISIBLE:  'New bug · Browse · Search · Repo', cursor=1",
     "SPEECH OUTPUT: 'New bug'",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: ' · '",
     "SPEECH OUTPUT: 'Browse'",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: ' · '",
     "SPEECH OUTPUT: 'Search'",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: ' · '",
     "SPEECH OUTPUT: 'Reports'",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: ' · '",
     "SPEECH OUTPUT: 'Account'",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: ' · '",
     "SPEECH OUTPUT: 'Admin'",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: ' · '",
     "SPEECH OUTPUT: 'Help'",
     "SPEECH OUTPUT: 'link'",
     "SPEECH OUTPUT: 'Logged In joanmarie.diggs@gmail.com | '",
     "SPEECH OUTPUT: 'Log Out'",
     "SPEECH OUTPUT: 'link'"]))

sequence.append(utils.AssertionSummaryAction())
sequence.start()
