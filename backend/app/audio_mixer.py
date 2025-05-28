from pydub import AudioSegment
import os
import json

#sound1 = AudioSegment.from_file("1+0.wav", format="wav")
sound2 = AudioSegment.from_file("victorian-waltz.mp3", format="mp3")

#combined = (sound2[:3000] - 10) + ( sound2[3000:4000] - 15) + [sound1 + 8][0].overlay(sound2[4000:]-15, position=0)

#combined.export("output.wav", format="wav")
soundX = sound2[1:2] - 15

for file in os.listdir("./static/")[0:1]:
    path = os.path.join(f"./static/{file}")
    for i in range(1,6):
        temp = [f'./static/{file}/{wav}' for wav in os.listdir(path) if f'{i}+' in wav]
        if(i == 1):
            soundX = (sound2[:3000] - 10) + ( sound2[3000:4000] - 15)
        else:
            soundX = sound2[1:2] - 15
        for j in temp:
            soundX = soundX + AudioSegment.from_file(j, format="wav")

        soundX = [soundX + 8][0].overlay(sound2[4000:]-18, position=0)
        soundX.export(f'./static/{file}/{i}.wav', format="wav")
    

        