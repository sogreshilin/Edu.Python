import codecs
import sys

freqs = {
    'о': 0.10983, 'е': 0.08483, 'а': 0.07998, 'и': 0.07367, 'н': 0.06700,
    'т': 0.06318, 'с': 0.05473, 'р': 0.04746, 'в': 0.04533, 'л': 0.04343,
    'к': 0.03486, 'м': 0.03203, 'д': 0.02977, 'п': 0.02804, 'у': 0.02615,
    'я': 0.02001, 'ы': 0.01898, 'ь': 0.01735, 'г': 0.01687, 'з': 0.01641,
    'б': 0.01592, 'ч': 0.01450, 'й': 0.01208, 'х': 0.00966, 'ж': 0.00940,
    'ш': 0.00718, 'ю': 0.00639, 'ц': 0.00486, 'щ': 0.00361, 'э': 0.00331,
    'ф': 0.00267, 'ъ': 0.00037, 'ё': 0.00013
}

russian_encodings = ('koi8-r', 'cp866', 'cp1251', 'iso_8859-5', 'mac_cyrillic')
alphabet = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
alphabet_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


class EncodingStatistics:
    def __init__(self, encoding_name):
        self.name = encoding_name
        self._prepare_char_to_ord()
        self._stats = dict()

    def _prepare_char_to_ord(self):
        bites = alphabet.encode(self.name)
        self._char_to_ord = dict()
        for i in range(len(alphabet_lower)):
            self._char_to_ord[alphabet[2 * i + 1]] = (bites[2 * i], bites[2 * i + 1])

    def update_stats(self, char, count):
        self._stats[char] = count

    def upper_ord(self, char):
        return self._char_to_ord[char][0]

    def lower_ord(self, char):
        return self._char_to_ord[char][1]

    def freqs(self):
        total_symbols = sum(self._stats.values())
        return {key: self._stats[key] / total_symbols for key in self._stats}


def next_bite(file, size=1024):
    while True:
        data = file.read(size)
        if not data:
            break
        for bite in data:
            yield bite


def count_bites(filename):
    bites_count = dict.fromkeys(range(128, 256), 0)

    with open(filename, 'rb') as file:
        for bite in next_bite(file):
            if bite >= 128:
                bites_count[bite] += 1

    return bites_count


def distance(expected, actual):
    rv = 0
    for key in expected:
        rv += (expected[key] - actual[key]) ** 2
    return rv


def get_closest_encoding(bites_count):
    distances = dict()

    for encoding in [EncodingStatistics(name) for name in russian_encodings]:
        for key in alphabet_lower:
            char_count = bites_count[encoding.upper_ord(key)] + bites_count[encoding.lower_ord(key)]
            encoding.update_stats(key, char_count)
        distances[encoding.name] = distance(freqs, encoding.freqs())

    return min(distances, key=distances.get)


def guess_encoding(filename):
    bites_count = count_bites(filename)
    return get_closest_encoding(bites_count)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Expected file name as a command line argument. '
              'File name was not found', file=sys.stderr)
        sys.exit(-1)

    filename = sys.argv[1]
    try:
        guessed_encoding = guess_encoding(filename)
        print(f'file encoding = {guessed_encoding}')
        value = input('Do you want to print file? y/n: ')
        if value.lower() == 'y':
            print(codecs.open(filename, encoding=guessed_encoding).read())

    except Exception as e:
        print(e, sys.stderr)
