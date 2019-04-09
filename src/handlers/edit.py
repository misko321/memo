import random

from prompt_toolkit import HTML


class Edit:
    def __init__(self, session, bindings, entries) -> None:
        self.session = session
        self.bindings = bindings
        self.entries = entries

    def prompt(self):
        self.session.default_buffer.read_only = lambda: False
        random_entry = random.choice(self.entries)
        if not random_entry.explanation:
            pass

        self.session.prompt(HTML(f"Edit: <blue>{random_entry.definition}</blue>"), key_bindings=self.bindings)
