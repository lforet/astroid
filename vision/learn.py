'''
The script learn.py will generate a visual vocabulary and train a classifier using a user provided set of already classified images. After the learning phase classify.py will use the generated vocabulary and the trained classifier to predict the class for any image given to the script by the user.

The learning consists of:

    Extracting local features of all the dataset images
    Generating a codebook of visual words with clustering of the features
    Aggregating the histograms of the visual words for each of the traning images
    Feeding the histograms to the classifier to train a model

The classification consists of:

    Extracting local features of the to be classified image
    Aggregating the histograms of the visual words for the image using the prior generated codebook
    Feeding the histogram to the classifier to predict a class for the image
'''


from os.path import exists, isdir, basename, join, splitext
import cv2
from glob import glob
from numpy import zeros, resize, sqrt, histogram, hstack, vstack, savetxt, zeros_like, loadtxt
import numpy as np
import scipy.cluster.vq as vq
from scipy.cluster.vq import whiten
import libsvm
from cPickle import dump, HIGHEST_PROTOCOL
import argparse
import csv
import cPickle as pickle
from skimage.feature import daisy

EXTENSIONS = [".jpg", ".bmp", ".png", ".pgm", ".tif", ".tiff"]
DATASETPATH = 'images'
PRE_ALLOCATION_BUFFER = 1000 # for sift
HISTOGRAMS_FILE = 'trainingdata.csv'
K_THRESH = 1 # early stopping threshold for kmeans originally at 1e-5, increased for speedup
CODEBOOK_FILE = 'codebook.file'
MODEL_FILE = 'trainingdata.svm.model'
MODEL_FILE_LR = 'LogisticRegression.model'
MODEL_FILE_SVM = 'SVM.model'
MODEL_FILE_KNN = 'KNN.model'


def parse_arguments():
    parser = argparse.ArgumentParser(description='train a visual bag of words model')
    parser.add_argument('-d', help='path to the dataset', required=False, default=DATASETPATH)
    args = parser.parse_args()
    return args


def get_categories(datasetpath):
    print datasetpath
    cat_paths = [files
                 for files in glob(datasetpath + "/*")
                  if isdir(files)]
    cat_paths.sort()
    cats = [basename(cat_path) for cat_path in cat_paths]
    return cats


def get_imgfiles(path):
    all_files = []
    all_files.extend([join(path, basename(fname))
                    for fname in glob(path + "/*")
                    if splitext(fname)[-1].lower() in EXTENSIONS])
    return all_files


#using SURF instead of SIFT for speed
def extractSift(input_files):
    print "extracting Sift features"
    all_features_dict = {}
    for i, fname in enumerate(input_files):
        features_fname = fname + '.sift'
        if exists(features_fname) == False:
            print "calculating sift features for", fname
            #sift.process_image(fname, features_fname)
            img = cv2.imread(fname)
            gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            #sift = cv2.SIFT()
            surf = cv2.SURF(400)
        print "gathering sift features for", fname,
        #locs, descriptors = sift.read_features_from_file(features_fname)
        #kp, descriptors = sift.detectAndCompute(gray, None)
        #kp, descriptors = surf.detectAndCompute(gray, None)

        surfDetector = cv2.FeatureDetector_create("SURF")
        surfDescriptorExtractor = cv2.DescriptorExtractor_create("SURF")
	keypoints = surfDetector.detect(im)
	(keypoints, descriptors) = surfDescriptorExtractor.compute(gray, keypoints)
        
	#print descriptors.shape
        all_features_dict[fname] = descriptors
    return all_features_dict


def dict2numpy(dict):
    nkeys = len(dict)
    array = zeros((nkeys * PRE_ALLOCATION_BUFFER, 128))
    pivot = 0
    for key in dict.keys():
        value = dict[key]
        nelements = value.shape[0]
        while pivot + nelements > array.shape[0]:
            padding = zeros_like(array)
            array = vstack((array, padding))
        array[pivot:pivot + nelements] = value
        pivot += nelements
    array = resize(array, (pivot, 128))
    return array

def save_data(features, classID):
	data_filename = HISTOGRAMS_FILE
	print 'writing image features to file: ', data_filename
	#write class data to file
	f_handle = open(data_filename, 'a')
	f_handle.write(str(classID))
	f_handle.write(', ')
	f_handle.close()

	f_handle = open(data_filename, 'a')
	for i in range(len(features)):
		f_handle.write(str(features[i]))
		f_handle.write(" ")
	f_handle.write('\n')
	f_handle.close()

def load_data(filename):
	data = []
	classID = []
	features = []
	features_temp_array = []
	print 'reading features and classID: ', filename
	f_handle = open(filename, 'r')
	reader = csv.reader(f_handle)
	#read data from file into arrays
	for row in reader:
		data.append(row)

	for row in range(0, len(data)):
		#print features[row][1]
		classID.append(int(data[row][0]))
		features_temp_array.append(data[row][1].split(" "))

	#removes ending element which is a space
	for x in range(len(features_temp_array)):
		features_temp_array[x].pop()
		features_temp_array[x].pop(0)

	#convert all strings in array to numbers
	temp_array = []
	for x in range(len(features_temp_array)):
		temp_array = [ float(s) for s in features_temp_array[x] ]
		features.append(temp_array)

	#make numpy arrays
	features = np.asarray(features)
	print classID, features 
	return classID, features


def computeHistograms(codebook, descriptors):
    code, dist = vq.vq(descriptors, codebook)
    histogram_of_words, bin_edges = histogram(code,
                                              bins=range(codebook.shape[0] + 1),
                                              normed=True)
    return histogram_of_words


def writeHistogramsToFile(nwords, labels, fnames, all_word_histgrams, features_fname):
    data_rows = zeros(nwords + 1) # +1 for the category label
    for fname in fnames:
        histogram = all_word_histgrams[fname]
        if (histogram.shape[0] != nwords): # scipy deletes empty clusters
            nwords = histogram.shape[0]
            data_rows = zeros(nwords + 1)
            print 'nclusters have been reduced to ' + str(nwords)
        data_row = hstack((labels[fname], histogram))
        data_rows = vstack((data_rows, data_row))
    data_rows = data_rows[1:]
    fmt = '%i '
    for i in range(nwords):
        fmt = fmt + '%f '
    savetxt(features_fname, data_rows, fmt)


if __name__ == '__main__':
    print "---------------------"
    print "## loading the images and extracting the sift features"
    args = parse_arguments()
    datasetpath = args.d
    cats = get_categories(datasetpath)
    ncats = len(cats)
    print "searching for folders at " + datasetpath
    if ncats < 1:
        raise ValueError('Only ' + str(ncats) + ' categories found. Wrong path?')
    print "found following folders / categories:"
    print cats
    print "---------------------"
    all_files = []
    all_files_labels = {}
    all_features = {}
    cat_label = {}
    for cat, label in zip(cats, range(ncats)):
        cat_path = join(datasetpath, cat)
        cat_files = get_imgfiles(cat_path)
        cat_features = extractSift(cat_files)
        all_files = all_files + cat_files
        all_features.update(cat_features)
        cat_label[cat] = label
        for i in cat_files:
            all_files_labels[i] = label

    print "---------------------"
    print "## computing the visual words via k-means"
    all_features_array = dict2numpy(all_features)
    nfeatures = all_features_array.shape[0]
    nclusters = int(sqrt(nfeatures))
    #all_features_array = whiten(all_features_array)
    codebook, distortion = vq.kmeans(all_features_array,
                                             nclusters,
                                             thresh=K_THRESH)

    with open(CODEBOOK_FILE, 'wb') as f:
        dump(codebook, f, protocol=HIGHEST_PROTOCOL)

    print "---------------------"
    print "## compute the visual words histograms for each image"
    all_word_histgrams = {}
    for imagefname in all_features:
        word_histgram = computeHistograms(codebook, all_features[imagefname])
        all_word_histgrams[imagefname] = word_histgram

    print "---------------------"
    print "## write the histograms to file to pass it to the svm"
    #for i in all_word_histgrams:
    #	print all_word_histgrams[i]

    writeHistogramsToFile(nclusters,
                          all_files_labels,
                          all_files,
                          all_word_histgrams,
                          HISTOGRAMS_FILE)

    print 'loading data file'
    data_file = loadtxt(HISTOGRAMS_FILE)
    classID = data_file[:,0].astype(int)
    Features = np.delete(data_file, 0,1)
    print classID, Features
    print "---------------------"
    print "## train svm"
    #c, g, rate, model_file = libsvm.grid(datasetpath + HISTOGRAMS_FILE,
                                        #png_filename='grid_res_img_file.png')
    from sklearn import svm
    model = svm.SVC(gamma=0.001, C=100.)
    model.fit(Features, classID)
    pickle.dump( model, open( MODEL_FILE, "wb" ) )

    from sklearn.linear_model import LogisticRegression
    clf2 = LogisticRegression().fit(Features, classID)
    pickle.dump( clf2 , open( MODEL_FILE_LR, "wb" ) )

    from sklearn import svm
    model = svm.SVC(gamma=0.001, C=100.)
    model.fit(Features, classID)
    pickle.dump( model, open( MODEL_FILE_SVM, "wb" ) )

    from sklearn.neighbors import KNeighborsClassifier
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(Features, classID)
    pickle.dump( neigh, open(MODEL_FILE_KNN, "wb" ) )


    print "--------------------"
    print "## outputting results"
    print "model file:", MODEL_FILE
    print "codebook file: " , CODEBOOK_FILE
    print "category ==> label"
    for cat in cat_label:
        print '{0:13} ==> {1:6d}'.format(cat, cat_label[cat])
