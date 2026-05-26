class ChatHistory:
    def __init__(self):
        self.history = []

    def append(self, role, message):
        self.history.append(
            {
                "role": role,
                "content": message
            }
        )