import os
import time
from openai import AzureOpenAI
from loguru import logger
from llm_client.llm_client import LLMClient
from typing import Optional, Sequence, Union, Mapping, Any, Iterator, Literal

class AzureOpenAIClient(LLMClient):
    def __init__(self, model="gpt-35-turbo", embed_model="text-embedding-ada-002", **kwargs):
        super().__init__(kwargs.get("azure_endpoint"), model, embed_model)
        self.client = AzureOpenAI(
            api_key=kwargs.get("api_key"),
            azure_endpoint=kwargs.get("azure_endpoint"),
            api_version=kwargs.get("api_version", "2024-07-01-preview")
        )
        self.model = model
        self.embed_model = embed_model
        logger.info("Azure OpenAI client initialized with endpoint: {}, model: {}, embedding model: {}", self.host, model, embed_model)

    def embed(self, input, **kwargs):
        logger.info("Generating embedding for input: {}", input)
        try:
            start_time = time.time()
            response = self.client.embeddings(model=self.embed_model, input=input, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info("Embed completed in {} seconds", elapsed_time)
            return ",".join(map(str, response['data'][0]['embedding']))
        except Exception as e:
            logger.error("Error while fetching embedding: {}", e)
            raise RuntimeError(f"Error while fetching embedding: {e}")

    def generate(self, prompt, **kwargs):
        logger.info("Generating response for prompt: {}", prompt)
        try:
            start_time = time.time()
            response = self.client.chat_completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            elapsed_time = time.time() - start_time
            logger.info("Generate completed in {} seconds", elapsed_time)
            return response['choices'][0]['message']['content']
        except Exception as e:
            logger.error("Error while fetching response: {}", e)
            raise RuntimeError(f"Error while fetching response: {e}")

    def chat(self, 
             messages: Optional[Sequence[dict]] = None, 
             **kwargs
    ) -> Union[Mapping[str, Any], Iterator[Mapping[str, Any]]]:
        logger.info("Starting chat with model: {}, messages: {}", self.model, messages)
        try:
            start_time = time.time()
            response = self.client.chat_completion(
                model=self.model,
                messages=messages,
                **kwargs
            )
            elapsed_time = time.time() - start_time
            logger.info("Chat completed in {} seconds", elapsed_time)
            return response['choices'][0]['message']['content']
        except Exception as e:
            logger.error("Error during chat: {}", e)
            raise RuntimeError(f"Error while chatting: {e}")

import asyncio
from openai import AzureOpenAIAsync

class AzureOpenAIAsyncClient(LLMClient):
    def __init__(self, model="gpt-35-turbo", embed_model="text-embedding-ada-002", **kwargs):
        super().__init__(kwargs.get("azure_endpoint"), model, embed_model)
        self.client = AzureOpenAIAsync(
            api_key=kwargs.get("api_key"),
            azure_endpoint=kwargs.get("azure_endpoint"),
            api_version=kwargs.get("api_version", "2024-07-01-preview")
        )
        self.model = model
        self.embed_model = embed_model
        logger.info("Azure OpenAI Async client initialized with endpoint: {}, model: {}, embedding model: {}", self.host, model, embed_model)

    async def embed(self, input, **kwargs):
        logger.info("Generating embedding for input: {}", input)
        try:
            start_time = time.time()
            response = await self.client.embeddings(model=self.embed_model, input=input, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info("Embed completed in {} seconds", elapsed_time)
            return ",".join(map(str, response['data'][0]['embedding']))
        except Exception as e:
            logger.error("Error while fetching embedding: {}", e)
            raise RuntimeError(f"Error while fetching embedding: {e}")

    async def generate(self, prompt, **kwargs):
        logger.info("Generating response for prompt: {}", prompt)
        try:
            start_time = time.time()
            response = await self.client.chat_completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            elapsed_time = time.time() - start_time
            logger.info("Generate completed in {} seconds", elapsed_time)
            return response['choices'][0]['message']['content']
        except Exception as e:
            logger.error("Error while fetching response: {}", e)
            raise RuntimeError(f"Error while fetching response: {e}")

    async def chat(self, 
                   messages: Optional[Sequence[dict]] = None, 
                   **kwargs
    ) -> Union[Mapping[str, Any], Iterator[Mapping[str, Any]]]:
        logger.info("Starting chat with model: {}, messages: {}", self.model, messages)
        try:
            start_time = time.time()
            response = await self.client.chat_completion(
                model=self.model,
                messages=messages,
                **kwargs
            )
            elapsed_time = time.time() - start_time
            logger.info("Chat completed in {} seconds", elapsed_time)
            return response['choices'][0]['message']['content']
        except Exception as e:
            logger.error("Error during chat: {}", e)
            raise RuntimeError(f"Error while chatting: {e}")