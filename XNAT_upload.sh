#!/bin/bash

echo -n 'Enter the filename you would like to upload: '; read FILENAME
echo -n 'Enter the project name: '; read PROJ

#Create subject SUBJECT01
curl -u admin:admin -X PUT "http://qifp-test.stanford.edu/data/projects/my_proj/subjects/SUBJECT01"

#Add zip to proj prearchive
#Can also add subject(person), experiment(image session) fields with SUBJECT_ID and EXPT_LABEL
curl -u admin:admin -X POST "http://qifp-test.stanford.edu/data/services/import?\
PROJECT_ID=$PROJ&\
import-handler=DICOM-zip&\
overwrite=append&\
prearchive=true&\
inbody=true" \
--data-binary @"$FILENAME"


