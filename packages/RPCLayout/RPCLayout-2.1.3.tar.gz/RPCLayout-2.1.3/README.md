# RPCLayout

![](https://cdn.discordapp.com/attachments/954499110763892807/955216312999739433/gato-digitando.gif)

A simple way to make a Discord rich presence with API using JSON parser to make it.
Includes a multiple functions to help in the development with apis json

** RPCLayout Stop in Last Build v2.0.3, no more updates until 21/03/22. Reason: Making web for documentation. **

# Installation
Simple as possible use:
```sh
python -m pip install RPCLayout
```
or clone code and use at module.
# Versions - Stable
### Version 2.1.3
- Added a functions to returns macs with m1 chip, use _system() or _isM1()
Small changes in ```__test__```class.

See it in https://pypi.org/project/RPCLayout/2.1.3/
### Version 2.0.3
- Fixed _checkGameIsClosed(), now recieves a string. Usage:
```python
myGame = "CSGO.exe"
while True: # main loop
    if _checkGameIsClosed(myGame) is True: # if the Game is closed returns True
        destroy(rpc, text="Game Exiting... RPC Disconnected.") # called destroy() function for destroy the rpc and process.
    time.sleep(60) # loop 60 s (ideal 5 seconds)
```

See it in https://pypi.org/project/RPCLayout/2.0.3/

### Version 2.0.2
- Fixed _waitingForGame() function, now recieve a string and complete the loop if found the game. Usage:
```python
myGame = "CSGO.exe" # depending operative system
_waitingForGame(myGame) # If found it, the code will continue. If not check your game variable.
# and continue the code...
while True:
    ...
```

- ```__test__``` class
    + Fixed callback_os(), change parameters
    + Can import as: ```import RPCLayout.__test__```

See it in https://pypi.org/project/RPCLayout/2.0.2/

### Version 2.0.1
+ Added:
    - ```__test__``` class for test functions.
    - _system() - Return the operating system
    - _getpid() - Return the actual PID of the program
    - destroy() - Destroy the actual process and RPC.
    - Added more HTTP Responses Error for request_api() function

See it in https://pypi.org/project/RPCLayout/2.0.1/

### Version 2.0.0
Bugs fixed, import fixed for MacOS

See it in https://pypi.org/project/RPCLayout/2.0.0/

# Repositories Used
[pypresence](https://github.com/qwertyquerty/pypresence)
[RotMGRPC](https://github.com/neopkr/RotMGRPC)

# Why?
I want to make more simple or easier to make an Discord Rich Presence with API.JSON, this idea born in my another project: [RotMGRPC](https://github.com/neopkr/RotMGRPC) meanwhile i was thinking how to make this process more faster or simple.

Yeah, it's a totally random idea but here i am


## Requires:
pip install requests
