from ollama import Client
from loguru import logger
from llm_client.llm_client import LLMClient

class OllamaClient(LLMClient):
    def __init__(self, host):
        """
        Initializes the Ollama client with the given host.

        :param host: The host address for the Ollama API.
        """
        super().__init__(host)
        self.client = Client(host=host)
        logger.info("Ollama client initialized with host: {}", host)

    def get_embedding(self, model, input):
        """
        Generates the embedding for a given text using the specified model.

        :param text: The text for which to generate the embedding.
        :param model: The model to use for generating the embedding.
        :return: The embedding of the text as a list.
        """
        logger.info("Generating embedding for text: '{}' using model: '{}'", input, model)
        try:
            response = self.client.embed(model=model, input=input)
            logger.info("Successfully generated embedding")
            return ",".join(map(str, response['embeddings']))
        except Exception as e:
            logger.error("Error while fetching embedding: {}", e)
            raise RuntimeError(f"Error while fetching embedding: {e}")