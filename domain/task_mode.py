from enum import Enum

class TaskMode(Enum):
    IMAGE = "image"
    PDFTOTEXT = "pdftotext"
    IMAGETOTEXT = "imagetotext"
    PDFTOIMAGE = "pdftoimage"
    PDFTOTEXTANDIAMGE = "pdftotextandimage"
    PDFTOTEXTBYCHUNK = "pdftotextbychunk"
    PDFTOIMAGEBYCHUNK = "pdftoimagebychunk"