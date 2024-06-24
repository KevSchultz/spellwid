import urwid
import pyttsx3
import random
import nltk
from nltk.corpus import words

# Ensure the 'words' corpus is downloaded
nltk.download("words")

# Fetch the list of words
word_list = words.words()


def generate_random_word(length: int) -> str:
    suitable_words = [word for word in word_list if len(word) == length]
    return random.choice(suitable_words) if suitable_words else ""


current_word = None
selected_length = 5  # Default word length
reveal_text_widget = urwid.Text("", align="center")

# ------ TUI Components ------


def list_button(label: str, callback: callable, user_args: tuple = ()) -> urwid.Button:
    button = urwid.Button(label)
    urwid.connect_signal(button, "click", callback, *user_args)
    return urwid.AttrMap(button, None, focus_map="reversed")


def game_menu() -> urwid.ListBox:
    length_label = urwid.Text(f"Word Length: {selected_length}")
    increase_button = list_button("Increase", increase_length)
    decrease_button = list_button("Decrease", decrease_length)
    start_button = list_button("Start", start_game)
    exit_button = list_button("Exit", exit_program)

    body = urwid.Pile(
        [
            urwid.Divider(),
            urwid.Text("Welcome to Spellwid!"),
            urwid.Divider(),
            urwid.AttrMap(length_label, None),
            urwid.Columns([increase_button, decrease_button]),
            urwid.Divider(),
            urwid.AttrMap(start_button, None),
            urwid.AttrMap(exit_button, None),
        ]
    )
    return urwid.ListBox(urwid.SimpleFocusListWalker([body]))


class SpeakEdit(urwid.Edit):
    def keypress(self, size, key):
        if key == "enter":
            check_guess(self.get_edit_text())
            self.set_edit_text("")
        else:
            return super().keypress(size, key)


def text_box() -> urwid.LineBox:
    return urwid.LineBox(
        SpeakEdit(align="center"),
        tlcorner="<",
        trcorner=">",
        blcorner="<",
        brcorner=">",
        tline="-",
        lline="|",
        rline="|",
        bline="-",
    )


def game_screen() -> urwid.Frame:
    header = [
        urwid.Divider(),
        urwid.AttrMap(urwid.Text("Spell the word!", align="center"), "streak"),
    ]

    body = [
        urwid.Divider(),
        text_box(),
        urwid.Divider(),
        reveal_text_widget,
        urwid.Divider(),
    ]

    button1 = list_button("Next", start_game)
    button2 = list_button(
        "Speak", lambda button: speak("Please spell the word " + current_word)
    )
    button3 = list_button("Exit", exit_program)

    button_row = urwid.Columns(
        [
            ("pack", button1),
            urwid.Divider(),
            ("pack", button2),
            urwid.Divider(),
            ("pack", button3),
        ]
    )

    body.append(button_row)

    return urwid.Frame(
        urwid.ListBox(urwid.SimpleFocusListWalker(body)), header=urwid.Pile(header)
    )


# ------ Callbacks ------


def speak(text: str) -> None:
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def start_game(button: urwid.Button) -> None:
    global current_word
    current_word = generate_random_word(selected_length)
    reveal_text_widget.set_text("")
    speak(f"The game is starting! Spell the word: {current_word}")
    main.original_widget = game_screen()


def check_guess(guess: str) -> None:
    global current_word
    if guess.lower() == current_word.lower():
        speak("Correct! Generating a new word.")
        current_word = generate_random_word(selected_length)
        reveal_text_widget.set_text("")
        speak(f"Spell the new word: {current_word}")
    else:
        reveal_text_widget.set_text(f"The correct word was: {current_word}")
        speak("Incorrect, try again.")


def increase_length(button: urwid.Button) -> None:
    global selected_length
    selected_length += 1
    update_menu()


def decrease_length(button: urwid.Button) -> None:
    global selected_length
    if selected_length > 1:
        selected_length -= 1
    update_menu()


def update_menu() -> None:
    main.original_widget = game_menu()


def exit_program(button: urwid.Button) -> None:
    raise urwid.ExitMainLoop()


def exit_on_q(key: str) -> None:
    if key in {"q", "Q"}:
        exit_program(None)


# ------ Main ------

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
    urwid.MainLoop(top, palette=palette, unhandled_input=exit_on_q).run()
