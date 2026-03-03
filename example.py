import soundfile as sf

from kittentts import KittenTTS

# it will run blazing fast on any GPU. But this example will run on CPU.

# Step 1: Load the model
# m = KittenTTS("KittenML/kitten-tts-mini-0.8") # 80M version (highest quality)
m = KittenTTS("KittenML/kitten-tts-micro-0.8") # 40M version (balances speed and quality )
# m = KittenTTS("KittenML/kitten-tts-nano-0.8") # 15M version (tiny and faster )


# Step 2: Generate the audio 

# this is a sample from the TinyStories dataset. 
text = "Kittens run and jump. They meow and purr. Happy little cats play."


# available_voices : ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo']
voice = 'Rosie'



audio = m.generate(text=text, voice=voice )

# Save the audio
sf.write('output.wav', audio, 24000)
print("Audio saved to output.wav")