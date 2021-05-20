from PIL import Image
from array import *
from colormap import rgb2hex
import glob
import xlwt
from xlwt import Workbook

class BGcolorChk:
	def __init__(self):
		self.size = 0
		self.rgbList = []
		self.colorList = []
		self.im =0
		self.pix=0
		self.size=0
		self.w=0
		self.h=0
		self.l1 = [ [40,10], [80,10], [120,10], [160,10], [10,20], [10,30], [10,40], [10,60], [self.w-10,20], [self.w-10,30], [self.w-10,40], [self.w-10,60] ]
		self.select = []
		self.image_list = []
		self.image_list = [f for f in glob.glob("*.jpg")]
		#print(self.image_list)
		self.bgColor = []

	def resize(self):
		for x in range(len(self.image_list)):
			#newsize = (132,170)
			newsize = (212,280)
			p_img = "./"+self.image_list[x]
			p_img = Image.open(p_img)
			p_img = p_img.resize(newsize)
			# Save the edited image
			p_img.save("./" + self.image_list[x], quality=100, subsampling=0)

	def readImg(self,loc):
		self.select = []
		self.im=0
		self.pix=0
		self.size=0
		self.w=0
		self.h=0
		self.rgbList=[]
		self.colorList = []
		self.im = Image.open(loc)
		self.pix = self.im.load()
		self.size = self.im.size
		self.w = self.size[0]
		self.h = self.size[1]

	def loopImg(self):
		for x in range(len(self.image_list)):
			self.readImg(self.image_list[x])
			print("Going to Read Image :: ", self.image_list[x])
			self.bgDetect()

	def get_color(self, color):
		r, g, b = color
		#if g < r / 2 and b < r / 2:
		if (r >= 150 and r <= 255 and g >= 0 and g <= 50 and b >= 0 and b <= 50) or (r > 100 and g < 50 and b < 60):
			#print("Pic BG Color IS :: RED")
			return "red"
		if r > 180 and b > 180 and g > 180:
			#print("Pic BG Color IS :: White")
			return "white"
		if (r <= 90 and g >= 70 and b >= 139) or (r > 90 and g >= 140 and b >= 160) or (r < 50 and g < 83 and b > 50):
			#print("Pic BG Color IS :: Blue")
			return "blue"
		else:
			return "ERROR"  		

	def bgDetect(self):
		for x in range(12):
			self.rgbList.append(self.pix[self.l1[x][0],self.l1[x][1]])
		for y in range(12):
			self.colorList.append(self.get_color(self.rgbList[y]))
		
		self.select.append(self.colorList.count('blue'))
		self.select.append(self.colorList.count('red'))
		self.select.append(self.colorList.count('white'))
		self.select.append(self.colorList.count('ERROR'))
		max_value = max(self.select)
		if self.select.index(max_value) == 0 and max_value > 7:
	 		self.bgColor.append("blue")
		elif self.select.index(max_value) == 1 and max_value > 7:
			self.bgColor.append("red")
		elif self.select.index(max_value) == 2 and max_value > 7:
			self.bgColor.append("white")
		elif self.select.index(max_value) == 3 and max_value > 7:
			self.bgColor.append("ERROR")
		else:
			self.bgColor.append("ERROR-last")
		#print(self.bgColor)

	def writeXls(self):
		wb = Workbook()
		# add_sheet is used to create sheet.
		sheet1 = wb.add_sheet('Sheet 1')
		for x in range(len(self.image_list)):
			sheet1.write(x, 0, self.image_list[x])
			sheet1.write(x, 1, self.bgColor[x])
		wb.save('xlwt example.xls')
    	
		

def main(obj):
	obj.resize()
	obj.loopImg()
	obj.writeXls()
	print("DONE ...!")

if __name__ == '__main__':
	obj = BGcolorChk()
	main(obj)
