from os import wait
from time import sleep
import tracker
from websites import websites


class Wclass():
    def __init__(self, oldString, url, id):
        self.oldString = oldString
        self.url = url
        self.id = id

    def __repr__(self):
        return "url: " + self.url + " id: " + self.id + " oldString: " + self.oldString

    def __str__(self):
        return "url: " + self.url + " id: " + self.id + " oldString: " + self.oldString


webObjects = list()
for i in websites:
    oldString = tracker.getInitialPage(i["url"], i["divId"])
    webObjects.append(Wclass(oldString, i["url"], i["divId"]))

for i in webObjects:
    print(i)
