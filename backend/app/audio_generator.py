from kokoro import KPipeline
import soundfile as sf 


pipeline = KPipeline(lang_code='a')

text = "Jacques-Louis David’s *Antoine Laurent Lavoisier and Marie Anne Lavoisier* (1788) is a landmark of Neoclassical portraiture, blending Enlightenment ideals with a hidden narrative of societal upheaval. This painting, once a testament to aristocratic grandeur, transformed into a symbol of scientific progress—a metamorphosis revealed through meticulous restoration. The work encapsulates the tension between wealth and knowledge, revolution and tradition, and the power of art to reframe identity."

generator = pipeline(text=text, voice='bm_george', speed=1)

for i, (gs, ps, audio) in enumerate(generator):
    sf.write(f'{i}.wav', audio, 24000)