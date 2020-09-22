# -*- coding: utf-8 -*-

import termcolor

class Farsi:
    # ===========================================================================
    null = ' '
    zero_width_non_joiner = '‌'
    letters_sticking_to_the_next_letter = ['ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع',
                                           'غ',
                                           'ف', 'ق', 'ك', 'ک', 'گ', 'ل', 'م', 'ن', 'ه', 'ي', 'ی']
    letters_sticking_to_the_previous_letter = ['آ', 'ا', 'أ', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر',
                                               'ز',
                                               'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ک', 'گ',
                                               'ل',
                                               'م', 'ن', 'و', 'ﺅ', 'ه', 'ة', 'ي', 'ی']
    alphabet = ['آ', 'ا', 'أ', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 'ط',
                'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ﺅ', 'ه', 'ة', 'ي', 'ی']
    alphabet_sticking_only_to_the_previous_letter = ['ﺂ', 'ﺎ', 'ﺄ', 'ﺐ', 'ﭗ', 'ﺖ', 'ﺚ', 'ﺞ', 'ﭻ', 'ﺢ', 'ﺦ', 'ﺪ', 'ﺬ',
                                                     'ﺮ',
                                                     'ﺰ', 'ﮋ', 'ﺲ', 'ﺶ', 'ﺺ', 'ﺾ', 'ﻂ', 'ﻆ', 'ﻊ', 'ﻎ', 'ﻒ', 'ﻖ', 'ﻚ',
                                                     'ﻚ',
                                                     'ﮓ', 'ﻞ', 'ﻢ', 'ﻦ', 'ﻮ', 'ﺆ', 'ﻪ', 'ﺔ', 'ﯽ', 'ﯽ']
    alphabet_sticking_only_to_the_next_letter = ['آ', 'ا', 'أ', 'ﺑ', 'ﭘ', 'ﺗ', 'ﺛ', 'ﺟ', 'ﭼ', 'ﺣ', 'ﺧ', 'د', 'ذ', 'ر',
                                                 'ز',
                                                 'ژ', 'ﺳ', 'ﺷ', 'ﺻ', 'ﺿ', 'ﻃ', 'ﻇ', 'ﻋ', 'ﻏ', 'ﻓ', 'ﻗ', 'ﻛ', 'ﻛ', 'ﮔ',
                                                 'ﻟ',
                                                 'ﻣ', 'ﻧ', 'و', 'ﺅ', 'ﻫ', 'ﺓ', 'ﻳ', 'ﻳ']
    alphabet_sticking_to_the_previous_and_to_the_next_letter = ['ﺂ', 'ﺎ', 'ﺄ', 'ﺒ', 'ﭙ', 'ﺘ', 'ﺜ', 'ﺠ', 'ﭽ', 'ﺤ', 'ﺨ',
                                                                'ﺪ',
                                                                'ﺬ', 'ﺮ', 'ﺰ', 'ﮋ', 'ﺴ', 'ﺸ', 'ﺼ', 'ﻀ', 'ﻄ', 'ﻈ', 'ﻌ',
                                                                'ﻐ',
                                                                'ﻔ', 'ﻘ', 'ﻜ', 'ﻜ', 'ﮕ', 'ﻠ', 'ﻤ', 'ﻨ', 'ﻮ', 'ﺆ', 'ﻬ',
                                                                'ﺔ',
                                                                'ﻴ', 'ﻴ']
    numerals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    farsi_numerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']

    # ===========================================================================
    @staticmethod
    def convert_farsi_letter(previous_letter: str, main_letter: str, next_letter: str) -> str:
        new_letter = main_letter

        if main_letter in Farsi.alphabet:
            position = Farsi.alphabet.index(main_letter)
            main_letter_sticks_to_the_previous_letter = False
            main_letter_sticks_to_the_next_letter = False

            # Check the previous letter
            if previous_letter in Farsi.letters_sticking_to_the_next_letter:
                main_letter_sticks_to_the_previous_letter = True

            # Check the next letter
            if next_letter in Farsi.letters_sticking_to_the_previous_letter:
                main_letter_sticks_to_the_next_letter = True

            # Convert the main letter
            if main_letter_sticks_to_the_previous_letter and main_letter_sticks_to_the_next_letter:
                new_letter = Farsi.alphabet_sticking_to_the_previous_and_to_the_next_letter[position]
            elif main_letter_sticks_to_the_previous_letter:
                new_letter = Farsi.alphabet_sticking_only_to_the_previous_letter[position]
            elif main_letter_sticks_to_the_next_letter:
                new_letter = Farsi.alphabet_sticking_only_to_the_next_letter[position]

        return new_letter

    # ===========================================================================
    @staticmethod
    # the string will be reversed while letters are being converted.
    def convert_string_farsi_letters(s: str) -> str:
        # //str = SubstituteEhwithTeh(str);
        new_s = ""

        if len(s) > 1:
            new_s += Farsi.convert_farsi_letter(Farsi.null, s[0], s[1])
            for i in range(1, len(s) - 1):
                new_s += Farsi.convert_farsi_letter(s[i - 1], s[i], s[i + 1])
            new_s += Farsi.convert_farsi_letter(s[-2], s[-1], Farsi.null)
        else:
            new_s = s

        return new_s

    # ===========================================================================
    @staticmethod
    # letters in words will be converted in place. no reversing.
    def convert_string_farsi_words(s):
        words = s.split()
        for word in words:
            s = s.replace(word, Farsi.convert_string_farsi_letters(word))
        s = ''.join(reversed(s))
        words = s.split()
        for word in words:
            is_farsi = False
            for letter in word:
                if letter in Farsi.alphabet or \
                        letter in Farsi.alphabet_sticking_only_to_the_next_letter or \
                        letter in Farsi.alphabet_sticking_only_to_the_previous_letter or \
                        letter in Farsi.alphabet_sticking_to_the_previous_and_to_the_next_letter:
                    is_farsi = True
            if not is_farsi:
                new_word = ''.join(reversed(word))
                s = s.replace(word, new_word)
        return s

    # ===========================================================================
    @staticmethod
    def print_farsi(s, color='white', reverse=False, end='\n'):
        new_s = Farsi.convert_string_farsi_letters(s)
        if reverse:
            new_s = new_s[::-1]
        print(termcolor.colored(new_s, color), flush=True, end=end)
