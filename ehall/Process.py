import json
class Process:
    def __init__(self, data):
        self.data = data
        self.Rdata = ""

    def check(self):
        if self.data[0] =='':
            self.normalMes()
        else:
            self.wrongMes()
            

    def wrongMes(self):
        dic = {
            "STATUS": "Error",
            "message": self.data[0]
        }
        self.Rdata = dic

    def clear(self):
        try:
           self.data[1]=json.loads(self.data[1])
        except:
           print(self.data[1]) 

    def normalMes(self):

        dic = {
            "STATUS": "OK",
            "message": self.data[1]
        }
        self.Rdata = dic

    def run(self):
        self.check()
        return self.Rdata