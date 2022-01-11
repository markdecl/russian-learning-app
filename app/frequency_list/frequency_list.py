poss_in_full = {
    '(v)' : 'verb',
    '(pr)' : 'preposition',
    '(conj)' : 'conjunction',
    '(apro)' : 'pronoun',
    '(spro)' : 'pronoun',
    '(s)' : 'noun',
    '(part)' : 'particle',
    '(a)' : 'adjective',
    '(adv)' : 'adverb',
    '(advpro)' : 'adverb',
    '(anum)' : 'numeral',
    '(num)' : 'numeral',
    '(intj)' : 'interjection',
    '(v)f' : 'verb'
}

freq_ranks = []
words = []
pos_tags = []

with open("C:\\Users\\MdeCL\\Desktop\\Vocab-Project\\supporting-files\\ru_nat_corpus_freq_list.txt", 'r', encoding='utf8') as file:
    file_read = file.read()
    lines = file_read.split('\n')
    idx = 1
    for line in lines:
        freq_rank = idx
        freq_ranks.append(freq_rank)
        bare_word = line.split(' ')[0]
        words.append(bare_word)
        pos_tag = line.split(' ')[1]
        pos_tags.append(poss_in_full[pos_tag])

        idx += 1

est_freqs_df = pd.read_csv(desktop_dir + '\\freqs.csv')
freqs_list = est_freqs_df.head(len(freq_ranks))['Frequency'].to_list()
freqs_list = [round(item) for item in freqs_list]

rnc_freq_list = pd.DataFrame({'Frequency rank' : freq_ranks, 'Estimated frequency' : freqs_list, 'Word' : words, 'PoS tag' : pos_tags})

corpus_size = rnc_freq_list['Estimated frequency'].sum()

grouped_df = pd.DataFrame()
idx = 0
while idx <= 10000:
    sect_df = rnc_freq_list.iloc[idx:idx + 100]
    sect_est_freq = sect_df['Estimated frequency'].sum()
    grouped_df = grouped_df.append(
                                {'Frequency ranks' : str(idx) + '-' + str(idx + 100),
                                   'Estimated frequency' : sect_est_freq,
                                   'Percentage of corpus' : sect_est_freq / corpus_size * 100},
                                  ignore_index = True
                                  )
    idx += 100
