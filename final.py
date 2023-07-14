import cv2
import os
import time
import uuid
import easyocr
import pyttsx3


# Load the models for English and Arabic
reader = easyocr.Reader(['en', 'ar'])
global img_name

IMAGES_PATH = 'images'
num_img = 3


def start_video():
    global img_name
    cap = cv2.VideoCapture(0)
    print('Collecting image for OCR')
    time.sleep(5)
    for img_num in range(num_img):
        ret, frame = cap.read()

        img_name = os.path.join(IMAGES_PATH, 'image_{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(img_name, frame)
        cv2.imshow('frame', frame)
        time.sleep(2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


def read_text(image_name, model_name, in_line=False):
    # Read the data
    text = model_name.readtext(image_name, detail=0, paragraph=in_line)

    return '\n'.join(text)


def convert_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # You can adjust the speech rate (words per minute) here

    # Set the speech language for each line based on its script
    for line in text.split('\n'):
        # Determine the script (Arabic or English) of the line
        if any(c.isalpha() for c in line):
            script = 'en'  # If the line contains any alphabetic characters, consider it English
        else:
            script = 'ar'  # Otherwise, consider it Arabic

        # Set the speech language to the identified script
        engine.setProperty('voice', f'{script}')

        # Speak the line
        engine.say(line)

    engine.runAndWait()


def perform_ocr():
    global img_name
    start_video()
    image_path = img_name
    text = read_text(image_path, reader)
    print(text)
    convert_to_speech(text)


if __name__ == "__main__":
    perform_ocr()
