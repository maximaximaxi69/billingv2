UNITS = [
    "nulle", "viens", "divi", "trīs", "četri", "pieci", "seši", "septiņi", "astoņi", "deviņi",
    "desmit", "vienpadsmit", "divpadsmit", "trīspadsmit", "četrpadsmit", "piecpadsmit",
    "sešpadsmit", "septiņpadsmit", "astoņpadsmit", "deviņpadsmit",
]
TENS = ["", "", "divdesmit", "trīsdesmit", "četrdesmit", "piecdesmit", "sešdesmit", "septiņdesmit", "astoņdesmit", "deviņdesmit"]
HUNDREDS = ["", "viens simts", "divi simti", "trīs simti", "četri simti", "pieci simti", "seši simti", "septiņi simti", "astoņi simti", "deviņi simti"]


def _to_words_under_1000(n: int) -> str:
    parts = []
    if n >= 100:
        parts.append(HUNDREDS[n // 100])
        n %= 100
    if n >= 20:
        parts.append(TENS[n // 10])
        if n % 10:
            parts.append(UNITS[n % 10])
    elif n > 0:
        parts.append(UNITS[n])
    return " ".join([p for p in parts if p]).strip() or "nulle"


def number_to_words_lv(amount: float) -> str:
    euros = int(amount)
    cents = round((amount - euros) * 100)

    if euros < 1000:
        euro_words = _to_words_under_1000(euros)
    else:
        thousands = euros // 1000
        rest = euros % 1000
        thousand_word = "tūkstotis" if thousands == 1 else "tūkstoši"
        euro_words = f"{_to_words_under_1000(thousands)} {thousand_word}"
        if rest:
            euro_words += f" {_to_words_under_1000(rest)}"

    return f"{euro_words} eiro un {cents:02d} centi"
