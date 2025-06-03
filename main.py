from emulator import Emulator
from agent import Agent


def main():
    emulator = Emulator("tetris.gb")
    emulator.initialize()

    agent = Agent(emulator)

    try:
        while True: agent.run()
    except KeyboardInterrupt:
        print("Game interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        emulator.stop()

if __name__ == "__main__":
    main()
