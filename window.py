import os
import wx
import logic
import matplotlib.figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg


class NumberValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.digits='0123456789'
        
    def Clone(self):
        return NumberValidator()

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()

        for x in val:
            if x not in self.digits:
                return False

        return True
    
    def OnChar(self, event):
        key = event.GetKeyCode()
        try:
            #8 - code of backspace, 9 - code tab
            if chr(key) in self.digits or key == 8 or key == 9:
                event.Skip()
            else:
                return False
        except ValueError, info:
            print chr(key)
            print info
        return     

class MainFrame(wx.Frame):
    
    def __init__(self, parent, id_, title, position, size, style, name):
        wx.Frame.__init__(self, parent, id_, title, position, size, style, name)
        self.SetMinSize(self.GetSize())
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.mainPanel = wx.Panel(self, -1, wx.DefaultPosition, self.GetSize())
        
        #creating new inserted sizer for text input
        self.insertedSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.staticTextCount = wx.StaticText(self.mainPanel, -1, "input count of classes:")
        self.insertedSizer1.Add(self.staticTextCount, 0, wx.ALIGN_CENTER)
        self.textCountOfClasses = wx.TextCtrl(self.mainPanel, validator=NumberValidator())
        self.insertedSizer1.Add(self.textCountOfClasses)
        self.mainSizer.Add(self.insertedSizer1, 0, wx.ALIGN_CENTER)
        #creating button for choosing data
        self.chooseDataBtn = wx.Button(self.mainPanel, -1, 'choose data file')
        self.path = ''#path to data file
        self.Bind(wx.EVT_BUTTON, self.OnClickChoseData, self.chooseDataBtn)
        #button start_calculation
        self.startBtn = wx.Button(self.mainPanel, -1, 'start calculation')
        self.Bind(wx.EVT_BUTTON, self.OnClickBtnStart, self.startBtn)
        #creating button for saving result in file
        self.saveBtn = wx.Button(self.mainPanel, -1, 'save results')
        self.result = ''
        self.Bind(wx.EVT_BUTTON, self.OnClickSaveBtn, self.saveBtn)
        #new inserted sizer
        self.insertedSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.insertedSizer2.Add(self.chooseDataBtn, 0, wx.ALIGN_CENTER)
        self.insertedSizer2.Add(self.startBtn, 0, wx.ALIGN_CENTER)
        self.insertedSizer2.Add(self.saveBtn, 0, wx.ALIGN_CENTER)
        self.mainSizer.Add(self.insertedSizer2, 0, wx.ALIGN_CENTER)
        
        #create graph
        self.resultClasses = list()
        self.namesObjects = list()
        self.listX = list()
        self.listY = list()
        self._graphStep = 0.01
        self.updateBtn = wx.Button(self.mainPanel, -1, 'Draw')
        
        self.listOfVariables = []
        
        self.chosenVar1 = ''
        self.chosenVar2 = ''
        self.insertedSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.instructionStatText1 = wx.StaticText(self.mainPanel, -1, 'Choose first variable')
        self.var1Choice = wx.Choice(self.mainPanel, choices=self.listOfVariables)
        self.var1Choice.Bind(wx.EVT_CHOICE, self.OnVar1Choice)
        
        self.instructionStatText2 = wx.StaticText(self.mainPanel, -1, 'Choose second variable')
        self.var2Choice = wx.Choice(self.mainPanel, choices=self.listOfVariables)
        self.var2Choice.Bind(wx.EVT_CHOICE, self.OnVar2Choice)

        self.insertedSizer3.Add(self.instructionStatText1, 0, wx.ALIGN_CENTER)
        self.insertedSizer3.Add(self.var1Choice, 0, wx.EXPAND)
        self.insertedSizer3.Add(self.instructionStatText2, 0, wx.ALIGN_CENTER)
        self.insertedSizer3.Add(self.var2Choice, 0, wx.EXPAND)
        
        #setting parameters of the plot
        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
        self.canvas.SetMinSize((100, 500))
        
        self.mainSizer.Add(self.insertedSizer3, 0, wx.ALIGN_CENTER)
        self.mainSizer.Add(self.canvas, flag=wx.ALL | wx.EXPAND, border=2)
        self.mainSizer.Add(self.updateBtn, flag=wx.ALIGN_CENTER, border=2)
        self.Bind(wx.EVT_BUTTON, self._onUpdateClick, self.updateBtn)
        
        self.mainPanel.SetSizer(self.mainSizer)
    
    def DrawGraph(self):
        self.axes.clear()
        self.axes.set_xlabel(self.chosenVar1)
        self.axes.set_ylabel(self.chosenVar2)
        self.axes.plot(self.listX, self.listY, 'or')
        self.axes.grid()
        for i in range(len(self.namesObjects)):
            self.axes.text(self.listX[i], self.listY[i], self.namesObjects[i])
            
        self.axes.set_xlim([0, max(self.listX)+2])
        self.axes.set_ylim([0, max(self.listY)+2])
        self.canvas.draw()
    
    def OnVar1Choice(self, event): 
        self.chosenVar1 = self.var1Choice.GetString(self.var1Choice.GetSelection())
        index_ = self.listOfVariables.index(self.chosenVar1)+1
        self.listX = logic.get_values(self.path, index_)
        
    def OnVar2Choice(self, event): 
        self.chosenVar2 = self.var2Choice.GetString(self.var2Choice.GetSelection())    
        index_ = self.listOfVariables.index(self.chosenVar2) + 1
        self.listY = logic.get_values(self.path, index_)
            
    def _onUpdateClick(self, event):   
        if self.chosenVar1 == '' or self.chosenVar2 == '':
            self.Warn(self, 'Choose variables')
        else:
            self.DrawGraph()

    def OnClickSaveBtn(self, event):
        #creating the dialogWindow for saving
        if not self.resultClasses:
            self.Warn(self, 'Nothing to save')
        else:
            wildcard = ("Comma separated values(*.csv)|*.csv|" 
                        "All files(*.*)|*.*")
            dialogSaveData=wx.FileDialog(self, "Save file as ...", 
                                     os.getcwd(), 
                                     defaultFile="save.csv", 
                                     wildcard=wildcard, style=wx.SAVE)
            if dialogSaveData.ShowModal() == wx.ID_OK:
                path = dialogSaveData.GetPath()
                file_ = open(str(path), 'w')
                #creating the string for file
                stringForFile = self.PrepareStringForSaving(self.resultString)
                file_.write(stringForFile)
                file_.close()
                
            dialogSaveData.Destroy()
            
    def PrepareStringForSaving(self, inStr):
        res = ''
        for i in range(len(inStr)):
            if inStr[i] == ':':
                res = res+', '
                continue
            if inStr[i] == ' ':
                continue
            else:
                res = res + inStr[i]
        return res
            
    def OnClickBtnStart(self, event):
        countOfClasses = self.textCountOfClasses.GetValue()
        if str(self.path) == '' or not os.path.isfile(self.path):
            self.Warn(self, "Wrong path")
        else:
            if countOfClasses == '':
                self.Warn(self, 'input count of classes')
            else:
                self.resultClasses = logic.calculating(self.path, int(countOfClasses))
                mes = ("Count of classes can not be bigger "  
                "than count of objects in input data")
                if not self.resultClasses:
                    self.Warn(self, mes)
                    return
                self.resultString = self.CreateResultString(self.resultClasses)
                resultFrame = ResultFrame(self, -1, 'result of calculating', 
                                         wx.DefaultPosition,(200, 200), wx.DEFAULT_FRAME_STYLE, 
                                         'rezult_frame', self.resultString)
                resultFrame.Show()
    
    def CreateResultString(self, resultClasses):
        resultString = ''
        for i in range(len(resultClasses)):
            resultString = resultString + resultClasses[i][0] + ': '
            for j in range(1, len(resultClasses[i])):
                resultString = resultString+resultClasses[i][j][0]
                if j != len(resultClasses[i]) - 1:
                    resultString = resultString + ", "
            resultString = resultString + '\n'
        return resultString
        
        
    def OnClickChoseData(self, event):
        wildcard =("Comma separated values(*.csv)|*.csv|"
                    "Text files(*.txt)|*.csv|"
                    "All files(*.*)|*.*")
        dialogDataChoose = wx.FileDialog(None, "Choose the data file", os.getcwd(), 
                                         "", wildcard, wx.OPEN)
        if dialogDataChoose.ShowModal() == wx.ID_OK:
            self.path = dialogDataChoose.GetPath()
            self.listOfVariables = logic.get_list_of_variables(self.path)
            self.var1Choice.SetItems(self.listOfVariables)
            self.var2Choice.SetItems(self.listOfVariables)
            self.namesObjects = logic.get_list_of_names(self.path)
            
        dialogDataChoose.Destroy()
    
    def Warn(self, parent, message, caption = 'Warning!'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()


class ResultFrame(wx.Frame):
        
    def __init__(self, parent, id_, title, position, size, style, name, resultString):
        wx.Frame.__init__(self, parent, id_, title, position, size, style, name)
        self.scroll=wx.ScrolledWindow(self, -1)
        statTextResult=wx.StaticText(self.scroll)
        statTextResult.SetLabel(resultString)
        self.scroll.SetScrollbars(1, 1, statTextResult.GetSize()[0], 
                                  statTextResult.GetSize()[1])
        
class App(wx.App):
    
    def OnInit(self):
        self.frame=MainFrame(None, -1, 'k-means method', 
                         wx.DefaultPosition, (600, 700), wx.DEFAULT_FRAME_STYLE, 'main_frame')
        self.frame.Show()
        self.SetTopWindow(self.frame)
      
        return True
    
if __name__=='__main__':
    app=App()
    app.MainLoop()