import openai

# GPT-3'e erişmek için API anahtarınızı ayarlayın
openai.api_key = "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"

# GPT-3'ü kullanmak için bir Prompt nesnesi oluşturun
prompt = openai.Prompt(text="Hello, I'm GPT-3. What can I do for you?")

# GPT-3'ten bir cevap almak için generate() metodunu çağırın
response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, temperature=0.5)

# Cevabı ekrana yazdırın
print(response.text)