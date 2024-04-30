
import cv2
import os

POS_PATH = os.path.join('images')

# Get user input for the common name
custom_name = input("Enter a common name for the images: ")

cap1 = cv2.VideoCapture(0)



image_counter = 0  # Counter for images with the same name

while cap1.isOpened():
    ret, frame = cap1.read()

    cv2.imshow('Image Collection', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('a'):
        # Use a constant name without a unique identifier
        imgname = os.path.join(POS_PATH, f'{custom_name}_{image_counter}.jpg')
        cv2.imwrite(imgname, frame)
        print(f"Image {imgname} saved!")
        image_counter += 1

    elif key == ord('q'):
        break

cap1.release()
cv2.destroyAllWindows()