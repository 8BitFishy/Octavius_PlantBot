import time
import RPi.GPIO as GPIO
import os


class RF_Manager:
    def __init__(self, binary_codes):
        self.binary_codes = binary_codes
        
    def Code_Picker(self, devicelist, target, action, number=None):
        
        if target == "black" or target == "white" and number != None:
            colour = target
            plug = number
            for i in range(len(self.binary_codes)):
                if self.binary_codes[i][0] == colour and self.binary_codes[i][1] == plug and self.binary_codes[i][2] == action:
                    print(f"Binary code - {self.binary_codes[i][3]}")
                    self.transmit_code(self.binary_codes[i][3])
        
        elif target == 'all':
            for i in range(len(self.binary_codes)):
                if self.binary_codes[i][2] == action:
                    self.transmit_code(self.binary_codes[i][3])
                    #time.sleep(0.2)

        else:
            for i in range(len(devicelist)):
                if devicelist[i][2] == target or devicelist[i][1] == target:
                    colour = devicelist[i][0]
                    plug = devicelist[i][1]
                    for i in range(len(self.binary_codes)):
                        if self.binary_codes[i][0] == colour and self.binary_codes[i][1] == plug and self.binary_codes[i][2] == action:
                                    self.transmit_code(self.binary_codes[i][3])
        
        return


    def transmit_code(self, binary_code):
        NUM_ATTEMPTS = 30
        TRANSMIT_PIN = 24
        #Transmit a chosen code string using the GPIO transmitter
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
        code = str(binary_code[0])
        print(f"Sending code {code}")
        for t in range(NUM_ATTEMPTS):
            for i in code:
                if i == '1':
                    GPIO.output(TRANSMIT_PIN, 1)
                    time.sleep(binary_code[2])
                    GPIO.output(TRANSMIT_PIN, 0)
                    time.sleep(binary_code[4] - binary_code[2])
                elif i == '0':
                    GPIO.output(TRANSMIT_PIN, 1)
                    time.sleep(binary_code[3])
                    GPIO.output(TRANSMIT_PIN, 0)
                    time.sleep(binary_code[3] - binary_code[2])
                else:
                    continue
            GPIO.output(TRANSMIT_PIN, 0)
            time.sleep(binary_code[1])
        GPIO.cleanup()
        return


        
def Generate_Code_List():
    binary_codes = []
    dir = "RF_Binary_Codes/Plugs-"

    for i in range(2):
        if i == 0:
            plug = 'Black'
        if i == 1:
            plug = "White"
        for file in os.walk(f"{dir}{plug}"):
            filelist = list(file[2])
            for file in filelist:
                with open(f"{dir}{plug}/{file}") as f:
                    code = []
                    for k in range(5):
                        line = next(f).strip()
                        data, value = line.rsplit(" - ")
                        if k == 0:
                            value = int(value)
                        else:
                            value = float(value)
                        
                        code.append(value)
                    binary_codes.append([plug.lower(), int(file[0]), file[2:5].rstrip('_').lower(), code])

    return binary_codes

def Generate_Devicelist():   
    devicelist = []
    dir = os.path.join("SystemLists/devicelist.txt")
    with open(dir) as f:
        line = f.read().splitlines()
        for i in line:
            colour, plug, device = i.rsplit("-")
            devicelist.append([colour, plug, device])
        for i in range(len(devicelist)):
            devicelist[i][0] = devicelist[i][0].lower()
            devicelist[i][0].rstrip()
            devicelist[i][1] = int(devicelist[i][1])
            devicelist[i][2] = devicelist[i][2].lower()
            devicelist[i][2].rstrip()
    return devicelist


def Generate_RF_Manager():
    binary_codes = Generate_Code_List()
    RF_Man = RF_Manager(binary_codes)
    return RF_Man
    
    
    
if __name__ == '__main__':
    RF_Man = Generate_RF_Manager()
    devicelist = Generate_Devicelist()
    
    while True:
        
        user_input = input("Enter your command: ")
        command = user_input.split(" ")
        colour = command[0].lower()
        try:
            plug = int(command[1])
            action = command[2].lower()

        except:
            plug = None
            action = command[1].lower()
        try:
            print(f"Target = {colour}")
            print(f"Number = {plug}")
            print(f"Action = {action}")
        except:
            pass
        RF_Man.Code_Picker(devicelist, colour, action, number=plug)
        
        time.sleep(2)
