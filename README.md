# pdftoaudiobook

##########################################

## Credits to: https://www.youtube.com/watch?v=kyZ_5cvrXJI
## Modified by: Caio Araujo

##########################################

##########################################

# GOAL: 

- call the python and pass the pdf 
- create 1 mp3 file per page (easier to divide by days)
- added language (so i can convert books both in english and spanish)
- control the speed 


Troubles
- pdffilereader was deprecated and error  --- PyPDF2.errors.PdfReadError: PDF starts with '♣▬', but '%PDF-' expected  --- was happening
    - solution  : https://stackoverflow.com/questions/72215976/pypdf2-errors-pdfreaderror-pdf-starts-with-but-pdf-expected
- later on, the pdf file had an issue : PyPDF2.errors.PdfReadError: EOF marker not found --- 
    - solution : https://stackoverflow.com/questions/45390608/eof-marker-not-found-while-use-pypdf2-merge-pdf-file-in-python
- Code working with redundant functions. 



##########################################
# HOW TO:

## 0. Create a virtual environment

python -m venv venv

## 1. Activate venv

.\venv\Scripts\activate


## 2. install dependencies

pip install pyttsx3
pip install pypdf2 
pip install pyaudio
pip install speak
pip install ffmpeg

## 3. Copy the pdf in the input folder


## 4. Call the main function adding the pdf name, language (es/en) and speed

#accepted languages ( es , en)
#speed rate by default is 200 

python main.py pdfname.pdf es 150

## 5. Voilà, check output files in the /output/pdfname/
