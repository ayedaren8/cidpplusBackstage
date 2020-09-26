from ehall.Spider import Spider
from ehall.SpiderJw import SpiderJw
from ehall.SpiderPost import SpiderPost
from ehall.Process import Process
from ehall.config import config
import json
import time


class Recive():
    URL = {
        "info": "https://jw.cidp.edu.cn/RegisterInfo/RegisterManageHandler.ashx",
        "cardMoney": "http://ehall.cidp.edu.cn/publicapp/sys/myyktzd/api/getConsumeByRange.do?startY=2019&startM=7&endY=2019&endM=12&isOvered=0&_=",
        "netCost": "http://ehall.cidp.edu.cn/jsonp/personalRemind/getViewDataDetail.do?wid=950af967525b4bffb3db654958683e3d&mailAccount=&_=",
        "exam": "https://jw.cidp.edu.cn/Student/StudentExamArrangeTableHandler.ashx",
        "course": "https://jw.cidp.edu.cn/Teacher/TimeTableHandler.ashx",
        "grade":"https://jw.cidp.edu.cn/Teacher/MarkManagement/StudentAverageMarkSearchFZ.aspx",
    }

    DATA = {
        "course": {'action': 'getTeacherTimeTable', 'isShowStudent': '1', 'semId': '62', 'testTeacherTimeTablePublishStatus': '1'},
        "exam": {'semId': '62'},
        "info": {'action': 'getInfo'}
    }

    PostApi = ["grade", "info", "exam", "course"]

    def __init__(self, request):
        self.request = request
        self.username = json.loads(request.body)["username"]
        self.password = json.loads(request.body)["password"]
        self.apiname = json.loads(request.body)["apiname"]
        self.res = ""
        self.configs()

    def configs(self):
        cf = config()
        semID = cf.get("SCHOOL", 'SemID')
        dic = {
            "course": {'action': 'getTeacherTimeTable', 'isShowStudent': '1', 'semId': semID, 'testTeacherTimeTablePublishStatus': '1'},
            "exam": {'semId': semID}}
        Recive.DATA.update(dic)
        
    def choose(self):
        if self.apiname in Recive.PostApi:
            self.post()
        else:
            self.get()

    def post(self):
        if self.apiname == 'grade':
            SPD = SpiderJw(url=Recive.URL[self.apiname],username=self.username, password=self.password)
            RES = SPD.run()
            self.res = Process(RES).run()
        else:
            SPD = SpiderPost(url=Recive.URL[self.apiname], username=self.username,
                             password=self.password, data=Recive.DATA[self.apiname])
            RES = SPD.run()
            self.res = Process(RES).run()

    def get(self):
        re = int(round(time.time() * 1000))
        SPD = Spider(url=Recive.URL[self.apiname]+str(re),
                     username=self.username, password=self.password)
        RES = SPD.run()
        self.res = Process(RES).run()

    def run(self):
        self.choose()
        return self.res