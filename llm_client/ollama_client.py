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

    def embed(self, model, input):
        """
        Generates the embedding for a given input using the specified model.
        
        :param model: The model to use for generating the embedding.
        :param input: The input for which to generate the embedding.
        :return: The embedding of the input as a list, array, or string, depending on the implementation.
        """
        logger.info("Generating embedding for input: '{}' using model: '{}'", input, model)
        try:
            response = self.client.embed(model=model, input=input)
            logger.info("Successfully generated embedding")
            return ",".join(map(str, response['embeddings']))
        except Exception as e:
            logger.error("Error while fetching embedding: {}", e)
            raise RuntimeError(f"Error while fetching embedding: {e}")
        
    def generate(self, model, prompt):
        """
        Generates a response for a given prompt using the specified model.
        
        :param model: The model to use for generating the response.
        :param prompt: The prompt for which to generate the response.
        :return: The response from the model.
        """
        logger.info("Generating response for prompt: '{}' using model: '{}'", prompt, model)
        try:
            output = self.client.generate(model=model, prompt=prompt)
            logger.info("Successfully generated response")
            return output["response"]
        except Exception as e:
            logger.error("Error while fetching response: {}", e)
            raise RuntimeError(f"Error while fetching response: {e}")