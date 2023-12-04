from time import sleep
from datetime import datetime
from os import listdir, system, remove
from os.path import isfile, join


class Command_Manager():
    def __init__(self, directory):
        self.directory = directory
        self.protected_files = ['Octavius_Plantbot.py', 'Telegram_Manager.py', 'Camera_Manager.py', 'RF_Manager.py', 'Plant_Manager.py', 'Command_Manager.py']
        self.git_repo = 'https://raw.githubusercontent.com/8BitFishy/Octavius_PlantBot/main/'


    def Download_File(self, filename):
        system(f"wget -P {self.directory} {self.git_repo}{filename}")


    def Download_and_Remove_Files(self):
        try:
            self.Download_File("README.md")
            system(f"mv -f {self.directory}README.md.1 {self.directory}README.md")

            for i in range(len(self.protected_files)):
                self.Download_File(self.protected_files[i])
                system(f"mv -f {self.directory}{self.protected_files[i]}.1 {self.directory}{self.protected_files[i]}")

            return True, None

        except Exception as E:
            return False, E


    def Update(self, telegram_manager):
        print(str(datetime.now()).split('.')[0] + " - Action - Update")
        telegram_manager.Send_Message(f"Updating files")
        success, E = self.Download_and_Remove_Files()
        if success:
            print(str(datetime.now()).split('.')[0] + " - Update Complete")
            telegram_manager.Send_Message(f"Update complete, Rebooting")
            self.Reboot(telegram_manager)

        else:
            self.Handle_Error(E, telegram_manager)


    def Download(self, command, telegram_manager):
        filename = str(command[1])

        try:
            print(str(datetime.now()).split('.')[0] + f" - Action - Download {filename}")
            telegram_manager.Send_Message(f"Downloading {filename} from my repo")
            self.Download_File(filename)
            telegram_manager.Send_Message(f"{filename} downloaded")

        except Exception as E:
            self.Handle_Error(E, telegram_manager)

        return


    def Handle_Error(self, E, telegram_manager):
        telegram_manager.Send_Message("Action failed - " + E.__class__.__name__)
        print(str(datetime.now()).split('.')[0] + " - failed with exception:")
        print(E)
        return


    def Talk(self, telegram_manager):
        telegram_manager.Send_Message("I am active. My current commands are: ")
        telegram_manager.Send_Message("[Plug colour] [plug number] [on/off]")
        telegram_manager.Send_Message("Pic / Photo")
        telegram_manager.Send_Message("Video [length]")
        telegram_manager.Send_Message("Talk")
        telegram_manager.Send_Message("Reboot")
        telegram_manager.Send_Message("Update")
        telegram_manager.Send_Message("Download (filename")
        telegram_manager.Send_Message("Print files")
        telegram_manager.Send_Message("Print (filename)")
        telegram_manager.Send_Message("Length (filename)")
        telegram_manager.Send_Message("Delete (filename)")
        return


    def Reboot(self, telegram_manager):
        print(str(datetime.now()).split('.')[0] + " - Rebooting")
        telegram_manager.Send_Message("Rebooting")
        try:
            system("sudo reboot")
        except Exception as E:
            self.Handle_Error(E, telegram_manager)
        return


    def Delete(self, command, telegram_manager):
        filename = str(command[1])
        if filename not in self.protected_files:
            print(str(datetime.now()).split('.')[0] + " - Action - Deleting file: " + filename)
            telegram_manager.Send_Message(f"Deleting {filename}")

            try:
                remove(f'{self.directory}{filename}')
                telegram_manager.Send_Message(f"{filename} deleted")

            except Exception as E:
                self.Handle_Error(E, telegram_manager)

        else:
            telegram_manager.Send_Message("That file is protected, please don't delete this")

        return


    def Print_Files(self, telegram_manager):

        print(str(datetime.now()).split('.')[0] + " - Action - Read file names")

        try:
            print(str(datetime.now()).split('.')[0] + " - Searching directory: \n" + self.directory)
            telegram_manager.Send_Message("Files found:")

            for f in listdir(self.directory):
                if isfile(join(self.directory, f)):
                    telegram_manager.Send_Message(f)

        except Exception as E:
            self.Handle_Error(E, telegram_manager)


    def Print_File_Contents(self, command, telegram_manager):
        filename = str(command[1])
        with open(f'{self.directory}/{filename}') as file:
            count = sum(1 for _ in file)
            file.close()
        if count > 0:
            print(str(datetime.now()).split('.')[0] + " - Action - Sending file: ")
            print(f'{self.directory}{filename}')
            telegram_manager.Send_Message(f"Accessing {filename}")

            try:
                f = open(f'{self.directory}{filename}')
                if len(command) == 3:
                    for line in (f.readlines()[-int(command[2]):]):
                        telegram_manager.Send_Message(str(line).strip())

                else:
                    file_text = ""
                    for line in f.read():
                        file_text += (str(line))
                    telegram_manager.Send_Message(file_text)
                f.close()

            except Exception as E:
                self.Handle_Error(E, telegram_manager)

        else:
            telegram_manager.Send_Message(f"{filename} is currently empty")


    def File_Length(self, command, telegram_manager):
            filename = str(command[1])
            print(str(datetime.now()).split('.')[0] + " - Action - Sending length of file: " + filename)
            telegram_manager.Send_Message(f"Reading length of {filename}")

            try:
                with open(f'{self.directory}{filename}') as file:
                    count = sum(1 for _ in file)
                    telegram_manager.Send_Message(f"File is {count} lines long")
                    file.close()

            except Exception as E:
                self.Handle_Error(E, telegram_manager)


    def Take_Picture(self, camera_manager, telegram_manager):
        try:
            print(f"{str(datetime.now()).split('.')[0]} - Accessing camera to take picture")
            image_file = camera_manager.Take_Picture()
            telegram_manager.Send_Image(image_file)
            print(f"{str(datetime.now()).split('.')[0]} - Sending picture")
            return True

        except Exception as E:
            self.Handle_Error(E, telegram_manager)
            return False



    def Take_Video(self, command, camera_manager, telegram_manager):
        try:
            print(f"{str(datetime.now()).split('.')[0]} - Accessing camera to record {command[1]} second video")
            video_file, output = camera_manager.Take_Video(command[1])
            telegram_manager.Send_Video(video_file)
            print(f"{str(datetime.now()).split('.')[0]} - Sending video")
            return True

        except Exception as E:
            self.Handle_Error(E, telegram_manager)
            return False


    def Send_RF_Code(self, command, telegram_manager, rf_manager):

        print(str(datetime.now()).split('.')[0] + f" - Action - {command[0].lower()} {command[1]} {command[2]}")
        telegram_manager.Send_Message(f"Turning plug {command[0].lower()} {command[1]} {command[2]}")
        result = rf_manager.Code_Picker(target=str(command[0]).lower(), plug=command[1], action=command[2].lower())

        if result == 0:
            print(f"{str(datetime.now()).split('.')[0]} - Binary code transmitted")
            telegram_manager.Send_Message(f"Plug {command[0].lower()} {command[1]} turned {command[2]}")
            return True

        elif result == 1:
            print(f"{str(datetime.now()).split('.')[0]} - No binary codes available, could not transmit")
            telegram_manager.Send_Message(f"No binary codes found, please check files")
        elif result == 2:
            print(f"{str(datetime.now()).split('.')[0]} - Requested target not found")
            telegram_manager.Send_Message(f"Requested target not found")
        elif result == 3:
            print(f"{str(datetime.now()).split('.')[0]} - Failed to transmit code")
            telegram_manager.Send_Message(f"Failed to transmit code")
        elif result == 4:
            print(f"{str(datetime.now()).split('.')[0]} - Unknown error")
            telegram_manager.Send_Message(f"Unknown error")

        return False


def Generate_Command_Manager(directory):
    command_manager = Command_Manager(directory)
    return command_manager


if __name__ == '__main__':

    directory = __file__.strip("Command_Manager.py").strip(":")

    command_manager = Command_Manager(directory)

    update = input(f"Download file - 1\nUpdate Files - 2\n")

    if int(update) == 1:
        command_manager.Download(input("Enter the name of the file to download:\n"))


    elif int(update) == 2:
        command_manager.Download_and_Remove_Files()
