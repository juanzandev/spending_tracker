from .constants import RECOMENDATION_PROMPT, SCORE_PROMPT
from dotenv import load_dotenv
import os
from groq import Groq
import pandas as pd

class ScoreAgent:
    def __init__(self) -> None:
        self.rec_prompt = RECOMENDATION_PROMPT
        self.score_prompt = SCORE_PROMPT
        load_dotenv() # load vars defined in the .env file to global env
        key = os.getenv('API_KEY') # get env variables
        # connect to the API endpoint
        self.client = Groq(api_key = key)

    def generate(self, client, prompt_template : str):

        try:
            # generate responses
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt_template
                    }
                ],
                temperature=0.9,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
                seed=123
            )
            return completion
        except Exception as e:
            print(f"Ops! Failed to generate response from LLM from {e}")
    
    def recommendation(self, score=0) -> str:
        # define the prompt with the instructions
        # here is where the prompt engineering comes to play, I have created a template but feel free to change it
        prompt_template = f'''<s>[INST]{self.rec_prompt}\n
        Your answers must be short, friendly yet professional, and helpful.
        Please give up to five financial recommendations based on the student's spending score of: {score}[/INST]
        '''

        completion = self.generate(client=self.client, prompt_template=prompt_template)
        raw_response = completion.choices[0].message.content
        clean_response = raw_response.replace('\n', '')
        return raw_response
    
    def fetch_score(self) -> int:
        data = pd.read_csv("/Users/odaiclet/Desktop/coding_projects/spending_tracker_oct31/pages/util/User_1.csv")
        data_json = data.tail(100)
        prompt_template = f'''<s>[INST]{self.score_prompt}
        Data: {data_json.to_json()}\n
        Restrict your answer to absolutely one integer between 1 and 10. Don't provide an explanation for the answer.[/INST]
        '''
        completion = self.generate(client=self.client, prompt_template=prompt_template)
        score = completion.choices[0].message.content
        return score