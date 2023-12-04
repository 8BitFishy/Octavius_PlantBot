from datetime import date, datetime
from time import sleep

class RFException(Exception):
    pass

class Timeout(Exception):
    pass

class Plant_Manager():
    def __init__(self, directory):
        self.directory = directory
        self.watering_diary = "Watering_Diary.txt"


    def Water_Plants(self, rf_manager, duration=10):
        timeout = 0

        try:
            result = rf_manager.Code_Picker(target="white", plug=1, action="off")

            if result != 0:
                raise RFException

            else:
                result = 1

                rf_manager.Code_Picker(target="white", plug=1, action="on")
                sleep(duration)

                while result != 0:
                    result = rf_manager.Code_Picker(target="white", plug=1, action="off")
                    timeout += 1
                    sleep(1)
                    if timeout >= 20:
                        raise Timeout

                if result == 0:
                    self.Update_Diary(duration)
                    return True, None

                else:
                    return False, None


        except Exception as E:
            return False, E


    def Water_On_Demand(self, rf_manager, telegram_manager, duration):
        print(f"{str(datetime.now()).split('.')[0]} - Watering plant for {duration} seconds")
        telegram_manager.Send_Message(f"Watering plant for {duration} seconds")

        success, E = self.Water_Plants(rf_manager, duration)

        if success:
            print(f"{str(datetime.now()).split('.')[0]} - Scheduled plant watering cycle initiated")
            telegram_manager.Send_Message(f"Plant watering complete")
            return None

        else:
            return E



    def Water_Schedule(self, rf_manager, telegram_manager):

        if self.Check_Diary():
            print(f"{str(datetime.now()).split('.')[0]} - Scheduled plant watering cycle initiated")
            success, E = self.Water_Plants(rf_manager)

            if success:
                print(f"{str(datetime.now()).split('.')[0]} - Scheduled plant watering cycle stopped")
                telegram_manager.Send_Message(f"Plants watered")
                return None

            else:
                return E


    def Update_Diary(self, duration):
        with open(f"{self.directory}{self.watering_diary}", "a") as file:
            file.write(f"{str(datetime.now()).split('.')[0]} - {duration} seconds")
            file.close()
        return



    def Check_Diary(self):
        with open(f"{self.directory}{self.watering_diary}", "r") as file:
            for line in (file.readlines()[-int(1):]):
                data = line.split(" - ")
                last_water = data[0]
            file.close()

        last_water = date(int(last_water.split("-")[0]), int(last_water.split("-")[1]), int(last_water.split("-")[2]))
        current_date = date(datetime.now().year, datetime.now().month, datetime.now().day)

        if current_date - last_water >= 7:
            return True

        else:
            return False
