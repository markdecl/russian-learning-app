from fsplit.filesplit import FileSplit

fs = FileSplit(file='C:\\Users\\MdeCL\\Desktop\\opus tmx files\\Russian\\UNPC (need to split).tmx', splitsize=700000000, output_dir='C:\\Users\\MdeCL\\Desktop\\UNPC split files')

fs.split()


parallel_corp_folder = 'data\\parallel_corpus_files'

num_sources = 0
for tmx_folder in os.listdir(parallel_corp_folder):
    num_sources += 1

para_texts_df = pd.DataFrame()

ru_sents = []
en_sents = []
chunk_idx = 1

for tmx_folder in os.listdir(parallel_corp_folder):
    sent_idx = 1

    print(tmx_folder)

    with open(parallel_corp_folder + tmx_folder, 'rb') as fin:
        tmx_file = tmxfile(fin, 'en', 'ru')

        for node in tmx_file.unit_iter():
            try:
                node_target_sent = node.gettarget()
                if 16 < len(node_target_sent) < 75:
                    en_sents.append(node.getsource())
                    ru_sents.append(node_target_sent)
                    sent_idx += 1
                    chunk_idx += 1
            except Exception:
                print(node)

            if chunk_idx > 20000:
                para_text_df = pd.DataFrame({'Source sentence' : ru_sents,
                                            'Target sentence' : en_sents})
                para_text_df['Source'] = tmx_folder
                para_texts_df = para_texts_df.append(para_text_df, ignore_index = True)
                print('20,000 sentences appended to para_texts_df.')
                ru_sents = []
                en_sents = []
                chunk_idx = 1

        print(sent_idx)



# Randomly order DataFrame rows
para_texts_df = para_texts_df.sample(frac=1).reset_index(drop=True)


# Clean, standardise and preprocess parallel corpus
para_texts_df = para_texts_df.dropna()

# Drop duplicates in source and target sentences
para_texts_df.drop_duplicates('Source sentence', inplace=True)
para_texts_df.drop_duplicates('Target sentence', inplace=True)

def filter_sent_quality(df_row):
    return_bool = True
    src_sent = df_row['Source sentence']
    src_sent_tokens = src_sent.split(' ')
    target_sent = df_row['Target sentence']
    target_sent_tokens = target_sent.split(' ')
    if len(src_sent_tokens) > 2.2 * len(target_sent_tokens) or len(src_sent_tokens) * 2 < len(target_sent_tokens):
        return_bool = False
    if sum(c.isdigit() for c in src_sent) >= 7:
        return_bool = False
    if len(src_sent) < 22:
        return_bool = False

    return return_bool


para_texts_df = para_texts_df[para_texts_df.apply(filter_sent_quality, axis=1)]

def bare_source_sent(sent):
    sent = sent.lower()
    sent = [char for char in sent if char.isalpha() or char.isspace()]
    sent = ''.join(sent)
    return sent

# Delete rows whose first 20 characters are the same as those of another row
para_texts_df['Bare source sentence'] = para_texts_df['Source sentence'].apply(bare_source_sent)
para_texts_df['Bare source sentence first chars'] = para_texts_df['Bare source sentence'].str[:20]
para_texts_df.drop_duplicates('Bare source sentence first chars', inplace=True)
para_texts_df = para_texts_df.drop(columns = ['Bare source sentence', 'Bare source sentence first chars'])

def stand_sent(sent):
    sent = ''.join([char for char in sent if (char.isalpha() or char.isdigit() or char.isspace() or char in string.punctuation)])
    sent = sent.strip().lower()
    sent = ' ' + sent + ' '
    puncts = [',', '.', ';', ':', '!', '?', '(', ')', '{', '}', '\"', '\'', '[', ']']
    for punct in puncts:
        sent = sent.replace(punct, ' ' + punct + ' ')
    sent = sent.replace('  ', ' ').replace('   ', ' ').strip()

    return sent

stand_src_sents = para_texts_df['Source sentence'].apply(stand_sent)
para_texts_df['Standardised source sentence'] = stand_src_sents

def stand_en_sent(sent):

    sent = ''.join([char for char in sent if (char.isalpha() or char.isdigit() or char.isspace() or char in string.punctuation)])
    if type(sent) == str:
        sent = sent.strip().lower()
        sent = ' ' + sent + ' '
        elisions = {'that\'s' : 'that is',
                    'it\'s' : 'it is',
                    'what\'s' : 'what is',
                    'who\'s' : 'who is',
                    'I\'m' : 'I am',
                    'I\'ve' : 'I have',
                    'he\'s' : 'he is',
                    'she\'s' : 'she is',
                    'isn\'t' : 'is not',
                    'won\'t' : 'will not',
                    'gonna' : 'going to',
                    '\'ve' : ' have',
                    '\'re' : ' are'
                   }
        for elision_key in elisions.keys():
            sent = sent.replace(elision_key, elisions[elision_key])
        puncts = [',', '.', ';', ':', '!', '?', '(', ')', '{', '}', '\"', '\'', '[', ']']
        for punct in puncts:
            sent = sent.replace(punct, ' ' + punct + ' ')
        sent = sent.replace('  ', ' ').replace('   ', ' ').strip()

    return sent

stand_target_sents = para_texts_df['Target sentence'].apply(stand_en_sent)
para_texts_df['Standardised target sentence'] = stand_target_sents

# Pre-process the source sentences to make subsequent processing faster:
def preprocess_sent(sent_df_row):

    sent = sent_df_row['Standardised source sentence'].replace('  ', ' ').replace('   ', ' ').strip()

    lemmed_sent = []
    coll_lemmed_sent = []
    pos_tag_list = []
    cases_list = []

    sent_tokens = sent.split(' ')
    lem = True
    for token in sent_tokens:
        p = morph.parse(token)[0]
        lemmed_sent.append(p.normal_form)
        pos = str(p.tag.POS)
        if pos != None:
            pos_tag_list.append(pos)
        else:
            pos_tag_list.append('None')
        case = p.tag.case
        if case != None:
            cases_list.append(case)
        else:
            cases_list.append('None')
        if lem == True:
            coll_lemmed_sent.append(p.normal_form)
        else:
            coll_lemmed_sent.append(token)
        if pos == 'PREP':
            lem = False
        elif pos in ['INFN', 'VERB', 'NOUN']:
            lem = True

    lemmed_sent = ' '.join(lemmed_sent)
    coll_lemmed_sent = ' '.join(coll_lemmed_sent)
    pos_tag_list = ' '.join(pos_tag_list)
    cases_list = ' '.join(cases_list)

    return lemmed_sent, coll_lemmed_sent, pos_tag_list, cases_list

start = time.time()
l_df = para_texts_df
lemmed_sents, coll_lemmed_sents, pos_tag_list, case_list = zip(*l_df.apply(preprocess_sent, axis=1))
l_df.insert(1, 'Lemmed source sentence', list(lemmed_sents))
l_df.insert(2, 'Coll lemmed source sentence', coll_lemmed_sents)
l_df.insert(3, 'Source sentence PoS tags', pos_tag_list)
l_df.insert(3, 'Source sentence cases', case_list)
end = time.time()
print(end - start)
para_texts_df = para_texts_df[~para_texts_df['Lemmed source sentence'].isnull()]
para_texts_df.head()

# Explore the data to find disparities between estimated frequency and frequency in parallel corpus:

for index, row in para_texts_df.iloc[100:200].iterrows():
    print(row['Standardised source sentence'])
    print(row['Standardised target sentence'])
    print('\n')


anomalies_df = pd.DataFrame()

for index, row in rnc_freq_list.iloc[2000:2010].iterrows():

    estimated_freq = row['Estimated frequency']
    query = row['Word']
    query_pos_full = row['PoS tag']
    print(index)
    print(query)

    query_forms = []
    query_parse = morph.parse(query)[0]
    for word_form in query_parse.lexeme:
        form = word_form[0]
        query_forms.append(form)
        if 'ё' in form:
            query_forms.append(form.replace('ё', 'е'))
    query_forms = list(set(query_forms))

    results_df = pd.DataFrame()
    for query_form in query_forms:
        query_form_results_df = para_texts_df[para_texts_df['Standardised source sentence'].str.contains(' ' + query_form + ' ', regex = False)]
        results_df = results_df.append(query_form_results_df)
#     p = morph.parse(query)[0]
#     lemmed_query = p.normal_form
#     results_df = reduced_df[reduced_df['Lemmed source sentence'].str.contains(' ' + lemmed_query + ' ', regex = False)]
    results_df = results_df.drop_duplicates('Source sentence')
    print('NUMBER OF CONCORDANCE RESULTS AFTER DELETING DUPLICATES:', len(results_df.index))
    concordance_freq = len(results_df.iloc[:])

    open_subtitles_freq = len(results_df[results_df['Source'].str.contains('OpenSubtitles')])
    un_freq = len(results_df[results_df['Source'].str.contains('MultiUN')])
    qed_freq = len(results_df[results_df['Source'].str.contains('QED')])
    wiki_freq = len(results_df[results_df['Source'].str.contains('Wikipedia')])

    anomalies_df = anomalies_df.append({
                                        'Term' : query,
                                        'Estimated frequency' : estimated_freq,
                                        'Actual frequency' : concordance_freq,
                                        'Open Subtitles frequency' : open_subtitles_freq,
                                        'Multi UN frequency' : un_freq,
                                        'QED frequency' : qed_freq,
                                        'Wikipedia frequency' : wiki_freq
                                       },
                                        ignore_index = True)

    print('\n')

anomalies_df['Anomaly score'] = anomalies_df['Estimated frequency'] / anomalies_df['Actual frequency']
anomalies_df.sort_values('Anomaly score', ascending=False)

for group_name, group_df in para_texts_df.groupby('Source'):
    print(group_name)
    for index, row in group_df.iloc[0:30].iterrows():
        print(row['Standardised source sentence'])
        print(row['Standardised target sentence'])
        print('\n')
    print('\n\n')

Add a column for the sentences' genre/register and create a function to return a register tag from a list of registers:
def get_register(source):
    register_dict = {
        'GlobalVoices' :
        'MultiUN_1' : 'political',
        'MultiUN_2' : 'political',
        'MultiUN_3' : 'political',
        'MultiUN_4' : 'political',
        'MultiUN_5' : 'political',
        'MultiUN_6' : 'political',
        'MultiUN_7' : 'political',
        'MultiUN_8' : 'political',
        'OpenSubtitles_1' : 'informal',
        'OpenSubtitles_2' : 'informal',
        'OpenSubtitles_4' : 'informal',
        'QED' : 'journalism'
        'TED2013' : 'journalism',
        'Tanzil.tmx' :
        'Tatoeba' : 'general'
        'Wikipedia' : 'general'
    }
for group_name, group_df in para_texts_df.groupby('Source'):
    print(group_name)

# Save para_texts_df to csv:
para_texts_df.to_csv(desktop_dir + '\\para_texts_df.csv', sep = '\t')

# Load para_texts_df from csv:
para_texts_df = pd.read_csv(desktop_dir + '\\para_texts_df.csv', sep = '\t')
