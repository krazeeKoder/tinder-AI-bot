# tinder-AI-bot
This is a prototype tinder bot capable of learning the user's preferences and then simulating the user's actions of liking and disliking other profiles on the Tinder platform. For this, an existing TensorFlow CNN has been retrained with images downloaded from Tinder. The code is **not production-ready**, so please feel free to check it out and adjust/personalize it.

A detailed description and documentation of the project can be found [here](https://google.com).

## Usage

### `facebook_tokenloader.py`

This script is copied and adjusted from [kotaroyama](https://github.com/kotaroyama/Get-Tinder-XAuthToken/blob/main/get_tinder_auth.py). It enables to get a XAuthToken for accessing the Tinder API. (You need a Facebook account that is connected to your Tinder account in this step)

### `tinder_image_downloader.py`

Uses the XAuthToken you fetched in the previous step and downloads images from Tinder users to a local folder.

### `image_sorter.py`

Displays the previously downloaded images and puts them to new folders (body_like, body_dislike, face_like, face_dislike, indifferent) according to a user input.

### `classifier_bot.py`

Starts a Tinder session with your personal profile (XAuthToken needed) and assigns the values like/dislike to a given Tinder user according to the outcome of the classification (for this a TensorFlow model has been retrained - described in the next section).

Note that personalization is needed at this point: The script will only start classifying a new profile after user input. Furthermore, liking and disliking is commented out. Also actions like sending a message to a user we matched with could be implemented easily (see [Pynder](https://github.com/charliewolf/pynder)). Additionally, it is recommended to insert some random sleeps.

## Retraining the Convolutional Neural Net

I used the [TensorFlow mobilenet](https://github.com/tensorflow/models/tree/master/research/slim/nets/mobilenet) in this project and retrained it on the Tinder images which I downloaded and labeled.

To build the model you can use something like:

    make_image_classifier \
        --image_dir my_image_dir \
        --tfhub_module https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4 \
        --image_size 224 \
        --saved_model_dir my_dir/new_model \
        --labels_output_file class_labels.txt \
        --tflite_output_file new_mobile_model.tflite \
        --summaries_dir my_log_dir

Documentation on Tensorflow retraining can be found [here](https://github.com/tensorflow/hub/tree/master/tensorflow_hub/tools/make_image_classifier).

## Installation

