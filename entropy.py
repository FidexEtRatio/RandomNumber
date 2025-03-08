import cv2
import numpy

def get_entropy(img):
    # convert image to grayscale for reduced complexity
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    # histogram
    histogram = cv2.calcHist([img], [0], None, [256], [0, 256])

    # normalize histogram to get probabilities for Shannon's entropy
    histogram = histogram / histogram.sum()

    # calculate entropy

    entropy = -numpy.sum(histogram * numpy.log2(histogram + 1e-10)) # added a constant to avoid calculating log(0)

    return entropy