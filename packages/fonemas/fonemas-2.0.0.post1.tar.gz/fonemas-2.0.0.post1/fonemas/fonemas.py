#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import silabeador


class transcription:
    def __init__(self, sentence, mono=False, epenthesis=True):
        self.sentence = self.__letters(self.__clean(sentence.lower(),
                                                    epenthesis))
        self.phonology = self.transcription_fnl(self.sentence, mono)
        self.transliteration = self.transcription_fnt(self.phonology)
        self.phonetics = {'words': self.transliteration['phon_words'],
                          'syllables': self.transliteration['phon_syllables']}
        self.ascii = {'words': self.transliteration['ascii_words'],
                      'syllables': self.transliteration['ascii_syllables']}

    @staticmethod
    def ipa2ascii(words):
        translation = {'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u',
                       'j': 'j', 'w': 'w',
                       'b': 'b', 'β': 'B', 'd': 'd', 'ð': 'D',
                       'g': 'g', 'ɣ': 'G',
                       'p': 'p', 't': 't', 'k': 'k',
                       'l': 'l', 'ʎ': 'L', 'r': 'R', 'ɾ': 'r',
                       'm': 'm', 'ɱ': 'M', 'n': 'n', 'ŋ': 'N', 'ɲ': '9',
                       'tʃ': 'X', 'ʝ': 'y', 'x': 'x', 'χ': '4',
                       'f': 'f', 's': 's', 'z': 'z', 'θ': 'Z'}
        for phoneme in translation:
            words = words.replace(phoneme, translation[phoneme])
        return words

    @staticmethod
    def __clean(sentence, epenthesis):
        symbols = ['(', ')', '—', '…', ',', ';', ':', '?', '!', "'", '.',
                   '«', '»', '–', '—', '“', '”', '‘', '’', '"', '-', '(', ')']
        letters = {'õ': 'o', 'æ': 'ae',
                   'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u'}
        for x in symbols:
            if x in sentence:
                sentence = sentence.replace(x, '')
        for x in letters:
            if x in sentence:
                sentence = sentence.replace(x, letters[x])
        if epenthesis:
            sentence = re.sub(r'\bs((?![aeiouáéíóúäëïöü]))', r'es\1', sentence)
        return sentence

    def __splitvariables(self, sentence, mono):
        syllabic = []
        wordy = []
        for word in sentence.split():
            if len(word) > 5 and word.endswith('mente'):
                syllabification = silabeador.syllabification(
                    word[:-5], True, True)
                syllables = syllabification.syllables
                if len(syllables) > 1:
                    syllables = syllables + ['ˌmen', 'te']
                    stress = syllabification.stress - 2
                    word = word.replace('mente', 'ˌmente')
                else:
                    syllables = syllables + ["'men", 'te']
                    stress = -2

            else:
                syllabification = silabeador.syllabification(word, True, True)
                syllables = syllabification.syllables
                stress = syllabification.stress
            conta = 0
            diph = self.__diphthongs(word, syllables)
            word = diph['word']
            syllables = diph['syllables']
            syllables[stress] = f"'{syllables[stress]}"
            for idx, slb in enumerate(syllables):
                for char in slb:
                    if char == "'":
                        word = word[:conta] + "'" + word[conta:]
                    else:
                        conta += 1
            for idx, syllable in enumerate(syllables):
                if mono and len(syllables) == 1:
                    syllable = syllable.strip("'")
                syllabic += [syllable]
            if len(syllabic) == 1:
                word = word.replace("'", '')
            wordy += [word]
        return {'words': wordy, 'syllables': syllabic}

    @staticmethod
    def __letters(sentence):
        letters = {'b': 'be', 'c': 'ce', 'd': 'de', 'f': 'efe', 'g': 'ge',
                   'h': 'hache', 'j': 'jota', 'k': 'ka', 'l': 'ele',
                   'm': 'eme', 'n': 'ene', 'p': 'pe', 'q': 'ku',
                   'r': 'erre', 's': 'ese', 't': 'te', 'v': 'ube',
                   'w': 'ubedoble', 'x': 'ekis', 'z': 'ceta', 'ph': 'peache'}
        for letter in letters:
            sentence = re.sub(rf'\b{letter}\b', 'letters[letter]', sentence)
        return sentence

    def transcription_fnl(self, sentence, mono):
        diacritics = {'á': 'a', 'à': 'a', 'ä': 'a',
                      'é': 'e', 'è': 'e', 'ë': 'e',
                      'í': 'i', 'ì': 'i', 'ï': 'i',
                      'ó': 'o', 'ò': 'o', 'ö': 'o',
                      'ú': 'u', 'ù': 'u', 'ü': 'u'}

        consonants = {'w': 'b', 'v': 'b', 'z': 'θ', 'x': 'ks', 'j': 'x',
                      'ñ': 'ɲ', 'qu': 'k', 'll': 'ʎ', 'ch': 'tʃ',
                      'r': 'ɾ', 'R': 'r',
                      'ce': 'θe', 'cé': 'θé', 'cë': 'θë',
                      'ci': 'θi', 'cí': 'θí', 'cï': 'θï', 'cj': 'θj',
                      'c': 'k', 'ph': 'f', 'h': ''}
        sentence = re.sub(r'(?:([nls])r|rr|\br)', r'\1R', sentence)
        sentence = sentence.replace('r', 'ɾ')
        for consonant in consonants:
            if consonant in sentence:
                sentence = sentence.replace(consonant, consonants[consonant])
        if 'y' in sentence:
            sentence = sentence.replace('y', 'ʝ')
            sentence = re.sub(r'ʝ\b', 'j', sentence)
            for key, value in diacritics.items():
                if key in 'áéíóú':
                    sentence = re.sub(rf'{value}ʝ\b', f'{key}i', sentence)
            # sentence = re.sub(r'y', 'ʝ', sentence)
            # sentence = re.sub(r'ʝ\b', 'i', sentence)
            sentence = re.sub(r'ʝ((?![aeiouáéíóú]))', r'i\1', sentence)
        if 'g' in sentence:
            for reg in [
                [r'g([eiéíiëï])', rf'x\1'],
                    [r'g[u]([eiéíëï])', rf'g\1']]:
                sentence = re.sub(reg[0], reg[1], sentence)
            if 'gü' in sentence:
                sentence = sentence.replace('gü', 'gw')
        transcription = self.__splitvariables(sentence, mono)
        words = transcription['words']
        syllables = transcription['syllables']
        for letter in diacritics:
            words = [word.replace(letter, diacritics[letter])
                     for word in words]
            syllables = [syllable.replace(letter, diacritics[letter]) for
                         syllable in syllables]
        return {'words': words, 'syllables': syllables}

    @staticmethod
    def __fsubstitute(words):
        words = words.replace('b', 'β').replace('d', 'ð').replace('g', 'ɣ')
        words = re.sub(r'([mnɲ ^])(\-*)β', r'\1\2b', words)
        words = re.sub(r'([mnɲlʎ ^])(\-*)ð', r'\1\2d', words)
        words = re.sub(r'([mnɲ ^])(\-*)ɣ', r'\1\2g', words)
        words = re.sub(r'θ(\-*)([bdgβðɣmnɲlʎrɾ])', r'ð\1\2', words)
        words = re.sub(r's(\-*)([bdgβðɣmnɲlʎrɾ])', r'z\1\2', words)
        words = re.sub(r'f(\-*)([bdgβðɣmnɲʎ])', r'v\1\2', words)
        allophones = {'nb': 'mb', 'nf': 'ɱf',
                      'nk': 'ŋk', 'ng': 'ŋg', 'nx': 'ŋx',
                      'xu': 'χu', 'xo': 'χo', 'xw': 'χw',
                      'n-b': 'm-b', 'n-f': 'ɱ-f',
                      'n-k': 'ŋ-k', 'n-g': 'ŋ-g', 'n-x': 'ŋ-x'
                      }
        if any(allophone in words for allophone in allophones):
            for allophone in allophones:
                words = words.replace(allophone, allophones[allophone])
        return words.replace('-', ' ')

    def transcription_fnt(self, phonology):
        words = ' '.join(phonology['words'])
        syllables = '-'.join(phonology['syllables'])
        phon_words = self.__fsubstitute(words)
        phon_syllables = self.__fsubstitute(syllables)
        ascii_words = self.ipa2ascii(phon_words)
        ascii_syllables = self.ipa2ascii(phon_syllables)
        return {'phon_words': self.__fsubstitute(phon_words).split(),
                'phon_syllables': self.__fsubstitute(phon_syllables).split(),
                'ascii_words': self.__fsubstitute(ascii_words).split(),
                'ascii_syllables': self.__fsubstitute(ascii_syllables).split()}

    @staticmethod
    def __replace_ocurrence(string, origin, to, num):
        strange_char = '$&$@$$&'
        if string.count(origin) < 0:
            return string
        elif string.count(origin) > 1:
            return string.replace(origin, strange_char, num).replace(
                strange_char, origin, num-1).replace(to, strange_char, 1)
        else:
            return string.replace(origin, to)

    def __diphthongs(self, word, syllables):
        i = 0
        j = 0
        for idx, syllable in enumerate(syllables):
            if re.search('[aeiouáéíóú]{2,}', syllable):
                i += 1
                syllable = re.sub(r'([aeouáééóú])i', r'\1j', syllable)
                syllable = re.sub(r'([aeoiáééóú])u', r'\1w', syllable)
                word = self.__replace_ocurrence(word,
                                                syllables[idx],
                                                syllable, i)
            if re.search('[ui][aeiouáééiíóú]', syllable):
                j += 1
                syllable = re.sub(r'i([aeouáééiíóú])', r'j\1', syllable)
                syllable = re.sub(r'u([aeioáééiíóú])', r'w\1', syllable)
                word = self.__replace_ocurrence(word,
                                                syllables[idx],
                                                syllable, j)
            syllables[idx] = syllable
        return {'word': word, 'syllables': syllables}
