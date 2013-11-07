#!/usr/bin/env python

import sys
sys.path.append( "../lib/" )
import easygui as eg
import cv2
import skimage.feature



def find_features(img):
	#img = preprocess_img(img)
	#features = houghlines(img, 20)
	#features = features360_avg(img)
	#features = features360(img, preprocess=True, coin_center=None, step360=1, averaging=False, classID=0)
	#features = binary_compare(img)
	#features = goodfeatures(img)
	#print img, type(img)

	#gray scale the image if neccessary
	#if img.shape[2] == 3:
	#	img = img.mean(2)

	#img = mahotas.imread(imname, as_grey=True)
	#features = mahotas.features.haralick(img).mean(0)
	#f2 = features
	#print 'haralick features:', features, len(features), type(features[0])
	
	#features = mahotas.features.lbp(img, 1, 8)
	#f2 = np.concatenate((f2,features))
	#print 'LBP features:', features, len(features), type(features[0])

	#features = mahotas.features.tas(img)
	#f2 = np.concatenate((f2,features))
	#print 'TAS features:', features, len(features), type(features[0])


	#features = mahotas.features.zernike_moments(np.mean(img,2), 2, degree=8)
	#print 'ZERNIKE features:', features, len(features), type(features[0])
	#f2 = np.concatenate((f2,features))

	#hu_moments = []
	#hu_moments =  np.array(cv.GetHuMoments(cv.Moments(cv.fromarray(img))))
	#print "HU_MOMENTS: ", hu_moments
	#features = flatten(hu_moments)
	#f2 = np.concatenate((f2,features))
	#features = f2


	#DAISY
	#gray scale the image if neccessary
	print type(img)
	if img.shape[2] != None:
		img = img.mean(2)
	img_step = int(img.shape[1]/4)
	img_radius = int(img.shape[1]/10)
	descs, descs_img =  skimage.feature.daisy(img, step=img_step, radius=img_radius, rings=2, histograms=8, orientations=8, normalization='l2', visualize=True)
	features = descs.ravel()
	#print type(descs_img), type(array2cv(descs_img))
	cv2.imwrite("images/daisy_img.png", descs_img) #cv2array(array2cv(descs_img)))

	#raw_input ("press enter")
	#plt.axis('off')
	#plt.imshow(descs_img)
	#descs_num = descs.shape[0] * descs.shape[1]
	#plt.title('%i DAISY descriptors extracted:' % descs_num)
	#plt.show()
	#print len(features.ravel())


	#print len(features[0][0])
	print "All Features: ", features, len(features)
	'''
	#features_surf = surf.surf(np.mean(img,2))
	#print "SURF:", features_surf, " len:", len(features_surf)

	try:
		import milk

		# spoints includes both the detection information (such as the position
		# and the scale) as well as the descriptor (i.e., what the area around
		# the point looks like). We only want to use the descriptor for
		# clustering. The descriptor starts at position 5:
		descrs = features_surf[:,5:]

		# We use 5 colours just because if it was much larger, then the colours
		# would look too similar in the output.
		k = 5
		surf_pts_to_ID = 50
		values, _  = milk.kmeans(descrs, k)
		colors = np.array([(255-52*i,25+52*i,37**i % 101) for i in xrange(k)])
	except:
		values = np.zeros(100)
		colors = [(255,0,0)]
	surf_img = surf.show_surf(np.mean(img,2), features_surf[:surf_pts_to_ID], values, colors)
	#imshow(surf_img)
	#show()
	'''
	#houghlines opencv

	#try:
	#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#gray = CVtoGray(numpy2CV(img))
	#print gray

	#except:
	#	print "no houghlines available"
	#img1 = mahotas.imread('temp.png')
	#T_otsu = mahotas.thresholding.otsu(img1)
	#seeds,_ = mahotas.label(img > T_otsu)
	#labeled = mahotas.cwatershed(img1.max() - img1, seeds)
	#imshow(labeled)
	#show()
	'''
	for x in hu_moments[0]:
		if x < 0: x = (x * -1)
		print math.log10(x)
	distmin = 0
	degree = 0
	for x in range(359):

		img2 = cv.CloneImage(array2cv(grey))
		#img2 = rotate_image(img2, x)
		#print type(img2)
		img2 = CVtoPIL(img2)
		img2 = img2.rotate(x, expand=1)
		#print type(img2)
		img2 = PILtoCV(img2,1)
		cv.ShowImage("45", img2)
		cv.WaitKey()
		#print type(img2)
		hu_moments2 = []
		hu_moments2 =  np.array(cv.GetHuMoments(cv.Moments(cv.GetMat(img2))))
		hu_moments2 = hu_moments2.reshape(1, (hu_moments2.shape[0]))
		distance_btw_images = scipy.spatial.distance.cdist(hu_moments, hu_moments2,'euclidean')
		if (distance_btw_images < distmin): degree = x
		print x, ": ", log10(distance_btw_images )
		#print "HUMOMENTS2: ", hu_moments2
		#for x in hu_moments2:
		#	print math.log10(x)
	print "degree = ", degree
	'''
	return features



if __name__=="__main__":
	video = None
	webcam1 = None
	img1 = None
	try:
		img1 = cv2.imread('temp.png')
	except:
		pass
	if len(sys.argv) > 1:
		try:
			video = cv2.VideoCapture(sys.argv[1])
			print video, sys.argv[1]
		except:
			print "******* Could not open image/video file *******"
			print "Unexpected error:", sys.exc_info()[0]
			#raise		
			sys.exit(-1)
	#eg.rootWindowPosition = "+100+100"
	reply = ""
	while True:
		ready_to_display = False
		#eg.rootWindowPosition = eg.rootWindowPosition
		#print 'reply=', reply		
		#if reply == "": reply = "Next Frame"
		'''
		if reply == "Sample":
			img1 = cv2.imread('temp.png')
			path = "../coin_images/jheads/"
			filename = "jhead"+ str(time.time()) + ".jpg"
			image_to_save = array2image(img1)
			image_to_save.save(path+filename)	

		if reply == "JTAIL":
			img1 = cv2.imread('temp.png')
			path = "../coin_images/jtails/"
			filename = "jtail" + str(time.time()) + ".jpg"
			image_to_save = array2image(img1)
			image_to_save.save(path+filename)	

		if reply == "OHEAD":
			img1 = cv2.imread('temp.png')
			path = "../coin_images/oheads/"
			filename = 'ohead' + str(time.time()) + ".jpg"
			image_to_save = array2image(img1)
			image_to_save.save(path+filename)


		if reply == "OTAIL":
			img1 = cv2.imread('temp.png')
			path = "../coin_images/otails/"
			filename = 'otail' + str(time.time()) + ".jpg"
			image_to_save = array2image(img1)
			image_to_save.save(path+filename)

		if reply == "Test Img":	
			img1 = cv2.imread('temp.png')
			path = "../coin_images/unclassified/"
			filename = str(time.time()) + ".jpg"
			image_to_save = array2image(img1)
			image_to_save.save(path+filename)
		'''

		if reply == "Quit":
			print "Quitting...."
			sys.exit(-1)

		#if reply == "TEST":
			#sift()
		#	test()
			#img_to_classify = cv2.imread('temp.png')
			#compare_rms(img_to_classify)

		'''
		if reply == "Predict":
			print "AI predicting"
			img1 = cv2.imread('temp.png')
			#img1 = preprocess_img(img1)
			#cv2.imwrite('postprocessed_img.png', img1)
			#predicted_classID = predict_class(img1)
			predicted_classID = predict_class_360(img1, step360=40)
			if predicted_classID == 1: answer = "Jefferson HEADS"
			if predicted_classID == 2: answer = "Monticello TAILS"
			if predicted_classID == 3: answer = "Other HEADS"
			if predicted_classID == 4: answer = "Other TAILS"
			print "------------------------------------------"
			print "FINAL: predicted_classID:", answer
		'''

		'''
		if reply == "Subsection":
			img1 = Image.open('temp.png')
			print img1
			xx = subsection_image(img1, 16,True)
			print xx
			#while (xx != 9):
			#	time.sleep(1)
		'''

		if reply == "Features":
			#img = mahotas.imread('temp.png', as_grey=True)
			img1 = cv2.imread('images/temp.jpg')
			#img1 = preprocess_img(img1)
			find_features(img1)
			#features360(img1, preprocess=True, coin_center=None, step360=360, averaging=False, classID=0)
			ready_to_display = True

		'''
		#if reply == "Retrain AI":
		#	print "Retraining AI"
		#	train_ai()

	
		if reply == "Next Coin":
			print "clearing coin shoot..."
			coinid_servo.arm_up(100)
			time.sleep(.2)
			coinid_servo.arm_down()
			#time.sleep(.2)
			print "Acquiring new image.."
			if video != None: 
				img1 = np.array(grab_frame_from_video(video)[VIDEO_CAM])
				print "test"
			else:
				get_new_coin(coinid_servo, dc_motor)
				time.sleep(.5)
				img1 = cv2array(snap_shot(VIDEO_CAM))
			#img1 = preprocess_img(img1)
			cv2.imwrite('temp.png', img1)
			#img1 = array2image(img1)
			#print type(img1)
			#img1.save()
		

		if reply == "Process Imgs":
			print "Processing all training images....."
			process_all_images()
			time.sleep(1)

		if reply == "Del AI File":
			data_filename = 'sample_feature_data.csv'
			f_handle = open(data_filename, 'w')
			f_handle.write('')
			f_handle.close()
			data_filename = 'sample_ai_model.mdl'
			f_handle = open(data_filename, 'w')
			f_handle.write('')
			f_handle.close()
		'''

		try:
			#reply =	eg.buttonbox(msg='Coin Trainer', title='Coin Trainer', choices=('TEST', 'JHEAD', 'JTAIL', 'OHEAD', 'OTAIL', 'Test Img', 'Next Coin', 'Predict', 'Features','Process Imgs', 'Retrain AI' , 'Del AI File', 'Quit'), image='temp.png', root=None)			
			reply =	eg.buttonbox(msg='Coin Trainer', title='Coin Trainer', choices=('Features', 'Quit'), image='images/temp.jpg', root=None)
		except:
			pass



