#-*- coding: UTF-8 -*-  
#!/usr/bin/env python
import wx
# import test
import os
from PIL import Image

class MyPanel(wx.Panel):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.FlexGridSizer(4, 3, 12, 12)

        urlLabel = wx.StaticText(self, label="原签名文件目录:")
        self.url = wx.TextCtrl(self)
        spacer1 = wx.StaticText(self, label="")

        pathLabel = wx.StaticText(self, label="输出文件目录:")
        self.path = wx.TextCtrl(self)
        spacer2 = wx.StaticText(self, label="")
        spacer3 = wx.StaticText(self, label="")
        self.spacer4 = wx.StaticText(self, label="")

        ChoosePathBtn1 = wx.Button(self, label="选择")
        ChoosePathBtn2 = wx.Button(self, label="选择")

        progressLabel = wx.StaticText(self, label="进度:")
        self.progress = wx.Gauge(self)
        self.BeginDownloadBtn = wx.Button(self, label=r"转为透明背景")

        sizer.AddMany(
            [(urlLabel, 2, wx.EXPAND), (self.url, 1, wx.EXPAND), (ChoosePathBtn1, 2, wx.EXPAND),
            (pathLabel, 2, wx.EXPAND), (self.path, 1, wx.EXPAND), (ChoosePathBtn2, 2, wx.EXPAND),
            (progressLabel, 2, wx.EXPAND), (self.progress, 1, wx.EXPAND), (spacer2, 2, wx.EXPAND),
            (spacer3, 2, wx.EXPAND), (self.BeginDownloadBtn, 1, wx.EXPAND), (self.spacer4, 2, wx.EXPAND)
            ])

        sizer.AddGrowableCol(1, 1)

        hbox.Add(sizer, proportion = 2, flag = wx.ALL|wx.EXPAND, border = 15)
        self.SetSizer(hbox)

        self.SetAutoLayout(1)
        self.Show(True)

        self.Bind(wx.EVT_BUTTON, self.ChoosePath1, ChoosePathBtn1)
        self.Bind(wx.EVT_BUTTON, self.ChoosePath2, ChoosePathBtn2)

        self.Bind(wx.EVT_BUTTON, self.BeginDownload, self.BeginDownloadBtn)        

        self.inputPathValue = ""
        self.outputPathValue = ""

    def ChoosePath1(self, event):
        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.inputPathValue = dialog.GetPath()
            self.url.SetValue(self.inputPathValue)

    def ChoosePath2(self, event):
        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.outputPathValue = dialog.GetPath()
            self.path.SetValue(self.outputPathValue)

    def BeginDownload(self, event):
        inputPathValue = self.url.GetValue()
        outputPathValue = self.path.GetValue()
        if inputPathValue == outputPathValue:
            dlg = wx.MessageDialog(None, "请选择与原签名文件目录不同的输出目录", "警告", wx.OK )
            if dlg.ShowModal() == wx.ID_YES:
                print "YES"
        else:
            self.BeginDownloadBtn.Disable()
            files = os.listdir(inputPathValue)
            fileCount = len(files)
            self.progress.SetRange(fileCount)
            for i in range(0, len(files)):
                file = os.path.join(inputPathValue, files[i])
                img = Image.open(file)
                img = img.convert('RGBA')
                r, g, b, alpha = img.split()

                w,h=img.size
                data=list(img.getdata())
                for x in range(w):
                    for y in range(h):
                        if(data[y*w+x][0]>150 or data[y*w+x][1]>150 or data[y*w+x][2]>150):
                            alpha = 100
                            img.putpixel((x,y),(255,255,255,0))
                bg = Image.new("RGBA", img.size, (255, 255, 255, 0))
                bg.paste(img,img)
                bg.save(os.path.join(outputPathValue, files[i]))
                count = self.progress.GetValue()
                count += 1
                self.progress.SetValue(count)
            if count == fileCount:
                self.BeginDownloadBtn.Enable()
                self.progress.SetValue(0)

app = wx.App(False)
frame = wx.Frame(None)
panel = MyPanel(frame)
frame.Show();
app.MainLoop()
