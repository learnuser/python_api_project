import sys
import subprocess
import re
from pymongo import MongoClient
import csv
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator


def converts(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    laparams = LAParams()
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=laparams)
    interpreter = PDFPageInterpreter(manager, converter)
    laparams.char_margin = 30
    laparams.line_margin = float(50)
    laparams.word_margin = float(50)
    device = PDFPageAggregator(manager, laparams=laparams)

    infile = fname
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
        layout = device.get_result()
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def score_test(fname,collection_name,prefix,mongodb_id):
    test_result = []
    # Call converts function to parse pdf file with adjusted laparams.
    hy = converts(fname)
    # Regex to find acronym in debugger module in the report.
    acronym_pattern = r'(.*)_agey'
    acr_regex = re.compile(acronym_pattern)
    acronym = acr_regex.findall(hy)
    # Regex to find all variables in the report.
    pattern = r'('+acronym[0]+'_\w+)\s(.*)'
    regex = re.compile(pattern)
    result = regex.findall(hy)
    # Regex to find 'id' in Mongodb for comparison.
    id_pattern = r'.*'+prefix+'(.*).pdf'
    id_regex = re.compile(id_pattern)
    id_value = id_regex.findall(fname.filename)
    print id_value,id_value[0],len(id_value)
    # Connect to MongoDB
    client = MongoClient('10.106.199.110',27017)
    db = client.mtcf
    temp = 'db.'+collection_name
    collection = eval(temp)
    data = collection.find_one({mongodb_id:int(id_value[0])})
    if not data: return "No data found in MongoDB for given ID."
    # Compare data from report to Mongo DB.
    for r in result:
        y = str(r[1]).split(" ")[0]
        y = y.strip()
        if r[0] in data.keys():
            if type(data[r[0]]) == int or type(data[r[0]]) == float:
                data[r[0]] = float(data[r[0]])
                y = float(y)
            if y != data[r[0]]:
                temp_result = str(r[0])+ str(y)+ str(data[r[0]])
                test_result.append(temp_result)
                #print r[0], y, data[r[0]]
    return test_result



##for r in result:
##    if r[0] not in data.keys():
##        print r[0]+ ' not present in MTCF file.'



#fname = open('C:/Users/umurasa/Documents/2017/Q3 Release/dummy/MTCF_ID_8475.pdf','rb')


#score_test(fname,'CVLT3_QI','MTCF_ID_','ID')


