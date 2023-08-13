import dataclasses
import typing

import openai
import openai.openai_object


@dataclasses.dataclass
class Message:
    """A data class representing a message which includes role and content.

    Attributes:
        role (str): Role of the message sender.
        content (str): The actual text message."""

    role: str
    content: str


class Conversation:
    """Class for creating conversation with the openai API.

    Attributes:
        model (str): The openai model to be used for conversation.
        messages (list[Message]): List of `Message` instances to start conversation with.
        model_args (dict): Extra arguments to the model."""

    def __init__(
        self,
        model: str,
        messages: list[Message],
        **kwargs: typing.Any,
    ):
        """Initialize conversation with provided model, messages, and extra args.

        Args:
            model (str): The openai model to be used for the conversation.
            messages (list[Message]): List of `Message` instances to start the conversation with.
            **kwargs: Extra arguments to the model"""
        self.model = model
        self.messages = messages
        self.model_args = kwargs

    def request(self) -> openai.openai_object.OpenAIObject:
        """Send a request to the openai API for the conversation and return the response.

        Returns:
            openai.openai_object.OpenAIObject: The response from the openai API after providing the conversation.
        """
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
        """Append a new message to the list of messages in the conversation.

        Args:
            message (Message): An instance of `Message` to be added to the conversation.
        """
        self.messages.append(message)
