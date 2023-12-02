from time import sleep, ctime
from os import listdir, system, remove
from os.path import isfile, join


class Command_Manager():
    def __init__(self, directory):
        self.directory = directory
        self.protected_files = ['Octavius_Plantbot.py', 'Telegram_Manager.py', 'Camera_Manager.py', 'RF_Manager.py', 'Command_Manager.py']
        self.git_repo = 'https://raw.githubusercontent.com/8BitFishy/Octavius_PlantBot/deployed/'


    def Update(self, telegram_manager):
        print(ctime() + " - Action - Update")
        telegram_manager.Send_Message(f"Updating files")

        try:
            for i in range(len(self.protected_files)):
                system(f"rm {self.directory}{self.protected_files[i]}")
                system(f"wget -P {self.directory} {self.git_repo}{self.protected_files[i]}")

            print(ctime() + " - Update Complete")
            telegram_manager.Send_Message(f"Update complete, Rebooting")
            self.Reboot(telegram_manager)

        except Exception as E:
            self.Handle_Error(E, telegram_manager)


    def Download(self, command, telegram_manager):
        filename = str(command[1])

        try:
            print(ctime() + f" - Action - Download {filename}")
            telegram_manager.Send_Message(f"Downloading {filename} from my repo")
            system(f"wget -P {self.directory} {self.git_repo}{filename}")
            telegram_manager.Send_Message(f"{filename} downloaded")

        except Exception as E:
            self.Handle_Error(E, telegram_manager)

        return

    def Handle_Error(self, E, telegram_manager):
        telegram_manager.Send_Message("Action failed - " + E.__class__.__name__)
        print(ctime() + " - failed with exception:")
        print(E)
        return

    def Talk(self, telegram_manager):
        telegram_manager.Send_Message("I am active. My current commands are: ")
        telegram_manager.Send_Message("On")
        telegram_manager.Send_Message("Off")
        telegram_manager.Send_Message("Hold")
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
        print(ctime() + " - Rebooting")
        telegram_manager.Send_Message("Rebooting")
        try:
            system("sudo Reboot")
        except Exception as E:
            self.Handle_Error(E, telegram_manager)
        return

    def Delete(self, command, telegram_manager):
        filename = str(command[1])
        if filename not in self.protected_files:
            print(ctime() + " - Action - Deleting file: " + filename)
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

        print(ctime() + " - Action - Read file names")

        try:
            print(ctime() + " - Searching directory: \n" + self.directory)
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
            print(ctime() + " - Action - Sending file: ")
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
            print(ctime() + " - Action - Sending length of file: " + filename)
            telegram_manager.Send_Message(f"Reading length of {filename}")

            try:
                with open(f'{self.directory}{filename}') as file:
                    count = sum(1 for _ in file)
                    telegram_manager.Send_Message(f"File is {count} lines long")
                    file.close()

            except Exception as E:
                self.Handle_Error(E, telegram_manager)







def Generate_Command_Manager(directory):
    command_manager = Command_Manager(directory)
    return command_manager