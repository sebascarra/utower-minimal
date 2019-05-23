# UTower Python scripts

These Python scripts are used by a closed-source node.js server to use the GPIO of a Raspberry Pi 3 Model B running stock Raspbian Stretch. 

## How to use this repository.

The node.js server only has to run scripts terminating in *app.py. For instance, the following will energize pump "my pump" (connected to pins specified in device_manager.py, line 11) in direction 1 (CW or CCW depening on how the motor has been physically wired):

```
python3 peristaltic_app.py start "my pump" 1
```


