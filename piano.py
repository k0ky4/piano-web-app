import json
import os
from abc import abstractmethod
from enum import Enum
import fingers


class Piano:
    def __init__(self):
        self.NONE_KEY = 88
        self.piano_keys = [
            PianoKey("A0", 0, self),
            PianoKey("A#0", 1, self),
            PianoKey("B0", 2, self)
            ]
        semitones = 3
        for octave in range(1, 8):
            self.piano_keys.append(PianoKey(f"C{octave}", semitones, self))
            self.piano_keys.append(PianoKey(f"C#{octave}", semitones + 1, self))
            self.piano_keys.append(PianoKey(f"D{octave}", semitones + 2, self))
            self.piano_keys.append(PianoKey(f"D#{octave}", semitones + 3, self))
            self.piano_keys.append(PianoKey(f"E{octave}", semitones + 4, self))
            self.piano_keys.append(PianoKey(f"F{octave}", semitones + 5, self))
            self.piano_keys.append(PianoKey(f"F#{octave}", semitones + 6, self))
            self.piano_keys.append(PianoKey(f"G{octave}", semitones + 7, self))
            self.piano_keys.append(PianoKey(f"G#{octave}", semitones + 8, self))
            self.piano_keys.append(PianoKey(f"A{octave}", semitones + 9, self))
            self.piano_keys.append(PianoKey(f"A#{octave}", semitones + 10, self))
            self.piano_keys.append(PianoKey(f"B{octave}", semitones + 11, self))
            semitones += 12
        self.piano_keys.append(PianoKey("C8", semitones, self))

        self.piano_keys.append(PianoKey("NONE_KEY", 88, self))

    def __getitem__(self, index):
        if isinstance(index, int):
            if not 0 <= index <= self.NONE_KEY:
                index = self.NONE_KEY
            return self.piano_keys[index]
        else:
            for key in self.piano_keys:
                if key.name == index:
                    return key
            
            return self.piano_keys[self.NONE_KEY]
            # raise IndexError("There's no such key!")

    # __iter__ ? for piano_key in piano is not used


class PianoKey:
    def __str__(self):
        return f"key: {self.name}, semitones from A0: {self.semitones}"
    
    def __init__(self, name: str, semitones: int, piano: Piano):
        self.name = name
        self.semitones = semitones
        self.piano = piano
    
    def __add__(self, step: int):
        return self.piano[self.semitones + step]
    
    def __radd__(self, step: int):
        return self + step
    
    def __sub__(self, step: int):
        return self + (-step)


class Interval(Enum):
    UNISON = 0
    MINOR_SECOND = 1
    MAJOR_SECOND = 2
    MINOR_THIRD = 3
    MAJOR_THIRD = 4
    PERFECT_FOURTH = 5
    AUGMENTED_FOURTH = 6
    DIMINISHED_FIFTH = 6
    PERFECT_FIFTH = 7
    MINOR_SIXTH = 8
    MAJOR_SIXTH = 9
    MINOR_SEVENTH = 10
    MAJOR_SEVENTH = 11
    OCTAVE = 12
    MINOR_NINTH = 13
    MAJOR_NINTH = 14
    MINOR_TENTH = 15
    MAJOR_TENTH = 16
    PERFECT_ELEVENTH = 17
    AUGMENTED_ELEVENTH = 18
    DIMINISHED_TWELFTH = 18
    PERFECT_TWELFTH = 19
    MINOR_THIRTEENTH = 20
    MAJOR_THIRTEENTH = 21
    MINOR_FOURTEENTH = 22
    MAJOR_FOURTEENTH = 23
    PERFECT_FIFTEENTH = 24


class Scale:
    def __init__(self, scale_name: str):
        self.steps_up, self.steps_down = get_scale_steps(scale_name)


class Arpeggio:
    def __init__(self, harmony, subharmony):
        # minor
        # major
        # minor broken
        # major broken
        # minor long
        # major long
        # each of 11
        # all 11 together
        # ???
        pass


class Chord:
    def __init__(self, chord_name):
        # list[list[str]]
        self.inversions = get_chord_inversions(chord_name)


class Builder:
    @staticmethod
    @abstractmethod
    def build(piano: Piano, start_key: PianoKey, name: str, ) -> list[str]:
        raise NotImplementedError("This method is abstract!")
    

class BuildScale(Builder):
    @staticmethod
    def build(piano: Piano, start_key: PianoKey, scale_name="natural_minor") -> list[tuple[str]]:
        # octaves - TODO ?
        octaves = 2
        result = []
        scale = Scale(scale_name)
        # left/right - TODO ?
        f_left, f_right = fingers.get_scale_fingers(start_key.name, scale_name)
        current_key = start_key

        steps = [0]
        for _ in range(octaves):
            steps.extend(scale.steps_up)

        for _ in range(octaves):
            steps.extend(scale.steps_down)

        for step, right_finger in zip(steps, f_right):
            current_key += step
            result.append((current_key.name, right_finger))
                
        return result


class BuildArpeggio(Builder):
    @staticmethod
    def build(piano: Piano, start_key: PianoKey, arpeggio_name="minor"):
        pass


class BuildChord(Builder):
    @staticmethod
    def build(piano: Piano, start_key: PianoKey, chord_name="minor") -> list[list[tuple[str]]]:
        
        result = []
        chord = Chord(chord_name)
        # left/right - TODO ?
        f_left, f_right = fingers.get_chord_fingers(start_key.name, chord_name)

        for i, inversion_steps in enumerate(chord.inversions):
            current_key = start_key
            inversion = []
            for step, right_finger in zip(inversion_steps, f_right[i]):
                current_key += step
                inversion.append((current_key.name, right_finger))

            result.append(inversion)
        
        return result


class BuildInterval(Builder):
    @staticmethod
    def build(piano: Piano, start_key: PianoKey, interval_name="unison", direction=1) -> list[str]:
        assert direction == 1 or direction == -1

        end_key = start_key + direction * Interval[interval_name.upper()].value

        return [start_key.name, end_key.name]


def get_scale_steps(scale_name: str) -> tuple[list[int], list[int]]:
    scales_json = os.path.join("static", "json", "scales.json")

    with open(scales_json, "r") as fp:

        scales_parsed = json.load(fp)

        if scale_name not in scales_parsed.keys():
            raise ValueError("Unknown scale!")
            
        steps_up = scales_parsed[scale_name]
            
        scale_name = scale_name.replace("melodic_", "natural_")
            
        steps_down = [-x for x in reversed(scales_parsed[scale_name])]

        return steps_up, steps_down


def get_arpeggio_steps(scale_name: str) -> tuple[list[int], list[int]]:
    pass


def get_chord_inversions(chord_name: str) -> list[list[int]]:
    chords_json = os.path.join("static", "json", "chords.json")

    with open(chords_json, "r") as fp:

        chords_parsed = json.load(fp)

        if chord_name not in chords_parsed.keys():
            raise ValueError("Unknown chord!")
    
        return chords_parsed[chord_name]


if __name__ == "__main__":
    piano = Piano()
    print(BuildScale.build(piano, piano["C4"], scale_name="natural_minor"))
    print(BuildChord.build(piano, piano["C4"], chord_name="min"))
    key = piano["A4"]
    print(key - 4, key, key + 4)
