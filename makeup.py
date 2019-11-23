import numpy as np 
import cv2
import dlib
import imutils
from imutils import face_utils
import tkinter
import math

FACIAL_LANDMARKS_IDXS = {"mouth": (48, 68),
		"right_eyebrow" : (17, 22),
		"left_eyebrow" : (22, 27),
		"right_eye" : (36, 42),
		"left_eye" : (42, 48),
		"nose" : (27, 35),
		"jaw" : (0, 17)}

makeupTypes = {
	"lipstick" : ["mouth"],
	"brow" : ["right_eyebrow", "left_eyebrow"],
	"eyeliner" : ["right_eye", "left_eye"],
	"eyeshadow" : ["right_eye", "left_eye"],
	"contour": ["jaw"],
	"highlight" : ["nose", "right_cheek", "left_cheek"], 
	"blush" : ["left_cheek", "right_cheek"]
}


predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

#########################################################################
# Editing the Photo
#########################################################################

featureDict = {"lips" : ["mouth"],
"brows" : ["right_eyebrow", "left_eyebrow"],
"eyeliner" : ["right_eye", "left_eye"],
"shadow" : ["right_eye", "left_eye"],
"liner" : ["right_eye", "left_eye"],
"contour": ["jaw"],
"highlight" : ["left_cheek", "right_cheek"], 
"blush" : ["left_cheek", "right_cheek"]}

class Lips(object):
	def __init__(self, img, currentFeature, alpha, color):
		self.img = img
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		self.rects = detector(self.gray, 1)
		self.currentFeature = currentFeature
		self.editables = featureDict[self.currentFeature]
		self.shape = predictor(self.gray, self.rects[0])
		self.shape = face_utils.shape_to_np(self.shape)
		self.alpha = alpha
		self.color = color
		self.alphaMax = 0.95
		self.alphaMin = 0.05

	def editPhoto(self):
		if self.color == None:
			return self.img
		for landmark in self.editables:
			if landmark == "mouth":
				(i, j) = face_utils.FACIAL_LANDMARKS_IDXS[landmark]
				clone = self.img.copy()
				color = self.color
				pts = self.shape[i:j]
				pts = pts.reshape((-1, 1, 2))
				cv2.fillPoly(clone,[pts], self.color)
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)
		return self.img

class Brows(object):
	def __init__(self, img, currentFeature, alpha, color):
		self.img = img
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		self.rects = detector(self.gray, 1)
		self.currentFeature = currentFeature
		self.editables = featureDict[self.currentFeature]
		self.shape = predictor(self.gray, self.rects[0])
		self.shape = face_utils.shape_to_np(self.shape)
		self.alpha = alpha
		self.color = color
		self.alphaMax = 0.5
		self.alphaMin = 0.05

	def editPhoto(self):
		if self.color == None:
			return self.img
		for landmark in self.editables:
			if landmark == "right_eyebrow":
				(i, j) = face_utils.FACIAL_LANDMARKS_IDXS[landmark]
				clone = self.img.copy()
				pts = self.shape[i:j]
				refPts = self.shape[37:40]
				browBase = self.shape[18:21]
				newpts = []
				for i in range(len(refPts)-1, -1,-1):
					delta = 1/3
					newpt = [browBase[i][0], browBase[i][1] - int((browBase[i][1] - refPts[i][1])*delta)]
					newpts += [newpt]
					delta *= 1/3
				convertedList = []
				for pt in pts:
					converted = [pt[0], pt[1]]
					convertedList += [converted]
				convertedList += newpts
				convertedList = np.array(convertedList)
				# pts = pts.reshape((-1, 1, 2))
				cv2.fillPoly(clone,[convertedList], self.color, 1)
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)
			
			if landmark == "left_eyebrow":
				(i, j) = face_utils.FACIAL_LANDMARKS_IDXS[landmark]
				clone = self.img.copy()
				pts = self.shape[i:j]
				refPts = self.shape[47:43:-1]
				browBase = self.shape[23:27]
				newpts = []
				for i in range(len(refPts)-1, -1,-1):
					delta = 1/3
					newpt = [browBase[i][0], browBase[i][1] - int((browBase[i][1] - refPts[i][1])*delta)]
					newpts += [newpt]
					delta *= 1/3
				convertedList = []
				for pt in pts:
					converted = [pt[0], pt[1]]
					convertedList += [converted]
				convertedList += newpts
				convertedList = np.array(convertedList)
				# pts = pts.reshape((-1, 1, 2))
				cv2.fillPoly(clone,[convertedList], self.color, 1)
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)

		return self.img

class Shadow(object):
	def __init__(self, img, currentFeature, alpha, color):
		self.img = img
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		self.rects = detector(self.gray, 1)
		self.currentFeature = currentFeature
		self.editables = featureDict[self.currentFeature]
		self.shape = predictor(self.gray, self.rects[0])
		self.shape = face_utils.shape_to_np(self.shape)
		self.alpha = alpha
		self.color = color
		self.alphaMax = 0.7
		self.alphaMin = 0.1

	def editPhoto(self):
		if self.color == None:
			return self.img
		for landmark in self.editables:
			if landmark == "right_eye":
				clone = self.img.copy()
				eyeBase = self.shape[36:40]
				# print("eyeBase ", eyeBase)
				browRef = self.shape[18:22]
				# print("browRef ", browRef)
				finalPts = []
				for i in range(len(eyeBase)):
					deltaY = int((eyeBase[i][1] - browRef[i][1])*0.25) + 11
					# print(deltaY)
					newY = eyeBase[i][1] - deltaY
					# print(newY)
					newPoint = [eyeBase[i][0], newY]
					# print(newPoint)
					finalPts += [newPoint]
					# print(finalPts)
				finalPts = np.vstack([np.array(finalPts), eyeBase[::-1]])
				cv2.fillPoly(clone,[finalPts], self.color, 1)
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)
			if landmark == "left_eye":
				clone = self.img.copy()
				eyeBase = self.shape[42:46]
				# print("eyeBase ", eyeBase)
				browRef = self.shape[22:26]
				# print("browRef ", browRef)
				finalPts = []
				for i in range(len(eyeBase)):
					deltaY = int((eyeBase[i][1] - browRef[i][1])*0.25) + 11
					# print(deltaY)
					newY = eyeBase[i][1] - deltaY
					# print(newY)
					newPoint = [eyeBase[i][0], newY]
					# print(newPoint)
					finalPts += [newPoint]
					# print(finalPts)
				finalPts = np.vstack([np.array(finalPts), eyeBase[::-1]])
				cv2.fillPoly(clone,[finalPts], self.color, 1)
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)

		return self.img

class Liner(object):
	def __init__(self, img, currentFeature, alpha, color):
		self.img = img
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		self.rects = detector(self.gray, 1)
		self.currentFeature = currentFeature
		self.editables = featureDict[self.currentFeature]
		self.shape = predictor(self.gray, self.rects[0])
		self.shape = face_utils.shape_to_np(self.shape)
		self.alpha = alpha
		self.color = color
		self.alphaMax = 0.8
		self.alphaMin = 0.5

	def editPhoto(self):
		if self.color == None:
			return self.img
		for landmark in self.editables:
			if landmark == "right_eye":
				i, j = 36, 40
				clone = self.img.copy()
				pts = self.shape[i:j]
				modifiedPts = []
				for pt in pts:
					modifiedPts += [[pt[0], pt[1]-10]]
				modifiedPts = np.array(modifiedPts)
				print(modifiedPts)
				pts = modifiedPts
				for point in range(len(pts)):
					try:
						cv2.line(clone, tuple(pts[point]), tuple(pts[point + 1]), self.color, thickness = 5)
					except:
						continue
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)
			if landmark == "left_eye":
				i, j = 42, 46
				clone = self.img.copy()
				pts = self.shape[i:j]
				modifiedPts = []
				for pt in pts:
					modifiedPts += [[pt[0], pt[1]-10]]
				modifiedPts = np.array(modifiedPts)
				pts = modifiedPts
				for point in range(len(pts)):
					try:
						cv2.line(clone, tuple(pts[point]), tuple(pts[point + 1]), self.color, thickness = 5)
					except:
						continue
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)

		return self.img

class Highlight(object):
	def __init__(self, img, currentFeature, alpha, color):
		self.img = img
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		self.rects = detector(self.gray, 1)
		self.currentFeature = currentFeature
		self.editables = featureDict[self.currentFeature]
		self.shape = predictor(self.gray, self.rects[0])
		self.shape = face_utils.shape_to_np(self.shape)
		self.alpha = alpha
		self.color = color
		self.alphaMax = 0.15
		self.alphaMin = 0.03

	def editPhoto(self):
		if self.color == None:
			return self.img
		for landmark in self.editables:
			if landmark == "right_cheek":
				clone = self.img.copy()
				startY = self.shape[30][1]
				startX = self.shape[38][0]
				start = [startX, startY]
				midptX = self.shape[19][0]
				midptY = self.shape[30][1]
				midpt = [midptX, midptY]
				finalX = (self.shape[1][0] + self.shape[18][0])//2
				finalY = (self.shape[15][1] + self.shape[14][1])//2
				final = [finalX, finalY]
				highlight = [start, midpt, final]
				pts = np.array(highlight)
				for point in range(len(pts)):
					try:
						cv2.line(clone, tuple(pts[point]), tuple(pts[point + 1]), self.color, thickness = 20)
					except:
						continue
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)
			if landmark == "left_cheek":
				clone = self.img.copy()
				startY = self.shape[30][1]
				startX = self.shape[45][0]
				start = [startX, startY]
				midptX = self.shape[26][0]
				midptY = self.shape[29][1]
				midpt = [midptX, midptY]
				finalX = (self.shape[15][0] + self.shape[26][0])//2
				finalY = (self.shape[15][1] + self.shape[16][1])//2
				final = [finalX, finalY]
				highlight = [start, midpt, final]
				pts = np.array(highlight)
				for point in range(len(pts)):
					try:
						cv2.line(clone, tuple(pts[point]), tuple(pts[point + 1]), self.color, thickness = 20)
					except:
						continue
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)

		return self.img

class Blush(object):
	def __init__(self, img, currentFeature, alpha, color):
		self.img = img
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		self.rects = detector(self.gray, 1)
		self.currentFeature = currentFeature
		self.editables = featureDict[self.currentFeature]
		self.shape = predictor(self.gray, self.rects[0])
		self.shape = face_utils.shape_to_np(self.shape)
		self.alpha = alpha
		self.color = color
		self.alphaMax = 0.2
		self.alphaMin = 0.03

	def editPhoto(self):
		if self.color == None:
			return self.img
		for landmark in self.editables:
			if landmark == "left_cheek":
				clone = self.img.copy()
				centerX = self.shape[26][0]
				centerY = self.shape[29][1]
				majorxi = self.shape[43][0]
				majorxii = self.shape[46][0]
				majoryi = self.shape[43][1]
				majoryii = self.shape[46][1]
				majorsq1 = (majorxi-majorxii)*(majorxi-majorxii)
				majorsq2 = (majoryi-majoryii)*(majoryi-majoryii)
				minorxi = self.shape[46][0]
				minorxii = self.shape[47][0]
				minoryi = self.shape[46][1]
				minoryii = self.shape[47][1]
				minorsq1 = (minorxi-minorxii)*(minorxi-minorxii)
				minorsq2 = (minoryi-minoryii)*(minoryi-minoryii)
				majordist = int(math.sqrt(majorsq1 + majorsq2))
				minordist = int(math.sqrt(minorsq1 + minorsq2))
    			# taken from https://stackoverflow.com/questions/35176451/\
    			# python-code-to-calculate-angle-between-three-point-using-their-3d-coordinates
				a = self.shape[15]
				b = self.shape[36]
				c = self.shape[17]
				ba = a - b
				bc = c - b
				cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
				angle = np.degrees(np.arccos(cosine_angle)) + 180
				cv2.ellipse(clone, (centerX , centerY), (majordist, minordist), angle, 0, 180, self.color, -1)
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)
			if landmark == "right_cheek":
				clone = self.img.copy()
				centerX = self.shape[19][0]
				centerY = self.shape[30][1]
				majorxi = self.shape[43][0]
				majorxii = self.shape[46][0]
				majoryi = self.shape[43][1]
				majoryii = self.shape[46][1]
				majorsq1 = (majorxi-majorxii)*(majorxi-majorxii)
				majorsq2 = (majoryi-majoryii)*(majoryi-majoryii)
				minorxi = self.shape[46][0]
				minorxii = self.shape[47][0]
				minoryi = self.shape[46][1]
				minoryii = self.shape[47][1]
				minorsq1 = (minorxi-minorxii)*(minorxi-minorxii)
				minorsq2 = (minoryi-minoryii)*(minoryi-minoryii)
				majordist = int(math.sqrt(majorsq1 + majorsq2))
				minordist = int(math.sqrt(minorsq1 + minorsq2))
    			# taken from https://stackoverflow.com/questions/35176451/\
    			# python-code-to-calculate-angle-between-three-point-using-their-3d-coordinates
				a = self.shape[15]
				b = self.shape[36]
				c = self.shape[17]
				ba = a - b
				bc = c - b
				cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
				angle = np.degrees(np.arccos(cosine_angle)) + 225
				cv2.ellipse(clone, (centerX , centerY), (majordist, minordist), angle, 0, 180, self.color, -1)
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)
		return self.img


class Contour(object):
	def __init__(self, img, currentFeature, alpha, color):
		self.img = img
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		self.rects = detector(self.gray, 1)
		self.currentFeature = currentFeature
		self.editables = featureDict[self.currentFeature]
		self.shape = predictor(self.gray, self.rects[0])
		self.shape = face_utils.shape_to_np(self.shape)
		self.alpha = alpha
		self.color = color
		self.alphaMax = 0.5
		self.alphaMin = 0.03

	def editPhoto(self):
		if self.color == None:
			return self.img
		for landmark in self.editables:
			if landmark == "jaw":
				(i, j) = face_utils.FACIAL_LANDMARKS_IDXS[landmark]
				i += 1
				j -= 1
				clone = self.img.copy()
				pts = self.shape[i:j]
				for point in range(len(pts)):
					try:
						cv2.line(clone, tuple(pts[point]), tuple(pts[point + 1]), self.color, thickness = 7)
					except:
						continue
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)
			if landmark == "left_cheek":
				clone = self.img.copy()
				startY = self.shape[34][1]
				startX = self.shape[45][0]
				start = [startX, startY]
				midptX = self.shape[26][0]
				midptY = self.shape[31][1]
				midpt = [midptX, midptY]
				finalX = (self.shape[15][0] + self.shape[26][0])//2
				finalY = (self.shape[15][1] + self.shape[16][1])//2
				final = [finalX, finalY]
				highlight = [start, midpt, final]
				pts = np.array(highlight)
				for point in range(len(pts)):
					try:
						cv2.line(clone, tuple(pts[point]), tuple(pts[point + 1]), self.color, thickness = 20)
					except:
						continue
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)
			if landmark == "right_cheek":
				clone = self.img.copy()
				startY = self.shape[31][1]
				startX = self.shape[38][0]
				start = [startX, startY]
				midptX = self.shape[19][0]
				midptY = self.shape[31][1]
				midpt = [midptX, midptY]
				finalX = (self.shape[1][0] + self.shape[18][0])//2
				finalY = (self.shape[15][1] + self.shape[14][1])//2
				final = [finalX, finalY]
				highlight = [start, midpt, final]
				pts = np.array(highlight)
				for point in range(len(pts)):
					try:
						cv2.line(clone, tuple(pts[point]), tuple(pts[point + 1]), self.color, thickness = 20)
					except:
						continue
				cv2.addWeighted(clone, self.alpha, self.img, 1-self.alpha, 0, self.img)
		
		return self.img

# img = editPhoto(img, gray, rects, [], "left_cheek")
# img = imutils.resize(img, width = 500, inter = cv2.INTER_CUBIC)
# cv2.imshow("img", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()