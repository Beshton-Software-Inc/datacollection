import json
import pandas as pd
import numpy as np 

class jsonDemo:
    def __init__(self):
        self.__obj__ = """
            {"name": "Wes",
            "places_lived": ["United States", "Spain", "Germany"],
            "pet": null,
            "siblings": [{"name": "Scott", "age": 25, "pet": "Zuko"},
            {"name": "Katie", "age": 33, "pet": "Cisco"}]
            }
            """
        
    def get_json_to(self):
        result = json.loads(self.__obj__)
        siblings = pd.DataFrame(result['siblings'], columns=['name', 'age'])
        print(siblings)
        
def main():
    demo = jsonDemo()
    demo.get_json_to()
    
if __name__=='__main__':
	main()        