from dragonfly import Dictation, MappingRule
from castervoice.lib.actions import Key, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R


class EmacsRule(MappingRule):
    mapping = {
        # global
        "(cancel|quit)": R(Key("c-g")),
        "undo that": R(Key("c-underscore")),
        "kill emacs": R(Key("c-x, c-c")),
        "open file": R(Key("c-x, c-f")),
        "save file": R(Key("c-x, c-s")),
        "save as": R(Key("c-x, c-w")),
        "save all": R(Key("c-x, s")),
        "revert to file": R(Key("c-x, c-v")),
        "revert buffer": R(Key("a-x")),
        "kill buffer": R(Key("c-x, k")),
        "switch buffer": R(Key("c-x, b")),
        "begin selection": R(Key("c-space")),
        "cancel selection": R(Key("c-g")),
        "cut selection": R(Key("c-w")),
        "paste": R(Key("c-y")),
        "copy number <n>": R(Key("c-x, r, s, %(n)d")),
        "paste number <n>": R(Key("c-x, r, i, %(n)d")),
        # delete
        "forward delete": R(Key("c-d")),
        "delete word": R(Key("a-backspace")),
        "forward delete word": R(Key("a-d")),
        # move
        "go to line <n>": R(Key("a-g, a-g") + Text("%(n)d") + Key("enter")),
        "word forward": R(Key("a-f")),
        "word backward": R(Key("a-b")),
        "line forward": R(Key("c-e")),
        "line backward": R(Key("c-a")),
        "paragraph forward": R(Key("a-rbrace")),
        "paragraph backward": R(Key("a-lbrace")),
        "document forward": R(Key("a-langle")),
        "document backward": R(Key("a-rangle")),
        "function forward": R(Key("ac-a")),
        "function backward": R(Key("ac-e")),
        "bracket forward": R(Key("ac-n")),
        "bracket backward": R(Key("ac-p")),
        # search and replace
        "search fore": R(Key("c-s")),
        "search back": R(Key("c-r")),
        "query replace": R(Key("a-percent")),
        # org
        "clock in": R(Key("c-c, c-x, c-i")),
        "refresh table": R(Key("c-c, c-c")),
        # magit
        "(Maggy|magit)": R(Key("c-x, g")),
        # window management
        "win fore": R(Key("c-x, o")),
        "win back": R(Key("c-u") + Text("-1") + Key("c-x, o")),
        "kill win": R(Key("c-x, 0")),
        "keep one win": R(Key("c-x, 1")),
        "split win sauce": R(Key("c-x, 2")),
        "split win ross": R(Key("c-x, 3")),
        "show buffers": R(Key("c-u, c-x, c-b"))
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "mim": ""}


def get_rule():
    return EmacsRule, RuleDetails(name="E max", executable="Emacs", title="")
