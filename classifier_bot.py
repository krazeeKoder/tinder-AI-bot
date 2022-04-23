import os
import pynder
import label_profile
import urllib.request

current_profile_dir = 'current_profile/'


def main():
    XAuthToken = 'your token'
    session = pynder.Session(XAuthToken=XAuthToken)
    session.update_location(48.193371, 16.366072)
    users = session.nearby_users()

    for user in users:
        input("start profile")
        photos = user.get_photos()
        print(user.name)
        cnt = 0
        for photo in photos:
            image_name = current_profile_dir + user.name + "_" + str(cnt) + "_" + str(
                user.age) + "_" + user.id + ".jpg"
            print(image_name)
            urllib.request.urlretrieve(photo, image_name)
            cnt += 1
        like = label_profile.label_all_pictures(current_profile_dir)
        print(like)

        # like or dislike based on classification outcome
        # if like:
        #     user.like()
        # else:
        #     user.dislike()

        input("del pics")
        for photo in os.listdir(current_profile_dir):
            image = current_profile_dir + photo
            os.remove(image)


if __name__ == "__main__":
    main()
