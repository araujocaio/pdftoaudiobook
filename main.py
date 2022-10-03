# encoding=utf8
from multiprocessing.dummy import current_process
import pyttsx3
import PyPDF2
import sys
import os

es_lang = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
en_lang = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

#Remove the EOF 
def reset_eof_of_pdf_return_stream(pdf_stream_in:list):
    # find the line position of the EOF
    for i, x in enumerate(pdf_stream_in[::-1]):
        if b'' in x:
            actual_line = len(pdf_stream_in)-i
            print(f'EOF found at line position {-i} = actual {actual_line}, with value {x}')
            break

    # return the list up to that point
    return pdf_stream_in[:actual_line]

def WriteNewFile(_filename, new_name):
    # opens the file for reading
    with open( _filename , 'rb') as p:
        txt = (p.readlines())

    # get the new list terminating correctly
    txtx = reset_eof_of_pdf_return_stream(txt)

    # write to new pdf
    with open(new_name, 'wb') as f:
        f.writelines(txtx)


def CreateDir(foldername):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory +"/output/" , foldername )
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)


def WriteNewFileTest( _filename ):

    EOF_MARKER = b'%%EOF'
    newname = _filename

    with open(_filename, 'rb') as f:
        contents = f.read()

    # check if EOF is somewhere else in the file
    if EOF_MARKER in contents:
        # we can remove the early  and put it at the end of the file
        contents = contents.replace(EOF_MARKER, b'')
        contents = contents + EOF_MARKER
    else:
        # Some files really don't have an EOF marker
        # In this case it helped to manually review the end of the file
        print(contents[-8:]) # see last characters at the end of the file
        # printed b'\n%%EO%E'
        contents = contents[:-6] + EOF_MARKER

        newname = _filename.replace('.pdf', '') + '_fixed.pdf'

    with open( newname ,  'wb') as f:
        f.write(contents)

    return newname

def change_voice(engine, language, gender='VoiceGenderMale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

def WritePagesToMp3(foldername, pdfReader, lang, speed):
        pages = pdfReader.numPages
        speaker = pyttsx3.init()

        #100 ishalf the speed rate by default
        speaker.setProperty('rate', speed)
        #voices = speaker.getProperty('voices') 
       
        if (lang=="es"):
            speaker.setProperty('voice', es_lang)
        else:
            speaker.setProperty('voice', en_lang )


        for num in range(1, pages):
            page = pdfReader.getPage(num)
            text = page.extractText()
            #speaker.say(text)
            currentPage = './output/'+ foldername+'/page'+ str(num)+'.mp3'
            speaker.save_to_file(text, currentPage )
            print("File "+ str( currentPage ) + " saved")
            speaker.runAndWait()

        print("Process Finished with " + str(pages) + " audio files generated!")


#HOW 
def main(_filename, language, speed):
    try:
        print("Process Started")
        foldername = _filename.replace('.pdf', '') 
        CreateDir(foldername)
        print(foldername)
        book = open("./input/"+ _filename , 'rb')
        print("./input/"+ _filename)

        print(".")
        pdfReader = PyPDF2.PdfReader(book, strict=False)
        print("..")
        WritePagesToMp3( foldername,pdfReader , language , speed )
    except:
        #probably the pdf EOF is truncated, so we recreate:
        print("Process Started")
        foldername = _filename.replace('.pdf', '') 
        CreateDir(foldername)
        newfilename = "./input/"+foldername+'_fixed.pdf'
        WriteNewFile("./input/"+_filename, newfilename )
        print(".")
        book = open( newfilename , 'rb')
        print("..")
        pdfReader = PyPDF2.PdfReader(book, strict=False)
        print("...")
        WritePagesToMp3(foldername, pdfReader , language, speed )
        #NewFileName = WriteNewFileTest( _filename )
        #pdfReader = PyPDF2.PdfReader(NewFileName, strict=False)
        #WritePagesToMp3( pdfReader )

#call python main.py youarebadass.pdf en 150
if __name__ == "__main__":
    _filename = sys.argv[1] 
    language = sys.argv[2]
    speed = sys.argv[3]
    print(_filename)
    print(language)
    print(speed)
    main( _filename , language , speed )
