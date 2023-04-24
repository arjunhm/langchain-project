from django.conf import settings

import requests
import json
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain


class LinkedInPostGenerator:
    def __init__(self):
        pass

    def __get_llm_chain(self):
        llm = OpenAI()
        template = """Generate a LinkedIn Post with around 75-150 words for the following topic
                        Topic: {topic}"""
        prompt = PromptTemplate(template=template, input_variables=["topic"])
        return LLMChain(prompt=prompt, llm=llm)

    def generate_text(self, topic):
        llm_chain = self.__get_llm_chain()
        return llm_chain.run(topic)

    def generate_image(self, topic):
        BASE_URL = "https://api.openai.com/v1/images/generations"

        payload = {
            "prompt": f"A photo appropriate for a LinkedIn post based on the following topic: {topic}",
            "n": 1,
            "size": "1024x1024",
        }
        payload_json = json.dumps(payload)

        response = requests.post(
            BASE_URL,
            headers={
                "Authorization": f"Bearer {settings.OPEN_AI_KEY}",
                "Content-Type": "application/json",
            },
            data=payload_json,
        )

        if response.status_code == 200:
            return self.__extract_url(response)
        return None

    def __extract_url(self, response):
        try:
            response = response.json()
            return response.get("data", [])[0].get("url")
        except Exception as e:
            print(e)
            return None
