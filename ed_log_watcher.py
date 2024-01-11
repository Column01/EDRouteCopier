import json
import os
import threading
import time
from typing import Callable, Union


class EDLogWatcher:
    def __init__(self, log_file_path: os.PathLike, route_file_path: os.PathLike) -> None:
        self.log_file_path = log_file_path
        self.route_file_path = route_file_path

        # Log file tracking information
        self._prev_pos = 0
        self._f_stats = os.stat(self.log_file_path)
        # Mapping of event listeners
        self.event_listeners = {}
        # Filled in start()
        self.thread = None 

    def start(self) -> bool:
        self.thread = threading.Thread(target=self.watch_log_file)
        self.thread.start()
        return self.thread.is_alive()

    def watch_log_file(self) -> None:
        _first_run = True
        while True:
            # Check if the file has been modified
            new_file_stats = os.stat(self.log_file_path)
            if new_file_stats.st_mtime != self._f_stats.st_mtime or _first_run:
                # Force it to load all the data the first time around ignoring file changes
                if _first_run:
                    _first_run = False
                # File has been modified, store new file stats and seek to previous position to read new lines
                self._f_stats = new_file_stats
                with open(self.log_file_path, 'r') as f:
                    f.seek(self._prev_pos)
                    # Read new lines after the previous position and process them immediately
                    for line in f:
                        try:
                            json_data = json.loads(line)
                            event = json_data.get("event")
                            listeners = self.event_listeners.get("all", []) + self.event_listeners.get(event, [])
                            if len(listeners) > 0:
                                for listener in listeners:
                                    listener(json_data)
                        except json.JSONDecodeError as e:
                            print(f"Error parsing line: {line}: {e}")

                    # Update the previous position
                    self._prev_pos = f.tell()
            time.sleep(1)
    
    def register_callback(self, event: Union[str, "all"], func: Callable) -> None:
        listeners = self.event_listeners.get(event)
        if listeners is None:
            self.event_listeners[event] = [func]
        else:
            listeners.append(func)
