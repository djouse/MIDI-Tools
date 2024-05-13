import os
import pypianoroll
import matplotlib.pyplot as plt
import numpy as np
import pretty_midi

dir_path = os.path.dirname(os.path.realpath(__file__))
input_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input_midi")
output_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output_midi")

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
        self.LENGTH     = self.midi.tempo.shape[0]
        self.BEAT_SIZE  = self.midi.resolution
        self.N_BEATS    = self.midi.tempo.shape[0] // self.midi.resolution

        #time_step_length = 60.0 / tempo / self.midi.resolution
        
    def plotter(self):
        for i, track in enumerate(self.midi.tracks):
            aux = track
            aux.trim(0, 12 * self.midi.resolution)
            fig, ax = plt.subplots()
            pypianoroll.plot_pianoroll(ax, aux.pianoroll, aux.is_drum, resolution=self.midi.resolution)
            fig.savefig(f'{dir_path}/track_plots/track_{i}.png')
        return
    def getNumberOfTracks(self):
        return len(self.midi.tracks)
    def getSizeOfTracks(self):
        return max(len(track.pianoroll) for track in self.midi.tracks)
    
    def setDownbeatSteps(self, bpm):
        return 
    def getDownbeatSteps(self):
        return self.midi.get_downbeat_steps()
    def setTempo(self, bpm=None):
        if not bpm:
            pretty_midi.PrettyMIDI(os.path.join(self.input_path, self.input))
            tempo=midi_data.estimate_tempo()
            bpm = tempo
        tempo = np.empty([self.LENGTH,1]).astype(np.float64)
        tempo.fill(bpm)
        print(tempo)
        self.midi.tempo = tempo
    def saveVersion(self):
        path = os.path.join(output_dir_path, "output.mid")
        midi_data = self.midi.to_pretty_midi()
        midi_data.write(path)
    
midi = Midi("input.mid", "input")
print(midi.midi.tempo)
midi_data = pretty_midi.PrettyMIDI('input/input.mid')
tempo=midi_data.estimate_tempo()
print(tempo)
print(midi_data.get_tempo_changes())
end_time=midi_data.get_end_time()
beats_time = midi_data.get_beats()
beats_tick = []
for b in beats_time:
    tick = midi_data.time_to_tick(b)
    beats_tick.append(tick)

print(beats_time)
print(beats_tick)

print(end_time)
midi.setTempo(tempo)
midi.saveVersion()
