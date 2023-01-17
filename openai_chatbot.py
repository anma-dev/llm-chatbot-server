import logging
from typing import Tuple


class OpenAIChatbot():
    def __init__(
        self,
        openai,
        initial_prompt: str,
        names: Tuple[str, str] = ("AI", "Human"),
        end_token: str = "END",
        openai_engine: str = "text-davinci-003"
    ):
        self.openai = openai
        self.initial_prompt = initial_prompt
        self.names = names
        self.end_token = end_token
        self.openai_engine = openai_engine

        self.prompt = ""
        self.stop = [f"{name}:" for name in names]

    def start_session(self):
        self.prompt = f"{self.initial_prompt}\n"
        return self._get_all_utterances()

    def send_response(self, response: str):
        self._add_response(self.names[1], response.strip())
        return self._get_all_utterances()

    def session_ended(self) -> bool:
        return not self.prompt

    def _add_response(self, name: str, response: str):
        self.prompt += f"\n{name}: {response}"

    def _get_all_utterances(self):
        return [self._get_next_utterance()]

    def _get_next_utterance(self):
        self.prompt += f"\n{self.names[0]}:"

        logging.debug(
            f"Requesting OpenAI completion for prompt:\n{self.prompt}")
        completion = self.openai.Completion.create(
            engine=self.openai_engine,
            prompt=self.prompt,
            max_tokens=150,
            stop=self.stop,
            temperature=0.9
        )

        utterance = completion.choices[0]["text"].strip()
        logging.debug(f"Got utterance: {repr(utterance)}")

        end_token_pos = utterance.find(self.end_token)
        if end_token_pos != -1:
            utterance = utterance[:end_token_pos].strip()
            # Ending the session
            self.prompt = ""
        else:
            self.prompt = f"{self.prompt} {utterance}"

        return utterance
