
	
import os
import wx
from pytesser import *

 
class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')
 
        self.panel = wx.Panel(self.frame)
 
        self.PhotoMaxSize = 240
 
        self.createWidgets()
        self.frame.Show()
	self.text = ""
 
    def createWidgets(self):
        instructions = 'Browse for an image before performing OCR'
        img = wx.EmptyImage(240,240)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))
        self.OCRCtrl = wx.StaticText(self.panel, size = (240, 240))
		
        instructLbl = wx.StaticText(self.panel, label=instructions)
	OCRlbl = wx.StaticText(self.panel, label="OCR Text")
        self.photoTxt = wx.TextCtrl(self.panel, size=(200,-1))
	
	#Browse button	
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
 	
	#OCR Button
     	OCRBtn = wx.Button(self.panel, label='OCR')
        OCRBtn.Bind(wx.EVT_BUTTON, self.onOCR)
 	

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)

        self.mainSizer.Add(self.imageCtrl, 0, flag=wx.TOP|wx.ALIGN_CENTER,border = 5)

	self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)

	self.mainSizer.Add(OCRlbl, 0, wx.ALL, 5)

	

        self.mainSizer.Add(self.OCRCtrl, 0, flag=wx.LEFT|wx.ALIGN_CENTER, border = 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)

        self.sizer.Add(browseBtn, 0, wx.ALL, 5)        
        self.sizer.Add(OCRBtn, 0, wx.ALL, 5) 

        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()
 
    def onBrowse(self, event):
        """ 
        Browse for file
        """
        wildcard = "Image Files (*.jpg,*.jpeg,*.png,*.tif)|*.tif;*.jpg;*.jpeg;*.png"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy() 
        self.onView()

    def onOCR(self, event):
        """ 
        perform OCR
        """
        filepath = self.photoTxt.GetValue()
        
       
        im = Image.open(filepath)
        text = image_to_string(im)
  
        print text
        wx.MessageBox("OCR successfully completed. Also the text has been copied to the clipboard", "Success")
        
        #OCR text is saved in OCRProgram.txt
        inf = open('OCRprogram.txt','w')
        inf.write(text)
        inf.close()
        
        #clipboard data attaching
        self.dataObj = wx.TextDataObject()
        self.dataObj.SetText(text)
        if wx.TheClipboard.Open(): 
			wx.TheClipboard.SetData(self.dataObj)
			wx.TheClipboard.Close() 
	else:
			wx.MessageBox("Unable to open the clipboard", "Error")
        
    def displayOCR(self,parent):              
        print text 

    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
 
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
 
if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()
