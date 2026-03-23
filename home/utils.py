#Justin-Kenneth Denault
#261296919

ZERO = 0.0
#1

#1.1
def get_list(s):
    """ (str) -> list of str

    Convert a dash-separated string into a normalized token list. 
    Splits on '-',strips surrounding spaces, converts to lowercase,
     and removes empty tokens.

    >>> get_list('password management-IT maintenance- computer repair')
    ['password management', 'it maintenance', 'computer repair']

    >>> get_list('python-sql-etl')
    ['python', 'sql', 'etl']

    >>> get_list('basketball-shooting-defense-rebounding')
    ['basketball', 'shooting', 'defense', 'rebounding']
    """
    parts = s.split('-')
    item_list = []

    for part in parts:
        cleaned = part.strip()

        if cleaned:  # This is True if cleaned is not empty
            lowercase_word = cleaned.lower()
            item_list.append(lowercase_word)

    return item_list

#1.2
def make_vocabulary(items):
    """ (list[list of str]) -> list of str

    Build a shared vocabulary of unique tokens from nested lists.
    Collects all tokens, converts to lowercase, removes duplicates,
    and returns sorted list.

    >>> make_vocabulary([['Python','SQL'],['python','etl','sql']])
    ['python', 'sql', 'etl']

    >>> make_vocabulary([['LeBron','Kobe'],['LeBron','Jordan']])
    ['lebron', 'kobe', 'jordan']

    >>> make_vocabulary([['point-guard','shooting'],['shooting',
    ...                 'defense']])
    ['point-guard', 'shooting', 'defense']
    """
    vocab = []
    for inner_list in items:
        for word in inner_list:
            word_lower = word.lower()
            if word_lower not in vocab:
                vocab.append(word_lower)
    return vocab

#1.3
def vectorize(tokens, vocab):
    """ (list of str, list of str) -> list of int

    Convert a token list into a bag-of-words count vector aligned
    with vocabulary.For each vocabulary item, counts how many times
    it appears in tokens (case-insensitive).

    >>> vocab = ['etl','python','sql']
    >>> vectorize(['python','etl','python'], vocab)
    [1, 2, 0]

    >>> vocab = ['basketball','shooting','defense']
    >>> vectorize(['Basketball','shooting','dunk','shooting'], vocab)
    [1, 2, 0]

    >>> vocab = ['point-guard','shooting','rebounding']
    >>> vectorize(['point-guard','Point-Guard','assist'], vocab)
    [2, 0, 0]
    """
    count_list = [0] * len(vocab)
    for token in tokens:
        token_lower = token.lower()
        for i in range(len(vocab)):
            if vocab[i] == token_lower:
                count_list[i] += 1

    return count_list

#1.4
def cosine_similarity(v1, v2):
    """ (list of float, list of float) -> float

    Calculate cosine similarity between two vectors. Returns 0.0 if either
    vector has zero norm, otherwise returns dot product divided by product
    of Euclidean norms, rounded to two decimal places.

    >>> cosine_similarity([1, 2, 0], [0, 2, 1])
    0.8

    >>> cosine_similarity([3.0, 4.0], [3.0, 4.0])
    1.0

    >>> cosine_similarity([2.5, 1.5], [5.0, 3.0])
    1.0
    """
    if len(v1) != len(v2):
        raise ValueError("v1 and v2 have different lengths")

    dot_product = ZERO
    for i in range(len(v1)):
        dot_product += v1[i] * v2[i]

    norm_v1 = ZERO
    for x in v1:
        norm_v1 += x ** 2
    norm_v1 = norm_v1 ** 0.5

    norm_v2 = ZERO
    for x in v2:
        norm_v2 += x ** 2
    norm_v2 = norm_v2 ** 0.5

    if norm_v1 == ZERO or norm_v2 == ZERO:
        return ZERO

    cos_sim = dot_product / (norm_v1 * norm_v2)
    return round(cos_sim, 2)
