from __future__ import print_function
import cv2
import pytesseract
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
from PIL import ImageGrab


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = 'nope'

SAMPLE_RANGE_NAME = 'Taulukko1!A2:G'

custom_config = r'--oem 3 --psm 6 outputbase digits'
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd=tesseract_path



def clipboard_image():
    img = ImageGrab.grabclipboard()
    if img is None:
        print("you have not copied an image to the clipboard, disabling upload to google sheets")
        return False
    img = img.crop((3210,230,3780,760))
    img.save('tmp.jpg', 'JPEG')
    return True

def read_stats(imagefile):
    img = cv2.imread(imagefile)

    # get grayscale image
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #thresholding
    def thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        

    gray = get_grayscale(img)
    thresh = thresholding(gray)

    #cv2.imshow('thresh',thresh)
    #cv2.waitKey(0)



    txt = pytesseract.image_to_boxes(thresh, config=custom_config)

    stats = txt.split()
    
    stats_dirty = [stats[x:x+6] for x in range(0, len(stats), 6)]
    stats_chunked = []
    for i in range(len(stats_dirty)):
        if stats_dirty[i][0] != '-':
            stats_chunked.append(stats_dirty[i])
    print(stats_chunked)
    first_row = join_numbers(filter(filter_first_row,stats_chunked))
    print(first_row)
    first_row = [int(x) for x in first_row]
    second_row = join_numbers(filter(filter_second_row,stats_chunked))
    print(second_row)
    second_row = [int(x) for x in second_row]
    third_row = join_numbers(filter(filter_third_row,stats_chunked))
    print(third_row)
    third_row = [int(x) for x in third_row]
    fourth_row = join_numbers(filter(filter_fourth_row,stats_chunked))
    print(fourth_row)
    fourth_row = [float(x) for x in fourth_row]

    return first_row+second_row+third_row+fourth_row

def main(newimg):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    today=datetime.date.today().strftime("%d.%m.%Y")
    stats = read_stats('tmp.jpg')
    print(stats)
    row_to_add = [today,stats[0],stats[1],stats[2],stats[5],stats[3],stats[4]]
    print(row_to_add)
    
    
    if (newimg):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=SAMPLE_RANGE_NAME,body={'range':SAMPLE_RANGE_NAME,'values':[row_to_add],'majorDimension':'ROWS'},valueInputOption='USER_ENTERED').execute()



def filter_first_row(number):
    return abs(int(number[2])-443)<4

def filter_second_row(number):
    return abs(int(number[2])-124)<4 and int(number[1])-280>0

def filter_third_row(number):
    return abs(int(number[2])-81)<4 and int(number[1])-280>0

def filter_fourth_row(number):
    return abs(int(number[2])-55)<4 and int(number[1])-280<0

def join_numbers(characters):
    numbers = []
    numbers_completed = -1
    last_character_trailing_x = '0'
    for char in characters:
        distance = abs(int(char[1])-int(last_character_trailing_x))
        if distance < 15:
            numbers[numbers_completed] += char[0]
        else:
            numbers_completed += 1
            numbers.append(char[0])
        last_character_trailing_x = char[3]
    return numbers

if __name__ == '__main__':
    # if(len(sys.argv)<2):
    #     print("No file supplied, aborting..")
    #     exit(0)
    try:
        newimg = clipboard_image()
        main(newimg)
        input('image processed, press enter to exit')
    except Exception as e:
        print(e)
        input('something went wrong')
	# stats = read_stats('tmp.jpg')
    # print(stats)
    
