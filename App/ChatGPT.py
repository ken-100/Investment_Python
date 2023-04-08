import openai

# APIキーの設定
openai.api_key = " "


def Chat(msg):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": msg},
        ],
    )
    print(response.choices[0]["message"]["content"].strip())
    
    
msg = "What are the benefits of using Python for web development?"
Chat(msg)
