"""
Compatible with Python 3.12
Last MOD: 3/29/2024

Updated by Yu Okamura
Please contact yokamura@asu.edu for errors.
"""

import time
import keyboard
import serial

def send_data(ser, first, second, cache):
    """
    Sends data from the website to the Arduino microcontroller.
    :param ser: Serial connection object.
    :param first: Letter in decimal.
    :param second: Column index.
    :param cache: Cache array to store sent data.
    """
    arduino(ser, first)
    time.sleep(1)
    column_count = second
    ser.write(bytes([column_count]))  # sends number
    print(ser.readline().decode().strip())  # Read the newest output from the Arduino
    cache.append(first)

def clear_cache(ser, cache):
    """
    Clears the letter cache.
    :param ser: Serial connection object.
    :param cache: Cache array to be cleared.
    """
    column_count = 0
    for i in cache:
        print("")
        arduino(ser, i)
        arduino(ser, column_count)
        column_count += 1

    cache.clear()

def arduino(ser, character):
    """
    Encodes character and sends it to the Arduino, and reads any inputs from the Arduino.
    :param ser: Serial connection object.
    :param character: Character to send (expected as a string or int).
    """
    ser.write(chr(character).encode())  # Encode character and send to Arduino
    print(ser.readline().decode().strip())  # Read and print the newest output from Arduino

def webinfo_to_arduino(ser, engine, text, data, cache):
    """
    Processes and sends web information letter by letter to Arduino based on data.json references.
    :param ser: Serial connection object.
    :param engine: Text-to-speech engine instance.
    :param text: Text to process and send.
    :param data: Data from JSON containing letter mappings.
    :param cache: Cache array for managing sent data.
    """
    count = 0
    for i in text:
        print("\nCharacter:", i)

        for x in data["letters"]:
            if x["letter"] == i:
                print("CELL:", count)
                print("Shift:", x["shift"])

                if ser:
                    send_data(ser, x["shift"], count, cache)
                time.sleep(1)

                if count == 9:
                    flag = True
                    print("Press 'x + right arrow' to continue")

                    while flag:
                        if keyboard.is_pressed('x+right arrow'):
                            count = 0
                            clear_cache(ser, cache)
                            flag = False
                else:
                    count += 1

        # Quit if 'x + down arrow' is pressed
        if keyboard.is_pressed('x+down arrow'):
            engine.say('Quitting')
            engine.runAndWait()
            print("Quitting")
            break
