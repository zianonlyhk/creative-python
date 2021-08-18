import cairo
import copy
import random
import numpy as np
import librosa as lr


# INTERFACE ###########################################################################################
SIDE_LENGTH = 4000  # number of pixcel of the output image side
numRounds = 60  # number of loop rounds, i.e. No. of layers
numStepsInRound = 12000  # number of array elements in a loop round
# change the audio file name here:
audio, sRate = lr.load("undercurrent.wav")
# INTERFACE ###########################################################################################


# setting the drawing canvas
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, SIDE_LENGTH, SIDE_LENGTH)
ctx = cairo.Context(surface)
ctx.scale(1, 1)
ctx.rectangle(0, 0, SIDE_LENGTH, SIDE_LENGTH)
ctx.set_source_rgb(0, 0, 0)
ctx.fill()


def polar_to_cartesian(_r, _theta):
    _x = _r * np.cos(_theta) + SIDE_LENGTH / 2
    _y = _r * np.sin(_theta) + SIDE_LENGTH / 2
    return _x, _y


# loading audio and creating arrays
audioLen = len(audio)
corrAudioLen = audioLen-audioLen % (numRounds*numStepsInRound)
audioStep = corrAudioLen//(numRounds*numStepsInRound)
roundStep = audioStep*numStepsInRound
vibrAmplitude = SIDE_LENGTH//40
reversedAudio = copy.copy(audio[:corrAudioLen])
reversedAudio = reversedAudio[::-1]

# initialising drawing position
r = SIDE_LENGTH // 2
theta = -np.pi / 2
x, y = polar_to_cartesian(r, theta)
ctx.move_to(x, y)

tubeDepth = 0
for i in range(0, corrAudioLen, audioStep):
    print("progress:", i, "/", corrAudioLen)
    x, y = polar_to_cartesian(r + vibrAmplitude * (reversedAudio[i]), theta)
    try:
        if vibrAmplitude * abs(reversedAudio[i] - reversedAudio[i - audioStep]) < 1:
            ctx.line_to(x, y)
    except IndexError:
        pass
    if (i + audioStep) % roundStep == 0:
        ctx.close_path()
        ctx.set_source_rgb(0, 0, 0)
        ctx.fill_preserve()
        dice = 1 - .4*tubeDepth - .1*random.random()
        ctx.set_source_rgb(dice, dice, 0)
        ctx.set_line_width(4)
        ctx.stroke()
        tubeDepth += 1/numRounds

        # initialising drawing position
        r -= SIDE_LENGTH // 3 // numRounds
        theta = -np.pi / 2
        x, y = polar_to_cartesian(r, theta)
        ctx.move_to(x, y)
    else:
        theta -= 2 * np.pi / roundStep * audioStep

print("progress:", corrAudioLen, "/", corrAudioLen, "done!")

surface.write_to_png('output_img.png')
