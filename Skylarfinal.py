import pandas as pd
import os
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim
from psychopy.core import Clock, quit, wait
from psychopy.event import Mouse
from psychopy.hardware.keyboard import Keyboard
from psychopy.visual import Slider

### DIALOG BOX ROUTINE ###
exp_info = {'participant_nr': '', 'age': ''}
dlg = DlgFromDict(exp_info)

# If pressed Cancel, abort!
if not dlg.OK:
    quit()
else:
    # Quit when either the participant nr or age is not filled in
    if not exp_info['participant_nr'] or not exp_info['age']:
        quit()
        
    # Also quit in case of invalid participant nr or age
    if int(exp_info['participant_nr']) > 99 or int(exp_info['age']) < 18:
        quit()
    else:  # let's star the experiment!
        print(f"Started experiment for participant {exp_info['participant_nr']} "
                 f"with age {exp_info['age']}.")

# Initialize a fullscreen window with my monitor (HD format) size
# and my monitor specification called "samsung" from the monitor center
win = Window(size=(1920, 1080), fullscr=False, monitor='samsung')

# Also initialize a mouse, although we're not going to use it
mouse = Mouse(visible=True)

# Initialize a (global) clock
clock = Clock()

# Initialize Keyboard
kb = Keyboard()
kb.clearEvents()

### START BODY OF EXPERIMENT ###


### WELCOME ROUTINE ###
# Create a welcome screen and show for 2 seconds
welcome_txt_stim = TextStim(win, text="Welcome to this experiment!", color=(1, 0.41, 0.71), font='Calibri', height=0.3)
welcome_txt_stim.draw()
win.flip()
wait(2.0)

### INSTRUCTION ROUTINE ###
instruct_txt = """ 
In this experiment, you will see emotional faces (either happy or angry) with a word above the image (either “happy” or “angry”).

you need to respond to the EXPRESSION of the face and ignore the word. You respond with the arrow keys:
    HAPPY expression = left
    ANGRY expression = right
(Press ‘enter’ to start the experiment!)
 """
 
 # Show instructions and wait until response (return)
instruct_txt = TextStim(win, instruct_txt, alignText='left', height=0.085)
instruct_txt.draw()
win.flip()

# Initialize keyboard and wait for response
kb = Keyboard()
while True:
    keys = kb.getKeys()
    if 'return' in keys:
        # The for loop was optional
        for key in keys:
            print(f"The {key.name} key was pressed within {key.rt:.3f} seconds for a total of {key.duration:.3f} seconds.")
        break  # break out of the loop! if return is hit then you can go to the next screen

### TRIAL LOOP ROUTINE ###
# Read in conditions file
cond_df = pd.read_excel('emo_conditions.xlsx')
cond_df = cond_df.sample(frac=1)

# Create fixation target (a plus sign)
fix_target = TextStim(win, '+')
trial_clock = Clock()

# START exp clock
clock.reset()

# Show initial fixation
fix_target.draw()
win.flip()
wait(1)

for idx, row in cond_df.iterrows():
    # Extract current word and smiley
    curr_word = row['word']
    curr_smil = row['smiley']

    # Create and draw text/img
    stim_txt = TextStim(win, curr_word, pos=(0, 0.3))
    stim_img = ImageStim(win, curr_smil + '.png', )
    stim_img.size *= 0.5  # make a bit smaller

    # Initially, onset is undefined
    cond_df.loc[idx, 'onset'] = -1

    trial_clock.reset()
    kb.clock.reset()
    while trial_clock.getTime() < 2:
        # Draw stuff
        
        if trial_clock.getTime() < 0.5:
            stim_txt.draw()
            stim_img.draw()
        else:
            fix_target.draw()
            
        win.flip()
        if cond_df.loc[idx, 'onset'] == -1:
            cond_df.loc[idx, 'onset'] = clock.getTime()
        
        # Get responses
        resp = kb.getKeys()
        if resp:
            # Stop the experiment when 'q' is pressed
            if 'q' in resp:
                quit()

            # Log reaction time and response
            cond_df.loc[idx, 'rt'] = resp[-1].rt
            cond_df.loc[idx, 'resp'] = resp[-1].name

            # Log correct/incorrect
            if resp[-1].name == 'left' and curr_smil == 'happy':
               cond_df.loc[idx, 'correct'] = 1
            elif resp[-1].name ==  'right' and curr_smil == 'angry':
                cond_df.loc[idx, 'correct'] = 1
            else:
                cond_df.loc[idx, 'correct'] = 0

effect = cond_df.groupby('congruence').mean(numeric_only=True)
rt_con = effect.loc['congruent', 'rt']
rt_incon = effect.loc['incongruent', 'rt']
acc = cond_df['correct'].mean()

txt = f"""
Your reaction times are as follows:

    Congruent: {rt_con:.3f}
    Incongruent: {rt_incon:.3f}

Overall accuracy: {acc:.3f}
"""
result = TextStim(win, txt)
result.draw()
win.flip()
wait(5)

prompt = TextStim(
    win,
    text="next please answer two questions about your mood.\n\nPress RETURN to continue",
    wrapWidth=1.5,
    height=0.08,
    alignText='center'
)
prompt.draw()
win.flip()

# wait for the participant to hit RETURN
kb = Keyboard()
kb.clearEvents()
while True:
    keys = kb.getKeys(keyList=['return'], waitRelease=False)
    if keys:
        break

# Ask two mood questions, each on a slider from 1 to 5:

questions = [
    "How happy are you feeling right now?\n(1 = Not at all, 5 = Extremely)",
    "How angry are you feeling right now?\n(1 = Not at all, 5 = Extremely)"
]
ratings = []

for q in questions:
    slider = Slider(
        win, 
        ticks=[1,2,3,4,5], 
        labels=['1','2','3','4','5'], 
        pos=(0, -0.2), 
        size=(1, 0.1), 
        style='rating', 
        granularity=1
    )
    prompt_stim = TextStim(
        win, 
        text=q, 
        pos=(0, 0.2), 
        wrapWidth=1.5, 
        height=0.08,
        alignText='center'
    )

    while slider.getRating() is None:
        prompt_stim.draw()
        slider.draw()
        win.flip()
    ratings.append(slider.getRating())
    wait(0.25)

# face
happy_rating, angry_rating = ratings
if happy_rating >= angry_rating:
    face_img = ImageStim(win, 'happy.png')
else:
    face_img = ImageStim(win, 'angry.png')

# thank‑you
thank_you = TextStim(
    win,
    text="Thank you",
    pos=(0, 0.3),     
    alignText='center',
    height=0.1
)

# face & thank you
face_img.size *= 0.5
face_img.draw()
thank_you.draw()
win.flip()
wait(2.0)

cond_df['participant_nr'] = exp_info['participant_nr']

summary_df = pd.DataFrame({
    'participant_nr': exp_info['participant_nr'],
    'age':            exp_info['age'],
    'happy_rating':   happy_rating,
    'angry_rating':   angry_rating
}, index=[0])

summary_file = 'all_summary.csv'
if not os.path.isfile(summary_file):
    summary_df.to_csv(summary_file, index=False)
else:
    summary_df.to_csv(summary_file, mode='a', header=False, index=False)

trials_file = 'all_trials.csv'
if not os.path.isfile(trials_file):
    cond_df.to_csv(trials_file, index=False)
else:
    cond_df.to_csv(trials_file, mode='a', header=False, index=False)

win.close()
quit()