# EDRouteCopier

Python code that takes a neutron plotter route and automatically copies the next system name for you when entering the previous target system

## Installation and usage

1. Download and install Python (tested on version 3.12)
2. Run the script using `python main.py` inside the source system
    - Make sure that you are using a [Spansh](https://www.spansh.co.uk/plotter) route for the route file
    - Be sure to select your latest log file from the file picker dialogue
    - **Being inside the source system you plotted from is important!** The route copier relies on the first system you are in being the source system. If you are never in that system then it will never copy the next target meaning it will not progress the route as intended.

## Todo

### General

- [ ] Test with an actual route
- [x] Update install and usage guides
- Travel metrics
  - [x] Distance Traveled
  - [x] Jumps made

### UI Related

- [x] Make a UI
- [x] Display current System info
- [x] Display nav target system info
- [x] Display in game target system info
  - Provided in journals as `FSDTarget`
- [x] Display remaining/total jumps in route
  - Info will be from spansh route and may not be accurate as a result
  - Maybe also display actual jumps remaining for current nav target from the journal (provided in `FSDTarget` again)
