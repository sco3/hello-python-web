#!/usr/bin/env -S uv run


import gc
import threading
import time
import uvicorn
from collections import Counter
import main

class Monitor:
    saved_dicts: str = "\ninit\n"
    step: int = 0

    @staticmethod
    def save_dicts() -> str:
        # Initialize a Counter to count unique dictionary strings

        dict_counter = Counter()

        # Collect all dictionary objects
        for obj in gc.get_objects():
            if isinstance(obj, dict):
                dict_str = str(obj)
                dict_counter[dict_str] += 1

        # Get the top 20 most common dictionaries
        top_dicts = dict_counter.most_common(20)

        # Create the output string with count first
        result = ""
        for dict_str, count in top_dicts:
            result += f"Count: {count} - {dict_str}\n"
        #print ("result1 = ", result)
        return result

    @classmethod
    def update_saved_dicts(cls):
        # Update the saved_dicts attribute with the output of save_dicts
        cls.saved_dicts = cls.save_dicts()
        #print ("result2 = ", cls.saved_dicts)

        #cls.step += 1
        #cls.saved_dicts = "step: "+str(cls.step)

    @classmethod
    def start_periodic_update(cls, interval: int):
        def run():
            while True:
                time.sleep(interval)
                try:
                    cls.update_saved_dicts()
                    print ("ok")

                except:
                    Monitor.saved_dicts = "\nerror\n"

        # Start the periodic update in a separate thread
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    # Example usage of Monitor class with periodic update

    main.monitor=Monitor
    Monitor.start_periodic_update(interval=60)  # Updates after "interval" seconds

    port=8080

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="debug",
        workers=1,
    )
