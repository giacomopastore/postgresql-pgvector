from abc import ABC, abstractmethod

class LLMClient(ABC):
    def __init__(self, host, model, embed_model):
        """
        Initializes the LLM client with the given host.

        :param host: The host address for the LLM API.
        """
        self.host = host

    @abstractmethod
    def embed(self, input, **kwargs):
        """
        Generates the embedding for a given input using the specified model.
        
        :param input: The input for which to generate the embedding.
        :return: The embedding of the input as a list, array, or string, depending on the implementation.
        """
        pass
    
    @abstractmethod
    def generate(self, prompt, **kwargs):
        """
        Generates a response for a given prompt using the specified model.
        
        :param prompt: The prompt for which to generate the response.
        :return: The response from the model.
        """
        pass