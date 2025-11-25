from machine import Pin, PWM
from servo_translator import translate
import time

SHOULDER_SERVO = PWM(Pin(0))
SHOULDER_SERVO.freq(50)

ELBOW_SERVO = PWM(Pin(1))
ELBOW_SERVO.freq(50)

WRIST_SERVO = PWM(Pin(2))
WRIST_SERVO.freq(50)

GOTO_TAG = "G1"
SERVO_CONTROL_TAG = "M"

SHOULDER_TAG = "S"
ELBOW_TAG = "E"

WRIST_UP_DEGREE = 0
WRIST_DOWN_DEGREE = 30

def read_gcode(file_name, raw_gcode_commands):
    with open(file_name, "r") as f:
        for line in f:
            line = str(line)
            raw_gcode_commands.append(line.strip())

def interpret_gcode(raw_gcode_commands):
    for command in raw_gcode_commands:
        command = str(command)
        if command.startswith(GOTO_TAG):
            angles = command[2:].split()

            shoulder_angle = None
            elbow_angle = None
            for angle in angles:
                angle = str(angle).strip()
                if (angle).startswith(SHOULDER_TAG):
                    shoulder_angle = float(angle[1:])
                elif (angle).startswith(ELBOW_TAG):
                    elbow_angle = float(angle[1:])
            try:
                execute_move_arm(shoulder_angle, elbow_angle)
            except:
                print(f"Invalid command: {command}")
        elif command.startswith(SERVO_CONTROL_TAG):
            code = command[1:]

            if code == "3":
                # Places the wrist in the "down" position
                WRIST_SERVO.duty_u16(translate(WRIST_DOWN_DEGREE))
            elif code == "5":
                # Places the wrist in the "up" position
                WRIST_SERVO.duty_u16(translate(WRIST_UP_DEGREE))
            elif code == "18":
                print("disabling servos")
                break
            else:
                print("Unexpected error. You shouldn't be here.")
        
        time.sleep(0.5)

def execute_move_arm(shoulder_angle, elbow_angle):
    if ((shoulder_angle == None) or (elbow_angle == None)):
        raise ValueError
    
    SHOULDER_SERVO.duty_u16(translate(shoulder_angle))
    ELBOW_SERVO.duty_u16(translate(elbow_angle))

raw_gcode_commands = []
read_gcode("line.gcode", raw_gcode_commands)

for command in raw_gcode_commands:
    print(command)

    time.sleep(0.5)

interpret_gcode(raw_gcode_commands)