'''
    Author: Pinky Era Dehino

    Description: 
    This python file converts image files to text format. 
    By default, files are saved to OCR/output/conv#, where # is the number of files inside the output folder

    In case the python command is invoked outside the parent folder, the 


    file format supported: jpg, jpeg, png

    Usage:
    python imgtotxt.py --source test/test1.PNG  
'''
import pytesseract
import cv2
import os 
import argparse
import sys
from pathlib import Path
from datetime import datetime

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0] # get root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
valid = ('jpeg', 'jpg', 'png')
thresh = ['mean-c', 'gaussian-c', 'mean', 'gaussian', 'binary']

# def extract(path, threshold):

#     if threshold is None:         # read the image file as it is
#         img = cv2.imread(path)
#     elif threshold.lower() not in thresh:
#         print("ERROR invalid threshold value must be ", thresh)
#         exit(1)
#     else:                               # read input image as grayscale
#         img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        
#         if threshold.lower() == 'mean-c':
#             t = cv2.ADAPTIVE_THRESH_MEAN_C
#             #img = cv2.adaptiveThreshold(img, 255, t, cv2.THRESH_BINARY,11,2)
#         elif threshold.lower() == 'gaussian-c':
#             t = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
#             #img = cv2.adaptiveThreshold(img, 255, t, cv2.THRESH_BINARY,11,2)
#         elif threshold.lower() == 'binary':
#             img = cv2.threshold(img,127, 255, cv2.THRESH_BINARY)
#         else:
#             exit(1)
        

#         img = cv2.adaptiveThreshold(img, 255, t, cv2.THRESH_BINARY,11,2)
#     return pytesseract.image_to_string(img), img


def extract(path, threshold, morph = True):

    if threshold is None:                                           # read the image file as it is
        img = cv2.imread(path)
    else:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)                # read input image as grayscale
        blur = cv2.GaussianBlur(img, (0,0), sigmaX=33, sigmaY=33)    # blur image
        img = cv2.divide(img, blur, scale=255)                      # background removal method; whitens bg

        if threshold.lower() not in thresh:
            print("ERROR invalid threshold value must be ", thresh)
            exit(1)
        elif threshold.lower() == 'mean-c' or threshold.lower() == 'mean':                               
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
        elif threshold.lower() == 'gaussian-c' or threshold.lower() == 'gaussian':                               
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        elif threshold.lower() == 'binary':                               
            i, img = cv2.threshold(img,200, 255, cv2.THRESH_BINARY)
        else:
            print('EXITED')
            exit(1)

    if morph:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        

    return pytesseract.image_to_string(img), img


def valid_ext(source):
    ext = source.split('.')[-1:]
    ext = ext[0].lower()
    
    if ext in valid:
        return True
    else:
        return False


def parse_var():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, help='input image file')
    parser.add_argument('--save-as', type=str, help='set output folder name')
    parser.add_argument('--save-txt', action='store_true', help='save results to txt file')

    # preprocessing commands
    '''
        for more thresholding techniques, see https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
    '''
    parser.add_argument('--threshold', type=str, help='Options: [mean-c, gaussian-c, binary]')

    return parser.parse_args()

def main(args):

    source = args.source
    threshold = args.threshold
    

    if source is None:
        print('ERROR No source file. Use --source argument to add file path')
    elif os.path.exists(source) is False:
        print('ERROR File does not exist.')
    elif valid_ext(source) is False:
        print("Invalid file format. Valid formats are ", valid)
    else:
        savedir = ROOT / 'output'
    
        if os.path.exists(savedir) is False:     # if output folder does not exist, then create output folder
            os.mkdir(savedir)

        text,img = extract(source, threshold)
        print('\nExtracted: \n\n',text)
        
        if args.save_txt:
            if args.save_as is not None:
                filename = str(args.save_as)
            else:
                filename = "conv_" + str(datetime.now().strftime("%m%d%y_%H%M%S"))

            savedir = os.path.join(savedir,filename)
            os.mkdir(savedir)

            # save image to directory
            cv2.imwrite(os.path.join(savedir,'img.jpeg'), img)

            # save extracted text to file.txt
            f = open(os.path.join(savedir,'file.txt'), 'w')
            f.writelines(text) 
            f.close()

            print('Output saved to ', savedir)
        


if __name__ == '__main__':
    var = parse_var()
    main(var)