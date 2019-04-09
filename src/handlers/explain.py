import random

from prompt_toolkit import HTML


class Explain:
    def __init__(self, session, bindings, entries) -> None:
        self.session = session
        self.bindings = bindings
        self.entries = entries

    def prompt(self):
        self.session.default_buffer.read_only = lambda: False
        random_entry = random.choice(self.entries)

        if not random_entry.explanation:
            self.session.prompt(HTML(f"Explain: <red>{random_entry.definition}</red>"), key_bindings=self.bindings)
