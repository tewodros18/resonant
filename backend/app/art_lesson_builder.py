import requests
from pydantic import BaseModel


class LessonAnswerFormat(BaseModel):
    intro: str
    section1: str 
    section2: str
    section3: str
    outro: str
    objects: list[str]

class ArtLessonBuilder:
    """"A class to build art lessons using Sonar API."""

    #Define class variables, API URL , PROMPT FILE, DEFAULT MODEL

    def __init__(self):
        # setup api key from environment vairable
        # setup the prompt file for the specific art, this wil be used to generate the lesson
        # instantiate art objects
        pass
    def construct_prompt(self):
        # constract the prompt that would get a structured output from sonar
        # chapters,object identification names(chair, man)
        pass
    def construct_lesson_from_api(self, painting_name):
        #use constracted promte to query sonar to generate a structured output

        system_prompt = ""
        painting_name = "Antoine Laurent Lavoisier (1743–1794) and Marie Anne Lavoisier by Jacques Louis David"
        
        with open('./app/prompt.md', 'r', encoding='utf-8') as f:
            system_prompt = f.read().strip()

        url = "https://api.perplexity.ai/chat/completions"
        headers = {"Authorization": "Bearer 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"}
        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "{system_prompt}"},
                {"role": "user", "content": (
                    "Prepare a video script about the painting {painting_name}"
                    "in the style of great art explained youtube channel. Don't mention about the youtube channel just take insipration from it."
                    "Please output a JSON object containing the following fields: "
                    "Objects should be one words, and not contain description, example: 'man', 'woman', 'sword'"
                    "intro, section1, section2, section3, outro, objects[]"
                )},
            ],
            "response_format": {
                    "type": "json_schema",
                "json_schema": {"schema": LessonAnswerFormat.model_json_schema()},
            },
        }
        response = requests.post(url, headers=headers, json=payload).json()
        return response["choices"][0]["message"]["content"]

    def generate_audio(self):
        # use each lesson section to generate audio
        pass
 
    
    



