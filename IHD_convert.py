import zipfile
import os
import csv
import pydicom

from pydicom.data import get_testdata_file
from pydicom.filereader import read_dicomdir

file_list = []
handle = open("C_train.csv")

#change to file naming format
for line in handle:
    line = line.rstrip()
    file_list.append("ID_" + line + ".dcm")
file_list = file_list[1:] #remove "id" label
print(file_list)

#extract desired files
with zipfile.ZipFile('rsna-intracranial-hemorrhage-detection.zip', 'r') as file:

    #list of files already uploaded
    uploaded = []
    with open('uploaded.csv', newline='') as inputfile:
        for row in csv.reader(inputfile):
            uploaded.append(row[0])
    print(uploaded)
            
    count = 0
    #extract files not already uploaded
    for f in file_list:
        if f not in uploaded:
            path = os.getcwd() + "/upload/"
            e_file = 'rsna-intracranial-hemorrhage-detection/stage_2_train/' + f
            file.extract(e_file, path)
            
            ds = pydicom.dcmread(path + e_file)
            
            if 'SOPClassUID' not in ds:
                ds.SOPClassUID = ds.file_meta.MediaStorageSOPClassUID
                
            ds.PatientName = ds.PatientID
            ds.PatientID = f[3:-4]
            
            ds.save_as(path + e_file)
            
            with open('uploaded.csv', 'a') as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow([f])
            print(f)
            
            count += 1
            if count == 10000:
                break
        else:
            print(f, "is already uploaded")
        

