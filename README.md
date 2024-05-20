# OCR-Image-to-text

This repository uses the pytesseract library to convert image to text. The required libraries are in the requirements.txt file.

To convert image to text, use the following code
```
python imgtotxt.py --source test/test1.PNG
```

The following are additional arguments to use:

| Argument | Second Header |
| ------------- | ------------- |
| ```--save-as```  | set output folder name  |
| ```--save-txt```  | save results to txt file  |
| ```--threshold``` | use different threshold values [mean-c, gaussian-c, binary] |





Here is a sample output:
## INPUT:
![alt-text](https://github.com/pfdhn/OCR-Image-to-text/blob/main/sample/sample1.png)

## OUTPUT:
![alt-text](https://github.com/pfdhn/OCR-Image-to-text/blob/main/sample/sample1_output.png)
