import os
import argparse  

class CSVReader :    
    "comments"
    def __init__(self, filename):   
        self.file1 = filename
        
    def readFile(self): 
        for line in open(self.file1, "r"):   
            print (line)
        
          
        

def main():
    #python readcsv.py --filename="~/Downloads/meeting.txt"
    parser = argparse.ArgumentParser(description='Count audio duration')
    parser.add_argument('--filename', help='folder with audio files', type=str, required=True)
    args = parser.parse_args()

    demo = CSVReader(args.filename) 
    demo.readFile()
  
 
if __name__=='__main__':
	main()