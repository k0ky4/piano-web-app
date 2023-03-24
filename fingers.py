import json
import os

def get_scale_fingers(key_name: str, scale_name: str) -> tuple[list[int], list[int]]:

    scales_fingers_json = os.path.join("static", "json", "scales_fingers.json")

    with open(scales_fingers_json, "r") as fp:

        scales_fingers_parsed = json.load(fp)
        filtered_by_key = scales_fingers_parsed[key_name[:-1]]

        if scale_name not in filtered_by_key.keys():
            scale_name = 'default'
        
        left = list(filtered_by_key[scale_name]['left_hand'][:-1])
        right = list(filtered_by_key[scale_name]['right_hand'][:-1])


        if scale_name == 'melodic_minor':
            scale_name = 'default'
        
        left.extend(reversed(filtered_by_key[scale_name]['left_hand']))
        right.extend(reversed(filtered_by_key[scale_name]['right_hand']))

    return left, right


def get_arpeggio_fingers(key_name: str, scale_name: str) -> tuple[list[int], list[int]]:
    pass


def get_chord_fingers(key_name: str, chord_name: str) -> tuple[list[int], list[int]]:

    chords_fingers_json = os.path.join("static", "json", "chords_fingers.json")

    with open(chords_fingers_json, "r") as fp:

        chords_fingers_parsed = json.load(fp)
        filtered_by_key = chords_fingers_parsed[key_name[:-1]]

        if chord_name not in filtered_by_key.keys():
            chord_name = 'default'

        left = list(filtered_by_key[chord_name]['left_hand'])
        right = list(filtered_by_key[chord_name]['right_hand'])

    return left, right
