# Create idiom dictionary:

# Scrape wordreference:

def wordref_phrases_scrape(word):

    base_url = "https://www.wordreference.com/ruen"
    full_url = base_url + '/' + word
    full_url = full_url.replace('\n','')
    response = requests.get(full_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.select('div #article'):
            # to extract the phrases in the wordref definition
            if a.find('span', 'phrase') != None:
                extracted_phrases_dict = {}

                quick_dict = {}

                for phrase_ru_tag in a.findAll('span', 'phrase'):

                    phrase_ru_text = phrase_ru_tag.get_text()
                    phrase_ru_text = phrase_ru_text

                    #print(phrase_ru_text, phrase_en_text)

                    #Divide phrase syntax into multiple phrases where applicable:
                    phrase_variants = ['', '', '']

                    phrase_ru_text_list = []

                    idx = 0
                    for word in phrase_ru_text.split(' '):

                        #print(word)

                        if '/' in phrase_ru_text:
                            #print(phrase_ru_text.split('/'))
                            phrase_ru_text_list.append(word.split('/'))
                        else:
                            phrase_ru_text_list.append([word])

                        idx += 1

                    #print(phrase_ru_text_list)


                    for word_group in phrase_ru_text_list:
                        #print(word_group)
                        for word in word_group:
                            for item in phrase_variants:
                                item += word + ' '

                    #print(phrase_variants)

                    next_el = phrase_ru_tag.findNext()
                    if next_el.has_attr('class'):

                        if next_el["class"][0] == 'IN':

                            phrase_ru_text += ' (' + next_el.get_text() + ')'

                        elif next_el.get("class")[0] == 'ital' and next_el.get_text() == 'или':

                            words = phrase_ru_text.split(' ')

                            idx = 0
                            phrase_start = ''
                            phrase_one_end = ''
                            phrase_two_end = ''
                            for word in words:

                                if word == words[words.index('или') - 1]:
                                    phrase_one_end = word

                                elif word == words[words.index('или') + 1]:
                                    phrase_two_end = word

                                else:
                                    if word != words[words.index('или')]:
                                        phrase_start += word + ' '

                                idx += 1

                            phrase_ru_text = phrase_start + phrase_one_end
                            extracted_phrases_dict[phrase_start + phrase_two_end] = phrase_ru_tag.findNext('a').get_text()

                    phrase_en_tag = phrase_ru_tag.findNext('a')
                    phrase_en_text = phrase_en_tag.get_text()

                    next_en_tag = phrase_en_tag.findNext()

                    if next_en_tag.has_attr('class'):
                        if next_en_tag.get("class")[0] == 'ital' and next_en_tag.get_text() == 'или':
                            phrase_en_text += ' или'
                            nn_en_tag = next_en_tag.findNext()
                            if nn_en_tag.has_attr('href'):
                                phrase_en_text += ' ' + nn_en_tag.get_text()


                    extracted_phrases_dict[phrase_ru_text] = phrase_en_text

                return(extracted_phrases_dict)
            else:
                continue
    else:
        print(response)
        print('\tError connecting to wordreference.com.\nProgram stopped.')
        sys.exit()
wordref_phrases_scrape('от')
terms = []

# import freq list
with open('ru_corpus_freq_list.tsv', 'r') as file:

    output_file = open(proj_dir + '/ru_phrases_file10.txt', 'w+')

    row_count = 1

    start_now = False

    for index,row in rnc_freq_list.iterrows():

        term = row['words']
        term = term.replace('\n','')

        if term == 'рупор':
            start_now = True

        if start_now == True:
            print(term.upper())

            if wordref_phrases_scrape(word = term) != None:
                phrases = wordref_phrases_scrape(word = term)
                # clean up phrase: remove brackets, obj pronouns and accents

                if phrases:
                    for ru,eng in phrases.items():

                        print(ru + ' ' + '£' + eng + '\n')

                        output_file.write(ru + ' ' + '£' + eng + '\n')

            time.sleep(5)

        row_count += 1

    output_file.close()

file.close()

# Scrape phrases from dic.academic.ru:

def academic_ru_scrape(word):

    phrase_list = []
    full_url = 'https://translate.academic.ru/{}/ru/en/'.format(word)
    full_url = full_url.replace('\n','')
    response = requests.get(full_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for div in soup.find_all('div'):
            div_text = div.get_text()
            if bool(re.search('[а-яА-Я]', div_text)) == True and len(div_text) <= 130:
                phrase_list.append(div_text.replace('\n', ' ').replace('\t', ' '))
    else:
        print(response.status_code)

    return phrase_list
output_file = open(proj_dir + '\\dic_academic_ru_phrases.txt', 'w+', encoding='utf-8')
for index, row in rnc_freq_list.iterrows():
    print(index, row['Word'])
    while True:
        try:
            [output_file.write(phrase + '\n') for phrase in academic_ru_scrape(row['Word'])]
            time.sleep(5)
            break
        except Exception as e:
            print(e)
            time.sleep(5)
            continue

output_file.close()

# Filter and format the phrases from dic.academic.ru and export filtered phrases to txt file:

with open(proj_dir + '\\dic_academic_ru_phrases.txt', 'r', encoding='utf-8') as input_file:
    with open(proj_dir + '\\dic_academic_ru_phrases_filtered.txt', 'w+', encoding='utf-8') as output_file:

        phrase_dict = {}

        for line in input_file.readlines():
            if any(string in line for string in ['Перевод:',
                                         'Толкование перевода',
                                        'Толкование Перевод',
                                         'Экспорт словарей на сайты',
                                         'Пометить текст и поделиться']
                  ) == False:
                if bool(re.search(r'\d[\.\)]', line)) == False:
                    if bool(re.search(r'[а-яА-Я]', line)) == True:
                        if len(line.strip().split(' ')) > 1:

                            line = line.lower()

                            phrases = []
                            for phrase in line.split(';'):

                                phrase = re.sub(r'\([^)]*\)', '', phrase)
                                phrase = re.sub(r'\w+\.\s', '', phrase)
                                phrase = re.sub(r'\w+\.\;', ';', phrase)
                                if phrase.startswith(('- ',' - ', '— ', ' — ', ' —  ')):
                                    phrase = phrase[2:]

                                if bool(re.search(r'[а-яА-Я]+\s[\—\-]\s[a-zA-Z]+', phrase)) == True:
                                    ru = re.split(r'\s[\—\-]\s', phrase)[0]
                                    en = re.split(r'\s[\—\-]\s', phrase)[1]
                                else:
                                    if bool(re.search(r'[a-zA-Z]+\s*[a-zA-Z]', phrase)) == True:
                                        ru = re.sub(r'[a-zA-Z]+\s*[a-zA-Z]', '', phrase)
                                        en = re.findall(r'[a-zA-Z]+\s*[a-zA-Z]', phrase)[0]
                                    else:
                                        ru = phrase
                                        en = ''

                                ru = ''.join([char for char in ru if char.isalpha() or \
                                                                    char.isspace() or \
                                                                    char == '-'])
                                for key, value in {'о́' : 'о', 'я́' : 'я', 'и́' : 'и',
                                                   'э́' : 'э', 'а́' : 'а', 'е' : 'е',
                                                   'ы́' : 'ы', 'у́' : 'у'}.items():
                                    if key in ru:
                                        phrase = phrase.replace(key, value)
                                phrase = re.sub(r'\s+', ' ', ru)
                                ru = ' ' + ru.strip() + ' '

                                en = en.replace('\n', '')

                                if len(ru.strip().split(' ')) > 1:

                                    if (ru not in phrase_dict) or (phrase_dict[ru] == ''):
                                        phrase_dict[ru] = en

        for ru, en in phrase_dict.items():
            output_file.write((ru + '||' + en).replace('\n', '') + '\n')
            idiom_dict[ru] = {'Original ru phrase' : ru,
                             'Eng tran' : en}

Import dic.academic.ru filtered phrases by adding to idiom_dict:
with open(proj_dir + '\\dic_academic_ru_phrases_filtered.txt', 'r', encoding='utf-8') as input_file:
    for line in input_file:
        ru = line.split('||')[0]
        en = line.split('||')[1]

        idiom_dict[ru] = {'Original ru phrase' : ru,
                     'Eng tran' : en}

# Standardise and lemmatise idiom dictionary:

# REDUNDANT

def standardise_idiom(ru_idiom, eng_tran):

    return_dict = {}

    ru_phrase_for_lemming = ru_idiom.replace('    ', ' ')
    ru_phrase_for_lemming = ru_phrase_for_lemming.replace('  ', ' ')

    ru_phrase_for_lemming = ru_phrase_for_lemming.replace('-', '/')

    ru_phrase_for_lemming = ru_phrase_for_lemming.replace('кого/н', 'кого-н').replace('кому/н', 'кому-н')
    ru_phrase_for_lemming = ru_phrase_for_lemming.replace('что/н', 'что-н').replace('куда/нибудь', 'куда-нибудь')
    ru_phrase_for_lemming = ru_phrase_for_lemming.replace(' чём/н', ' чём-н')
    ru_phrase_for_lemming = ru_phrase_for_lemming.replace('из/за', 'из-за')

    print(ru_phrase_for_lemming)

    variants = []

    #Divide phrase syntax into multiple phrases where applicable:

    if '/' in ru_phrase_for_lemming:

        phrase_ru_text_list = ru_phrase_for_lemming.split(' ')

        print(phrase_ru_text_list)

        idx = 0
        for word in phrase_ru_text_list:

            if '/' in word:
                variant_words = word.split('/')
                slash_word_index = idx

            idx += 1

        for variant_word in variant_words:
            phrase_ru_text_list[slash_word_index] = variant_word
            print(phrase_ru_text_list)
            variants.append(' '.join(phrase_ru_text_list))

    else:
        variants.append(ru_phrase_for_lemming)


    print(variants)


    for variant in variants:

        ru_phrase_for_lemming = variant.replace('(perf)', '').replace('(impf)', '')

        ru_phrase_for_lemming = ru_phrase_for_lemming.replace('о́','о').replace('ы́','ы').replace('а́','а').replace('у́','у').replace('и́','и').replace('я́','я').replace('е́','е').replace('ю́','ю').replace('э́','э')
        ru_phrase_for_lemming = ru_phrase_for_lemming.replace('кого-н', '').replace('кому-н', '')
        ru_phrase_for_lemming = ru_phrase_for_lemming.replace('что-н', '').replace('кого-н', '').replace('куда-нибудь', '')
        ru_phrase_for_lemming = ru_phrase_for_lemming.replace('чём-н', '')
        ru_phrase_for_lemming = ru_phrase_for_lemming.replace('  +instr ', '').replace('+gen', '').replace('+dat', '').replace('+infin', '')


        lemmed_ru_phrase = lem_coll(ru_phrase_for_lemming)

        lemmed_ru_phrase = lemmed_ru_phrase.replace('  ', ' ')


        return_dict[lemmed_ru_phrase] = {'Original ru phrase' : variant, 'Eng tran' : eng_tran}

    return return_dict
standardise_idiom('приносить кого-н-что-н в жертву ', 'to sacrifice sb/sth ')
idiom_dict[' в перспективе ']
# RE-LEMMATISE THE IDIOM DICT SO THAT IT LEMMATISES EVERY WORD IN THE PHRASE:

original_ru_phrase_list = []
eng_tran_list = []

for key, value in idiom_dict.items():
    original_ru_phrase_list.append(value['Original ru phrase'])
    eng_tran_list.append(value['Eng tran'])

idiom_dict_df = pd.DataFrame({'Original ru phrase' : original_ru_phrase_list,
                              'Eng tran' : eng_tran_list
                             }
                            )

def lem_coll_from_string(coll_string):
    coll_string = ''.join([char for char in coll_string if char.isalpha() or \
                                                    char.isspace() or \
                                                    char == '-'])
    coll_string = coll_string.strip()
    coll_list = coll_string.split(' ')
    lem_coll = ' '
    for word in coll_list:
        p = morph.parse(word)[0]
        lem_coll += p.normal_form + ' '
    # replace ё with е (to account for variations in spelling practices in para_texts_df)
    lem_coll = lem_coll.replace('ё', 'е')
    return lem_coll

idiom_dict_df['Lemmed coll'] = idiom_dict_df['Original ru phrase'].apply(lem_coll_from_string)
idiom_dict_df.iloc[90020:90030]
idiom_dict_df[idiom_dict_df['Lemmed coll']==' еще бы ']

# Export idiom_dict_df to csv file:

idiom_dict_df.to_csv('C:\\Users\\MdeCL\\Google Drive\\Work, productivity and interests_\\computer science\\coding skills (technical)\\VS Code project files\\NLP
