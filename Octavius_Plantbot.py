import Camera_Manager
import RF_Manager
import Telegram_Manager
import Command_Manager
from platform import system
from time import ctime, sleep


class InitialisationError(Exception):
    pass


class PlantBot():
    def __init__(self, directory):
        self.telegram_manager = Telegram_Manager.generate_receiver(directory)
        self.rf_manager = RF_Manager.Generate_RF_Manager(directory)
        self.camera_manager = Camera_Manager.Generate_Camera_Manager(directory)
        self.command_manager = Command_Manager.Generate_Command_Manager(directory)

    def life_sign(self):

        if plantbot.telegram_manager == None:
            return False
        if plantbot.rf_manager == None:
            return False
        if plantbot.camera_manager == None:
            return False
        if plantbot.command_manager == None:
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

            elif action == "PHOTO" or action == "PIC":
                try:
                    print(f"{ctime()} - Accessing camera to take picture")
                    image_file = self.camera_manager.Take_Picture()
                    self.telegram_manager.Send_Image(image_file)
                    print(f"{ctime()} - Sending picture")

                except Exception as E:
                    self.command_manager.Handle_Error(E, self.telegram_manager)


        elif len(command) == 2:
            if action == "PRINT" and command[1] != "files":
                self.command_manager.Print_File_Contents(command, self.telegram_manager)

            elif action == "PRINT" and command[1] == "files":
                self.command_manager.Print_Files(self.telegram_manager)

            elif action == "VIDEO" and isinstance(command[1], int):

                try:
                    print(f"{ctime()} - Accessing camera to record {command[1]} second video")
                    video_file, output = self.camera_manager.Take_Video(command[1])
                    self.telegram_manager.Send_Image(video_file)
                    print(f"{ctime()} - Sending video")

                except Exception as E:
                    self.command_manager.Handle_Error(E, self.telegram_manager)


        elif len(command) == 3:

            if command[2].lower() == "on" or command[2].lower() == "off":
                print(ctime() + f" - Action - {command[0].lower()} {command[1]} {command[2]}")
                self.telegram_manager.Send_Message(f"Turning plug {command[0].lower()} {command[1]} {command[2]}")
                result = self.rf_manager.Code_Picker(target=str(command[0]).lower(), plug=command[1], action=command[2].lower())

                if result == 0:
                    print(f"{ctime()} - Binary code transmitted")
                    self.telegram_manager.Send_Message(f"Plug {command[0].lower()} {command[1]} turned {command[2]}")
                elif result == 1:
                    print(f"{ctime()} - No binary codes available, could not transmit")
                    self.telegram_manager.Send_Message(f"No binary codes found, please check files")
                elif result == 2:
                    print(f"{ctime()} - Requested target not found")
                    self.telegram_manager.Send_Message(f"Requested target not found")
                elif result == 3:
                    print(f"{ctime()} - Unknown error")
                    self.telegram_manager.Send_Message(f"Unknown error")

        else:
            print(ctime() + " - No action - Command not recognised")
            self.telegram_manager.Send_Message("Command not recognised")



if __name__ == '__main__':

    if system() == "Windows":
        directory = __file__.rpartition("\\")[0] + "\\"
    elif system() == "Linux":
        directory = __file__.strip("Octavius_Plantbot.py").strip(":")

    print(f"{ctime()} - Starting...")
    #sleep(10)
    print(f"{ctime()} - Initialising System")
    life_sign = False

    while not life_sign:

        try:
            plantbot = PlantBot(directory)
            life_sign = plantbot.life_sign()
            if not life_sign:
                raise InitialisationError

        except Exception as e:
            print(f"{ctime()} - Error initialising Plantbot - {e.__class__.__name__}")
            print(e)
            print(f"{ctime()} - Re-trying in 10 seconds")
            sleep(10)


    print(f"{ctime()} - Initialisation Complete")
    plantbot.telegram_manager.Send_Message("I am online...")
    plantbot.receiver_loop()
