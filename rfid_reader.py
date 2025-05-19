from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import requests
import time

reader = SimpleMFRC522()
API_ENDPOINT = "http://<your-api-url>/rfid-scan"

current_student_id = None

try:
    while True:
        print("Place RFID card/tag...")
        id, text = reader.read()
        rfid_data = text.strip()

        if rfid_data.startswith("STU"):
            current_student_id = rfid_data
            print(f"Student identified: {current_student_id}")
        elif rfid_data.startswith("BOOK") and current_student_id:
            book_id = rfid_data
            print(f"Issuing/Returning Book: {book_id} to Student: {current_student_id}")

            data = {'student_id': current_student_id, 'book_id': book_id}
            try:
                response = requests.post(API_ENDPOINT, json=data)
                print("Server response:", response.text)
            except Exception as e:
                print("Error sending data to server:", e)
        else:
            print("Scan a student card first!")

        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping...")
finally:
    GPIO.cleanup()
