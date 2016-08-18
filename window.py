import wx
import main_logic
from wx import Panel


class Frame(wx.Frame):
    
    def __init__(self, parent, id_, title, position, size, style, name):
        wx.Frame.__init__(self, parent, id_, title, position, size, style, name)
        self.SetMinSize(self.GetSize())
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel=wx.Panel(self,-1,wx.DefaultPosition,self.GetSize(),wx.TAB_TRAVERSAL|wx.NO_BORDER,'pan')
        button_start = wx.Button(panel,-1,'start calculation')
        button_start.SetMinSize(button_start.GetSize())
        sizer.Add(button_start, wx.ALIGN_CENTER, wx.EXPAND, wx.TOP)
        text_count_of_classes=wx.TextCtrl(panel, -1, "enter count of classes")
        text_count_of_classes.SetMinSize((100, 25))
        sizer.Add(text_count_of_classes,flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()
        
        
    def OnClick_button_start(self,event):
        
        rezult_classes=main_logic.calculating(self.count_of_classes)
        
class App(wx.App):
    
    def OnInit(self):
        self.frame=Frame(None, -1, 'k-means method',
                         wx.DefaultPosition, (600,700), wx.DEFAULT_FRAME_STYLE, 'main_frame')
        self.frame.Show()
        self.SetTopWindow(self.frame)
      
        return True
    
if __name__=='__main__':
    app=App()
    app.MainLoop()