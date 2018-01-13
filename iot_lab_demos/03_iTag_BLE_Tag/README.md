# iTag
## Demonstrations

Before executing a script, make sure that the smart tag is turned on by pressing its button until a click.

ID | File                                                                           | Description       
---|--------------------------------------------------------------------------------|------------------------------------------------------------------
01 | [01_iTag_activate_alarm.py](01_iTag_activate_alarm.py)                         | Activate the alarm of the tag
02 | [02_iTag_deactivate_alarm.py](02_iTag_deactivate_alarm.py)                     | Deactivate the alarm of the tag (it can also be deactivated by pressing its button)
03 | [03_iTag_spoofing.py](03_iTag_spoofing.py)                                     | Clone the tag
04 | [04_iTag_subscribe_btn_evt.py(04_iTag_subscribe_btn_evt.py)                    | Subscribe to the button events

### 03_iTag_spoofing.py
1. Edit the variable `PATH_TO_GATTACKER_FOLDER` with the path to the GATTacker installation folder
2. Launch the iSearching mobile application
3. Turn on the tag by pressing its button until a beep
4. Connect to the tag with iSearching
5. Launch this script
6. Turn off the tag by presing its button until a beep
iSearching should be now connected to the clone and not to the real device. The alarm isn't fired.

## Requirements
- [pygatt](https://github.com/peplin/pygatt)
- [GATTacker](https://github.com/securing/gattacker)
- [iSearching](https://play.google.com/store/apps/details?id=com.lenzetech.antilost)
