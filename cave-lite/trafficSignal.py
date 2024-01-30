from threading import Thread
from tkinter import font
from time import sleep
import tkinter as tk
import msgIntersect
from msgIntersect import red, yellow, green
import sys


class traffic_signal:
  def __init__(self, count, C, offset):
    global count_font
    self.count = count # countdown to next signal placed at center of each phase
    self.C = C # canvas to draw on
    self.offset = offset # position left to right for this instance to draw its light
    count_font = font.Font(family="Helvetica",size=20, weight="normal")
    C.create_rectangle(offset+0,30,offset+100,370,fill="black")
    C.create_oval(offset+3,40,offset+100,140,fill="gray")
    C.create_oval(offset+3,150,offset+100,250,fill="gray")
    C.create_oval(offset+3,260,offset+100,360,fill="gray")
    C.create_text(offset+50,95,font=count_font,text="")
    C.create_text(offset+50,205,font=count_font,text="")
    C.create_text(offset+50,315,font=count_font,text="")

  def setRed(self):
    self.redLight = self.C.create_oval(self.offset+3,40,self.offset+100,140,fill="red")
    self.redText = self.C.create_text(self.offset+50,95,font=count_font,text=self.count)

  def setYellow(self):
    self.yellowLight = self.C.create_oval(self.offset+3,150,self.offset+100,250,fill="yellow")
    self.yellowText = self.C.create_text(self.offset+50,205,font=count_font,text=self.count)

  def setGreen(self):
    self.greenLight = self.C.create_oval(self.offset+3,260,self.offset+100,360,fill="green")
    self.greenText = self.C.create_text(self.offset+50,315,font=count_font,text=self.count)
    

  def clearAll(self):
    self.C.delete(self.redLight)
    self.C.delete(self.yellowLight)
    self.C.delete(self.greenLight)

  def clearText(self):
    self.C.delete(self.redText)
    self.C.delete(self.yellowText)
    self.C.delete(self.greenText)

class signal:
  def __init__(self, top):
    self.top = top # hold a window frame
    self.C = tk.Canvas(self.top, bg="white", height=400, width=215)

  def red(self):
    self.light = traffic_signal(countdown,self.C,55)
    self.C.pack()
    self.light.setRed()
    red.on()
    yellow.off()
    green.off()

  def yellow(self):
    self.light = traffic_signal(countdown,self.C,55)
    self.C.pack()
    self.light.setYellow()
    red.off()
    yellow.on()
    green.off()

  def green(self):
    self.light = traffic_signal(countdown,self.C,55)
    self.C.pack()
    self.light.setGreen()
    red.off()
    yellow.off()
    green.on()

  def clear(self):
    self.light = traffic_signal(countdown,self.C,55)
    self.C.pack()
    red.off()
    yellow.off()
    green.off()


def getState():
  global countdown
  while(1):
    msgIntersect.all
    state = msgIntersect.updatingState
    countdown = msgIntersect.countdown
    status(state)
    sleep(0.1)

def status(status):
  if (status == "stop-And-Remain"):
    state.red()
  elif (status == "protected-clearance"):
    state.yellow()
  elif (status == "protected-Movement-Allowed"):
    state.green()
  else: state.clear()

def loop(top):
  top.mainloop()

def main():

  print("Starting Traffic Signal\n")
  global top
  global state
  top = tk.Tk() # create a window frame
  state = signal(top)

  stateChangeThread = Thread(target = getState, args=(),  daemon = True)
  stateChangeThread.start()

  loop(top)


if __name__ == '__main__':
  sys.exit(main())
