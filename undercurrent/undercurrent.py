import cairo
import copy
import random
import numpy as np
import librosa as lr

# setting the drawing canvas ###########################################################################################
SIDE_LENGTH = 4000  # parameter
a = 60
b = 12000
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, SIDE_LENGTH, SIDE_LENGTH)
ctx = cairo.Context(surface)
ctx.scale(1, 1)
ctx.rectangle(0, 0, SIDE_LENGTH, SIDE_LENGTH)
ctx.set_source_rgb(0, 0, 0)
ctx.fill()


# setting the drawing canvas ###########################################################################################
def polar_to_cartesian(_r, _theta):
    _x = _r * np.cos(_theta) + SIDE_LENGTH / 2
    _y = _r * np.sin(_theta) + SIDE_LENGTH / 2
    return _x, _y


audio, sRate = lr.load("undercurrent.wav")
audioLen = len(audio)
corrAudioLen = audioLen-audioLen % (a*b)
audioStep = corrAudioLen//(a*b)
roundStep = audioStep*b
vibrAmplitude = SIDE_LENGTH//40
reversedAudio = copy.copy(audio[:corrAudioLen])
reversedAudio = reversedAudio[::-1]

# initialising
r = SIDE_LENGTH // 2
theta = -np.pi / 2
x, y = polar_to_cartesian(r, theta)
ctx.move_to(x, y)

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
        dice = .8+.2*random.random()
        ctx.set_source_rgb(dice, dice, 0)
        ctx.set_line_width(4)
        ctx.stroke()

        # initialising
        r -= SIDE_LENGTH // 3 // a
        theta = -np.pi / 2
        x, y = polar_to_cartesian(r, theta)
        ctx.move_to(x, y)
    else:
        theta -= 2 * np.pi / roundStep * audioStep

print("progress:", corrAudioLen, "/", corrAudioLen, "done!")

surface.write_to_png('output_img.png')
