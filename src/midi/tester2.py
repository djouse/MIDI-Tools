import pretty_midi

midi_path = 'input/input.mid'
tempo = 130
midi_obj = pretty_midi.PrettyMIDI(midi_path)
# convert tempo
midi_length = midi_obj.get_end_time()
midi_obj.adjust_times([0, midi_length], [0, midi_length*161/120])
processed_mid = midi_path[:-4] + "_processed.mid"
midi_obj.write(processed_mid)

midi_obj = pretty_midi.PrettyMIDI('input/input_processed.mid')
print(midi_obj.get_downbeats())

