import urwid
import typing
import urwid
from collections.abc import Iterable

# ------ TUI Components ------


def list_button(
    label: str, callback: callable, user_args: tuple = None
) -> urwid.Button:
    button = urwid.Button(label)
    urwid.connect_signal(button, "click", callback, *user_args if user_args else ())
    return urwid.AttrMap(
        button, None, focus_map="reversed"
    )  # reverse colors when focused


def game_menu() -> urwid.ListBox:
    start_button = list_button("Start", start_game)
    exit_button = list_button("Exit", exit_program)
    body = [
        urwid.Divider(),
        urwid.Text("Welcome to Spellwid!"),
        urwid.Divider(),
        start_button,
        exit_button,
    ]
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def text_box() -> urwid.Edit:
    return urwid.LineBox(
    urwid.Edit(align="center"),
    tlcorner="<",
    trcorner=">",
    blcorner="<",
    brcorner=">",
    tline="-",
    lline="|",
    rline="|",
    bline="-",
)


def game_screen() -> urwid.ListBox:
    header = [
        urwid.Divider(),
        urwid.AttrMap(urwid.Text("Spell the word!", align="center"), "streak"),
    ]

    body = urwid.Filler(text_box(), valign="middle")
    header = urwid.Filler(urwid.Pile(header), valign="middle")

    return urwid.Frame(body, header=header)


# ------ Callbacks ------


def start_game(button: urwid.Button) -> None:
    main.original_widget = game_screen()


def exit_program(button: urwid.Button) -> None:
    raise urwid.ExitMainLoop()


main = urwid.Padding(game_menu(), left=2, right=2)

top = urwid.Overlay(
    main,
    urwid.SolidFill("\N{MEDIUM SHADE}"),
    align=urwid.CENTER,
    width=(urwid.RELATIVE, 60),
    valign=urwid.MIDDLE,
    height=(urwid.RELATIVE, 60),
    min_width=20,
    min_height=9,
)

palette = [
    ("banner", "black", "light gray"),
    ("streak", "black", "dark red"),
    ("bg", "black", "dark blue"),
    ("reversed", "standout", ""),
]

if __name__ == "__main__":
    urwid.MainLoop(top, palette=palette).run()