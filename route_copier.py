import os
import asyncio
import stat
import json
import time
import pyperclip
import csv


class RouteCopier:
    def __init__(self, log_file_path: os.PathLike, route_file_path: os.PathLike) -> None:
        self.log_file_path = log_file_path
        self.route_file_path = route_file_path

        # Quit the program if the log or route file paths are invalid/files do not exist
        if not os.path.isfile(log_file_path) or not os.path.isfile(route_file_path):
            exit("One or more file paths provided were invalid! Double check the log and route file paths!")
        
        # Log file tracking information
        self._prev_pos = 0
        self._f_stats = os.stat(log_file_path)

        # Turn the neutron route into a generator object and get the first target
        self.nav = self._nav_generator()
        self.nav_target = next(self.nav)

        print(f"Initial nav target: {self.nav_target}")

    def _nav_generator(self) -> dict:
        print(f"Loading neutron route from file: {self.route_file_path}")
        with open(self.route_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row

    def watch_log_file(self) -> None:
        _first_run = True
        while True:
            # Check if the file has been modified
            new_file_stats = os.stat(log_file_path)
            if new_file_stats.st_mtime != self._f_stats.st_mtime or _first_run:
                # Force it to load all the data the first time around ignoring file changes
                if _first_run:
                    _first_run = False
                # File has been modified, store new file stats and seek to previous position to read new lines
                self._f_stats = new_file_stats
                with open(log_file_path, 'r') as f:
                    f.seek(self._prev_pos)

                    # Read new lines after the previous position and process them immediately
                    for line in f:
                        try:
                            json_data = json.loads(line)
                            # CMDR has FSD Jumped to a system
                            if json_data.get("event") == "FSDJump":
                                star_system = json_data.get("StarSystem")
                                # Check if the system is the one we were targetting, if it is, copy the next system to the clipboard
                                if star_system == self.nav_target["System Name"]:
                                    print("Reached target system.")
                                    try:
                                        self.nav_target = next(self.nav)
                                        new_target = self.nav_target["System Name"]
                                        if new_target:
                                            pyperclip.copy(new_target)
                                            print(f"Copied: {new_target}")
                                        else:
                                            print("Couldn't copy next system in route!")
                                    except StopIteration:
                                        print("Reached the end of the route! Congratulations, CMDR, and good luck! o7")
                                        quit()

                        except json.JSONDecodeError as e:
                            print(f"Error parsing line: {line}: {e}")

                    # Update the previous position
                    self._prev_pos = f.tell()
            
            time.sleep(1)


if __name__ == "__main__":
    log_file_path = 'test_log.log'
    csv_file_path = 'systems.csv'
    route_copier = RouteCopier(log_file_path, csv_file_path)
    route_copier.watch_log_file()
