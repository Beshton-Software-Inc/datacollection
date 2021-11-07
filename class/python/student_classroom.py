import csv
import sys
class Room:
    studentList = dict()

    def __init__(self):
        with open('./studentlist.txt', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                self.studentList[row[0]] = row[1]
    
    def roomFinder(self):
        while True:
            name = input("enter student name: ")
            if name == "exit":
                break
            elif name in self.studentList:
                print("room number is", self.studentList[name])
            else: print("not found student name, please try again")

    def printRoomList(self, roomnumber):
        for student in self.studentList.keys():
            if studentList[student] == roomnumber:
                print('student:', student)
def main(args):
    r = Room() 
    print(r.roomFinder())
    
    
if __name__ == '__main__':
    main(sys.argv[1:])
   