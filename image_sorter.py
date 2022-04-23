import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os


def save_image(like_value, photo, img):
    filename = 'data/'

    # body like
    if like_value == 'b':
        print('body like')
        filename += 'body_like/' + photo
        plt.imsave(filename, img)

    # body dislike
    if like_value == 'bb':
        print('body dislike')
        filename += 'body_dislike/' + photo
        plt.imsave(filename, img)

    # face like
    if like_value == 'f':
        print('face like')
        filename += 'face_like/' + photo
        plt.imsave(filename, img)

    # face dislike
    if like_value == 'ff':
        print('face dislike')
        filename += 'face_dislike/' + photo
        plt.imsave(filename, img)

    # indifferent
    if like_value == 'i':
        print('indifferent')
        filename += 'indifferent/' + photo
        plt.imsave(filename, img)


def main():
    base_path = 'data/downloads/'
    for photo in os.listdir(base_path):
        photo_path = base_path + photo
        img = mpimg.imread(photo_path)
        plt.imshow(img)
        plt.show()

        like_value = input()

        # save pic to new folder and delete it from 'to_label' folder
        save_image(like_value, photo, img)
        os.remove(photo_path)


if __name__ == "__main__":
    main()
