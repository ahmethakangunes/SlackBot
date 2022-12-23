import openai

def GPT_Completion(text):
    ## Call the API key under your account (in a secure way)
    openai.api_key = "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"
    response = openai.Image.create(
    prompt=text,
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    print(image_url)


GPT_Completion("television on the sea")