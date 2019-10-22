import os
import pdfrw
from PyPDF2 import PdfFileWriter, PdfFileReader


TEMPLATE_PATH = 'postal_template.pdf'
OUTPUT_PATH = 'postal_output.pdf'
ENCRYPT_PATH = 'postal_encrypted.pdf'


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'



def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):    
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotations = template_pdf.pages[1][ANNOT_KEY]    
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY: 
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    print("Matched: ", key)
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                    )
        # Hack to change appearance so filled up text fields show in Preview
        annotation.update(pdfrw.PdfDict(AP=''))

    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
    


def encrypt(input_pdf, output_pdf, password):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_pdf)
 
    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))
 
    pdf_writer.encrypt(user_pwd=password, owner_pwd=None, 
                       use_128bit=True)
    with open(output_pdf, 'wb') as fh:
        pdf_writer.write(fh)

data_dict = {   
   'surname': 'Manocha',
   'firstname': 'Pranay',
   'addr1': 'Flat 1',
   'addr2': 'Gates Lane',
   'addr3': 'Somewhere',
   'postcode': 'SO15 1XY',
   'phoneno': '07885219531',
   'email':'test@gmail.com',
   #'permanentpostal':'On',
   'electiondate_dd':'12',  
   'electiondate_mm':'12',
   'electiondate_yyyy':'2019',
   'dob_dd':'01',
   'dob_mm':'01',
   'dob_yyyy':'2000',
   'app_dd':'22',
   'app_mm':'10',
   'app_yyyy':'2019'   
}

if __name__ == '__main__':
    # This works fine but I cannot figure out how to set the 'permanentpostal' field
    write_fillable_pdf(TEMPLATE_PATH, OUTPUT_PATH, data_dict)

    # Encrypting the PDF deletes all form data and additionally makes the PDF uneditable
    encrypt(OUTPUT_PATH,ENCRYPT_PATH,"password123!")