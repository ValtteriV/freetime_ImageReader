# freetime_ImageReader

## Purpose of the application
The purpose of this application is to be able to read numerical values from an image based on configured areas for the reads. The reading is done using Google's Tesseract. 

The goals for the final product are:
- Have a configuration GUI where the read areas are defined by hand
- Have checkboxes to pick and choose the image processing that seems to provide the most accurate results for the specific use-case
- After configuration is finished, the program should be able to read defined areas and output them in some manner (TBD)

## Purpose of the project
The original idea had two learning goals of getting a feel for computer vision as well as integrating programs to work alongside Google Sheets. The sandbox version is based on my original use-case where I wanted to track my progress in a game where there was no API endpoint I could use for logging into Google Sheets, and I was too lazy to write the numbers in myself any time I wanted to log a session. For the actual application I will be keeping the google sheets integration as a separate script that leverages the output of the application.