import json
import re


class Enigma:

    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    REFLECTOR = "EJMZALYXVBWFCRQUONTSPIKHGD"
    ROTOT_IC = "DMTWSILRUYQNKFEJCAZBPGXOHV"
    ROTOT_IIC = "HQZGPJTMOBLNCIFDYAWVEUSRKX"
    ROTOT_IIIC = "UQNTLSZFMREHDPXKIBVYGJCWOA"

    ROTORS = [ROTOT_IC, ROTOT_IIC, ROTOT_IIIC]

    def __init__(self, plugboard_config):
        self.plugboard_config: dict = plugboard_config

    def _calculate_rotor_position(self, idx) -> [int, int, int]:
        steps = len(self.ALPHABET)
        rotor_three = idx // (steps * steps)
        idx -= rotor_three * (steps * steps)
        rotor_two = idx // steps
        idx -= rotor_two * steps
        rotor_one = idx

        return rotor_one, rotor_two, rotor_three

    def _reflect(self, letter, reverse=False):
        primary = self.ALPHABET
        secondary = self.REFLECTOR
        if reverse:
            primary = self.REFLECTOR
            secondary = self.ALPHABET

        idx = primary.index(letter)
        return secondary[idx]

    def _rotor_permutation(self, letter, idx, rotor_idx, reverse=False):
        """compute next position between 0-25"""
        rotor_position = self._calculate_rotor_position(idx)[rotor_idx]

        primary = self.ALPHABET
        secondary = self.ROTORS[rotor_idx]
        if reverse:
            primary = self.ROTORS[rotor_idx]
            secondary = self.ALPHABET

        letter_idx = primary.index(letter)
        idx_with_rotation = (letter_idx + rotor_position) % len(self.ALPHABET)
        return secondary[idx_with_rotation]

    def _plugboard(self, letter: str):
        """emulate enigma plugboard"""
        # try direct search
        result = self.plugboard_config.get(letter)
        if result:
            return result

        # try inverse search
        key_list = list(self.plugboard_config.keys())
        val_list = list(self.plugboard_config.values())
        try:
            idx = val_list.index(letter)
            return key_list[idx]
        except ValueError:
            pass

        return letter

    def _process(self, text, reverse=False):
        text = re.sub('[^A-Z ]', " ", text)
        out = ""
        for idx, letter in enumerate(text):

            if letter == " ":
                out += " "
                continue

            letter = self._plugboard(letter)

            letter = self._rotor_permutation(letter, idx, rotor_idx=0, reverse=reverse)
            # letter = self._rotor_permutation(letter, idx, rotor_idx=1, reverse=reverse)
            # letter = self._rotor_permutation(letter, idx, rotor_idx=2, reverse=reverse)
            letter = self._reflect(letter, reverse=reverse)
            # letter = self._rotor_permutation(letter, idx, rotor_idx=2, reverse=not reverse)
            # letter = self._rotor_permutation(letter, idx, rotor_idx=1, reverse=not reverse)
            letter = self._rotor_permutation(letter, idx, rotor_idx=0, reverse=not reverse)

            letter = self._plugboard(letter)
            out += letter
        return out

    def encode(self, text):
        return self._process(text)

    def decode(self, text):
        return self._process(text, reverse=True)


if __name__ == '__main__':

    world = "CIAO ACMZaa BELLA"

    with open("config.json", "r") as f:
        settings = json.load(f)
        enigma = Enigma(settings["plugboard"])

        print(world)
        code = enigma.encode(world)
        print(code)
        code = enigma.decode(code)
        print(code)
