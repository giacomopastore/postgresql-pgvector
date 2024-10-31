from ollama import Client, AsyncClient, RequestError
from loguru import logger
from llm_client.llm_client import LLMClient
import time
from typing import Optional, Sequence, Union, Mapping, Any, Iterator, Literal

class OllamaClient(LLMClient):
    def __init__(self, host, model="llama3.2:3b", embed_model="mxbai-embed-large"):
        super().__init__(host, model, embed_model)
        self.client = Client(host=host)
        self.model = model
        self.embed_model = embed_model

        logger.info("Ollama client initialized with host: {}, model: {}, embedding model: {}", host, model, embed_model)

    def embed(self, input, **kwargs):
        logger.info("Generating embedding for input: {}", input)
        try:
            start_time = time.time()
            response = self.client.embed(model=self.embed_model, input=input, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"Embed completed in {elapsed_time} seconds")
            return ",".join(map(str, response['embeddings']))
        except Exception as e:
            logger.error("Error while fetching embedding: {}", e)
            raise RuntimeError(f"Error while fetching embedding: {e}")
        
    def generate(self, prompt, **kwargs):
        logger.info("Generating response for prompt: {}", prompt)
        try:
            start_time = time.time()
            output = self.client.generate(model=self.model, prompt=prompt, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"Generate completed in {elapsed_time} seconds")
            return output["response"]
        except Exception as e:
            logger.error("Error while fetching response: {}", e)
            raise RuntimeError(f"Error while fetching response: {e}")

class OllamaAsyncClient(LLMClient):
    def __init__(self, host, model="llama3.2:3b", embed_model="mxbai-embed-large"):
        super().__init__(host, model, embed_model)
        self.client = AsyncClient(host=host)
        self.model = model
        self.embed_model = embed_model

        logger.info("Ollama Async client initialized with host: {}, model: {}, embedding model: {}", host, model, embed_model)
    
    async def embed(self, input, **kwargs):
        logger.info("Generating embedding for input: {}", input)
        try:
            start_time = time.time()
            response = await self.client.embed(model=self.embed_model, input=input, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"Embed completed in {elapsed_time} seconds")
            return ",".join(map(str, response['embeddings']))
        except Exception as e:
            logger.error("Error while fetching embedding: {}", e)
            raise RuntimeError(f"Error while fetching embedding: {e}")
        
    async def generate(self, prompt, **kwargs):
        logger.info("Generating response for prompt: {}", prompt)
        try:
            start_time = time.time()
            output = await self.client.generate(model=self.model, prompt=prompt, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"Generate completed in {elapsed_time} seconds")
            return output["response"]
        except Exception as e:
            logger.error("Error while fetching response: {}", e)
            raise RuntimeError(f"Error while fetching response: {e}")
        
    async def chat(
        self,
        messages: Optional[Sequence[dict]] = None,
        **kwargs
    ) -> Union[Mapping[str, Any], Iterator[Mapping[str, Any]]]:
        try:
            logger.info("Starting chat with model: {}, messages: {}", self.model, messages)
            response = await self.client.chat(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return response
        except RequestError as e:
            logger.error("Error during chat: {}", e)
            raise RuntimeError(f"Error while chatting: {e}")
        
                
        