class Message:
    @staticmethod
    def create(role, content):
        return {"role": role, "content": content if type(content) is list else [content]}


class Block:
    @staticmethod
    def text(text):
        return {"type": "text", "text": text}

    @staticmethod
    def image(image):
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": "image/png", "data": image}
        }

    @staticmethod
    def tool_use(tool):
        return {
            "type": "tool_use",
            "id": tool.id,
            "name": tool.name,
            "input": tool.input
        }

    @staticmethod
    def tool_result(tool, content):
        return {
            "type": "tool_result",
            "tool_use_id": tool.id,
            "content": content if type(content) is list else [content]
        }
