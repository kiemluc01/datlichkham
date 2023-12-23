from django.conf import settings


client = settings.GPT_CLIENT

def getResponseGPTFromText(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": user_input
            }
        ],
        stream=False,
        max_tokens=2000,
    )
    return response.choices[0].message.content