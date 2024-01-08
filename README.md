# EDRouteCopier

Python code that takes a neutron plotter route and automatically copies the next system name for you when entering the previous target system

## Installation and usage

1. Download and install Python (tested on version 3.12)
2. Install requirements: `pip install requirements.txt` (run while in the project root folder)
3. Edit `route_copier.py`
    - Change `log_file_path` to point to your latest journal file in `C:\Users\<username>\Saved Games\Frontier Developments\Elite Dangerous`
    - Change `csv_file_path` to point to your neutron plotter route you downloaded from [Spansh](https://www.spansh.co.uk/plotter)
4. Run the script using `python route_copier.py` inside the source system
    - **Being inside the source system you plotted with is important!** The route copier relies on the first system you are in being the source system. If you are never in that system then it will never copy the next target meaning it will not progress the route as intended.

## Todo

### General

- [ ] Test with an actual route
- [ ] Automatically gather the latest journal (or maybe just use a file picker again...)
- [ ] Update install and usage guides
- Travel metrics
  - [ ] Distance Traveled
  - [ ] Jumps remaining out of (estimated) Total
  - [ ] Journey time length? (save timestamp of when the first jump is made and calculate trip time when last jump is complete)

### UI Related

- [ ] Make a UI
- [ ] Display current System info
- [ ] Display nav target system info
- [ ] Display in game target system info
  - Provided in journals as `FSDTarget`
- [ ] Display remaining/total jumps in route
  - Info will be from spansh route and may not be accurate as a result
  - Maybe also display actual jumps remaining for current nav target from the journal (provided in `FSDTarget` again)
