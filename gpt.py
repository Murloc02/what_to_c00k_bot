from g4f.client import Client


class Dialog:
    def __init__(self, messages: list = None):
        self.client = Client()
        if messages:
            self.messages = messages
        if not messages:
            self.messages = list()
            self.messages.append({"role": "system", "content": "You are an assistant."})

    def ask(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages)
        answer = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})
        return answer

    def ask_once(self, message):
        if type(message) == str:
            message_gpt = [{"role": "user", "content": message}]
        else:
            message_gpt = message
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message_gpt)
        answer = response.choices[0].message.content
        return answer

    def clear_messages(self):
        self.messages.clear()
        self.messages.append({"role": "system", "content": "You are an assistant."})
        return self.messages
