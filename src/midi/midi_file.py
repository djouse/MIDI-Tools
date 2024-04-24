import os
import pypianoroll
import matplotlib.pyplot as plt
import mido

class Midi():
    def __init__(self, input_midi, dir):
        self.input = input_midi
        self.input_path = os.path.abspath(dir)
        self.midi = pypianoroll.read(os.path.join(self.input_path, self.input))

        self.DRUMS      = self.midi.tracks[0]
        self.PIANO      = self.midi.tracks[1]
        self.GUITAR     = self.midi.tracks[2]
        self.BASS       = self.midi.tracks[3]
        self.STRINGS    = self.midi.tracks[4]

        self.midi.binarize()
        for i, track in enumerate(self.midi.tracks):
            aux = track
            aux.trim(0, 12 * self.midi.resolution)
            fig, ax = plt.subplots()
            pypianoroll.plot_pianoroll(ax, aux.pianoroll, aux.is_drum, resolution=self.midi.resolution)
            fig.savefig(f'track_plots/track_{i}.png')
        
    
    def getNumberOfTracks(self):
        return len(self.midi.tracks)
    def getSizeOfTracks(self):
        return max(len(track.pianoroll) for track in self.midi.tracks)
    def getDownbeatSteps(self):
        return self.midi.get_downbeat_steps()
    

    

    
    
midi = Midi("input.mid", "../../input")
print(midi.getNumberOfTracks())
print(midi.getSizeOfTracks())
print(midi.getDownbeatSteps())


