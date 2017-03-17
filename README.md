# classifier

Description:
This script is intended to gather human input on a batch of neural network generated images.
This gathered data will be used as a training set for our 2nd neural network (appraisal network). There is around 600 images in this batch.
Please don't spent more than 1 sec per image. Don't think too much about them. Follow your gut feeling :)

How to use:
1) Install python
2) ./setup.sh
3) python ./survey.py --username <username> --name <name>

Input for the program is strictly keyboard inputs: 'left' for bad, 'down' for ok, 'right' for good, and 'esc' to exit the program.
Upon pressing 'esc', a message will pop up to confirm the exit.
If yes, a result file will be generated. Please send us the result file via Slack: @achan or @dgonchar.
