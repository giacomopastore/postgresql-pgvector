from ollama import Client
from loguru import logger
from llm_client.llm_client import LLMClient

class OllamaClient(LLMClient):
    def __init__(self, host, model="llama3.2:3b", embed_model="mxbai-embed-large"):
        """
        Initializes the Ollama client with the given host.

        :param host: The host address for the Ollama API.
        """
        super().__init__(host, model, embed_model)
        self.client = Client(host=host)
        self.model = model
        self.embed_model = embed_model

        logger.info("Ollama client initialized with host: {}, model: {}, embedding model: {}", host, model, embed_model)

    def embed(self, input):
        """
        Generates the embedding for a given input using the specified model.
        
        :param input: The input for which to generate the embedding.
        :return: The embedding of the input as a list, array, or string, depending on the implementation.
        """
        logger.info("Generating embedding for input: {}", input)
        try:
            response = self.client.embed(model=self.embed_model, input=input)
            logger.info("Successfully generated embedding")
            return ",".join(map(str, response['embeddings']))
        except Exception as e:
            logger.error("Error while fetching embedding: {}", e)
            raise RuntimeError(f"Error while fetching embedding: {e}")
        
    def generate(self, prompt, format=None):
        """
        Generates a response for a given prompt using the specified model.
        
        :param prompt: The prompt for which to generate the response.
        :param format: The format of the response (e.g. json)
        :return: The response from the model.
        """
        logger.info("Generating response for prompt: {}", prompt)
        try:
            output = self.client.generate(model=self.model, prompt=prompt, format=format)
            logger.info("Successfully generated response")
            return output["response"]
        except Exception as e:
            logger.error("Error while fetching response: {}", e)
            raise RuntimeError(f"Error while fetching response: {e}")