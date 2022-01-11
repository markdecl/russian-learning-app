# Collocation filters:

with open("C:\\Users\\MdeCL\\Google Drive\\Work, productivity and interests_\\computer science\\coding skills (technical)\\VS Code project files\\NLP-powered Vocab Learning Strategy\\Russian Vocab Project\\ru_prepositions.txt", 'r', encoding='utf8') as file:
    file_read = file.read()
    preps = file_read.split('\n')
# Define Russian stop words
stop_words_lems = []
for index, row in rnc_freq_list.iloc[1:1000].iterrows():
    poss_to_keep = ['pronoun', 'verb', 'conjunction', 'adverb']
    if row['PoS tag'] in poss_to_keep:
        if index <= 50 or row['PoS tag'] in ['pronoun', 'conjunction']:
            stop_words_lems.append(row['Word'])

ru_stop_words = stop_words_lems

particles = ['не']
conjs = ['и', 'но', 'а', 'или', ]
prons = ['он', 'который']

ru_stop_words.remove('сказать')
ru_stop_words.remove('всякий')
ru_stop_words.remove('некий')
ru_stop_words.remove('данный')

ru_stop_words += ['нет', 'да', 'более', 'также', 'это', 'все', 'нее', 'очень'] + particles + conjs + prons

ru_stop_words = list(set(ru_stop_words))

# Import idiom_dict_df from csv file and convert back to Python dict format:

idiom_dict_df = pd.read_csv('C:\\Users\\MdeCL\\Google Drive\\Work, productivity and interests_\\computer science\\coding skills (technical)\\VS Code project files\\NLP-powered Vocab Learning Strategy\\Russian Vocab Project\\idiom_dict_df.csv')

idiom_dict_for_check = {}
for index, row in idiom_dict_df.iterrows():
    idiom_dict_for_check[row['Lemmed coll']] = {'Original ru phrase' : row['Original ru phrase'],
                                      'Eng tran' : row['Eng tran']
                                     }
idiom_dict_for_check[' еще бы ']

# coll_type_filter function:

def coll_type_filter(lemmed_coll, pos_tag_list, case_ahead):


    punct = ['=', '.', ':', '!', '?', ';', '-', '—', '\"', '\`\`', '«', '»', '(', ')', ]
    ignored_words = ru_stop_words

    coll_as_idiom_dict_key = ' ' + ' '.join(lemmed_coll) + ' '
    if (coll_as_idiom_dict_key in idiom_dict_for_check) or (coll_as_idiom_dict_key.replace('ё', 'е') in idiom_dict_for_check):
        coll_type = 'lex'
    else:
        if any([item in punct for item in lemmed_coll]):
            coll_type = 'punct'
        elif any([item.isdigit() for item in lemmed_coll]):
            coll_type = 'ignore'
        else:
            if (str(lemmed_coll[0]) == ',') or (str(lemmed_coll[-1]) == ','):
                coll_type = 'punct'
            else:
                if len(pos_tag_list) == 1:
                    coll_type = 'ignore'

                elif len(pos_tag_list) == 2:

                    if pos_tag_list[0] == 'PREP' and pos_tag_list[1] == 'NOUN':
                        coll_type = 'gram without case ahead'
                    elif pos_tag_list[0] == 'NOUN' and pos_tag_list[1] == 'PREP' and case_ahead != 'No case ahead':
                        coll_type = 'gram with case ahead'
                    elif pos_tag_list[0] in ['INFN', 'PRTF', 'VERB'] and pos_tag_list[1] == 'PREP' and case_ahead != 'No case ahead':
                        coll_type = 'gram with case ahead'
                    elif pos_tag_list[0] == 'ADJF' and pos_tag_list[1] == 'PREP' and case_ahead != 'No case ahead':
                        coll_type = 'gram with case ahead'
                    elif pos_tag_list[0] == 'ADVB' and pos_tag_list[1] == 'PREP' and case_ahead != 'No case ahead':
                        coll_type = 'gram with case ahead'

                    elif pos_tag_list[0] == 'ADVB' and pos_tag_list[1] == 'ADJF':
                        coll_type = 'lex'
                    elif pos_tag_list[0] == 'ADVB' and pos_tag_list[1]  in ['INFN', 'PRTF', 'VERB']:
                        coll_type = 'lex'
                    elif pos_tag_list[0] == 'ADJF' and pos_tag_list[1] == 'NOUN':
                        coll_type = 'lex'
                    elif pos_tag_list[0] == 'NOUN' and pos_tag_list[1] == 'NOUN':
                        coll_type = 'lex'
                    elif pos_tag_list[0]  in ['INFN', 'PRTF', 'VERB'] and pos_tag_list[1] == 'NOUN':
                        coll_type = 'lex'
                    elif pos_tag_list[0] == 'NOUN' and pos_tag_list[1]  in ['INFN', 'PRTF', 'VERB']:
                        coll_type = 'lex'

                    else:
                        coll_type = 'ignore'

                elif len(pos_tag_list) == 3:

                    if pos_tag_list[0] == 'PREP' and pos_tag_list[1] == 'NOUN' and pos_tag_list[2] == 'PREP' and case_ahead != 'No case ahead':
                        coll_type = 'gram with case ahead'

                    elif pos_tag_list[0] == 'NOUN' and pos_tag_list[2] == 'NOUN':
                        coll_type = 'lex'
                    elif pos_tag_list[0] == 'NOUN' and pos_tag_list[1] != 'CONJ' and pos_tag_list[2] in ['INFN', 'PRTF', 'VERB']:
                        coll_type = 'lex'
                    elif pos_tag_list[0] in ['INFN', 'PRTF', 'VERB'] and pos_tag_list[1] != 'CONJ' and pos_tag_list[2] == 'NOUN':
                        coll_type = 'lex'
                    elif pos_tag_list[0] == 'ADJF' and pos_tag_list[1] == 'NOUN' and pos_tag_list[2] == 'NOUN':
                        coll_type = 'lex'
                    elif pos_tag_list[0] == 'PREP' and pos_tag_list[1] == 'ADJF' and pos_tag_list[2] == 'NOUN':
                        coll_type = 'lex'
                    elif pos_tag_list[0] == 'PREP' and pos_tag_list[1] == 'NOUN' and pos_tag_list[2] == 'NOUN':
                        coll_type = 'lex'
                    elif pos_tag_list[0] == 'ADJF' and pos_tag_list[1] == 'CONJ' and pos_tag_list[2] == 'ADJF':
                        coll_type = 'lex'

                    else:
                        coll_type = 'ignore'

                elif len(pos_tag_list) >= 4:

                    if pos_tag_list[-1] != 'ADJF':
                        coll_type = 'lex'
                    else:
                        coll_type = 'ignore'

        stop_word_bool = False
        if coll_type == 'lex':
            if str(lemmed_coll[0]) not in ignored_words and str(lemmed_coll[-1]) not in ignored_words:
                coll_type = 'lex'
            else:
                coll_type = 'ignore'

    if len(lemmed_coll) == 1:
        coll_type = 'ignore'

    return coll_type
coll_type_filter(('хотя', 'бы'), ['CONJ', 'PART'], 'No case ahead')
corpus_size = rnc_freq_list['Estimated frequency'].sum()
word_freq_dict = {}
for index, row in rnc_freq_list.iterrows():
    word_freq_dict[row['Word']] = row['Estimated frequency']

def coll_score(n_grams_df_row):
    lemmed_coll = n_grams_df_row['Lemmed collocation']
    raw_freq = n_grams_df_row['Raw frequency']
    freq = n_grams_df_row['Frequency']

    combined_freq = 1
    for item in lemmed_coll:
        combined_freq = combined_freq * word_freq_dict[item]

    mi_score = math.log2(freq * corpus_size / combined_freq)

    return mi_score
test_df = pd.DataFrame({'Lemmed collocation': [('как', 'бы', 'то', 'ни', 'быть')],
                       'Raw frequency' : 110,
                       'Frequency' : 2000})

coll_score(test_df.iloc[0])

# Collocational analysis:

def lem_coll(coll):
    lem_coll = []
    for word in coll:
        p = morph.parse(word)[0]
        lem_coll.append(p.normal_form)
    return lem_coll
lem_coll(['для', ',', 'времен'])
def complex_lem_coll(coll):
    lem_coll = []
    lem = True
    for word in coll:
        p = morph.parse(word)[0]
        pos = p.tag.POS
        if lem == True:
            lem_coll.append(p.normal_form)
        else:
            lem_coll.append(word)
        if pos == 'PREP':
            lem = False
        elif pos in ['INFN', 'VERB', 'NOUN']:
            lem = True

    return lem_coll
sent = 'Из тумана вышла лагерная ограда – ряды проволоки , натянутые между железобетонными столбами'
coll = sent.split(' ')
complex_lem_coll(coll)
lem_coll(['для', ',', 'времен'])
def colls_from_sents_df_row(row, **kwargs):

    for arg in kwargs:
        query_forms = kwargs[arg]

    source = row['Source']
    src_sent = row['Standardised source sentence']
    sent_words_raw = row['Standardised source sentence'].replace('  ', ' ').split(' ')
    lemmed_sent_words_raw = row['Lemmed source sentence'].replace('  ', ' ').split(' ')
#     lemmed_sent_words_raw = row['Coll lemmed source sentence'].replace('  ', ' ').split(' ')
    pos_tag_list_raw = row['Source sentence PoS tags'].split(' ')
    case_list_raw = row['Source sentence cases'].split(' ')
    target_sent = row['Standardised target sentence']

    sent_words = []
    lemmed_sent_words = []
    pos_tag_list = []
    case_list = []
    token_idx = 0
    for token in lemmed_sent_words_raw:
        if token != '':
            lemmed_sent_words.append(token)
            sent_words.append(sent_words_raw[token_idx])
            pos_tag_list.append(pos_tag_list_raw[token_idx])
            if case_list_raw[token_idx] == 'nomn':
                case_list.append('accs')
            else:
                case_list.append(case_list_raw[token_idx])
        token_idx += 1

    for query in query_forms:
        try:
            q_idx = lemmed_sent_words.index(query)
        except Exception:
            pass

    start_b0 = []
    start_b1 = []
    start_b2 = []
    start_b3 = []
    start_b4 = []

    words_behind = 0
    while words_behind <= 3 and words_behind <= q_idx:
        words_ahead = 3
        while words_ahead >= 1:
            if q_idx + words_ahead <= len(sent_words):
                n_gram = sent_words[q_idx - words_behind:q_idx + words_ahead]
                n_gram = [word.lower() for word in n_gram]
                lemmed_n_gram = lemmed_sent_words[q_idx - words_behind:q_idx + words_ahead]
                n_gram_pos_list = pos_tag_list[q_idx - words_behind:q_idx + words_ahead]
                n_gram_case_list = case_list[q_idx - words_behind:q_idx + words_ahead]

                if q_idx + words_ahead + 1 < len(sent_words):
                    if n_gram_pos_list[-1] == 'VERB' or 'INFN' or 'PREP':
                        case_of_next_token = str(case_list[q_idx + words_ahead + 1])
                        if case_of_next_token != 'None':
                            case_ahead = case_of_next_token
                        else:
                            case_ahead = 'No case ahead'
                    else:
                        case_ahead = 'No case ahead'
                else:
                    case_ahead = 'No case ahead'
                if case_ahead == 'None':
                    print('COLLS FROM SENTS DF ROW LABELLED CASE AHEAD AS NONE')
                    case_ahead = 'No case ahead'

                # PASS N-GRAM THROUGH COLL TYPE FILTER TO FIND COLL TYPE:
                coll_type = coll_type_filter(lemmed_n_gram, n_gram_pos_list, case_ahead)

                src_sent_term_bold_list = []
                src_sent_coll_bold_list = []
                idx = 0
                for token in sent_words_raw:
                    if idx == q_idx:
                        src_sent_term_bold_list.append('<b><i>' + token + '</i></b>')
                        src_sent_coll_bold_list.append('<b><i>' + token + '</i></b>')
                    elif idx in [i for i in range(q_idx - words_behind, q_idx + words_ahead) if i != q_idx]:
                        src_sent_term_bold_list.append(token)
                        src_sent_coll_bold_list.append('<b>' + token + '</b>')
                    else:
                        src_sent_term_bold_list.append(token)
                        src_sent_coll_bold_list.append(token)
                    idx += 1
                src_sent_term_bold = ' '.join(src_sent_term_bold_list)
                src_sent_coll_bold = ' '.join(src_sent_coll_bold_list)

                meaning_dependent_info = []
                count_case = False
                for token in n_gram:
                    if count_case == True:
                        meaning_dependent_info.append(n_gram_pos_list[n_gram.index(token)])
                    else:
                        meaning_dependent_info.append('')
                    if n_gram_pos_list[n_gram.index(token)] == 'PREP':
                        count_case = True

                n_gram_package = {}
                n_gram_package['Source'] = source
                n_gram_package['Source sentence with term bold'] = src_sent_term_bold
                n_gram_package['Source sentence with coll bold'] = src_sent_coll_bold
                n_gram_package['Source'] = source
                n_gram_package['Collocation type'] = coll_type
                n_gram_package['Original N-gram'] = n_gram
                n_gram_package['Lemmed N-gram'] = lemmed_n_gram
                n_gram_package['Case ahead'] = case_ahead
                n_gram_package['N-gram PoS tags'] = n_gram_pos_list
                n_gram_package['N-gram cases'] = n_gram_case_list
                n_gram_package['N-gram meaning dependent info'] = meaning_dependent_info
                n_gram_package['N-gram term position'] = q_idx
                n_gram_package['N-gram collocate positions'] = [i for i in range(q_idx - words_behind, q_idx + words_ahead)  if i != q_idx]
                n_gram_package['Edited N-grams'] = []

                #COUNT COLLOCATIONS AT A DISTANCE (i.e. colls separated by a word).
                for word in n_gram[1:-1]:
                    word_idx = n_gram.index(word)
                    if sent_words.index(word) != q_idx:
                        word_before_pos = pos_tag_list[sent_words.index(word)-1]
                        word_pos = pos_tag_list[sent_words.index(word)]
                        word_ahead_pos = pos_tag_list[sent_words.index(word)+1]
                        removable_pos_tags = ['ADVB', 'ADJF']
                        if (word_pos in removable_pos_tags) or (word_before_pos in ['INFN', 'VERB'] and word_pos in ['NOUN', 'NPRO'] and word_ahead_pos == 'PREP'):

                            mut_n_gram = n_gram[:]
                            del mut_n_gram[word_idx]
                            edited_n_gram = mut_n_gram
                            edited_n_gram = [word.lower() for word in edited_n_gram]

                            mut_lemmed_n_gram = lemmed_n_gram[:]
                            del mut_lemmed_n_gram[word_idx]
                            lemmed_edited_n_gram = [word.lower() for word in mut_lemmed_n_gram]

                            mut_pos_list = n_gram_pos_list[:]
                            del mut_pos_list[word_idx]
                            edited_pos_tags = mut_pos_list

                            mut_case_list = n_gram_case_list[:]
                            del mut_case_list[word_idx]
                            edited_case_list = mut_case_list

                            # PASS N-GRAM THROUGH COLL TYPE FILTER TO FIND COLL TYPE:
                            edited_coll_type = coll_type_filter(lemmed_edited_n_gram, edited_pos_tags, case_ahead)

                            src_sent_term_bold_list = []
                            src_sent_coll_bold_list = []
                            idx = 0
                            for token in sent_words_raw:
                                if idx == q_idx:
                                    src_sent_term_bold_list.append('<b><i>' + token + '</i></b>')
                                    src_sent_coll_bold_list.append('<b><i>' + token + '</i></b>')
                                elif idx in [i for i in range(q_idx - words_behind, q_idx + words_ahead)  if i != q_idx and i != sent_words.index(word)]:
                                    src_sent_term_bold_list.append(token)
                                    src_sent_coll_bold_list.append('<b>' + token + '</b>')
                                else:
                                    src_sent_term_bold_list.append(token)
                                    src_sent_coll_bold_list.append(token)
                                idx += 1
                            src_sent_term_bold = ' '.join(src_sent_term_bold_list)
                            src_sent_coll_bold = ' '.join(src_sent_coll_bold_list)

                            meaning_dependent_info = []
                            count_case = False
                            for token in n_gram:
                                if count_case == True:
                                    meaning_dependent_info.append(n_gram_pos_list[n_gram.index(token)])
                                else:
                                    meaning_dependent_info.append('')
                                if n_gram_pos_list[n_gram.index(token)] == 'PREP':
                                    count_case = True

                            n_gram_package['Edited N-grams'].append({'Source' : source,
                                                                     'N-gram collocate positions' : [i for i in range(q_idx - words_behind, q_idx + words_ahead) if i != q_idx and i != sent_words.index(word)]
                                                                    })
                if words_behind == 0:
                    if n_gram_package not in start_b0:
                        start_b0.append(n_gram_package)
                elif words_behind == 1:
                    if n_gram_package not in start_b1:
                        start_b1.append(n_gram_package)
                elif words_behind == 2:
                    if n_gram_package not in start_b2:
                        start_b2.append(n_gram_package)
                elif words_behind == 3:
                    if n_gram_package not in start_b3:
                        start_b3.append(n_gram_package)
                elif words_behind == 4:
                    if n_gram_package not in start_b4:
                        start_b4.append(n_gram_package)

            words_ahead = words_ahead - 1
        words_behind += 1

    sent_package = {'Source' : source,
                    'Source sentence' : src_sent,
                    'Target sentence' : target_sent,
                    'PoS tag list' : pos_tag_list,
                    'Case list' : case_list,
                    'N-grams' : {'start_b0' : start_b0,
                                  'start_b1' : start_b1,
                                  'start_b2' : start_b2,
                                  'start_b3' : start_b3,
                                  'start_b4' : start_b4
                                 }
                    }

    return sent_package
start = time.time()
idx = 1
while idx <= 1:
    pp.pprint(colls_from_sents_df_row(results_df.iloc[6], query_forms = query_forms))
    idx += 1
end = time.time()
print(end - start)
def count_colls(sent_packages, query_forms, raw_min_coll_freq, est_min_coll_freq, est_eng_def_freq, raw_eng_def_freq, est_term_freq, raw_term_freq):

    n_grams_df = pd.DataFrame()
    colls_added = []

    for package in sent_packages:
        src_sent = package['Source sentence']
        target_sent = package['Target sentence']
        pos_tag_list = package['PoS tag list']
        case_list = package['Case list']
        n_grams_package = package['N-grams']

        for group, package in n_grams_package.items():

            coll_matched = False
            if package != []:
                for n_gram in package:

                        src = n_gram['Source']
                        src_sent_term_bold = n_gram['Source sentence with term bold']
                        src_sent_coll_bold = n_gram['Source sentence with coll bold']
                        coll_type = n_gram['Collocation type']
                        lemmed_coll_only = n_gram['Lemmed N-gram']
                        original_coll_only = n_gram['Original N-gram']
                        case_ahead = n_gram['Case ahead']
                        coll_pos_tags = tuple(n_gram['N-gram PoS tags'])
                        coll_cases = tuple(n_gram['N-gram cases'])
                        n_gram_idx = len(original_coll_only)

                        if coll_type == 'gram with case ahead':
                            lemmed_coll = tuple(lemmed_coll_only + [case_ahead])
                            original_coll = tuple(original_coll_only + [case_ahead])
                        else:
                            lemmed_coll = tuple(lemmed_coll_only)
                            original_coll = tuple(original_coll_only)

                        reorder_coll = False
                        if n_gram_idx == 2:
                            if ('ADVB' in coll_pos_tags) and (any(['INFN', 'PRTF', 'VERB']) in coll_pos_tags):
                                reordered_lemmed_coll = [lemmed_coll[1], lemmed_coll[0]]
                                reorder_coll = True
                        elif n_gram_idx == 3:
                            if (coll_pos_tags[0] == 'PREP') and (coll_pos_tags[1] == 'NOUN') and (coll_pos_tags[2] in ['INFN', 'PRTF', 'VERB']):
                                reordered_lemmed_coll = [lemmed_coll[2], lemmed_coll[0], lemmed_coll[1]]
                                reorder_coll = True

                        if lemmed_coll in colls_added:
                            n_grams_df = n_grams_df.append({'Source' : src,
                                                            'Source sentence with term bold' : src_sent_term_bold,
                                                            'Source sentence with coll bold' : src_sent_coll_bold,
                                                            'Target sentence' : target_sent,
                                                            'Original collocation' : original_coll,
                                                            'Lemmed collocation' : lemmed_coll,
                                                            'Collocation type' : coll_type
                                                            },
                                                              ignore_index = True)
                            coll_matched = True
                            colls_added.append(lemmed_coll)

                        elif (lemmed_coll not in colls_added) and (reorder_coll == True):
                            if reordered_lemmed_coll in colls_added:
                                n_grams_df = n_grams_df.append({'Source' : src,
                                                                'Source sentence with term bold' : src_sent_term_bold,
                                                                'Source sentence with coll bold' : src_sent_coll_bold,
                                                                'Target sentence' : target_sent,
                                                                'Original collocation' : original_coll,
                                                                'Lemmed collocation' : reordered_lemmed_coll,
                                                                'Collocation type' : coll_type
                                                                },
                                                                  ignore_index = True)
                                coll_matched = True
                                colls_added.append(reordered_lemmed_coll)

                        elif (lemmed_coll not in colls_added) and (reorder_coll == False):
                                n_grams_df = n_grams_df.append({'Source' : src,
                                                                'Source sentence with term bold' : src_sent_term_bold,
                                                                'Source sentence with coll bold' : src_sent_coll_bold,
                                                                'Target sentence' : target_sent,
                                                                'Original collocation' : original_coll,
                                                                'Lemmed collocation' : lemmed_coll,
                                                                'Collocation type' : coll_type
                                                                },
                                                                  ignore_index = True)
                                colls_added.append(lemmed_coll)

                        if coll_matched == False:
                            edited_n_grams = n_gram['Edited N-grams']
                            for edited_n_gram in edited_n_grams:

                                src = edited_n_gram['Source']
                                src_sent_term_bold = edited_n_gram['Source sentence with term bold']
                                src_sent_coll_bold = edited_n_gram['Source sentence with coll bold']
                                coll_type = edited_n_gram['Collocation type']
                                lemmed_coll_only = edited_n_gram['Lemmed Edited N-gram']
                                original_coll_only = edited_n_gram['Original Edited N-gram']
                                case_ahead = edited_n_gram['Case ahead']
                                coll_pos_tags = tuple(edited_n_gram['Edited N-gram PoS tags'])
                                coll_cases = tuple(edited_n_gram['Edited N-gram cases'])
                                n_gram_idx = len(original_coll_only)

                                if coll_type == 'gram with case ahead':
                                    lemmed_coll = tuple(lemmed_coll_only + [case_ahead])
                                    original_coll = tuple(original_coll_only + [case_ahead])
                                else:
                                    lemmed_coll = tuple(lemmed_coll_only)
                                    original_coll = tuple(original_coll_only)

                                reorder_coll = False
                                if n_gram_idx == 2:
                                    if ('ADVB' in coll_pos_tags) and (any(['INFN', 'PRTF', 'VERB']) in coll_pos_tags):
                                        reordered_lemmed_coll = [lemmed_coll[1], lemmed_coll[0]]
                                        reorder_coll = True
                                elif n_gram_idx == 3:
                                    if (coll_pos_tags[0] == 'PREP') and (coll_pos_tags[1] == 'NOUN') and (coll_pos_tags[2] in ['INFN', 'PRTF', 'VERB']):
                                        reordered_lemmed_coll = [lemmed_coll[2], lemmed_coll[0], lemmed_coll[1]]
                                        reorder_coll = True

                                if lemmed_coll in colls_added:
                                    n_grams_df = n_grams_df.append({'Source' : src,
                                                                    'Source sentence with term bold' : src_sent_term_bold,
                                                                    'Source sentence with coll bold' : src_sent_coll_bold,
                                                                    'Target sentence' : target_sent,
                                                                    'Original collocation' : original_coll,
                                                                    'Lemmed collocation' : lemmed_coll,
                                                                    'Collocation type' : coll_type
                                                                    },
                                                                      ignore_index = True)
                                    coll_matched = True
                                    colls_added.append(lemmed_coll)

                                elif (lemmed_coll not in colls_added) and (reorder_coll == True):
                                    if reordered_lemmed_coll in colls_added:
                                        n_grams_df = n_grams_df.append({'Source' : src,
                                                                        'Source sentence with term bold' : src_sent_term_bold,
                                                                        'Source sentence with coll bold' : src_sent_coll_bold,
                                                                        'Target sentence' : target_sent,
                                                                        'Original collocation' : original_coll,
                                                                        'Lemmed collocation' : reordered_lemmed_coll,
                                                                        'Collocation type' : coll_type
                                                                        },
                                                                          ignore_index = True)
                                        coll_matched = True
                                        colls_added.append(reordered_lemmed_coll)

                                elif (lemmed_coll not in colls_added) and (reorder_coll == False):
                                    n_grams_df = n_grams_df.append({'Source' : src,
                                                                    'Source sentence with term bold' : src_sent_term_bold,
                                                                    'Source sentence with coll bold' : src_sent_coll_bold,
                                                                    'Target sentence' : target_sent,
                                                                    'Original collocation' : original_coll,
                                                                    'Lemmed collocation' : lemmed_coll,
                                                                    'Collocation type' : coll_type
                                                                    },
                                                                      ignore_index = True)
                                    colls_added.append(lemmed_coll)


    def extract_eng_n_grams(df_row):
        target_sent = df_row['Target sentence']
        sent_tokens1 = target_sent.split(' ')
        sent_tokens = []
        for token in sent_tokens1:
            if token != '':
                sent_tokens.append(token)
        n_grams_package = []
        start_token_idx = 0
        while start_token_idx < sent_tokens.index(sent_tokens[-1]):
            start_token_list = []
            end_token_idx = sent_tokens.index(sent_tokens[-1])
            while start_token_idx < end_token_idx:
                n_gram_list = sent_tokens[start_token_idx:end_token_idx]
                lemmed_n_gram_list = n_gram_list
                #lemmed_n_gram_list = [english_lemmatizer.lemmatize(token) for token in n_gram_list]
                start_token_list.append({'Original n-gram' : n_gram_list,
                                         'Lemmed n-gram' : lemmed_n_gram_list,
                                         'Target sentence' : target_sent
                                        })
                end_token_idx = end_token_idx - 1
            n_grams_package.append(start_token_list)
            start_token_idx += 1
        return n_grams_package

    def top_eng_n_gram(series):
        n_grams_df = pd.DataFrame()
        colls_added = []
        for n_grams_package in series:
            for start_token_list in n_grams_package:
                coll_matched = False
                for n_gram_package in start_token_list:
                    n_gram_tuple = tuple(n_gram_package['Original n-gram'])
                    lemmed_n_gram_tuple = n_gram_package['Lemmed n-gram']
                    target_sent = n_gram_package['Target sentence']
                    if coll_matched == False:
                        # FILTER THE ENG N-GRAMS HERE:
                        if any(token in string.punctuation for token in lemmed_n_gram_tuple) == False:
                            contains_num = False
                            for token in lemmed_n_gram_tuple:
                                if any(char.isnumeric() for char in token):
                                    contains_num = True
                            if contains_num == False:
                                if lemmed_n_gram_tuple[0] not in eng_stop_words:
                                    if lemmed_n_gram_tuple[-1] not in eng_stop_words:
                                        ('--> PASSED THROUGH ENG COLL FILTER.')
                                        if lemmed_n_gram_tuple in colls_added:
                                            n_grams_df = n_grams_df.append({'Lemmed n-gram' : lemmed_n_gram_tuple,
                                                                            'Original n-gram' : n_gram_tuple,
                                                                            'Target sentence' : target_sent
                                                                           }, ignore_index = True)
                                            coll_matched = True
                                            colls_added.append(lemmed_n_gram_tuple)
                                        else:
                                            n_grams_df = n_grams_df.append({'Lemmed n-gram' : lemmed_n_gram_tuple,
                                                                            'Original n-gram' : n_gram_tuple,
                                                                            'Target sentence' : target_sent
                                                                           }, ignore_index = True)
                                            colls_added.append(lemmed_n_gram_tuple)
#                                     else:
#                                         print('COLL CONTAINS STOP WORDS AT END --> DIDN\'T PASS THROUGH ENG COLL FILTER.')
#                                 else:
#                                     print('COLL CONTAINS STOP WORDS AT START --> DIDN\'T PASS THROUGH ENG COLL FILTER.')
#                             else:
#                                 print('COLL CONTAINS NUMERAL --> DIDN\'T PASS THROUGH ENG COLL FILTER.')
#                         else:
#                             print('COLL CONTAINS PUNCT --> DIDN\'T PASS THROUGH ENG COLL FILTER.')

        if n_grams_df.empty == True:
            top_eng_coll_df_row = pd.DataFrame()
        else:
            group_idx = 1
            for name, group_df in n_grams_df.groupby(['Lemmed n-gram']):
                if group_idx == 1:
                    top_eng_coll_df_row = group_df.head(1)
                group_idx += 1

        return top_eng_coll_df_row

    colls_df = pd.DataFrame()
    if n_grams_df.empty == False:
        for name, group_df in n_grams_df.groupby(['Lemmed collocation']):
            top_n_gram_row = group_df.head(1)
            top_n_gram_row['Target sentence n-gram'] = top_n_gram_row['Target sentence']
            top_n_gram_row['Raw frequency'] = len(group_df.index)
            top_n_gram_row['Frequency'] = round(est_term_freq * len(group_df.index)/raw_term_freq)
            #top_n_gram_row['Source sentence with term bold'] = group_df.iloc[0]['Source sentence with term bold']
            #top_n_gram_row['Source sentence with coll bold'] = group_df.iloc[0]['Source sentence with coll bold']
            #top_n_gram_row['Target sentence'] = group_df.iloc[0]['Target sentence']

            other_sent_pairs_en = ''
            other_sent_pairs_ru_term_in_bold = ''
            other_sent_pairs_ru_coll_in_bold = ''
            other_sent_pairs_en_ru_term_in_bold = ''
            other_sent_pairs_ru_term_in_bold_en = ''
            other_sent_pairs_en_ru_coll_in_bold = ''
            other_sent_pairs_ru_coll_in_bold_en = ''
            idx = 1
            for index, row in group_df.iloc[1:].iterrows():
                other_sent_pairs_en += row['Target sentence'] + '<br><br>'
                other_sent_pairs_ru_term_in_bold += row['Source sentence with term bold'] + '<br><br>'
                other_sent_pairs_ru_coll_in_bold += row['Source sentence with coll bold'] + '<br><br>'
                other_sent_pairs_en_ru_term_in_bold += str(row['Target sentence']) + '<br>' + '<font color=\"green\">' + row['Source sentence with term bold'] + '</font>' + '<br><br>'
                other_sent_pairs_ru_term_in_bold_en += row['Source sentence with term bold'] + '<br>' + '<font color=\"green\">' + row['Target sentence'] + '</font>' + '<br><br>'
                other_sent_pairs_en_ru_coll_in_bold += str(row['Target sentence']) + '<br>' + '<font color=\"green\">' + row['Source sentence with coll bold'] + '</font>' + '<br><br>'
                other_sent_pairs_ru_coll_in_bold_en += row['Source sentence with coll bold'] + '<br>' + '<font color=\"green\">' + row['Target sentence'] + '</font>' + '<br><br>'
                idx += 1
                if idx == 7:
                    break

            top_n_gram_row['Other sentence pairs en'] = other_sent_pairs_en
            top_n_gram_row['Other sentence pairs ru term in bold'] = other_sent_pairs_ru_term_in_bold
            top_n_gram_row['Other sentence pairs ru coll in bold'] = other_sent_pairs_ru_coll_in_bold
            top_n_gram_row['Other sentence pairs en ru term in bold'] = other_sent_pairs_en_ru_term_in_bold
            top_n_gram_row['Other sentence pairs ru term in bold en'] = other_sent_pairs_ru_term_in_bold_en
            top_n_gram_row['Other sentence pairs en ru coll in bold'] = other_sent_pairs_en_ru_coll_in_bold
            top_n_gram_row['Other sentence pairs ru coll in bold en'] = other_sent_pairs_ru_coll_in_bold_en

            colls_df = colls_df.append(top_n_gram_row, ignore_index = True)

    colls_df = colls_df.sort_values('Frequency', ascending=False)

    gram_colls_df = colls_df[colls_df['Collocation type'].isin(['gram with case ahead', 'gram without case ahead'])]
    lex_colls_df = colls_df[colls_df['Collocation type']=='lex']

    print('\n\tCOUNT COLLS: EST MIN COLL FREQ:', est_min_coll_freq)
    print('\tCOUNT COLLS: RAW MIN COLL FREQ:', raw_min_coll_freq)

    print('\tCOUNT COLLS: FILTERING FOR LEX COLLS ABOVE MIN COLL FREQ')
    if lex_colls_df[(lex_colls_df['Frequency']>=est_min_coll_freq) & (lex_colls_df['Raw frequency']>= raw_min_coll_freq)].empty == False:
        return_df = lex_colls_df[(lex_colls_df['Frequency']>=est_min_coll_freq) & (lex_colls_df['Raw frequency']>= raw_min_coll_freq)]
        default_to_top_coll = False
    else:
        default_to_top_coll = True
        print('\tCOUNT COLLS: FILTERING FOR GRAM COLLS ABOVE MIN COLL FREQ')
        if gram_colls_df[(gram_colls_df['Frequency']>=est_min_coll_freq) & (gram_colls_df['Raw frequency']>= raw_min_coll_freq)].empty == False:
            return_df = gram_colls_df[(gram_colls_df['Frequency']>=est_min_coll_freq) & (gram_colls_df['Raw frequency']>= raw_min_coll_freq)].head(1)
        else:
            print('\tCOUNT COLLS: FILTERING FOR DEFAULT LEX COLL BELOW MIN COLL FREQ')
            if lex_colls_df.empty == False:
                return_df = lex_colls_df.head(1)
            else:
                print('\tCOUNT COLLS: FILTERING FOR DEFAULT GRAM COLLS BELOW MIN COLL FREQ')
                if gram_colls_df.empty == False:
                    return_df = gram_colls_df.head(1)
                else:
                    print('\tCOUNT COLLS: FILTERING FOR NO PUNCT COLLS')
                    no_punct_df = colls_df[colls_df['Collocation type']!='punct']
                    if no_punct_df.empty == False:
                        return_df = no_punct_df.head(1)
                    else:
                        print('\tCOUNT COLLS: DEFAULTING TO FIRST ROW IN COLLS DF')
                        if colls_df.empty == False:
                            return_df = colls_df.head(1)
                        else:
                            print('\tCOUNT_COLLS: NO COLLOCATIONS FOUND.')

    return lex_colls_df, return_df, gram_colls_df.head(3), default_to_top_coll
