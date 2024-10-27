from abc import ABC, abstractmethod

class LLMClient(ABC):
    def __init__(self, host):
        """
        Initializes the LLM client with the given host.

        :param host: The host address for the LLM API.
        """
        self.host = host

    @abstractmethod
    def get_embedding(self, input, model):
        """
        Generates the embedding for a given input using the specified model.

        :param input: The input for which to generate the embedding.
        :param model: The model to use for generating the embedding.
        :return: The embedding of the input as a list, array, or string, depending on the implementation.
        """
        pass