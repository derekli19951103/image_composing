## CSC320 Winter 2017 
## Assignment 1
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
import cv2 as cv
from itertools import product


# If you wish to import any additional modules
# or define other utility functions, 
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################


#########################################

#
# The Matting Class
#
# This class contains all methods required for implementing 
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
    #
    # The class constructor
    #
    # When called, it creates a private dictionary object that acts as a container
    # for all input and all output images of the triangulation matting and compositing 
    # algorithms. These images are initialized to None and populated/accessed by 
    # calling the the readImage(), writeImage(), useTriangulationResults() methods.
    # See function run() in run.py for examples of their usage.
    #
    def __init__(self):
        self._images = {
            'backA': None,
            'backB': None,
            'compA': None,
            'compB': None,
            'colOut': None,
            'alphaOut': None,
            'backIn': None,
            'colIn': None,
            'alphaIn': None,
            'compOut': None,
        }

    # Return a dictionary containing the input arguments of the
    # triangulation matting algorithm, along with a brief explanation
    # and a default filename (or None)
    # This dictionary is used to create the command-line arguments
    # required by the algorithm. See the parseArguments() function
    # run.py for examples of its usage
    def mattingInput(self):
        return {
            'backA': {'msg': 'Image filename for Background A Color', 'default': None},
            'backB': {'msg': 'Image filename for Background B Color', 'default': None},
            'compA': {'msg': 'Image filename for Composite A Color', 'default': None},
            'compB': {'msg': 'Image filename for Composite B Color', 'default': None},
        }

    # Same as above, but for the output arguments
    def mattingOutput(self):
        return {
            'colOut': {'msg': 'Image filename for Object Color', 'default': ['color.tif']},
            'alphaOut': {'msg': 'Image filename for Object Alpha', 'default': ['alpha.tif']}
        }

    def compositingInput(self):
        return {
            'colIn': {'msg': 'Image filename for Object Color', 'default': None},
            'alphaIn': {'msg': 'Image filename for Object Alpha', 'default': None},
            'backIn': {'msg': 'Image filename for Background Color', 'default': None},
        }

    def compositingOutput(self):
        return {
            'compOut': {'msg': 'Image filename for Composite Color', 'default': ['comp.tif']},
        }

    # Copy the output of the triangulation matting algorithm (i.e., the 
    # object Color and object Alpha images) to the images holding the input
    # to the compositing algorithm. This way we can do compositing right after
    # triangulation matting without having to save the object Color and object
    # Alpha images to disk. This routine is NOT used for partA of the assignment.
    def useTriangulationResults(self):
        if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
            self._images['colIn'] = self._images['colOut'].copy()
            self._images['alphaIn'] = self._images['alphaOut'].copy()

    # If you wish to create additional methods for the 
    # Matting class, include them here

    #########################################
    ## PLACE YOUR CODE BETWEEN THESE LINES ##
    #########################################

    #########################################

    # Use OpenCV to read an image from a file and copy its contents to the 
    # matting instance's private dictionary object. The key 
    # specifies the image variable and should be one of the
    # strings in lines 54-63. See run() in run.py for examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # leave the matting instance's dictionary entry unaffected and return
    # False, along with an error message
    def readImage(self, fileName, key):
        success = False
        msg = 'read error'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        img = cv.imread(fileName, cv.IMREAD_UNCHANGED)
        if img is not None:
            self._images[key] = img
            success = True
        #########################################
        return success, msg

    # Use OpenCV to write to a file an image that is contained in the 
    # instance's private dictionary. The key specifies the which image
    # should be written and should be one of the strings in lines 54-63. 
    # See run() in run.py for usage examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # return False, along with an error message
    def writeImage(self, fileName, key):
        success = False
        msg = 'write error'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        retval = cv.imwrite(fileName, self._images[key])
        if retval is not None:
            success = True
        #########################################
        return success, msg

    # Method implementing the triangulation matting algorithm. The
    # method takes its inputs/outputs from the method's private dictionary 
    # ojbect. 
    def triangulationMatting(self):
        """
success, errorMessage = triangulationMatting(self)
        
        Perform triangulation matting. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'matting error'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        backA = self._images["backA"]
        backB = self._images["backB"]
        compA = self._images["compA"]
        compB = self._images["compB"]
        h, w, d = backA.shape
        self._images["alphaOut"] = np.zeros((h, w, 4))
        self._images["colOut"] = np.zeros((h, w, 3))
        colOut = self._images["colOut"]
        alphaOut = self._images["alphaOut"]
        height = range(0,h)
        weight = range(0,w)
        for pos in product(height, weight):
            pixel_ba = backA[pos[0], pos[1]]
            pixel_bb = backB[pos[0], pos[1]]
            pixel_ca = compA[pos[0], pos[1]]
            pixel_cb = compB[pos[0], pos[1]]
            pixel_co = colOut[pos[0], pos[1]]
            pixel_ao = alphaOut[pos[0], pos[1]]
            delta_c = np.array([[int(pixel_ca[0]) - int(pixel_ba[0])],
                       [int(pixel_ca[1]) - int(pixel_ba[1])],
                       [int(pixel_ca[2]) - int(pixel_ba[2])],
                       [int(pixel_cb[0]) - int(pixel_bb[0])],
                       [int(pixel_cb[1]) - int(pixel_bb[1])],
                       [int(pixel_cb[2]) - int(pixel_bb[2])]])

            matrix = np.array([[1, 0, 0, -np.float64(pixel_ba[0])],
                      [0, 1, 0, -np.float64(pixel_ba[1])],
                      [0, 0, 1, -np.float64(pixel_ba[2])],
                      [1, 0, 0, -np.float64(pixel_bb[0])],
                      [0, 1, 0, -np.float64(pixel_bb[1])],
                      [0, 0, 1, -np.float64(pixel_bb[2])]])
            pseudo_inverse = np.linalg.pinv(matrix)

            result = np.dot(np.linalg.inv(np.dot(matrix.T, matrix)), np.dot(matrix.T, delta_c))

            pixel_co[0] = result[0]
            pixel_co[1] = result[1]
            pixel_co[2] = result[2]
            pixel_ao[3] = result[3] * 255
        success = True
        #########################################
        return success, msg

    def createComposite(self):
        """
        success, errorMessage = createComposite(self)
        
        Perform compositing. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'compositing error'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        back = self._images['backIn']
        h, w, d = back.shape
        self._images["compOut"] = np.zeros((h, w, 3))
        compOut = self._images["compOut"]
        colIn = self._images["colIn"]
        alphaIn = self._images['alphaIn']
        for i in range(0, h):
            for j in range(0, w):
                compOut[i][j] = colIn[i][j] + (1 - (np.float64(alphaIn[i][j][3]) / 255)) * back[i][j]
        success = True
        #########################################

        return success, msg
