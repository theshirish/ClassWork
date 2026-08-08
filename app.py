# pip install pydantic
from pydantic import BaseModel, Field
# import instructor
# from openai import OpenAI

# import settings

from settings import my_settings

# import os
# from dotenv import load_dotenv

print("Environment:", my_settings.env)
print("OpenAI API Key:", my_settings.openai_api_key)
print("OpenAI Base URL:", my_settings.open_ai_base_url)
print("Name Min Length:", my_settings.name_min_length)
print("Name Max Length:", my_settings.name_max_length)

# load_dotenv('.env')
# print(os.getenv('OPENAI_API_KEY'))
# print(os.getenv('MY_SECRET_KEY'))
# print(os.getenv('DECISION_API_KEY'))


class User(BaseModel):
    name: str = Field(min_length=3, max_length=50,
                      description="The user's name")
    age: int = Field(gt=0, lt=100, description="The user's age", default=18)
    occupation: str = Field(min_length=2, max_length=100,
                            description="The user's occupation")
    hobbies: list[str] = Field(default=[])
    email: str = Field(
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", default=None, description="The user's email address")


# name = input("Enter your name: ")
# age = int(input("Enter your age: "))


# print("Hello")
# try:
#     user = User(name=name, age=age, occupation="Software Engineer",
#                 hobbies=["Reading", "Gaming", "Hiking"], email="john.doe@example.com")
#     print(user)

# except Exception as e:
#     print("Error Occured : ", e)
