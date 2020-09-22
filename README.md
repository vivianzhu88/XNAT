# preparing-XNAT-data

### Task:
[Dataset](https://www.kaggle.com/c/diabetic-retinopathy-detection/data)

Upload set C (1/3 of dataset) into XNAT to act as client in distributed deep learning tasks.


### Descriptions:

1. **IHD_convert.py** extracts files from dataset and alters DICOM headers so compatible with XNAT

2. **XNAT_upload.sh** uploads fixed data through XNAT API

