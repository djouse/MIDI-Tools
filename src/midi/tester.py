
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import numpy as np
import pretty_midi


def get_tempo_events(mid):
    """Retrieve tempo change events from the MIDI file."""
    tempo_events = []
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo_events.append(msg)
    return tempo_events

def predict_bpm(mid, track_index):
    """Predict the BPM of a track by analyzing note-on events."""
    track = mid.tracks[track_index]
    note_on_times = []
    current_time = 0

    for msg in track:
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            note_on_times.append(current_time)
    
    if len(note_on_times) < 2:
        raise ValueError("Not enough note-on events to predict BPM.")
    
    # Calculate time differences between successive note-on events
    time_diffs = np.diff(note_on_times)
    avg_time_diff = np.mean(time_diffs)
    
    # Calculate BPM: avg_time_diff is in ticks, convert it to seconds per beat
    ticks_per_beat = mid.ticks_per_beat
    seconds_per_beat = avg_time_diff / ticks_per_beat
    bpm = 60 / seconds_per_beat
    
    return bpm

def adjust_tempo(mid, desired_tempo):
    """Stretch the MIDI file events to match the desired tempo."""
    # Get the first tempo event's tempo for simplicity
    tempo_events = get_tempo_events(mid)
    print(tempo_events)
    if not tempo_events:
        raise ValueError("No tempo events found in the MIDI file.")

    current_tempo = tempo_events[0].tempo  # Get the first tempo event's tempo
    stretch_factor = current_tempo / desired_tempo 

    new_mid = MidiFile()
    for track in mid.tracks:
        new_track = MidiTrack()
        new_mid.tracks.append(new_track)
        for msg in track:
            # Adjust the timing of all messages
            new_time = int(msg.time * stretch_factor)
            new_msg = msg.copy(time=new_time)
            new_track.append(new_msg)

            new_track.append(new_msg)

    return new_mid


# Load the MIDI file
input_filename = 'input/input.mid'
output_filename = 'input/output.mid'

# Read the MIDI file
mid = MidiFile(input_filename)

# Predict the BPM from the audio file
midi_data = pretty_midi.PrettyMIDI(input_filename)
predicted_bpm = midi_data.estimate_tempo()

# Convert predicted BPM to microseconds per beat
desired_tempo = mido.bpm2tempo(120)
print(desired_tempo)

# Adjust the tempo and add metronome track
new_mid = adjust_tempo(mid, desired_tempo)
new_mid.save(output_filename)
#new_mid_with_metronome = add_metronome_track(new_mid, predicted_bpm)

# Save the modified MIDI file
#new_mid_with_metronome.save(output_filename)

print(f"Saved adjusted MIDI file with metronome as {output_filename}")


