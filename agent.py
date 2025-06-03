import base64
import io
import logging

from anthropic import Anthropic
from apiutils import Message, Block
from config import MAX_TOKENS, MODEL_NAME, TEMPERATURE
from prompts import SYSTEM_PROMPT, SUMMARY_PROMPT, AVAILABLE_TOOLS

log_handlers = [logging.StreamHandler(), logging.FileHandler("agent.log")]
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", handlers=log_handlers)   
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, emulator):
        self.client = Anthropic()
        self.emulator = emulator
        self.max_history = 20
        self.message_history = [Message.create("user", Block.text("You may now begin playing."))]

    def run(self):
        if len(self.message_history) >= self.max_history:
            self.summarize_history()

        response = self.prompt_llm(self.message_history, SYSTEM_PROMPT, AVAILABLE_TOOLS)

        action_taken = False
        for block in response.content:
            if block.type == "text":
                logger.info(f"[Text] {block.text}")
            elif block.type == "tool_use":
                logger.info(f"[Tool] {block.name} {block.input}")
                self.message_history.append(Message.create("assistant", Block.tool_use(block)))

                tool_result = self.use_tool(block)
                self.message_history.append(Message.create("user", tool_result))
                action_taken = True

        if not action_taken:
            self.emulator.tick(60)  # Advance game 1 second

    def prompt_llm(self, messages, system_prompt, tools):
        return self.client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=messages,
            tools=tools,
            temperature=TEMPERATURE
        )

    def use_tool(self, tool):
        if tool.name == "press_buttons":
            for button in tool.input["buttons"]:
                self.emulator.press_button(button)
        else:
            logger.error(f"Unknown tool: {tool.name}")
            return Block.tool_result(tool.call, Block.text(f"Error: Unknown tool '{tool.name}'"))

        screenshot = self.get_screenshot(upscale=2)
        content = [
            Block.text(f"Here is the game area after running {tool.name}:"),
            Block.image(screenshot)
        ]

        return Block.tool_result(tool, content)

    def get_screenshot(self, upscale=1):
        screenshot = self.emulator.get_screenshot()

        if upscale > 1:
            new_size = (screenshot.width * upscale, screenshot.height * upscale)
            screenshot = screenshot.resize(new_size)

        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        return base64.standard_b64encode(buffered.getvalue()).decode()

    def summarize_history(self):
        self.message_history.append(Message.create("user", Block.text(SUMMARY_PROMPT)))
        response = self.prompt_llm(self.message_history, SYSTEM_PROMPT, AVAILABLE_TOOLS)

        summary_text = " ".join([block.text for block in response.content if block.type == "text"])
        logger.info(f"[Agent] Game Progress Summary:\n{summary_text}")

        screenshot = self.get_screenshot(upscale=2)
        content = [
            Block.text(f"CONVERSATION HISTORY SUMMARY\n{summary_text}"),
            Block.text("\n\nCurrent game area for reference:"),
            Block.image(screenshot),
            Block.text("You were just asked to summarize your playthrough so far, which is the summary you see above. You may now continue playing by selecting your next action.")
        ]

        self.message_history = [Message.create("user", content)]
