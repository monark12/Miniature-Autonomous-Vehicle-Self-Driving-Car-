import io
import socket
import struct
import cv2
from PIL import Image
import time

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('192.168.1.2', 8000))
server_socket.listen(0)
i=0
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        print(image_len)
        if not image_len:
            pass
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it

        image_stream.seek(0)
        image = Image.open(image_stream)
        
        image.save("training_images/frame"+str(i)+".jpg", "JPEG", quality=80, optimize=True, progressive=True)
        i+=1
        print ('----------------', time.time(), '----------------')
        print('Image is %dx%d' % image.size)
        image.verify()
        print('Image is verified')
        print ('--------------------------------')
finally:
    connection.close()
    server_socket.close()
