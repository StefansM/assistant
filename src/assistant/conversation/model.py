import dataclasses
import typing

import openai
import openai.openai_object


@dataclasses.dataclass
class Message:
    role: str
    content: str


class Conversation:
    def __init__(
        self,
        model: str,
        messages: list[Message],
        **kwargs: typing.Any,
    ):
        self.model = model
        self.messages = messages
        self.model_args = kwargs

    def request(self) -> openai.openai_object.OpenAIObject:
        message_dicts = [dataclasses.asdict(m) for m in self.messages]
        return typing.cast(
            openai.openai_object.OpenAIObject,
            openai.ChatCompletion.create(  # type: ignore
                model=self.model,
                messages=message_dicts,
                **self.model_args,
            ),
        )

    def add_message(self, message: Message) -> None:
        self.messages.append(message)
