letters = {
    'ь': '',
    'ъ': '',
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ы': 'yi',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    ' ': '_',
    '-': '_',
}


def translate_rus_eng(text):
    # Replacing Russian letters, english
    symbols = [
        '+', '-', ';', '.', ',', '(', ')', '*',
        '=', '/', '"', "'", ':', '!', '?'
    ]
    for index in symbols:
        text = text.replace(index, '')
    format_text = '{}'.format(text).lower()
    return ''.join(letters.get(x, x) for x in format_text)
