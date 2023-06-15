# MusicSpace

MusicSpace is a toy marketplace that we created in order to demonstrate the TakeOne Video Integration. 

## Prerequisites

You need to have the following installed prior to running the application: 

 - Docker

In order to use the local test scripts that mock the TakeOne Recording App, you will need to have the following installed:

 - Python (tested with v3.11.2)
 - ffmpeg (tested with v6.0)

## Configuration

First, you will need to make a copy of `dev.musicspace-service.override-sample.env`, naming it `dev.musicspace-service.override.env`. In here, you should fill in your Client ID, Client Secret, and Video Container Template ID that we provide. 

## Running

First, you'll need to build the containers using the following command:

```
docker compose build
```

Then, run the containers using the following command:

```
docker compose up
```

Once the application is up, you can visit your locally running MusicSpace app [here](http://localhost:3000).

## Creating a video

From the [Teacher list page](http://localhost:3000), click the sign in button to sign in as a teacher. By default, 15 teacher profiles have been created. Their usernames range from `teacher_0` to `teacher_14`, all with the password `passwordabc123`.

Once you've signed in, you'll be redirected to the teacher profile page. Click the `Create a profile video with TakeOne` button. When that operatin is completed, you should notice a page reload and the button text change to `Resend invitation email`. In the `data/musicspace-service/emails` directory, you should see that a test email has been sent. Open it and you should find the text that is similar to the following, contaning a JWT-based access code:

```
Hi Elizabeth Jones,

Congrats! Here's your code to start recording your TakeOne Video!


ey...C8

Sincerely,
Your friends at MusicSpace
```

### Implementation Details
TBD

Once you confirm that you have the access code, you can run the `app_user_workflow.py` script to simulate the user recording a video in the TakeOne Recording App.

Using a terminal, navigate to the `scripts/` directory. If you haven't already, create a virtual environment, activate it, and install dependencies.

```
python -m venv myenv
source myenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt   
```

Then, run the `app_user_workflow.py` using the following command:

```
python app_user_workflow.py app_user_config.json {code from email}
```

This script will upload the video and monitor the progess of the video production process. It may take some time (>15 minutes or so depending on the length of the video). This is a great time to go grab a snack :)

The teacher profile page is set up to fetch changes to the video container, so that when the video is done processing and it's published, the streaming information will be updated in the database. Therefore, once the `app_user_workflow.py` script is completed, you should be able to refresh the teacher profile page and see the streaming video.

> NOTE: In a production deployment, you'd likely want to use a webhook to be notified of changes in the publishing status of a video container.




