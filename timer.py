#!/usr/bin/env python

from tkinter import *
import time
from datetime import datetime

class Timer(Frame):  
    """ Implements timer frame widget """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0
        self._elapsedtime = 0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()
        self.something = StringVar()
        self.entryFunction()
        self.overalltime = 0

    def makeWidgets(self):                         
        """ Creates the time label """
        l = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=2, padx=2)                      
    
    def _update(self): 
        """ Update the time label with elapsed time """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))
        
    def Start(self):                                                     
        """ Start the timer, ignores if running """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1
    
    def Stop(self):                                    
        """ Stops the timer, ignores if stopped """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start
            self.overalltime = self._elapsedtime + self.overalltime
            self._setTime(self._elapsedtime)
            self._running = 0
            myfile= open("time.txt", "a")
            myfile.write("\n" + str(" Stop: " + 
            "%.2f" % self._elapsedtime +
            "\n--Overall Time: " +
             "%.2f" % self.overalltime + "\n"))
            myfile.close()
    
    def Reset(self):                                  
        """ Resets the timer """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
            myfile= open("time.txt", "a")
            myfile.write("\n" + str("%.2f" % self._elapsedtime))
            myfile.close()

        self._start = time.time()
        self.overalltime = 0.0
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)

    def Lap(self):
        """ Laps the timer """
        myfile= open("time.txt", "a")
        myfile.write("\n" + str("  Lap: " + "%.2f" % self._elapsedtime))
        myfile.close()
        self.overalltime = self._elapsedtime + self.overalltime
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)

    def addActivity(self):
        """ Saves activity's name and resets time """
        if self.entry.get() != "":
            myfile= open("time.txt", "a") 
            myfile.write("\nActivity: " + self.entry.get())
            myfile.close()

        self._start = time.time()
        self.overalltime = 0.0
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)

    def entryFunction(self):
        """ Area to enter your activity """
        self.something.set("Enter your activity here")
        self.entry = Entry(self, textvariable = self.something)
        self.entry.pack(fill=X, expand=NO, pady=2, padx=2)

def main():
    root = Tk()
    t = Timer(root)
    root.wm_title('Timer')
    t.pack(side=TOP)

    """ Buttons """
    Button(root, text='Submit Activity', width=10,
           command=t.addActivity).pack(side=TOP)    
    Button(root, text='Start',
           command=t.Start).pack(side=LEFT, pady=2, padx=2)
    Button(root, text='Lap',
           command=t.Lap).pack(side=LEFT, pady=2, padx=2)
    Button(root, text='Stop',
           command=t.Stop).pack(side=LEFT, pady=2, padx=2)
    Button(root, text='Reset',
           command=t.Reset).pack(side=LEFT, pady=2, padx=2)
    Button(root, text='Quit',
           command=root.quit).pack(side=LEFT, pady=2, padx=2)
    
    """ Adds date the application is started in the text field """
    now = datetime.now()
    myfile= open("time.txt", "a") 
    myfile.write('\n-----%s/%s/%s------' % (now.month, now.day, now.year))
    myfile.close()
    
    root.mainloop()

if __name__ == '__main__':
    main()
