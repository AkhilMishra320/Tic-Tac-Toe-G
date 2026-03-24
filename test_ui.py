import sys
import traceback
import threading
import time

def test():
    try:
        from unbeatable_ttt import UnbeatableGame
        game = UnbeatableGame()
        print("Game instance created successfully")
        # Start mainloop in a separate thread to avoid blocking
        def run():
            try:
                game.run()
            except Exception as e:
                print("Error in mainloop:", e)
                traceback.print_exc()
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        time.sleep(3)  # Wait a bit to see if window appears
        print("Test completed - window should be visible")
        # We can't close the window easily, just exit
        sys.exit(0)
    except Exception as e:
        print("Error during import or instantiation:", e)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test()