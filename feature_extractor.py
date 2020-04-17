import cv2
import json

global_feature_position = []
global_feature_position_top_left = []
global_feature_position_bottom_right = []
key_pressed = False
cropping = False


def read_data():
    data = []
    with open('feature_list.txt', 'rb') as fh:
        # read the data as binary data stream
        data = json.load(fh)
    print("Successfully read feature list from feature_list.data")
    return data


def write_data(feature_data):
    with open('feature_list.txt', 'w') as fh:
        # store the data as binary data stream
        json.dump(feature_data, fh)
    print("Successfully written feature list to feature_list.data")


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global global_feature_position_top_left, global_feature_position_bottom_right, cropping, key_pressed

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        global_feature_position_top_left = [x, y]
        cropping = True
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        global_feature_position_bottom_right = [x, y]
        cropping = False
        key_pressed = True


cv2.namedWindow('input_image')
cv2.setMouseCallback('input_image', click_and_crop)


def get_features(image):
    features = []

    while True:
        feature_name = input("Enter the name of the new feature that you want to add or press d to stop")
        if feature_name == "d":
            break

        while True:
            global global_feature_position_top_left, global_feature_position_bottom_right, key_pressed
            feature_location = []

            while True:
                # display the image and wait for a keypress
                cv2.imshow("input_image", image)
                key = cv2.waitKey(1) & 0xFF
                if key_pressed:
                    break

            print(global_feature_position_top_left, global_feature_position_bottom_right)

            feature_location.append(global_feature_position_top_left)
            feature_location.append(global_feature_position_bottom_right)

            feature = {'name': feature_name, 'loc_top_left': feature_location[0], 'loc_bottom_right': feature_location[1]}
            features.append(feature)
            global_feature_position_top_left = []
            global_feature_position_bottom_right = []
            key_pressed = False

            f'Do you want to add more {feature_name} features?'
            add_feature = input("press y or n.")
            if add_feature != "y":
                break

    return features


if __name__ == "__main__":
    input_image = cv2.imread('floor1.jpg')
    clone = input_image.copy()
    feature_list = get_features(clone)
    write_data(feature_list)
