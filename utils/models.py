import openai
from transformers import pipeline

openai.api_key = "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"


def classify(text):
    # Load the text classification pipeline
    classifier = pipeline("text-classification",
                          model="/Users/phung/IdeaProjects/swinburne/tech-design/project-source/scopeclassifier")
    # Classify the text
    result = classifier(text)
    if result[0]['label'] == 'LABEL_0':
        # In-scope
        return "in-scope", result[0]['score']
    return "out-of-scope", result[0]['score']


def generate_in_scope(text):
    converted_to_question = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'system',
                'content': 'You are an agent performing statement-to-question conversion task. You are not a chatbot agent. You can not respond to the user phrases as if you are a chatbot. You only paraphrase or echo back what the user said. Your prompts will be dry and will only contain the answer. If the user give you a question then you respond with the question. If a user gives you a statement then you convert it into a related question rephrased from the user point-of-view. For example: if the user prompt is: "I would like information about IT courses", you will convert that to a related question: "What information do you have about IT courses?". It must be from the user point-of-view. Write resulting text only'
            },
            {'role': 'user', 'content': text}
        ],
        temperature=0
    )
    response = openai.Completion.create(
        model='davinci:ft-personal-2023-05-21-04-30-16',
        prompt=converted_to_question['choices'][0]['message']['content'],
        temperature=0,
        max_tokens=200,
        stop=["END OF QUESTION", "END"],
        frequency_penalty=0.5,
        stream=True
    )
    for line in response:
        yield line['choices'][0]['text']


def generate_out_of_scope(text):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'system',
                'content': 'You are an FAQ chatbot for Swinburne University Online. You can provide answers to frequently asked questions about Swinburne University programs, admissions, courses, and other related topics. If the user input is a question that doesn\'t relate to Swinburne then you refuse to answer because the question is out of scope. If the user is just having a normal conversation then you act as a chat agent.'
            },
            {'role': 'user', 'content': text}
        ],
        temperature=0,
        stream=True
    )
    for line in response:
        chunk = line['choices'][0].get('delta', {}).get('content', '')
        if chunk:
            yield chunk
