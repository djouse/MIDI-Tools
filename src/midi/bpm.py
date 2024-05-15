import time
import pypianoroll
import numpy as np
import mido
import pretty_midi
import IPython.display
from midi2audio import FluidSynth

class Bpm:
    def __init__(self, bpm):
        self.space_between_beats = 0.5
        self.last_press = time.time()
        self.bpm = bpm
        self.times = []
        self._last_update = time.time()
        self._elapsed_time = 0.0
        self._last_closeness = 1.0
        self.on_beat = 0
        self.beat_num = 0
        self.finished_beat = 0
        self.first_beat = 0
        self.started_beat = 0
    
    def setBpm(self, bpm):
        self.bpm=bpm

    def update(self):
        the_time = time.time()
        self._elapsed_time += the_time - self._last_update
        self._last_update = the_time

        space_between_beats = 60.0 / self.bpm
        since_last_beat = the_time - self.on_beat

        self.finished_beat = self.on_beat and (since_last_beat > 0.1)
        if self.finished_beat:
            self.on_beat = 0

        closeness = self._elapsed_time % space_between_beats
        if closeness < self._last_closeness:
            self.on_beat = the_time
            self.finished_beat = 0
            self.beat_num += 1
            self.started_beat = 1
            self.first_beat = not (self.beat_num % 4)
        else:
            self.started_beat = 0

        self._last_closeness = closeness
    
    def bpmToMidiTrack(self, multitrack=None):
        size = 10240
        resolution = 24 #Time steps per quarter note
        bpm = self.bpm
        #time_step_length = 60.0 / tempo / resolution 
        tempo =  mido.bpm2tempo(bpm)/1000
        print(tempo)
        #print(time_step_length)
        track = pypianoroll.StandardTrack(name = "drums", program=0 , is_drum=True, pianoroll=np.zeros([3984, 128]))
        #for i in size:
        track.pianoroll[0:int(tempo):size-1, :] = 85
        multitrack = pypianoroll.Multitrack(tracks=[track])
        return multitrack
    

pm = pretty_midi.PrettyMIDI("input/input.mid")
end_time = pm.get_end_time()
print(end_time)

cello_c_chord = pretty_midi.PrettyMIDI()
# Create an Instrument instance for a cello instrument
cello_program = pretty_midi.instrument_name_to_program('Cello')
cello = pretty_midi.Instrument(program=cello_program)
# Iterate over note names, which will be converted to note number later
for note_name in ['C5', 'E5', 'G5']:
    # Retrieve the MIDI note number for this note name
    note_number = pretty_midi.note_name_to_number(note_name)
    # Create a Note instance for this note, starting at 0s and ending at .5s
    note = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=.5)
    # Add it to our cello instrument
    cello.notes.append(note)
# Add the cello instrument to the PrettyMIDI object
cello_c_chord.instruments.append(cello)
# Write out the MIDI data
cello_c_chord.write('cello-C-chord.mid')

fs = FluidSynth()
fs.play_midi('cello-C-chord.mid')
metronome = pretty_midi.PrettyMIDI()
# Create an Instrument instance for a cello instrument
note = pretty_midi.drum_name_to_note_number('Closed Hi Hat')
print(note)


drum = pretty_midi.Instrument(program=0, is_drum=True, name='Drums')
# Iterate over note names, which will be converted to note number later
# Retrieve the MIDI note number for this note name
# Create a Note instance for this note, starting at 0s and ending at .5s

current_t=0.0
t_shot = 60.0/120.0
time_array = np.arange(current_t,3.0,t_shot)
print(time_array)
notes = []

#for t in time_array:
t=2
pretty_midi.Note(velocity=100, pitch=note, start=t, end=(t+0.5))

# Add it to our cello instrument
print(notes)
drum.notes.append(pretty_midi.Note(velocity=100, pitch=note, start=t, end=(t+0.5)))
metronome.instruments.append(pretty_midi.Instrument(drum))

# Write out the MIDI data
metronome.write('cello-C-chord.mid')

#pp = pypianoroll.from_pretty_midi(pretty_midi.PrettyMIDI("input/input.mid"))
#print(pp)

bpm = Bpm(120)
track = bpm.bpmToMidiTrack()
#midi = pypianoroll.to_pretty_midi(track)
#midi.write("midi_metronome.mid")
fs = FluidSynth()
fs.play_midi('cello-C-chord.mid')
