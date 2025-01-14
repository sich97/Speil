def preview_image(image, name="window", time=1000):
    import cv2
    cv2.imshow(name, image)
    if cv2.waitKey(time):
        cv2.destroyAllWindows()


def image_to_string(image):
    import cv2
    import base64
    encoded, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer)


def string_to_image(string):
    import numpy as np
    import cv2
    import base64
    img = base64.b64decode(string)
    # noinspection PyTypeChecker
    npimg = np.fromstring(img, dtype=np.uint8)
    return cv2.imdecode(npimg, 1)
