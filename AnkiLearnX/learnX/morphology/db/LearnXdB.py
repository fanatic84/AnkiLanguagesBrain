import os
import sqlite3

from learnX.utils.Log import *
from learnX.utils.Globals import *


class LearnXdB:
    
    instance = None

    @staticmethod
    def getInstance():
       if LearnXdB.instance == None:
           LearnXdB.instance = LearnXdB()
       return LearnXdB.instance
       
    def __init__(self):

        self.learnXPath = learnXPath = Globals.LearnXPath

        self.dbPath = os.path.join(learnXPath, 'learnX', 'db', 'db.learnX')
        self.sqlPath = os.path.join(learnXPath, 'learnX', 'morphology', 'db', 'sql', 'tables.sql')        
        
        self.conn = sqlite3.connect(self.dbPath)
        
    def createDataBase(self):
        self.conn = sqlite3.connect(self.dbPath)
        
        c = self.conn.cursor()
        sqlScript = open(self.sqlPath, "r")
        c.executescript(sqlScript.read())
        
        self.conn.commit()
        c.close

    def openDataBase(self):
        return self.conn

