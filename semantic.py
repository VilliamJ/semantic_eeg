# load modules
from psychopy import visual, core, event, data, gui
# import module for getting filenames
import glob
# import module for randomization
import random
# import module for creating data frame and saving log file
import pandas as pd
# import module to create new directory 
import os


#define dialogue box (important that this happens before you define the window)
box = gui.Dlg(title="Sizes of Circles")
box.addField("Participant ID: ")
box.addField("Age: ")
box.addField("Gender: ", choices=["Female", "Male", "Other"])

box.show()
if box.OK:  # To retrieve data from the popup window
    ID = box.data[0]
    AGE = box.data[1]
    GENDER = box.data[2]
elif box.Cancel:  # To cancel the experiment if the popup is closed
    core.quit()

# define window
win = visual.Window(fullscr=False, color="black")

# define stop watch
stopwatch = core.Clock()

# get date for a unique logfile name
date = data.getDateStr()

# define logfile
# prepare pandas data frame for recorded data
columns = ['time_stamp', 'id', 'age', 'gender', 'word', 'keypress', 'reaction_time']
logfile = pd.DataFrame(columns=columns)

# make sure that there is a logfile directory and otherwise make one
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")

# define logfile name
logfile_name = "logfiles/logfile_{}_{}.csv".format(ID, date)

# text
instruction = '''
Welcome to this experiment! This experiment consists of two phases\n\n
In the first phase, a total of XX words will be presented to you and your task is to simply memorize these words. \n\n
In the second phase, you will be shown words one at a time and asked whether you have previously seen this word in the experiment.\n\n\n
You do this by pressing Y for YES if you have seen it. If the word has not appeared earlier, press N for NO. \n\n\n
If you understand these rules, please press any key to begin the experiment.
'''

goodbye = '''
The experiment is done. Thank you for your participation!
'''

# List of 100 words
school_related_words = ["classroom", "teacher", "student", "homework", "exam", "textbook", "pencil", "notebook", "chalkboard", "backpack", 
                        "library", "principal", "lunchbox", "recess", "graduation", "science", "mathematics", "history", "literature", "geography", 
                        "chemistry", "physics", "biology", "art", "music", "physicaleducation", "bell", "desk", "attendance", "diploma", 
                        "project", "quiz", "education", "schoolbus", "cafeteria", "playground", "blackboard", "algebra", "geometry", 
                        "language", "spelling", "backpack", "notebook", "schoolwork", "reportcard", "pta", "fieldtrip", "uniform", "clock", "learning"]

unrelated_words = ["cat", "river", "pizza", "story", "lamp", "park", "car", "flower", "hat", "ball", "guitar", "sun", "key", "chair", "dog", "moon", 
                   "rain", "shoe", "house", "apple", "song", "bike", "bird", "clock", "cloud", "star", "cup", "smile", "game", "duck", "candy", 
                   "beach", "icecream", "color", "letter", "dance", "baby", "train", "sleep", "run", "bear", "laugh", "ocean", "bridge", "book", 
                   "tree", "chair", "sky", "fire", "mountain"]

# Combine the two lists
all_words = school_related_words + unrelated_words

# Shuffle the combined list
random.shuffle(all_words)

# function for showing text and waiting for a key press
def introduction(txt):
    message = visual.TextStim(win, text = txt, alignText = "left", height = 0.05)
    message.draw()
    win.flip()
    response = event.waitKeys()

def msg(txt):
    message = visual.TextStim(win, text = txt, alignText = "center", height = 0.15)
    message.draw()
    win.flip()

def get_response():
    key = event.waitKeys(keyList=["space", "escape", "y", "n"])
    if key[0] == "escape":
        core.quit()
    else:
        response = key[0]

    return response


random_word = random.choice(all_words)

# Create a text stimulus
text_stimulus = visual.TextStim(win, text='', height=30)


################ beginning of experiment ###############
introduction(instruction)

# preparing image stimulus
for word in all_words:
    msg(word)
    
    # start recording reaction time
    stopwatch.reset()
    
    # get reaction time
    reaction_time = stopwatch.getTime()
    
    response = get_response()
    # wait for a keypress and record the response
    
    
    logfile = logfile.append({
        'time_stamp': date,
        'id': ID,
        'age': AGE,
        'gender': GENDER,
        'keypress': response,
        'word': word,
        'reaction_time': reaction_time}, ignore_index = True)
    
#print(get_response(stimulus))

# save data to directory
logfile.to_csv(logfile_name)

# show goodbye message
msg(goodbye)

