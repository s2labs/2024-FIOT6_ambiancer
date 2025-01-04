"""
Includes the controlling logic for the 32x32 iDotMatrix through BT.

The iDotMatrix is controlled via BT using a secondary program within 
the idotmatrix folder. The value of --address must be changed to match
the BT Address of the device. The value in this code is using MacOS.

"""
import subprocess
import time


COMMAND_LISTS = {
    "sad": "python3 idotmatrix/app.py --address 9E22F3A3-DB21-8ACD-AF8C-74111C920472 --image true --set-image idotmatrix/images/sad.png --set-brightness 100",  # negative
    "neutral": "python3 idotmatrix/app.py --address 9E22F3A3-DB21-8ACD-AF8C-74111C920472 --image true --set-image idotmatrix/images/confused.png --set-brightness 100",
    "happy": "python3 idotmatrix/app.py --address 9E22F3A3-DB21-8ACD-AF8C-74111C920472 --image true --set-image idotmatrix/images/happy.png --set-brightness 100",  # positive
    "faster": "python3 idotmatrix/app.py --address 9E22F3A3-DB21-8ACD-AF8C-74111C920472 --set-gif idotmatrix/images/MainCharacter_32x32_run.gif --process-gif 32",
    "slower": "python3 idotmatrix/app.py --address 9E22F3A3-DB21-8ACD-AF8C-74111C920472 --set-gif idotmatrix/images/Geoff-anims-x2_Walk.gif --process-gif 32",
    "time-over": "python3 idotmatrix/app.py --address 9E22F3A3-DB21-8ACD-AF8C-74111C920472 --set-gif idotmatrix/images/d3785ecb3978661.gif --process-gif 32",
    "disgust": "python3 idotmatrix/app.py --address 9E22F3A3-DB21-8ACD-AF8C-74111C920472 --image true --set-image idotmatrix/images/sick.png --set-brightness 100",
    "fear": "python3 idotmatrix/app.py --address 9E22F3A3-DB21-8ACD-AF8C-74111C920472 --image true --set-image idotmatrix/images/fear.png --set-brightness 100",
    "surprise": "python3 idotmatrix/app.py --address 9E22F3A3-DB21-8ACD-AF8C-74111C920472 --image true --set-image idotmatrix/images/surprised.png --set-brightness 100",
    "angry": "python3 idotmatrix/app.py --address 9E22F3A3-DB21-8ACD-AF8C-74111C920472 --image true --set-image idotmatrix/images/angry.png --set-brightness 100"
}


def matrix_command(action: str):
    print(f"Seeking for {action}")
    cmd = COMMAND_LISTS.get(action, None)
    if cmd is None:
        print(f"The incoming action {action} is not recognized...")
        return
    cmd = cmd.split(" ")
    subprocess.run(cmd)
    pass


if __name__ == "__main__":
    matrix_command("time-over")
    time.sleep(5)
    matrix_command("sad")
    time.sleep(2)
    matrix_command("neutral")
