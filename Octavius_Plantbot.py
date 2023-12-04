import Camera_Manager
import RF_Manager
import Telegram_Manager
import Command_Manager
import Plant_Manager

from platform import system
from time import sleep
from datetime import datetime

class InitialisationError(Exception):
    pass


class PlantBot():
    def __init__(self, directory):
        self.telegram_manager = Telegram_Manager.generate_receiver(directory)
        self.rf_manager = RF_Manager.Generate_RF_Manager(directory)
        self.camera_manager = Camera_Manager.Generate_Camera_Manager(directory)
        self.command_manager = Command_Manager.Generate_Command_Manager(directory)
        self.plant_manager = Plant_Manager.Generate_Plant_Manager(directory)


    def life_sign(self):

        if plantbot.telegram_manager == None:
            return False
        if plantbot.rf_manager == None:
            return False
        if plantbot.camera_manager == None:
            return False
        if plantbot.command_manager == None:
            return False
        if plantbot.plant_manager == None:
            return False

        return True



    def receiver_loop(self):
        while True:
            text = self.telegram_manager.Get_Response()
            if text != "":
                self.Interpret_Commands(text)



            sleep(2)



    def Interpret_Commands(self, msg):

        command = msg.split()
        action = command[0].upper()

        for i in range(len(command)):
            if command[i].isnumeric():
                try:
                    command[i] = int(command[i])
                except:
                    command[i] = float(command[i])

        try:
            if len(command) == 1:
                if action == "HELLO":
                    self.telegram_manager.Send_Message("Hello, what can I do for you?")

                elif action == 'TALK':
                    self.command_manager.Talk(self.telegram_manager)

                elif action == "REBOOT":
                    self.command_manager.Reboot(self.telegram_manager)

                elif action == "DELETE":
                    self.command_manager.Delete(command, self.telegram_manager)

                elif action == "LENGTH":
                    self.command_manager.File_Length(command, self.telegram_manager)

                elif action == "UPDATE":
                    self.command_manager.Update(self.telegram_manager)

                elif action == "DOWNLOAD":
                    self.command_manager.Download(command, self.telegram_manager)

                elif action == "PHOTO" or action == "PIC" or action == "PICTURE":
                    self.command_manager.Take_Picture(self.command_manager, self.telegram_manager)


            elif len(command) == 2:

                if action == "PRINT" and command[1] == "files":
                    self.command_manager.Print_Files(self.telegram_manager)

                elif action == "VIDEO" and isinstance(command[1], int):
                    self.command_manager.Take_Video(command, self.camera_manager, self.telegram_manager)

                elif action == "WATER" and isinstance(command[1], int):
                    E = self.plant_manager.Water_On_Demand(self.rf_manager, self.telegram_manager, duration = int(command[1]))
                    if E is not None:
                        self.command_manager.Handle_Error(E, self.telegram_manager)

            elif len(command) == 3:

                if action == "PRINT" and command[1] != "files":
                    self.command_manager.Print_File_Contents(command, self.telegram_manager)

                elif command[2].lower() == "on" or command[2].lower() == "off":
                    self.command_manager.Send_RF_Code(command, self.telegram_manager, self.rf_manager)


            else:
                print(str(datetime.now()).split('.')[0] + " - No action - Command not recognised")
                self.telegram_manager.Send_Message("Command not recognised")

        except Exception as E:
            self.command_manager.Handle_Error(E, self.telegram_manager)



if __name__ == '__main__':

    if system() == "Linux":
        directory = __file__.strip("Octavius_Plantbot.py").strip(":")
        sleep(10)

    else:
        directory = __file__.rpartition("\\")[0] + "\\"

    print(f"{str(datetime.now()).split('.')[0]} - Starting...")
    print(f"{str(datetime.now()).split('.')[0]} - Initialising System")
    life_sign = False
    success = False
    timeout = 0

    plantbot = None

    while not life_sign:

        try:
            plantbot = PlantBot(directory)
            life_sign = plantbot.life_sign()
            if not life_sign:
                raise InitialisationError

        except Exception as e:
            print(f"{str(datetime.now()).split('.')[0]} - Error initialising Plantbot - {e.__class__.__name__}")
            print(e)
            print(f"{str(datetime.now()).split('.')[0]} - Re-trying in 10 seconds")
            sleep(10)

    print(f"{str(datetime.now()).split('.')[0]} - Initialisation Complete")

    while not success:
        success = plantbot.telegram_manager.Send_Message("I am online...")
        if timeout > 10:
            success = True
        timeout += 1

    plantbot.receiver_loop()
