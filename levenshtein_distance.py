import streamlit as st


def load_vocab(file_path):  # load built-in dictionary (there are some vocab in .txt file)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set(line.strip().lower() for line in lines))
    return words


def levenshtein_distance(token1, token2):
    len_t1, len_t2 = len(token1), len(token2)
    distances = [[0] * (len_t2 + 1) for _ in range(len_t1 + 1)]

    for t1 in range(1, len_t1 + 1):
        distances[t1][0] = t1
    for t2 in range(1, len_t2 + 1):
        distances[0][t2] = t2

    for t1 in range(1, len_t1 + 1):
        for t2 in range(1, len_t2 + 1):
            if token1[t1 - 1] == token2[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                distances[t1][t2] = min(
                    distances[t1][t2 - 1] + 1,  # Insertion
                    distances[t1 - 1][t2] + 1,  # Deletion
                    distances[t1 - 1][t2 - 1] + 1  # Substitution
                )

    return distances[len_t1][len_t2]


def main():
    # load vocab in built-in dictionary
    vocabs = load_vocab_file(file_path=r'./vocab.txt')
    st.title('Word Correction using Levenshtein Distance')
    word = st.text_input('Word:')

    if st.button('Compute'):
        leven_dist = dict()

        for vocab in vocabs:
            leven_dist[vocab] = levenshtein_distance(word, vocab)
            
        # sorted by distance
        sorted_dist = dict(
            sorted(leven_dist.items(), key=lambda item: item[1]))
        correct_word = list(sorted_dist.keys())[0]
        st.write('Correct Word: ', correct_word)
        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)
        col2.write('Distances')
        col2.write(sorted_dist)


if __name__ == "__main__":
    main()
