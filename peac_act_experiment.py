from psychopy import prefs, visual, event, core, sound, data, gui
import pandas as pd
import random
import itertools

#setting audio device preferences (had some issues with this)
prefs.hardware['audioLib'] = ['PTB']
prefs.hardware['audioDevice'] = ['4'] 

#create stopwatch to monitor reading time
stopwatch = core.Clock()

# Create window for displaying stimuli
win = visual.Window(color = 'black', fullscr = False)

# Function for displaying text. Receives a string and displays it
def dis_txt(text_to_display):
    #Creates message, draws it and flips the window
    mes = visual.TextStim(win,text_to_display,color="white", wrapWidth = 1.5)
    mes.draw(win)
    win.flip()

#Function for playing a sound
def play_sound(note):
    sound_to_play = sound.Sound(f"stimuli/notes/{note}.mp3", sampleRate=44100, stereo=True)
    sound_to_play.play()


### Chord sequences
#0th chord is the out-of-key chord.
#Can be inserted instead of the critical word chord (5th tuple index in sentence)
chord_seqs = [
    ##Experiment sentence chords
    (["a3","e4","a4","c-5"], #out_of_key_chord
    ["c3","c4","g4","e5"],["e3","c4","g4","c5"],["f3","f4","a4","d5"],
    ["c3","g4","c5","e5"],["g3","g4","b4","d5"],["a3","e4","a4","c5"],
    ["f3","f4","a4","c5"],["g3","f4","g4","b4"],["c3","e4","g4","c5"]),

    (["g3","a-3","d-4"], #out_of_key_chord
    ["c3","g3","c4","e4"],["d3","a3","c4","f4"],["c3","e3","c4","g4"],
    ["a3","e3","c4","a4"],["a3","f3","c4","f4"],["g3","b3","e4"],
    ["d3","a3","f4"],["g3","f3","b3","d4"],["c3","e3","g3","c4"]),

    (["c-3","a3","a4","e5"], #out_of_key_chord
    ["c4","e4","g4","c5"],["a3","e4","a4","c5"],["c4","e4","g4","e5"],
    ["f3","c4","a4","f5"],["e3","c4","g4","e5"],["c3","a3","a4","e5"],
    ["d3","a3","f4","d5"],["g3","f4","b3"],["c3","g3","e4","c5"]),

    (["e3","b3","g-4","b4"], #out_of_key_chord
    ["c3","g3","e4","c5"],["b3","g3","f4","d5"],["c3","g3","e4","c5"],
    ["c3","c4","g4","e5"],["f3","a3","a4","c5"],["e3","c4","g4","c5"],
    ["g3","b3","g4","d5"],["g3","d4","f4","b4"],["c3","c4","e4","c5"]),

    (["f3","f4","g-4","c-5"], #out_of_key_chord
    ["c3","c4","e4","g4"],["c3","c4","e4","a4"],["f3","c4","f4","a4"],
    ["e3","c4","g4","c5"],["g3","b3","g4","d5"],["f3","c4","a4","c5"],
    ["e3","c4","g4","c5"],["g3","d4","f4","b4"],["c3","c4","e4","c5"]),
 
    (["b3","f-4","d-5"], #out_of_key_chord
    ["c3","c4","e4","g4"],["e3","c4","g4","c5"],["f3","c4","f4","a4"],
    ["f3","a3","f4","c5"],["c3","g3","e4","e5"],["b3","f4","d5"],
    ["a3","c4","a4","e5"],["g3","d4","f4","b4"],["c3","c4","e4","c5"]),

    (["d-3","d-4","a-4","g5"], #out_of_key_chord
    ["c4","e4","g4","c5"],["b3","d4","g4","d5"],["a3","c4","a4","e5"],
    ["g3","e4","b4","e5"],["f3","d4","a4","f5"],["c3","e4","c5","g5"],
    ["f3","c4","a4","c5"],["e3","g4","c5","e5"],["d3","d4","a4","f5"],
    ["g3","b3","g4","d5"],["c3","c4","g4","c5"]),

    (["d-3","d-4","f-4","b4"], #out_of_key_chord
    ["c3","g3","e4","c5"],["b3","g3","g4","d5"],["c3","c4","g4","e5"],
    ["g3","b3","g4","d5"],["f3","c4","a4","c5"],["e3","c4","g4","c5"], #something wrong
    ["d3","d4","f4","a4"],["g3","d4","f4","g4"],["c3","c4","e4","c5"]),

    (["d-3","g4","a-4","d-5"], #out_of_key_chord
    ["c3","e4","g4","c5"],["c4","e4","g4","c5"],["b3","d4","g4","d5"],
    ["a3","c4","c5","e5"],["g3","d4","b4","g5"],["f3","f4","a4","c5"],
    ["e3","g4","c5","e5"],["d3","f4","a4","f5"],["g3","f4","b4","d5"],["c3","e4","g4","c5"]),

    (["g-3","c4","c5","d-5"], #out_of_key_chord
    ["c3","c4","g4","e5"],["e3","c4","g4","e4"],["d3","d4","a4","f5"],
    ["f3","c4","a4","f5"],["e3","c4","c5","g5"],["f3","d4","b4","g5"],
    ["a3","c4","c5","e5"],["g3","c4","g4","e5"],["g3","b3","f4","d5"],
    ["c3","c4","e4","c5"]),

    (["f3","g-3","f4","c-5"], #out_of_key_chord
    ["c3","g3","e4","c5"],["g3","d4","b4"],["d3","f3","d4","a4"],
    ["g3","d4","b4"],["e3","g3","e4","c5"],["g3","e4","c5"],["f3","a3","f4","c5"],
    ["e3","c4","g4","c5"],["g3","d4","g4","b4"],["g3","b3","f4","d5"],["c3","c4","e4","c5"]),

    (["g-3","c4","d-4","c5"], #out_of_key_chord
    ["c4","e4","g4","c5"],["g3","d3","g4","b4"],["c4","g4","e5"],
    ["f3","c4","a4","f5"],["e3","c4","g4","c5"],["d3","a3","f4","d5"],
    ["g3","b3","f4","d5"],["a3","c4","e4","c5"],["g3","d4","f4","b4"],["c3","e4","g4","c5"]),

## Filler sentences chords
    (["c3","g3","e4","c5"],["a3","b3","e4","c5"],["b3","a3","g4","d5"],
    ["g3","f4","b4"],["c3","g3","e4","c5"]),

    (["c3","c4","e4","g4"], ["e3","c4","g4","c5"],["f3","d4","f4","a4"],
    ["g3","d4","f4","b4"],["c3","c4","e4","c5"]),

    (["c3","c4","g4","e5"], ["f3","c4","a4","f5"],["g3","a-3","g4","d-5"],
    ["g3","b3","f4","d5"],["c3","c4","e4","c5"]),

    (["c3","g3","e4","c5"], ["b3","g3","g4","d5"],["a3","f3","a4","c5"],
    ["g3","f4","b4"],["c3","g3","e4","c5"]),

    (["c4","e4","g4","c5"],["b3","f4","g4","d5"],["a3","e4","a4","c5"],
    ["f3","d4","a4","c5"],["g3","f4","g4","b4"],["c3","e4","g4","c5"]),

    (["c3","g3","e4","c5"],["d3","f3","d4","f5"],["e3","g3","c4","e5"],
    ["f3","a3","f4","d5"],["g3","b3","f4","d5"],["c3","c4","e4","c5"]),

    (["c4","e4","g4","c5"],["a3","f4","a4","c5"],["c4","e4","g4","e5"],
    ["f3","d4","a4","f5"],["g3","f4","b4","d5"],["c3","e4","g4","c5"]),

    (["c3","c4","g4","e5"],["f3","a3","f4","d5"],["a3","c4","e4","c5"],
    ["g3","e4","g4","c5"],["g3","f4","g4","b4"],["c3","e4","g4","c5"]),

    (["c3","g3","e4","c5"],["c3","a3","e4","c5"],["c3","a3","f4","a4"],
    ["d3","f3","f4","a4"],["g3","f4","b4"],["c3","g3","e4","c5"]),

    (["c3","c4","g4","e5"],["d3","f4","a4","d5"],["f3","c4","a4","c5"],
    ["e3","e4","g-4","b4"],["g3","f4","g4","b4"],["c3","c4","g4","c5"]),

    (["c3","c4","g4","e5"],["f3","c4","a4","f5"],["c3","c4","g4","e5"],
    ["d3","a3","f4","d5"],["g3","b3","f4","d5"],["c3","c4","e4","c5"]),

    (["c3","g3","e4","c5"],["e3","g3","e4","c5"],["d3","a3","f4","d5"],
    ["f3","a3","f4","c5"],["g3","f4","b4"],["c3","g3","e4","c5"]),

    (["c3","g3","e4","c5"],["b3","g3","f4","d5"],["c3","g3","e4","e5"],
    ["a3","e4","c5"],["g3","b3","f4","d5"],["c3","c4","e4","c5"]),

    (["c3","c4","g4","e5"],["d3","b3","f4","d5"],["e3","c4","g4","c5"], #this one
    ["f3","f4","a4","c5"],["g3","f4","g4","b4"],["c3","e4","g4","c5"]),

    (["c4","e4","g4","c5"],["g3","b3","f4","d5"],["a3","c4","e4","c5"],
    ["f3","c4","f4","a4"],["g3","b3","f4","a4"],["c3","g3","e4","c5"]),

    (["c3","e3","c4","g4"],["b3","d4","g4"],["a3","e3","c4","e4"],
    ["g3","c4","e4"],["g3","f3","b3","d4"],["c3","e3","g3","c4"]),

    (["c4","e4","g4","c5"],["a3","e4","a4","c5"],["d4","f4","a4","d5"],
    ["f3","f4","a4","c5"],["e3","c4","g4","e5"],["g3","b3","f4","d5"],["c3","c4","e4","c5"]),

    (["c3","e4","c5","g5"],["g3","d4","b4","g5"],["a3","c4","c5","e5"],
    ["f3","c4","a4","f5"],["g3","c4","g4","e5"],["g3","b3","f4","d5"],["c3","c4","e4","c5"]), #skulle være nummer 28

    (["c3","e4","g4","c5"],["b3","d3","g4","d5"],["c3","c4","g4","e5"],
    ["d3","b3","b4","f5"],["e3","c4","g4","e5"],["g3","b3","f4","d5"],["c3","c4","e4","c5"]),

    (["c3","c4","g4","e5"],["e3","c4","g4","g5"],["f3","c4","a4","f5"],
    ["f3","c-4","g-4","e5"],["g3","c4","g4","e5"],["g3","b3","f4","d5"],["c3","c4","e4","c5"]),

    (["c4","e4","g4","c5"],["b3","f4","b4","d5"],["a3","e4","c5","e5"],["f3","a4","c5","f5"],
    ["e3","g4","c5","g5"],["d3","f4","f5","a5"],["g3","f4","d5","b5"],["c3","e4","c5","c6"]),

    (["c3","g3","e4","c5"],["f3","a3","c4","c5"],["e3","g3","c4","c5"],["d3","a3","d4","f5"],
    ["c3","a3","e4","e5"],["b3","g4","d5"],["g3","b3","f4","d5"],["c3","c4","e4","c5"]),

    (["c3","c4","g4","e5"],["d3","b3","f4","d5"],["e3","c4","g4","c5"],["f3","c4","a4","f5"],
    ["g3","b3","g4","d5"],["g-3","c4","d-4","c5"],["g3","d4","f4","b4"],["c3","c4","e4","c5"]),

    (["c3","c4","e4","g4"],["e3","c4","g4","c5"],["g3","c4","c5","e5"],["a3","c4","c5","f5"],
    ["f3","c4","a4","c5"],["d3","f4","a4","d5"],["g3","f4","g4","b4"],["c3","e4","g4","c5"])
]
###Sentences
#Normal sentences
norm_sentences = [
    ["During / the exam, / the nervous student / wrote / hurriedly.",
     "Was the student nervous?",
     1, 5, 0,
     "filler", 1, chord_seqs[12]],

    ["The new waitress / accidentally spilled / coffee / all over / the grouchy customer.",
     "Did the waitress spill coffee?",
     1, 5, 0,
     "filler", 2, chord_seqs[13]],

    ["The students / cheered / when / the class bell / rang.",
     "Did the students cheer before the bell rang?",
     0, 4, 3,
     "filler_out_of_key", 3, chord_seqs[14]],

    ["At the circus, / fifteen clowns / managed / to fit / into a Volkswagen Beetle.",
     "Were there more than 17 clowns?",
     0, 5, 0,
     "filler", 4, chord_seqs[15]],

    ["The farmer / was / concerned / about / the lack / of rain.",
     "Was the farmer concerned about there being too much rain?",
     0, 6, 0,
     "filler", 5, chord_seqs[16]],

    ["As / the parade / passed by / the school, / the kids / cheered.",
     "Did the parade pass by the kindergarten?",
     0, 6, 0,
     "filler", 6, chord_seqs[17]],

    ["While / the guard / watched / the television, / the prisoner / escaped.",
     "Was the guard watching the prisoner?",
     0, 6, 0,
     "filler", 7, chord_seqs[18]],

    ["As / the musician / practiced / the violin, / the baby / cried.",
     "Was the baby happy?",
     0, 6, 0,
     "filler", 8, chord_seqs[19]],

    ["The bored spectators / jeered / when / the quarterback / fumbled / the ball.",
     "Did the spectators enjoy the game?",
     0, 5, 0,
     "filler", 9, chord_seqs[20]],

    ["The guy / was / so hungry, / he ate / three cheeseburgers / and a milkshake.",
     "Did he have more than two cheeseburgers?",
     1, 6, 4,
     "filler_out_of_key", 10, chord_seqs[21]],

    ["The computer / froze / before / the document / was / saved.",
     "Did something happen to the document?",
     1, 6, 0,
     "filler", 11, chord_seqs[22]],

    ["The weather forecast / predicted / rain, / but / it was / a sunny day.",
     "Was the forecast correct?",
     0, 6, 0,
     "filler", 12, chord_seqs[23]],

    ["The baseball manager / turned away / and spat / after / the star player / struck out.",
     "Was the manager angry at the star player?",
     1, 6, 0,
     "filler", 13, chord_seqs[24]],

    ["The jury / debated / for three days / before / returning / a guilty verdict.",
     "Did the jury agree right away?",
     0, 5, 0,
     "filler", 14, chord_seqs[25]],

    ["After / watching / the movie, / the critic / wrote / a negative review.",
     "Did the critic like the movie?",
     0, 6, 0,
     "filler", 15, chord_seqs[26]],

    ["When / the monster / suddenly / appeared, / the audience / shrieked.",
     "Was the audience scared?",
     1, 5, 0,
     "filler", 16, chord_seqs[27]],

    ["While / the dog / chased / the ball, / the boy / talked / to his friends.",
     "Was the dog chasing a bone?",
     0, 7, 0,
     "filler", 17, chord_seqs[28]],

    ["While / at the zoo, / the kid / saw / a bunch / of monkeys / eating bananas.",
     "Did the kid see more than one monkey?",
     1, 7, 0,
     "filler", 18, chord_seqs[29]],

    ["The old man / was / furious / when / the kids / ran / across his lawn.",
     "Does the old man like it when kids run across his lawn?",
     0, 6, 0,
     "filler", 19, chord_seqs[30]],

    ["The motivated student / studied / all night long, / but then / overslept / and missed / the test.",
     "Was the student motivated?",
     1, 7, 4,
     "filler_out_of_key", 20, chord_seqs[31]],

    ["While / the construction worker / fixed / the house, / the family / went / on vacation / to Florida.",
     "Did the family work on the house?",
     0, 8, 0,
     "filler", 21, chord_seqs[32]],

    ["As / the professor / lectured / about / the boring topic, / the students / tried / to stay awake.",
     "Were the students bored?",
     1, 7, 0,
     "filler", 22, chord_seqs[33]],

    ["During / the football game, / my girlfriend / went shopping / and / bought / three pairs / of shoes.",
     "Is the girlfriend interested in football?",
     0, 8, 6,
     "filler_out_of_key", 23, chord_seqs[34]],

    ["After / the party / last weekend, / everyone / felt / terrible / at work / on Monday.",
     "Did they have a party?",
     1, 8, 0,
     "filler", 24, chord_seqs[35]]
]

# Expected syntactic garden path sentences
exsynsen = [
    ["The chef / who wore / the poofy hat / remembered that / the recipe / would / require / using / fresh basil.",
     "Did the chef need fresh basil for the recipe?",
     1, 9, 6,
     "expected_syntactic", 37, chord_seqs[0]],

    ["The scientist / wearing / thick glasses / confirmed that / the hypothesis / was / being / studied / in his lab.",
     "Was the hypothesis ignored by the scientist?",
     0, 9, 6,
     "expected_syntactic", 38, chord_seqs[1]],

    ["At the ceremony, / the director / who was very famous / accepted that / the award / would / go / to his brother / this year.",
     "Did the director accept that the award would go to his brother this year?",
     1, 9, 6,
     "expected_syntactic", 39, chord_seqs[2]],

    ["The fan / of the rock band / heard that / the song / on the website / would / be played / during the concert / next week.",
     "Will the song be played next month instead of next week?",
     0, 9, 6,
     "expected_syntactic", 40, chord_seqs[3]],

    ["After / the trial, / the attorney / advised that / the defendant / was / likely / to commit / more crimes.",
     "Did the attorney advise that the defendant was likely to commit more crimes?",
     1, 9, 6,
     "expected_syntactic", 41, chord_seqs[4]],

    ["The author / with the glasses / wrote that / the novel / about pirates / was / likely / to be / a best-seller.",
     "Is it unlikely that the novel will sell well?",
     0, 9, 6,
     "expected_syntactic", 42, chord_seqs[5]],

    ["During / finals week, / the student / forgot that / the solution / was / in the book / so / worked / on the problem / all night.",
     "Did the student know the solution was in the book?",
     0, 11, 6,
     "expected_syntactic", 43, chord_seqs[6]],

    ["At the end / of the day, / the apprentice / to the carpenter / learned that / the skill / was / quite marketable / in the city.",
     "Was the skill useful in the city?",
     1, 9, 7,
     "expected_syntactic", 44, chord_seqs[7]],

    ["After / Physics class, / the teacher / recalled that / the answer / to the hard question / was / written / in the back / of the book.",
     "Was the answer missing from the book?",
     0, 10, 7,
     "expected_syntactic", 45, chord_seqs[8]],

    ["In the movie, / the superhero / who wore / a flowing cape / promised that / the woman / would / not / get away / with the crime.",
     "Did the superhero promise that the woman would not get away?",
     1, 10, 7,
     "expected_syntactic", 46, chord_seqs[9]],

    ["During / the fourth day / of the trial, / the jury / doubted that / the witness / would / arrive / to testify / against / the defendant.",
     "Was the jury confident the witness would testify?",
     0, 11, 7,
     "expected_syntactic", 47, chord_seqs[10]],

    ["During / his lecture, / the professor / with a long beard / revealed that / the solution / to the difficult problem / was / not correct / and poorly written.",
     "Was the solution incorrect?",
     1, 10, 8,
     "expected_syntactic", 48, chord_seqs[11]]
]

# Unexpected syntactic garden path sentences
uexsynsen = [
    ["The chef / who wore / the poofy hat / remembered / the recipe / would / require / using / fresh basil.",
     "Did the chef need fresh basil for the recipe?",
     1, 9, 6,
     "unexpected_syntactic", 37, chord_seqs[0]],

    ["The scientist / wearing / thick glasses / confirmed / the hypothesis / was / being / studied / in his lab.",
     "Was the hypothesis ignored by the scientist?",
     0, 9, 6,
     "unexpected_syntactic", 38, chord_seqs[1]],

    ["At the ceremony, / the director / who was very famous / accepted / the award / would / go / to his brother / this year.",
     "Did the director accept that the award would go to his brother this year?",
     1, 9, 6,
     "unexpected_syntactic", 39, chord_seqs[2]],

    ["The fan / of the rock band / heard / the song / on the website / would / be played / during the concert / next week.",
     "Will the song be played next month instead of next week?",
     0, 9, 6,
     "unexpected_syntactic", 40, chord_seqs[3]],

    ["After / the trial, / the attorney / advised / the defendant / was / likely / to commit / more crimes.",
     "Did the attorney advise that the defendant was likely to commit more crimes?",
     1, 9, 6,
     "unexpected_syntactic", 41, chord_seqs[4]],

    ["The author / with the glasses / wrote / the novel / about pirates / was / likely / to be / a best-seller.",
     "Is it unlikely that the novel will sell well?",
     0, 9, 6,
     "unexpected_syntactic", 42, chord_seqs[5]],

    ["During / finals week, / the student / forgot / the solution / was / in the book / so / worked / on the problem / all night.",
     "Did the student know the solution was in the book?",
     0, 11, 6,
     "unexpected_syntactic", 43, chord_seqs[6]],

    ["At the end / of the day, / the apprentice / to the carpenter / learned / the skill / was / quite marketable / in the city.",
     "Was the skill useful in the city?",
     1, 9, 7,
     "unexpected_syntactic", 44, chord_seqs[7]],

    ["After / Physics class, / the teacher / recalled / the answer / to the hard question / was / written / in the back / of the book.",
     "Was the answer missing from the book?",
     0, 10, 7,
     "unexpected_syntactic", 45, chord_seqs[8]],

    ["In the movie, / the superhero / who wore / a flowing cape / promised / the woman / would / not / get away / with the crime.",
     "Did the superhero promise that the woman would not get away?",
     1, 10, 7,
     "unexpected_syntactic", 46, chord_seqs[9]],

    ["During / the fourth day / of the trial, / the jury / doubted / the witness / would / arrive / to testify / against / the defendant.",
     "Was the jury confident the witness would testify?",
     0, 11, 7,
     "unexpected_syntactic", 47, chord_seqs[10]],

    ["During / his lecture, / the professor / with a long beard / revealed / the solution / to the difficult problem / was / not correct / and poorly written.",
     "Was the solution incorrect?",
     1, 10, 8,
     "unexpected_syntactic", 48, chord_seqs[11]]
]
# Expected semantic garden path sentences
exsemsen = [
    ["The / doctor / examined / the blind mole / before it / burrowed / away / into / the soil",
     "Did the mole hide in the soil?",
     1, 9, 6,
     "expected_semantic", 25, chord_seqs[0]],

    ["The / baseball player / reached for / the hairy bat / before / it fluttered / out / of / sight",
     "Was the bat alive?",
     1, 9, 6,
     "expected_semantic", 26, chord_seqs[1]],

    ["The / student / examined / the data table / before noticing / a missing column / in / the / report",
     "Was there nothing missing in the report?",
     0, 9, 6,
     "expected_semantic", 27, chord_seqs[2]],

    ["The / gymnast / checked her / bank balance / by using her / phone / and / opening her / bank app",
     "Did she check her physical balance?",
     0, 9, 6,
     "expected_semantic", 28, chord_seqs[3]],

    ["The / athlete / threw / the masquerade ball / in order to / celebrate / his marriage / with  / loved ones",
     "Did the athlete organize a party to celebrate his marriage?",
     1, 9, 6,
     "expected_semantic", 29, chord_seqs[4]],

    ["The / old man / went to / the river bank / to withdraw his / net / which / was / empty",
     "Did the old man go to withdraw money?",
     0, 9, 6,
     "expected_semantic", 30, chord_seqs[5]],

    ["The / friends / went to / the wooden club / in order to / throw it out / with / the / other / wooden / waste",
     "Did the friends go to a social club?",
     0, 11, 6,
     "expected_semantic", 31, chord_seqs[6]],

    ["The carpenter / had strong hands / and a / big wooden chest, / which / he used / to store / family / heirlooms",
     "Did the carpenter use the chest to store something important?",
     1, 9, 7,
     "expected_semantic", 32, chord_seqs[7]],

    ["The / young woman / enjoyed / the traffic jam, / as sitting / in her / car / gave her / time / to relax",
     "Did the woman enjoy being stuck in traffic?",
     1, 10, 7,
     "expected_semantic", 33, chord_seqs[8]],

    ["The / grooms brother / fit in / one last / grilled toast / in his / mouth, / winning / the / eating contest",
     "Did the grooms brother hold a speech?",
     0, 10, 7,
     "expected_semantic", 34, chord_seqs[9]],

    ["The / surgeon / noticed / that / the pipe organ / had a great / timbre / as / the organist / played / it",
     "Was the organ a musical instrument?",
     1, 11, 7,
     "expected_semantic", 35, chord_seqs[10]],

    ["The / street / cleaner / picked up / the kitty litter / in / order to / adopt them / with / his wife",
     "Did the street cleaner adopt some pets?",
     1, 10, 8,
     "expected_semantic", 36, chord_seqs[11]]
]
# Unexpected semantic garden path sentences
uexsemsen = [
    ["The / doctor / examined / the mole / before it / burrowed / away / into / the soil",
     "Did the mole hide in the soil?",
     1, 9, 6,
     "unexpected_semantic", 25, chord_seqs[0]],

    ["The / baseball player / reached for / the bat / before / it fluttered / out / of / sight",
     "Was the bat alive?",
     1, 9, 6,
     "unexpected_semantic", 26, chord_seqs[1]],

    ["The / student / examined / the table / before noticing / a missing column / in / the / report",
     "Was there nothing missing in the report?",
     0, 9, 6,
     "unexpected_semantic", 27, chord_seqs[2]],

    ["The / gymnast / checked her / balance / by using her / phone / and / opening her / bank app",
     "Did she check her physical balance?",
     0, 9, 6,
     "unexpected_semantic", 28, chord_seqs[3]],

    ["The / athlete / threw / the ball / in order to / celebrate / his marriage / with  / loved ones",
     "Did the athlete organize a party to celebrate his marriage?",
     1, 9, 6,
     "unexpected_semantic", 29, chord_seqs[4]],

    ["The / old man / went to / the bank / to withdraw his / net / which / was / empty",
     "Did the old man go to withdraw money?",
     0, 9, 6,
     "unexpected_semantic", 30, chord_seqs[5]],

    ["The / friends / went to / the club / in order to / throw it out / with / the / other / wooden / waste",
     "Did the friends go to a social club??",
     0, 11, 6,
     "unexpected_semantic", 31, chord_seqs[6]],

    ["The carpenter / had strong hands / and a / big chest, / which / he used / to store / family / heirlooms",
     "Did the carpenter use the chest to store something important?",
     1, 9, 7,
     "unexpected_semantic", 32, chord_seqs[7]],

    ["The / young woman / enjoyed / the jam, / as sitting / in her / car / gave her / time / to relax",
     "Did the woman enjoy being stuck in traffic?",
     1, 10, 7,
     "unexpected_semantic", 33, chord_seqs[8]],

    ["The / grooms brother / fit in / one last / toast / in his / mouth, / winning / the / eating contest",
     "Did the grooms brother hold a speech?",
     0, 10, 7,
     "unexpected_semantic", 34, chord_seqs[9]],

    ["The / surgeon / noticed / that / the organ / had a great / timbre / as / the organist / played / it",
     "Was the organ a musical instrument?",
     1, 11, 7,
     "unexpected_semantic", 35, chord_seqs[10]],

    ["The / street / cleaner / picked up / the litter / in / order to / adopt them / with / his wife",
     "Did the street cleaner adopt some pets?",
     1, 10, 8,
     "unexpected_semantic", 36, chord_seqs[11]]
]


#Lists of sentences
senlists = [0] * 4
senlists[0] = norm_sentences + exsynsen[0:6] + uexsynsen[6:12] + exsemsen[0:6] + uexsemsen[6:12]
senlists[1] = norm_sentences + exsynsen[0:6] + uexsynsen[6:12] + exsemsen[6:12] + uexsemsen[0:6]
senlists[2] = norm_sentences + exsynsen[6:12] + uexsynsen[0:6] + exsemsen[0:6] + uexsemsen[6:12]
senlists[3] = norm_sentences + exsynsen[6:12] + uexsynsen[0:6] + exsemsen[6:12] + uexsemsen[0:6]

#Creating key counterbalancing lists
#Creates a list of all permutations of 3 0s and 3 1s.
cbalance_lists = sorted({tuple(p) for p in itertools.permutations([0,0,0,1,1,1])}
)

#Experiment loop

#Dialogue box with music experience and condition
dialog_box = gui.Dlg(title="Assignment 03 experiment")
dialog_box.addField("Music experience (years):", label="Music experience (years):")
dialog_box.addField("Condition:", label="Condition:", choices=[0,1,2,3])
if dialog_box.show(): # To retrieve data from dialog box
    music_experience = dialog_box.data["Music experience (years):"]
    condition = dialog_box.data["Condition:"]
if not dialog_box.OK:
    print("User cancelled the experiment.")
    core.quit() # Exits the entire PsychoPy application

#choose lists and assign random participant id
chosen_list = senlists[condition]
chosen_cb_list = random.choice(cbalance_lists) + random.choice(cbalance_lists) + random.choice(cbalance_lists) + random.choice(cbalance_lists)
partid = random.randint(0,100000)

#add counterbalanced chord conditions to sentences
for c in range(len(chosen_list)):
    if chosen_list[c][5] == "filler":
        chosen_list[c].append(1)
    elif chosen_list[c][5] == "filler_out_of_key":
        chosen_list[c].append(0)
    else:
        chosen_list[c].append(chosen_cb_list)

#shuffle order of sentences
random.shuffle(chosen_list)

#Welcome text
dis_txt("Welcome and thank you for participating in my study. The purpose of this study is to examine reading comprehension. In this experiment, you will read sentences while listening to chord sequences. After each sentence, you will be asked a comprehension question, so please read carefully! The chords are not important. Press space to continue to the terms of the experiment")
event.waitKeys(keyList=["space"])

#Terms and consent
dis_txt("This study is ran by Viktor Nielsen, 3rd semester bachelor student at Cognitive Science at Aarhus University. To continue participation, you must consent to me recording your data from the experiment. I don't collect any personal data apart from years of musical experience, so your data is completely anonymized. You will be assigned a unique random ID, which neither of us will know. This also means that you won't be able to withdraw consent for me to use your data after the experiment. To consent to these terms and continue the experiment, please press space")
event.waitKeys(keyList=["space"])

#Experiment description
dis_txt("During the experiment, you'll be presented with a part of a sentence at a time, not the full sentence. Once you've read one sequence, you can press space to continue to the next. After the last sequence of the sentence, you'll be presented with a yes/no question which you should answer to the best of your ability. You can answer yes by pressing y on the keyboard and no by pressing n on the keyboard. Before continuing, you'll have one trial sentence and comprehension question to read and answer in order to get a feel for the experiment. ")
event.waitKeys(keyList=["space"])

#trial run
trial_sentence = "The / family van / had / trouble / starting / as it / was / very cold / outside"
trial_wlist = trial_sentence.split("/")
trial_chords = chord_seqs[0]
for i in range(len(trial_wlist)):
    dis_txt(trial_wlist[i])
    trial_chord = trial_chords[i+1]
    for chord_tone in trial_chord:
            play_sound(chord_tone)
    event.waitKeys(keyList = ["space"])

#trial question
dis_txt("Could the family not start the van because of the heat?")
trial_answer_key = event.waitKeys(keyList = ["y","n"])
if trial_answer_key[0] == "escape":
    core.quit()
if trial_answer_key == ['n']:
    dis_txt("Correct! You're ready for the experiment! Press space to receive your first real sentence")
else:
    dis_txt("Wrong answer. I'm sure you've got the gist of it though ;). Press space to receive your first real sentence")
event.waitKeys(keyList = ["space"])


#instantiate lists for saving data
reading_time = [None]
reading_time.pop(0)
participant_id = [None]
participant_id.pop(0)
wordlength = [None]
wordlength.pop(0)
segment_category = [None]
segment_category.pop(0)
correct = [None]
correct.pop(0)
sentence_type = [None]
sentence_type.pop(0)
chord_key = [None]
chord_key.pop(0)
sentence_number = [None]
sentence_number.pop(0)
mus_experience = [None]
mus_experience.pop(0)

#loops over sentences and splits sentences into sequences. One loop is one sentence
for i in range(len(chosen_list)):
    sentence = chosen_list[i]
    wlist = sentence[0].split("/")
    chords = sentence[7]
    if sentence[8] == 0:
        key_cond = "out_of_key"
    else:
        key_cond = "in_key"
    
    #loops over sequences in a sentence, displays one sequence and plays the matching chord
    for j in range(len(wlist)): 
        #Plays the out-of-key chord at the critical point if a sentence has been assigned to be out_of_key
        if j == sentence[4] and key_cond == "out_of_key" and "filler" not in sentence[5]:
            chord = chords[0]
        elif "filler" in sentence[5]:
            chord = chords[j]
        else:
            chord = chords[j+1]
                
        #loops over chord tones and makes sure they're played at the same time
        for chord_tone in chord:
            play_sound(chord_tone)
        
        #display text and check time
        dis_txt(wlist[j])
        stopwatch.reset()
        continue_key = event.waitKeys(keyList=["space", "escape"])
        if continue_key[0] == "escape":
            core.quit()
            
        #assign segment category for each segment
        if j == sentence[4]-2:
            segment_category.append("pre_critical") 
        elif j == sentence[4]-1:
            segment_category.append("critical")
        elif j == sentence[4]:
            segment_category.append("post_critical")
        else:
            segment_category.append("non_critical")
        
        
        #Saving data in rows by sequence
        participant_id.append(partid)
        reading_time.append(stopwatch.getTime())
        wordlength.append(len(wlist[j]))
        sentence_type.append(sentence[5])
        sentence_number.append(sentence[6])
        chord_key.append(key_cond)
        mus_experience.append(music_experience)
    
    dis_txt(chosen_list[i][1])
    answer_key = event.waitKeys(keyList=["y","n", "escape"])
    
    answer = chosen_list[i][2]
    if answer_key[0] == "escape":
        core.quit()
    if answer_key == ['y'] and answer == 1 or answer_key == ['n'] and answer == 0:
        correct.extend([1]*len(wlist))
        dis_txt("Correct! Press space to begin reading the next sentence")
    else:
        correct.extend([0]*len(wlist))
        dis_txt("Wrong answer. Press space to begin reading the next sentence")
    if i < 47:
        event.waitKeys(keyList = ["space"])

#end of experiment
dis_txt("The experiment is over. Thank you so much for participating!")
event.waitKeys(keyList = ["space"])

#Saving data
df = pd.DataFrame({
"participant_id": participant_id, #to take consider individual impact on data
"reading_time": reading_time, #reading time of each segment - our dependent variable
"correct" : correct, #whether a participant answered the comprehension question correctly - our second depdendent variable
"characters": wordlength, #length of each segment - might impact reading time!
"segment_category": segment_category, #Whether a segment was critical or pre/post critical
"sentence_number": sentence_number, #The number of the sentence - allows us to id and compare time across sentences
"sentence_type": sentence_type, #The type of sentence - allows us to compare the different sentence types
"music_condition": chord_key, # Whether the chord sequence had a syntactically wrong chord at the critical segment
"music_experience": mus_experience
})

date = data.getDateStr()

logfile_name = "data/peac_logfile_{}_{}.csv".format(partid,date)
df.to_csv(logfile_name, index = False)


