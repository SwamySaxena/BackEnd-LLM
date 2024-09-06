import openai

def summarize_text(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Summarize the following text:\n\n{text}",
        max_tokens=200
    )
    return response['choices'][0]['text'].strip()

def answer_question(summary, question):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{summary}\n\nQ: {question}\nA:",
        max_tokens=100
    )
    return response['choices'][0]['text'].strip()
