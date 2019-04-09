#!/usr/bin/env python3
import csv
import re
from typing import List

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

from common import ModeSwitchException, Entry, Mode
from handlers.edit import Edit
from handlers.explain import Explain
from handlers.quiz import Quiz

mode_settings = {
    Mode.QUIZ: {
        'key': 'c-q',
        'handler': Quiz
    },
    Mode.EDIT: {
        'key': 'c-e',
        'handler': Edit
    },
    Mode.EXPLAIN: {
        'key': 'c-x',
        'handler': Explain
    }
}
current_mode = Mode.QUIZ


def load_file(filename: str) -> List[Entry]:
    with open(filename) as file:
        return [load_entry(line) for line in file.readlines()]


def load_entry(line):
    squashed = re.sub(r'\t+', '\t', line.strip())
    fragments = squashed.split('\t')
    if len(fragments) == 2:
        definition = fragments[0]
        explanation = fragments[1] if len(fragments) == 2 else ""
        return Entry(definition, explanation, Mode.QUIZ)
    else:
        return Entry(squashed, '', Mode.EXPLAIN)


def save_file(filename, entries):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|')
        for entry in entries:
            writer.writerow([entry.definition, entry.explanation, entry.last_review_timestamp])


def build_mode_handlers(session, entries):
    bindings = build_common_bindings({mode: settings['key'] for mode, settings in mode_settings.items()})
    return {mode: settings['handler'](session, bindings, entries) for mode, settings in mode_settings.items()}


def build_common_bindings(key_mappings):
    bindings = KeyBindings()

    for mode, key in key_mappings.items():
        bindings.add(key, eager=True)(lambda event, _mode=mode: change_mode_closure(event, _mode))

    return bindings


def change_mode_closure(event, mode):
    # bindings.add has a parameter called 'filter', but it passes unhandled keystrokes directly to the terminal
    # causing some undesired effects like printing '^Q'
    # here we filter out these keystrokes by simply doing nothing
    if mode != current_mode:
        event.app.exit(exception=ModeSwitchException(mode))


def main():
    session = PromptSession()
    entries = load_file('words.txt')
    handlers = build_mode_handlers(session, entries)
    global current_mode

    while True:
        try:
            handlers[current_mode].prompt()
        except ModeSwitchException as e:
            current_mode = e.mode
        except KeyboardInterrupt:
            exit(0)


if __name__ == '__main__':
    main()
