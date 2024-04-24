from setup import args
import midi

if __name__ == '__main__':
    midiFile = midi.Midi(args.input, args.input_dir)
    