from datetime import datetime, timedelta
import piexif 
import os

images = os.listdir(".")

for image in images:
    if image.endswith(".JPG"):
        # read current date time
        exif_dict = piexif.load(image)
        if piexif.ImageIFD.DateTime in exif_dict['0th']:
            current_time = exif_dict['0th'][piexif.ImageIFD.DateTime].decode("utf-8")
            current_time_stripped = datetime.strptime(current_time, "%Y:%m:%d %H:%M:%S")
            # print(f"Current Aufnahmedatum:{current_time_stripped}")

            # add six hours
            new_time_stripped = current_time_stripped + timedelta(hours = 6)
            new_time = new_time_stripped.strftime("%Y:%m:%d %H:%M:%S")
            # print(f"Current Aufnahmedatum:{new_time_stripped}")

            # update all EXIF fields
            new_time_bytes = new_time.encode("utf-8")
            exif_dict["0th"][piexif.ImageIFD.DateTime] = new_time_bytes
            exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_time_bytes
            exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = new_time_bytes

            # insert modified EXIF fields into original picture
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, image)

            print(f"Updated image Aufnahmedatum from '{current_time_stripped}' -> '{new_time_stripped}'")

# exif_dict = piexif.load("")
