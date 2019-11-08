# Cross Lingual Document Translator

## Introduction

Statistical Machine Translation is an empirical machine
translation technique using which translations are generated on the basis of statistical models trained on
bilingual text corpora.


## Directory Structure

```
├── code.py                          -> The testing code.
├── ir_project_notebook.ipynb        -> Notebook of training and testing code/
├── README.md                        -> This file :)
├── src.txt                          -> Testing Source para(english by default but can be changed)
├── target.txt                       -> Testing Destination para(english by default but can be changed)
├── translations.pickle              -> Translation dictionary object file, got by training
├── output/                          -> That's where the trained files will be stored
``` 

## How to run the code

```python
$ python3 code.py
```

## Sample Demo
```
FDUSER@admin18-OptiPlex-3020:~/ir_project/final_code$ python3 code.py 
Welcome to Cross Language Translations(English<-->Dutch)
Reading Translations.....
Reading the pickle time may takes time....
Which Translation you want?
1. ENGLISH TO DUTCH
2. DUTCH TO ENGLISH
Please select the option: 1
Enter source document path: src.txt
Enter target document path: target.txt
This document has cosine similarity: 0.32002844823759896
This document has Jacard similarity: 0.19047619047619047
Ouputing your result into filename: translated_1.txt
Do you want to continue? 
Please select the option(Y/N)?: y
Current Average cosine similarity: 0.32002844823759896
Current Average Jacard similarity: 0.19047619047619047
Which Translation you want?
1. ENGLISH TO DUTCH
2. DUTCH TO ENGLISH
Please select the option: 2
Enter source document path: target.txt
Enter target document path: src.txt
This document has cosine similarity: 0.3136121713991153
This document has Jacard similarity: 0.17857142857142858
Ouputing your result into filename: translated_2.txt
Do you want to continue? 
Please select the option(Y/N)?: n
Final Average cosine similarity: 0.15680608569955765
Final Average Jacard similarity: 0.08928571428571429
```

## Notebook

For training and detailed explanation checkout the `ir_project_notebook.ipynb` notebook file.