from os.path import dirname, realpath, isfile
from json import dump, load

class JsonManager:
    def __init__(self):
        self.path = dirname(realpath(__file__)) + '/'
    
    def create_json(self, file):
        data = {
            "nome":"",
            "votou_em":""
        }
        
        path_data_json = self.path + file
         
        if not isfile(path_data_json):
            with open(path_data_json, "w") as f:
                dump(data, f, indent=2, separators=(',', ': '))
            return True
            
        return False
    
    def read_json(self, file):
        if isfile(self.path + file):
            with open(self.path + file, 'r') as f:
                data = load(f)
            return data
        
        return False
    
    def update_json(self):
        ...

    
if __name__ == '__main__':
    jmanager = JsonManager()
    jmanager.create_json('data/data.json')
    print(jmanager.read_json('data/data.json')['nome'])
    