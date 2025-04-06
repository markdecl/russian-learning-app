# Perform analysis of each term in frequency list and write flashcards:
# Search the info about a word in the corpus and otherwise online:

# Semantic analysis
# Collocational analysis
# Grammatical analysis
# Register / genre analysis

TARGET_LANGUAGE_TO_ENGLISH_NOTE_TYPE = genanki.Model(
  1607392319,
  'TL-EN TYPE TEST v3',
  fields=[
    {'name': 'Scaled frequency'},
    {'name' : 'Frequency rank'},
    {'name' : 'Term/collocation test'},
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'Term with accent'},
    {'name': 'Distinguishing grammatical info'},
    {'name' : 'Conjugation and declension info'},
    {'name' : 'Top three grammatical collocations'},
    {'name': 'Definition being tested'},
    {'name': 'Other definitions'},
    {'name': 'Source sentence'},
    {'name': 'Target sentence'},
    {'name': 'Sentence source'},
    {'name' : 'Other sentence pairs ru'},
    {'name' : 'Other sentence pairs both'}
  ],
  templates=[
    {
      'name': 'TL-EN CARD TYPE',
      'qfmt': '<font>{{Term/collocation test}}<br><br><font size="+6">{{Term with accent}}</font><br><font size="-1">{{Conjugation and declension info}}<br>{{Distinguishing grammatical info}}<br>{{Top three grammatical collocations}}<br><hr><font size="+1"><font color="navy"><b>____</b><br>{{Other definitions}}</font><br><hr>{{Source sentence}}{{type:Target sentence}}<br>{{Other sentence pairs ru}}</font>',
      'afmt': '<font>{{Term/collocation test}}<br><br><font size="+6">{{Term with accent}}</font><br><font size="-1">{{Conjugation and declension info}}<br>{{Distinguishing grammatical info}}<br>{{Top three grammatical collocations}}<br><hr><font size="+1"><font color="navy"><b>{{Definition being tested}}</b><br>{{Other definitions}}</font><br><hr>{{Source sentence}}<br><font color="green">{{Target sentence}}</font>{{type:Target sentence}}<br>{{Other sentence pairs both}}</font>',
    }
  ]
)

en_tl_note_type = genanki.Model(
  1607392320,
  'EN-TL TYPE TEST v3',
  fields=[
    {'name': 'Scaled frequency'},
    {'name' : 'Frequency rank'},
    {'name' : 'Term/collocation test'},
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'Term with accent'},
    {'name': 'Distinguishing grammatical info'},
    {'name' : 'Conjugation and declension info'},
    {'name' : 'Top three grammatical collocations'},
    {'name': 'Definition being tested'},
    {'name': 'Other definitions'},
    {'name': 'Source sentence'},
    {'name': 'Target sentence'},
    {'name': 'Sentence source'},
    {'name' : 'Other sentence pairs en'},
    {'name' : 'Other sentence pairs both'}
  ],
  templates=[
    {
      'name': 'EN-TL CARD TYPE',
      'qfmt': '<font>{{Term/collocation test}}<br><br><font size="+6">______</font><br><br><font size="-1">{{Distinguishing grammatical info}}<br><hr><font size="+1"><font color="navy"><b>{{Definition being tested}}</b><br>{{Other definitions}}</font><br><hr>{{Target sentence}}{{type:Source sentence}}<br>{{Other sentence pairs en}}</font>',
      'afmt': '<font>{{Term/collocation test}}<br><br><font size="+6">{{Term with accent}}</font><br><font size="-1">{{Conjugation and declension info}}<br>{{Distinguishing grammatical info}}<br>{{Top three grammatical collocations}}<br><hr><font size="+1"><font color="navy"><b>{{Definition being tested}}</b><br>{{Other definitions}}</font><br><hr>{{Target sentence}}<br><font color="green">{{Source sentence}}</font>{{type:Source sentence}}<br>{{Other sentence pairs both}}</font>',
    }
  ]
)
rnc_freq_list[rnc_freq_list['Word']=='иней']
colls_written_to_cards = []
start_freq_rank = 4500
end_freq_rank = 5000
limited_freq_list = rnc_freq_list.iloc[start_freq_rank:end_freq_rank]
reduced_df_size = 8000000
max_concordance_results = 400
est_min_coll_freq = 370
raw_min_coll_freq = 2

deck_name = 'Russian Vocab ' + str(start_freq_rank) + '-' + str(end_freq_rank)

my_deck = genanki.Deck(2059400110, deck_name)

reduced_df = para_texts_df.iloc[0:reduced_df_size]

for index, row in limited_freq_list.iterrows():

    start_time = time.time()

    print(index)
    query = row['Word']
    print(query)
    freq_rank = row['Frequency rank']
    estimated_freq = row['Estimated frequency']
    print('TERM ESTIMATED FREQUENCY:', str(estimated_freq))
    query_pos_full = row['PoS tag']

    return_dict = eng_trans_and_syns(query, query_pos_full)
    inflected_eng_defs = return_dict['inflected_eng_defs']
    term_gender_colour = return_dict['term_gender_colour']
    term_with_accent = return_dict['term_with_accent']
    case_taken = return_dict['case_taken']
    disting_gram_info = return_dict['disting_gram_info']
    conjugation_declension_info = ', '.join(return_dict['conjugation_declension_info'])

    query_forms = []
    query_parse = morph.parse(query)[0]
    for word_form in query_parse.lexeme:
        form = word_form[0]
        query_forms.append(form)
        if 'ё' in form:
            query_forms.append(form.replace('ё', 'е'))
    query_forms = list(set(query_forms))

    p = morph.parse(query)[0]
    lemmed_query = p.normal_form
    results_df = reduced_df[reduced_df['Lemmed source sentence'].str.contains(' ' + lemmed_query + ' ', regex = False)]

    print('\n\nNUMBER OF CONCORDANCE RESULTS BEFORE DELETING DUPLICATES:', len(results_df.index))
    results_df = results_df.drop_duplicates('Source sentence')
    print('NUMBER OF CONCORDANCE RESULTS AFTER DELETING DUPLICATES:', len(results_df.index))
    concordance_freq = len(results_df.iloc[:])
    if len(results_df.index) > max_concordance_results:
        print('RESULTS DF REDUCED TO ' + str(max_concordance_results) + ' PAIRED SENTENCES.')
        results_df = results_df.iloc[0:max_concordance_results]
    reduced_concordance_freq = len(results_df.iloc[:])

    results_df['English definition'] = 'Unmatched'
    eng_def_idx = 1
    for basic_def, all_forms in inflected_eng_defs.items():
        for form in all_forms:
            form = form.strip().replace('.', ' ')
            form_wds = form.split(' ')
            wd_count = len(form_wds)
            if wd_count == 1:
                results_df[results_df['Standardised target sentence'].str.contains(' ' +  form + ' ', regex=False)] = results_df[results_df['Standardised target sentence'].str.contains(' ' +  form + ' ', regex=False)].replace('Unmatched', basic_def)
            elif wd_count == 2:
                results_df[results_df['Standardised target sentence'].str.contains(' ' +  form + ' ', regex=False)]['English definition'] = results_df[results_df['Standardised target sentence'].str.contains(' ' +  form + ' ', regex=False)]['English definition'].replace('Unmatched', basic_def)
                results_df[results_df['Standardised target sentence'].str.contains(' '+form_wds[0]+'.*'+form_wds[1]+' ', regex=True)]['English definition'] = results_df[results_df['Standardised target sentence'].str.contains(' '+form_wds[0]+'.*'+form_wds[1]+' ', regex=True)]['English definition'].replace('Unmatched', basic_def)
            elif wd_count == 3:
                results_df[results_df['Standardised target sentence'].str.contains(' ' +  form + ' ', regex=False)]['English definition'] = results_df[results_df['Standardised target sentence'].str.contains(' ' +  form + ' ', regex=False)]['English definition'].replace('Unmatched', basic_def)
                results_df[results_df['Standardised target sentence'].str.contains(' '+form_wds[0]+'.*'+form_wds[1]+' '+'.*'+form_wds[2]+' ', regex=True)]['English definition'] = results_df[results_df['Standardised target sentence'].str.contains(' '+form_wds[0]+'.*'+form_wds[1]+' '+'.*'+form_wds[2]+' ', regex=True)]['English definition'].replace('Unmatched', basic_def)

    print('\nRESULTS_DF.UNIQUE()', results_df['English definition'].unique())
    eng_def_idx = 1
    print('\nENG DEF VALUE COUNTS:')
    print(results_df[results_df['English definition']!='Unmatched']['English definition'].value_counts())

    basic_defs = results_df[results_df['English definition']!='Unmatched']['English definition'].value_counts().index.tolist()
    for eng_def in basic_defs:
        print('\nENG DEF INDEX:', eng_def_idx)
        print('ENG DEF:', eng_def)
        eng_def_df = results_df[results_df['English definition']==eng_def]
        if eng_def_df.empty == True:
            pass
        else:
            eng_def_df = eng_def_df.drop_duplicates('Source sentence')
            print('NUMBER OF SENTENCES FOR THIS ENGLISH DEFINITION:', len(eng_def_df.index))
            if eng_def_idx == 1:
                eng_def_freq = estimated_freq
            else:
                eng_def_freq = round(estimated_freq * (len(eng_def_df.index)/reduced_concordance_freq))
            print('ESTIMATED ENG DEF FREQUENCY:', eng_def_freq)

            if eng_def_freq < est_min_coll_freq:
                print('ESTIMATED ENGLISH DEFINITION FREQUENCY IS LOWER THAN MINIMUM COLL FREQUENCY --> NOT WRITING ANY FLASHCARDS FOR IT.')
            else:
                q_forms = query_forms
                return_series = eng_def_df.apply(colls_from_sents_df_row, query_forms=q_forms, axis=1)
                lex_colls_df, eng_def_colls_df, top_three_gram_colls_df, default_to_top_coll = count_colls(return_series.tolist(), q_forms, raw_min_coll_freq, est_min_coll_freq, eng_def_freq, len(eng_def_df.index), estimated_freq, reduced_concordance_freq)

                case_colour_dict = {'gent' : 'green',
                                    'datv' : 'purple',
                                   'loct' : 'blue',
                                   'ablt' : 'aqua'}
                gram_coll_list = []
                for index, row in top_three_gram_colls_df.iterrows():
                    gram_coll = ' '.join(row['Original collocation'])
                    for key, value in case_colour_dict.items():
                        if key in gram_coll:
                            gram_coll = gram_coll.replace(key, '<font color="' + value + '">' + key + '</font>')
                    gram_coll_list.append(gram_coll + ' ' + str(row['Raw frequency']))
                top_three_gram_colls = ' | '.join(gram_coll_list)
                print('TOP THREE GRAM COLLS:', top_three_gram_colls)
                print('\n')

                if eng_def_colls_df.empty == True:
                    print('ENG DEF COLLS DF RETURNED EMPTY.')
                else:
                    # Create cards for the English definition only
                    print('CARDS FOR ENG DEF ONLY:')
                    row = eng_def_colls_df.iloc[0]
                    card_freq = eng_def_freq
                    term_or_collocation = 'Term'
                    tl_test = query
                    en_test = eng_def
                    other_defs = '<br>'.join([item for item in basic_defs if item != eng_def])

                    source_sent_one = row['Source sentence with term bold']
                    target_sent_one = row['Target sentence']

                    other_sent_pairs_en = ''
                    other_sent_pairs_ru_term_in_bold = ''
                    other_sent_pairs_ru_coll_in_bold = ''
                    other_sent_pairs_en_ru_term_in_bold = ''
                    other_sent_pairs_ru_term_in_bold_en = ''
                    other_sent_pairs_en_ru_coll_in_bold = ''
                    other_sent_pairs_ru_coll_in_bold_en = ''
                    idx = 1
                    for index, lex_coll_row in lex_colls_df.iloc[1:].iterrows():
                        other_sent_pairs_en += lex_coll_row['Target sentence'] + '<br><br>'
                        other_sent_pairs_ru_term_in_bold += lex_coll_row['Source sentence with term bold'] + '<br><br>'
                        other_sent_pairs_ru_coll_in_bold += lex_coll_row['Source sentence with coll bold'] + '<br><br>'
                        other_sent_pairs_en_ru_term_in_bold += str(lex_coll_row['Target sentence']) + '<br>' + '<font color=\"green\">' + lex_coll_row['Source sentence with term bold'] + '</font>' + '<br><br>'
                        other_sent_pairs_ru_term_in_bold_en += lex_coll_row['Source sentence with term bold'] + '<br>' + '<font color=\"green\">' + lex_coll_row['Target sentence'] + '</font>' + '<br><br>'
                        other_sent_pairs_en_ru_coll_in_bold += str(lex_coll_row['Target sentence']) + '<br>' + '<font color=\"green\">' + lex_coll_row['Source sentence with coll bold'] + '</font>' + '<br><br>'
                        other_sent_pairs_ru_coll_in_bold_en += lex_coll_row['Source sentence with coll bold'] + '<br>' + '<font color=\"green\">' + lex_coll_row['Target sentence'] + '</font>' + '<br><br>'
                        idx += 1
                        if idx == 7:
                            break

                    print('\n\tCOLLOCATION TYPE:', row['Collocation type'])
                    print('\tRAW FREQUENCY:', row['Raw frequency'])
                    print('\tSCALED FREQUENCY:', row['Frequency'])
                    print('\tLEMMED COLLOCATION:', row['Lemmed collocation'])
                    print('\tORIGINAL COLLOCATION:', row['Original collocation'])
                    print('\tCARD FREQUENCY:', card_freq)
                    print('\n')

                    tl_en_note = genanki.Note(
                    model = tl_en_note_type,
                    fields = [str(card_freq),
                             str(freq_rank) + ' d' + str(eng_def_idx),
                             term_or_collocation,
                              tl_test,
                              en_test,
                              '<font color=\"' + term_gender_colour + '\">' + term_with_accent + '</font>' + case_taken,
                              disting_gram_info,
                              conjugation_declension_info,
                              top_three_gram_colls,
                              eng_def,
                              other_defs,
                              source_sent_one,
                              target_sent_one,
                              str(row['Source']),
                              other_sent_pairs_ru_term_in_bold,
                              other_sent_pairs_ru_term_in_bold_en
                                ]
                    )

                    my_deck.add_note(tl_en_note)

                    en_tl_note = genanki.Note(
                    model = en_tl_note_type,
                    fields = [str(round(card_freq * 1.05)),
                            str(freq_rank) + ' d' + str(eng_def_idx),
                             term_or_collocation,
                              en_test,
                              tl_test,
                              '<font color=\"' + term_gender_colour + '\">' + term_with_accent + '</font>' + case_taken,
                              disting_gram_info,
                              conjugation_declension_info,
                              top_three_gram_colls,
                              eng_def,
                              other_defs,
                              source_sent_one,
                              target_sent_one,
                              str(row['Source']),
                              other_sent_pairs_en,
                              other_sent_pairs_en_ru_term_in_bold
                                ]
                    )

                    my_deck.add_note(en_tl_note)

                    # Create cards for each collocation of the English definition
                    if default_to_top_coll == False:
                        coll_idx = 1
                        for index, row in eng_def_colls_df.iterrows():

                            print('COLL INDEX:', coll_idx)
                            card_freq = row['Frequency']
                            term_or_collocation = 'Collocation'
                            tl_test = ' '.join(row['Original collocation'])
                            en_test = row['Target sentence']
                            other_defs = '<br>'.join([item for item in basic_defs if item != eng_def])

                            source_sent_one = row['Source sentence with coll bold']
                            target_sent_one = row['Target sentence']

                            other_sent_pairs_en = row['Other sentence pairs en']
                            other_sent_pairs_ru_term_in_bold = row['Other sentence pairs ru term in bold']
                            other_sent_pairs_ru_coll_in_bold = row['Other sentence pairs ru coll in bold']
                            other_sent_pairs_en_ru_term_in_bold = row['Other sentence pairs en ru term in bold']
                            other_sent_pairs_ru_term_in_bold_en = row['Other sentence pairs ru term in bold en']
                            other_sent_pairs_en_ru_coll_in_bold = row['Other sentence pairs en ru coll in bold']
                            other_sent_pairs_ru_coll_in_bold_en = row['Other sentence pairs ru coll in bold en']

                            print('\n\tCOLLOCATION TYPE:', row['Collocation type'])
                            print('\tRAW FREQUENCY:', row['Raw frequency'])
                            print('\tSCALED FREQUENCY:', row['Frequency'])
                            print('\tLEMMED COLLOCATION:', row['Lemmed collocation'])
                            print('\tORIGINAL COLLOCATION:', row['Original collocation'])
                            print('\tCARD FREQUENCY:', card_freq)
                            print('\n')

                            # Check if a card for the collocation has already been written
                            if row['Lemmed collocation'] not in colls_written_to_cards:

                                colls_written_to_cards.append(row['Lemmed collocation'])

                                tl_en_note = genanki.Note(
                                model = tl_en_note_type,
                                fields = [str(card_freq),
                                         str(freq_rank) + ' d' + str(eng_def_idx) + ' c' + str(coll_idx),
                                         term_or_collocation,
                                          tl_test,
                                          en_test,
                                          '<font color=\"' + term_gender_colour + '\">' + term_with_accent + '</font>' + case_taken,
                                          disting_gram_info,
                                          conjugation_declension_info,
                                          top_three_gram_colls,
                                          eng_def,
                                          other_defs,
                                          source_sent_one,
                                          target_sent_one,
                                          str(row['Source']),
                                          other_sent_pairs_ru_coll_in_bold,
                                          other_sent_pairs_ru_coll_in_bold_en
                                            ]
                                )

                                my_deck.add_note(tl_en_note)

                                en_tl_note = genanki.Note(
                                model = en_tl_note_type,
                                fields = [str(round(card_freq * 1.05)),
                                        str(freq_rank) + ' d' + str(eng_def_idx) + ' c' + str(coll_idx),
                                         term_or_collocation,
                                          en_test,
                                          tl_test,
                                          '<font color=\"' + term_gender_colour + '\">' + term_with_accent + '</font>' + case_taken,
                                          disting_gram_info,
                                          conjugation_declension_info,
                                          top_three_gram_colls,
                                          eng_def,
                                          other_defs,
                                        source_sent_one,
                                          target_sent_one,
                                          str(row['Source']),
                                          other_sent_pairs_en,
                                          other_sent_pairs_en_ru_coll_in_bold
                                            ]
                                )

                                my_deck.add_note(en_tl_note)

                            coll_idx += 1

        eng_def_idx += 1

    print('\n\nNON MATCHED SENTS:')
    print(len(results_df[results_df['English definition']=='Unmatched'].index))
    # Find the top collocations in the unmatched sentences
    if len(results_df[results_df['English definition']=='Unmatched'].index) != 0:
        est_non_matched_sents_freq = round(estimated_freq * len(results_df.index)/concordance_freq)
        q_forms = query_forms
        return_series = results_df[results_df['English definition']=='Unmatched'].apply(colls_from_sents_df_row, query_forms=q_forms, axis=1)
        lex_colls_df, non_matched_sents_colls_df, top_three_gram_colls_df, default_to_top_coll = count_colls(return_series.tolist(), q_forms, raw_min_coll_freq, est_min_coll_freq, est_non_matched_sents_freq, len(results_df[results_df['English definition']=='Unmatched'].index), estimated_freq, reduced_concordance_freq)

        top_three_gram_colls = ''

        if default_to_top_coll == True:
            print('NO COLLS FOUND ABOVE MINIMUM FREQUENCIES --> NOT WRITING ANY FLASHCARDS.')
        else:
            if non_matched_sents_colls_df.empty == True:
                print('NON MATCHED SENTS COLLS DF RETURNED EMPTY.')
            else:
                coll_idx = 1
                for index, row in non_matched_sents_colls_df.iterrows():

                    term_or_collocation = 'Collocation'
                    eng_def = ''
                    other_defs = '<br>'.join(basic_defs)
                    card_freq = row['Frequency']
                    tl_test = ' '.join(row['Original collocation'])
                    en_test = row['Target sentence']

                    source_sent_one = row['Source sentence with coll bold']
                    target_sent_one = row['Target sentence']

                    other_sent_pairs_en = row['Other sentence pairs en']
                    other_sent_pairs_ru_term_in_bold = row['Other sentence pairs ru term in bold']
                    other_sent_pairs_ru_coll_in_bold = row['Other sentence pairs ru coll in bold']
                    other_sent_pairs_en_ru_term_in_bold = row['Other sentence pairs en ru term in bold']
                    other_sent_pairs_ru_term_in_bold_en = row['Other sentence pairs ru term in bold en']
                    other_sent_pairs_en_ru_coll_in_bold = row['Other sentence pairs en ru coll in bold']
                    other_sent_pairs_ru_coll_in_bold_en = row['Other sentence pairs ru coll in bold en']

                    print('\n\tCOLLOCATION TYPE:', row['Collocation type'])
                    print('\tRAW FREQUENCY:', row['Raw frequency'])
                    print('\tSCALED FREQUENCY:', row['Frequency'])
                    print('\tLEMMED COLLOCATION:', row['Lemmed collocation'])
                    print('\tORIGINAL COLLOCATION:', row['Original collocation'])
                    print('\tCARD FREQUENCY:', card_freq)
                    print('\n')

                    # Check if a card for the collocation has already been written
                    if row['Lemmed collocation'] not in colls_written_to_cards:

                        colls_written_to_cards.append(row['Lemmed collocation'])

                        tl_en_note = genanki.Note(
                            model = tl_en_note_type,
                            fields = [str(card_freq),
                                    str(freq_rank) + ' c' + str(coll_idx),
                                     term_or_collocation,
                                      tl_test,
                                      en_test,
                                      '<font color=\"' + term_gender_colour + '\">' + term_with_accent + '</font>' + case_taken,
                                      disting_gram_info,
                                      conjugation_declension_info,
                                      top_three_gram_colls,
                                      eng_def,
                                      other_defs,
                                      source_sent_one,
                                      target_sent_one,
                                      str(row['Source']),
                                      other_sent_pairs_ru_coll_in_bold,
                                        other_sent_pairs_ru_coll_in_bold_en
                                        ]
                        )

                        my_deck.add_note(tl_en_note)

                        en_tl_note = genanki.Note(
                        model = en_tl_note_type,
                        fields = [str(round(card_freq * 1.05)),
                                  str(freq_rank) + ' c' + str(coll_idx),
                                 term_or_collocation,
                                  en_test,
                                  tl_test,
                                  '<font color=\"' + term_gender_colour + '\">' + term_with_accent + '</font>' + case_taken,
                                  disting_gram_info,
                                  conjugation_declension_info,
                                  top_three_gram_colls,
                                  eng_def,
                                  other_defs,
                                  source_sent_one,
                                  target_sent_one,
                                  str(row['Source']),
                                   other_sent_pairs_en,
                                    other_sent_pairs_en_ru_coll_in_bold
                                    ]
                        )

                        my_deck.add_note(en_tl_note)

                    coll_idx += 1

    end_time = time.time()

    time_elapsed = end_time - start_time
    if time_elapsed <= 18:
        time.sleep(18 - time_elapsed)

    print('\n\n')

genanki.Package(my_deck).write_to_file('C:\\Users\\MdeCL\\Desktop\\Vocab Project Desktop Files\\russian_vocab.apkg')

print('\n\nFlashcard writing complete.')

# Export Anki deck file:

genanki.Package(my_deck).write_to_file('C:\\Users\\MdeCL\\Desktop\\Vocab Project Desktop Files\\russian_vocab.apkg')
