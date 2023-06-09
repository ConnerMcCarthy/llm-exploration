import time
import os.path
import json

import openai


def main():
    api_path = "./secret.txt"
    openai.api_key  = read_api_key(api_path)
    
    prompt = 'Sort this note into a catagory and explain why. The list of catagories is {physics, games, life, programming, work}. You can create another catagory if needed.'

    folder_name = 'KeepNotes'
    json_notes = read_json(folder_name)
    
    #Asks the same prompt with each note
    for note in json_notes:
            try:
                response = ask(prompt, 'Title: ' + note['title'] + note['textContent'])
                print('\n' + response['choices'][0]['message']['content'])
            # Waits for the rate limit and tries again
            except openai.error.RateLimitError as error:
                time.sleep(21)
                response = ask('\n' + prompt, 'Title: ' + note['title'] + note['textContent'])
                print(response['choices'][0]['message']['content'])


#Creates a gpt-3.5 Completetion. Uses prompts containing a note and a question.
def ask(prompt, notes):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a helpful assistant who processes notes."},
            {"role": "user", "content": "The note is here: " + notes},
            {"role": "user", "content": prompt}
        ]
    )
    return response

# Gathers all json files in the folder and returns a list of them
def read_json(note_path):
    json_notes = []
    for filename in os.listdir(note_path):
        if filename.endswith('.json'):
            file_path = os.path.join(note_path,filename)
            with open(file_path) as file:
                json_data = json.load(file)
                json_notes.append(json_data)
    return json_notes

def read_api_key(api_path):
    with open(api_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

if __name__ == '__main__':
    main()
