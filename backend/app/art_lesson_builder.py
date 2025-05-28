import requests
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
from kokoro import KPipeline
import soundfile as sf 
import re



class LessonAnswerFormat(BaseModel):
    intro: str
    section1: str 
    section2: str
    section3: str
    outro: str

class ArtLessonBuilder:
    """"A class to build art lessons using Sonar API."""

    #Define class variables, API URL , PROMPT FILE, DEFAULT MODEL

    def __init__(self):
        # setup api key from environment vairable
        # setup the prompt file for the specific art, this wil be used to generate the lesson
        # instantiate art objects
        load_dotenv()
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.sytem_prompt = self.construct_prompt()

    def construct_prompt(self):
        # constract the prompt that would get a structured output from sonar
        # chapters,object identification names(chair, man)
        with open('./app/prompt.md', 'r', encoding='utf-8') as f:
            system_prompt = f.read().strip()
        return system_prompt
    
    def construct_lesson_from_api(self, painting_name):
        #use constracted promte to query sonar to generate a structured output

        url = "https://api.perplexity.ai/chat/completions"
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": "sonar-reasoning",
            "messages": [
                {"role": "system", "content": "{system_prompt}"},
                {"role": "user", "content": (
                    f"Prepare a detailed work description about the painting {painting_name}"
                    "in the style of great art explained youtube channel. Don't mention about the youtube channel just take insipration from it."
                    "Please output a JSON object containing the following fields: "
                    "Don't put citations, astrix symbols in the json format for parsing purposes"
                    "don't include brackets and parentheses"
                    "or hash tags in the output, strictly plain"
                    "intro, section1, section2, section3, outro"
                )},
            ],
            "response_format": {
                    "type": "json_schema",
                "json_schema": {"schema": LessonAnswerFormat.model_json_schema()},
            },
        }
        response = requests.post(url, headers=headers, json=payload).json()

        def parse_json(input_str):
            # Find the last occurrence of the "</think> delimiter
            last_think_pos = input_str.rfind("</think>")
            
            json_str = input_str[last_think_pos + len("</think>"):]
            
            return json.loads(json_str)
            
        return parse_json(response["choices"][0]["message"]["content"])

    
    
    

ArtLessonBuilder = ArtLessonBuilder()


text = ''
response = []
for file in os.listdir("./static/")[0:1]:
    path = os.path.join(f"./static/{file}/{file}.json")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        lessonResponse = ArtLessonBuilder.construct_lesson_from_api(data["title"]+ " by " + data["artistDisplayName"])
        response =[f"{file}", lessonResponse['intro'], lessonResponse['section1'], lessonResponse['section2'], lessonResponse['section3'], lessonResponse['outro']]


pipeline = KPipeline(lang_code='a')
for j in range(1,len(response)):
    text = re.sub(r'[^a-zA-Z\s]', '', response[j])
    generator = pipeline(text=text, voice='bm_george', speed=1)
    for i, (gs, ps, audio) in enumerate(generator):
        sf.write(f'./static/{response[0]}/{j}+{i}.wav', audio, 24000)