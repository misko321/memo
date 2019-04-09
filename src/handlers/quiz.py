import random

from prompt_toolkit import print_formatted_text, HTML, PromptSession


class Quiz:
    def __init__(self, session, bindings, entries) -> None:
        self.session: PromptSession = session
        self.bindings = bindings
        self.entries = entries

    def prompt(self):
        self.session.default_buffer.read_only = lambda: True
        random_entry = random.choice(self.entries)
        if not random_entry.explanation:
            return

        self.session.prompt(HTML(f"Quiz: <yellow>{random_entry.definition}</yellow>"), key_bindings=self.bindings)

        print_formatted_text(HTML("<green>&lt;&lt;&lt; " + random_entry.explanation + "</green>"), end='\n')
