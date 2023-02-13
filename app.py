import requests
import openai

TELEGRAM_BOT_TOKEN = "5831434184:AAFpnWPOtiKsKbBDacHES-Q5NjaP_3A9k7A"

openai.api_key = "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"

def get_updates(last_update_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    payload = {
        "offset": last_update_id,
        "limit": 100,
        "timeout": 30,
    }
    response = requests.get(url, params=payload)
    return response.json()

def get_last_update_id(updates):
    return max([update["update_id"] for update in updates])

def handle_message(update):
    message = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text
    send_message(response, chat_id)



def chat(text):
    openai.api_key = "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"

    model_engine = "text-davinci-002"
    prompt = (f"{text}")

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message.strip()


def handle_updates(updates):
    for update in updates:
        if "message" in update:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
            if text == "/start":
                send_message("Welcome To AK-Stealers Bot!, If you have any questions or topics you'd like to talk about,  I'm here to help!", chat_id)
            if text == "/about":
                send_message("About Me:  I Am AK-Stealers Bot Developed By  AK Programmer | Powered By OpenAI. I Can generate human-like responses to a wide range of topics, from answering questions to having conversations on various subjects and much more. I have been trained on a large dataset of text from the internet, which allows me to respond to a wide range of questions and engage in various types of conversations. Whether you have a question about a specific topic.", chat_id)
            if text == "/help":
                send_message("Hello I'm AK-Stealers Bot!, I Am Chat Based Bot Which Can Generate Human-like Responses To Your Questions. My speciality is To Create A Code In Any Programming Languages, So It is So Easy To Chat With Me I'm here to help!", chat_id)
            else:
                send_message("Stealer's Bot Thinking On It...", chat_id)
                response = chat(text)
                send_message(response, chat_id)



def send_message(text, chat_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "text": text,
        "chat_id": chat_id,
    }
    requests.post(url, json=payload)

def main():
    last_update_id = 0
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates["result"]) + 1
            handle_updates(updates["result"])

if __name__ == "__main__":
    main()
