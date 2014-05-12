
import argparse
from cPickle import load
from train_bow import extractFeatures, computeHistograms, writeHistogramsToFile
from numpy import zeros, resize, sqrt, histogram, hstack, vstack, savetxt, zeros_like, loadtxt
import numpy as np
import cPickle as pickle

#constants
PRE_ALLOCATION_BUFFER = 1000
K_THRESH = 1 # early stopping threshold for kmeans originally at 1e-5, increased for speedup
EXTENSIONS = [".jpg", ".bmp", ".png", ".pgm", ".tif", ".tiff"]
DATASETPATH = 'images'
CODEBOOK_FILE = 'codebook.file'
MODEL_FILE_LR = 'LogisticRegression.model'
MODEL_FILE_SVM = 'SVM.model'
MODEL_FILE_KNN = 'KNN.model'
HISTOGRAMS_FILE = 'sample_histogram.dat'

def parse_arguments():
    parser = argparse.ArgumentParser(description='classify images with a visual bag of words model')
    parser.add_argument('-c', help='path to the codebook file', required=False, default=CODEBOOK_FILE)
    parser.add_argument('-m', help='path to the model file', required=False, default=MODEL_FILE_SVM)
    parser.add_argument('input_images', help='images to classify', nargs='+')
    args = parser.parse_args()
    return args


print "---------------------"
print "## extract Sift features"
all_files = []
all_files_labels = {}
all_features = {}

args = parse_arguments()
model_file = args.m
codebook_file = args.c
fnames = args.input_images
all_features = extractFeatures(fnames)
for i in fnames:
    all_files_labels[i] = 0 # label is unknown

print "---------------------"
print "## loading codebook from " + codebook_file
with open(codebook_file, 'rb') as f:
    codebook = load(f)

print "---------------------"
print "## computing visual word histograms"
all_word_histgrams = {}
for imagefname in all_features:
    word_histgram = computeHistograms(codebook, all_features[imagefname])
    all_word_histgrams[imagefname] = word_histgram

print "---------------------"
print "## pass histogram to prediction models"
nclusters = codebook.shape[0]
writeHistogramsToFile(nclusters,
                      all_files_labels,
                      fnames,
                      all_word_histgrams,
                      HISTOGRAMS_FILE)

print 'loading data file'
data_file = loadtxt(HISTOGRAMS_FILE)
#print data_file, type(data_file)
#classID = data_file[:,0].astype(int)
classID = data_file[0].astype(int)
#Features = np.delete(data_file, 0,1)
features = data_file[1:]
features = features.reshape(1, (features.shape[0]))
print classID, features
#sys.exit()

print "---------------------"
print "## test data with svm"

model_svm = pickle.load( open( MODEL_FILE_SVM, "rb" ) )
classID_svm = model_svm.predict(features)
print "SVM predicted classID:", classID_svm
print "SVM decision: ", model_svm.decision_function(features)

from sklearn.neighbors import KNeighborsClassifier
KNN_clf = KNeighborsClassifier(n_neighbors=2)
KNN_clf = pickle.load( open( MODEL_FILE_KNN, "rb" ) )
KNN_classID = KNN_clf.predict(features)
print "KNN predicted classID:", KNN_classID 
print "KNN predicted prob:", KNN_clf.predict_proba(features)

#from sklearn.svm import LinearSVC
#LinearSVC_clf = LinearSVC()
#LinearSVC_clf = pickle.load( open(MODEL_FILE, "rb" ) )
#LinearSVC_class = LinearSVC_clf.predict(features)
#print "LinearSVC_clf predicted classID:", LinearSVC_class
#print "LinearSVC predicted prob:", LinearSVC_clf.predict_proba(features)

from sklearn.linear_model import LogisticRegression
clf2 = pickle.load(open(MODEL_FILE_LR, "rb" ) )
print "LR2 predicted classID:",clf2.predict(features)
print "LR2 predicted prob:", clf2.predict_proba(features)

h = raw_input('')
