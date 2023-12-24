import os
os.environ["OPENAI_API_KEY"] = "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"
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import OpenAI
llm = OpenAI(temperature=0.9)

text = "What would be a good company name for a company that makes colorful socks?"
print(llm(text))
