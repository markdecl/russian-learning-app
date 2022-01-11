# Dictionary webscraping functions:

with open("C:\\Users\\MdeCL\\Google Drive\\Work, productivity and interests_\\computer science\\coding skills (technical)\\VS Code project files\\NLP-powered Vocab Learning Strategy\\Russian Vocab Project\\ru_prepositions.txt", 'r', encoding='utf8') as file:
    file_read = file.read()
    preps = file_read.split('\n')

def abbyy_scrape(word):
    """"Web-scrape the ABBYY Lingvo Live website
    for English definitions of a given Russian word"""

    url = "https://www.lingvolive.com/en-us/translate/ru-en/" + word

    def web_scrape_this_url(url):

        return_dict = {
        'PoS' : '',
        'Term with accent' : '',
        'Case taken' : '',
        'Grammatical info' : '',
        'Distinguishing gram info' : '',
        'English translations' : [],
        }

        reroute_link_found = False
        eng_def_found = False

        try:
            response = requests.get(url)
            print('RESPONSE FROM ABBYY LINGVO LIVE DICTIONARY:', response)
            #try:
            soup = BeautifulSoup(response.text, "html.parser")
            dict_div = soup.find('div', {'name' : '#dictionary'})
            first_def_div = dict_div.find('div', {'class' : '_1mexQ Zf_4w _3bSyz'})
            term_div = first_def_div.find('h1', {'class' : '_2bepj _2lIoa _3bSyz sSWiV Zf_4w _3bSyz'})
            print('TERM:', term_div.get_text())

            gram_info_div = first_def_div.find('p', {'data-reactid' : '.1a8ou94m96o.1.0.$content.0.1.1.1.1.0.0:$0.2:$1'})

            if first_def_div.find('ol', {'class' : '_2xKEq _1TaPP'}) != None:
                defs_div = first_def_div.find('ol', {'class' : '_2xKEq _1TaPP'})
            else:
                defs_div = first_def_div

            case_taken_dict = {
                'к' : ' к',
                'с' : ' с',
                'из' : ' из',
                'от' : ' от',
                'к' : ' к',
                'у' : ' у',
                'в' : ' в',
                'на' : ' на',
                'за' : ' за',
                'от' : ' от',
                'к' : ' к',
                'у' : ' у',
                'что-л.' : ' + acc',
                'кого-л./что-л.' : '+ acc',
                'кого-л.' : ' + <font color="green">gen</font>',
                'чего-л.' : ' + <font color="green">gen</font>',
                'кого-л./чего-л.' : ' + <font color="green">gen</font>',
                'кому-л.' : ' + <font color="purple">dat</font>',
                'чему-л.' : ' + <font color="purple">dat</font>',
                'кому-л./чему-л.' : ' + <font color="purple">dat</font>',
                'кем-л.' : ' + <font color="blue">instr</font>',
                'чем-л.' : ' + <font color="blue">instr</font>',
                'кем-л./чем-л.' : ' + <font color="blue">instr</font>',
            }

            def_texts = {}
            try:
                case_found = False

                # Iterate over definition divs
                for p_div in defs_div.find_all('p'):

                    s = p_div.get_text()

                    # Find the case that the word takes
                    if case_found == False:
                        case_tag = s[s.find("(")+1:s.find(")")]
                        case_tag = case_tag.replace(' / ', '/').strip()
                        case_units = case_tag.split(';')
                        case_unit = case_units[0]
                        case_unit_cases = case_unit.split(' ')
                        cases_taken = []
                        for case in case_unit_cases:
                            if case in preps:
                                cases_taken.append(' ' + case)
                            elif case in case_taken_dict:
                                value = case_taken_dict[case]
                                cases_taken.append(value)
                                case_found = True
                        return_dict['Case taken'] = ' '.join(cases_taken)

                    # Get filtered definition text
                    def_items = []
                    for span in p_div.find_all('span', {'class' : '_3zJig'}):
                        word = span.get_text()
                        if word != 'I':
                            def_items.append(word)
                    def_text = ' '.join(def_items)

                    # Add div text and filtered div text to def_texts dictionary
                    def_texts[s] = def_text

                for s, def_text in def_texts.items():

                    # Remove the long text in brackets that interfers with the later text splitting
                    def_text = re.sub(r" ?\([^)]+\|\|[^)]+\)", "", def_text).strip()
                    # Remove the text in brackets that contains a comma, as it interfers with the later text splitting:
                    def_text = re.sub(r" ?\([^)]+\,[^)]+\)", "", def_text).strip()

                    final_defs = []

                    def_text = def_text.replace('; ', ', ')
                    def_texts = def_text.split(', ')

                    for defin in def_texts:

                        defins = []

                        if bool(re.search('[a-zA-Z]', defin)) == True:

                            eng_def_found = True
                            if ' / ' in defin:
                                if defin.count(' / ') >= 2:
                                    defins += defin.split(' / ')
                                else:
                                    word_tokens = defin.split(' ')
                                    word_tokens = ['', '', ''] + word_tokens + ['', '', '']
                                    slash_idx = word_tokens.index('/')
                                    var_one = ' '.join(word_tokens[:slash_idx] + word_tokens[slash_idx+2:]).strip()
                                    var_two = ' '.join(word_tokens[:slash_idx-2] + word_tokens[slash_idx+1:]).strip()
                                    defins.append(var_one)
                                    defins.append(var_two)
                            else:
                                defins.append(defin)

                            for defin in defins:
                                if '(' and ')' in defin:
                                    def_text_without_bracket_text = re.sub(r" ?\([^)]+\)", "", defin).strip()
                                    def_text_with_bracket_text = defin.replace('(', '').replace(')', '').strip()

                                    if '||' not in def_text_with_bracket_text:
                                        final_defs += [def_text_without_bracket_text, def_text_with_bracket_text]
                                    else:
                                        final_defs += [def_text_without_bracket_text]
                                else:
                                    defin = defin.replace('(', '').replace(')', '').strip().lower()
                                    final_defs += [defin]

                    to_dict = ', '.join(final_defs)

                    if to_dict != '':
                        if any(item in to_dict for item in ['Все права защищены.', 'II']) == False:
                            to_dict = re.sub(r'[\s]+', ' ', to_dict)
                            to_dict = re.sub(r'[а-яА-Я]+', '', to_dict)
                            to_dict = to_dict.replace('smb.', '')
                            to_dict = re.sub(r'[\s]+\, ', ', ', to_dict)
                            to_dict = to_dict.replace('(', '').replace(')', '').strip()

                            cleaned_def = re.sub(r" ?\([^)]+\)", "", to_dict)
                            cleaned_def = cleaned_def.replace(')', '')
                            cleaned_def = cleaned_def.replace('the ', '')
                            if cleaned_def.startswith('to '):
                                cleaned_def = cleaned_def[2:]
                            cleaned_def = cleaned_def.replace(', ', '|').replace('; ', '|').strip()
                            cleaned_def_list = cleaned_def.split('|')

                            [defin.strip() for defin in cleaned_def_list]

                            cleaned_def_list = [''.join([char for char in defin if char.isalpha() or char.isspace()]).strip() for defin in cleaned_def_list]

                            cleaned_def_list = list(set(cleaned_def_list))

                            return_dict['English translations'].append([s, cleaned_def_list])

                            eng_def_found = True

                    if p_div.get_text() != '':
                        if p_div.find('a') != None:
                            reroute_link_found = True
                            a_element = p_div.find('a')
                            reroute_url = 'https://www.lingvolive.com' + a_element['href']
                            break
                        else:
                            reroute_url = ''

            except Exception as e:
                reroute = False
                reroute_url = ''
                return return_dict, reroute, reroute_url

            if reroute_link_found == True and eng_def_found == False:
                reroute = True
            else:
                reroute = False

            return return_dict, reroute, reroute_url

        except Exception as e:
            print('-----------ABBYY LINGVO SCRAPE RAISED AN ERROR:')
            print(e)
            reroute = False
            reroute_url = ''
            return return_dict, reroute, reroute_url

    return_dict, reroute, reroute_url = web_scrape_this_url(url)
    if reroute == True:
        print('REROUTING...')
        return_dict, reroute, reroute_url = web_scrape_this_url(reroute_url)
        if reroute == True:
            return_dict, reroute, reroute_url = web_scrape_this_url(reroute_url)


    pos_codes = {
        'нареч.' : 'adverb',
        'прил.' : 'adjective',
        'ж.р.' : 'noun',
        'м.р.' : 'noun',
        'несовер.' : 'verb',
        'предл.' : 'preposition',
        'союз' : 'conjunction',
        'частица' : 'particle'
    }

    term_pos = ''

    return_dict['PoS'] = term_pos

    return return_dict


def wiktionary_parser_eng_trans_scrape(word, pos):
    language = 'russian'
    parser = WiktionaryParser()
    return_dict = {
        'PoS' : '',
        'Term with accent' : '',
        'Grammatical info' : '',
        'Distinguishing gram info' : '',
        'English translations' : [],
        'Idiomatic phrases' : []
    }
    try:
        if parser.fetch(word, language) != None:
            try:
                data = parser.fetch(word, language)[0]
                #print(data)
                try:
                    for definition in data['definitions']:
                        if definition['partOfSpeech'] == pos:
                            return_dict['PoS'] = definition['partOfSpeech']
                            term_with_accent = definition['text'][0]
                            return_dict['Idiomatic phrases'] = definition['examples']
                            term_with_accent = ''
                            eng_trans = []
                            text_idx = 0
                            defs_to_reroute = ['Alternative spelling of', 'superlative degree of', 'short neuter singular of', ]
                            if any(item in definition['text'][1] for item in defs_to_reroute):
                                alt_spelling = definition['text'][1].split(' of ')[1]
                                alt_spelling = alt_spelling.split()[0]
                                alt_spelling = alt_spelling.replace('о́', 'о').replace('е́', 'е').replace('и́', 'и').replace('у́', 'у')
                                alt_spelling = alt_spelling.replace('ы́','ы').replace('а́','а')
                                if parser.fetch(alt_spelling, language) != None:
                                    try:
                                        data = parser.fetch(alt_spelling, language)[0]
                                        try:
                                            for definition in data['definitions']:
                                                if definition['partOfSpeech'] == pos:
                                                    return_dict['PoS'] = definition['partOfSpeech']
                                                    term_with_accent = definition['text'][0]
                                                    return_dict['Idiomatic phrases'] = definition['examples']
                                                    term_with_accent = ''
                                                    eng_trans = []
                                                    text_idx = 0
                                                    while text_idx + 1 <= len(definition['text']):
                                                        item = definition['text'][text_idx]
                                                        if text_idx == 0:
                                                            return_dict['Term with accent'] = item.split(' • ')[0]
                                                            return_dict['Grammatical info'] = item.split(' • ')[1]
                                                        else:
                                                            if 'passive of ' not in item:
                                                                eng_trans.append(item)
                                                        text_idx += 1
                                                    return_dict['English translations'] = eng_trans
                                        except Exception:
                                            print('Wiktionary Parser returned None.')
                                            sys.exit()
                                    except Exception:
                                        print('Wiktionary Parser returned None.')
                                        sys.exit()
                                else:
                                    print('Wiktionary Parser returned None.')
                                    sys.exit()
                            else:
                                while text_idx + 1 <= len(definition['text']):
                                    item = definition['text'][text_idx]
                                    if text_idx == 0:
                                        return_dict['Term with accent'] = item.split(' • ')[0]
                                        return_dict['Grammatical info'] = item.split(' • ')[1]
                                    else:
                                        if 'passive of ' not in item:
                                            eng_trans.append(item)
                                    text_idx += 1
                                return_dict['English translations'] = eng_trans
                except Exception:
                    print('Wiktionary Parser returned None.')
            except Exception:
                print('Wiktionary Parser returned None.')
        else:
            print('Wiktionary Parser returned None.')
    except Exception as e:
        print('Wiktionary Parser returned None.')
    formatted_eng_trans = []
    eng_tran_idx = 0
    while eng_tran_idx + 1 <= len(return_dict['English translations']):
        formatted_eng_trans.append(return_dict['English translations'][eng_tran_idx])
        eng_tran_idx += 1
    return_dict['English translations'] = formatted_eng_trans
    if 'impf (perfective' in return_dict['Grammatical info']:
        return_dict['Distinguishing gram info'] = 'imperfective'
    elif 'pf (imperfective'in return_dict['Grammatical info']:
        return_dict['Distinguishing gram info'] = 'perfective'

    return(return_dict)

def cooljugator_scrape(word, query_pos_full):

    conjugs_dict = {}

    pos_dict = {
        'adjective' : 'a',
        'noun' : 'n',
        'verb' : ''
    }

    base_url = 'https://cooljugator.com/ru'
    if query_pos_full in pos_dict:
        url = base_url + pos_dict[query_pos_full] + '/' + word

        response = requests.get(url)
        print('RESPONSE FROM COOLJUGATOR:', response)

        soup = BeautifulSoup(response.text, "html.parser")
        conjug_div = soup.find('section', {'id' : 'conjugations'})

        try:
            for table_div in conjug_div.find_all('div', {'class' : 'conjugation-table collapsable'}):
                for cell_div in table_div.find_all('div', {'class' : 'conjugation-cell conjugation-cell-four'}):
                    if cell_div.has_attr('id'):
                        cell_id = cell_div['id'].replace('_no_accent', '')
                        if cell_div.has_attr('data-stressed'):
                            conjugs_dict[cell_id] = cell_div['data-stressed']
                        elif cell_div.has_attr('data-default'):
                            conjugs_dict[cell_id] = cell_div['data-default']

                for cell_div in conjug_div.find_all('div', {'class' : 'conjugation-cell conjugation-cell-four leftmost'}):
                    if cell_div.has_attr('id'):
                        cell_id = cell_div['id'].replace('_no_accent', '')
                        if cell_div.has_attr('data-stressed'):
                            conjugs_dict[cell_id] = cell_div['data-stressed']
                        elif cell_div.has_attr('data-default'):
                            conjugs_dict[cell_id] = cell_div['data-default']

        except Exception as e:
            print('COOLJUGATOR SCRAPE RAISED AN ERROR:')
            print(e)

    else:
        print('COOLJUGATOR_SCRAPE: QUERY NOT A NOUN, VERB OR ADJECTIVE --> NOT SCRAPING.')

    return conjugs_dict


    def eng_trans_and_syns(query, query_pos_full):
    wikt_results = wiktionary_parser_eng_trans_scrape(query, query_pos_full)
    term_with_accent = wikt_results['Term with accent']
    if term_with_accent == '':
        term_with_accent = query
    term_without_accent = term_with_accent.replace('о́', 'о').replace('ы́', 'ы').replace('у́', 'у').replace('а́', 'а').replace('е́', 'е').replace('и́', 'и').replace('я́', 'я').replace('э́', 'э')
    term_with_accent = re.sub(r"(.)\1", '<u>' + r"\1\1" + '</u>', term_with_accent)
    gram_info = wikt_results['Grammatical info']
    disting_gram_info = wikt_results['Distinguishing gram info']

    if '\xa0n\xa0' in gram_info:
        term_gender_colour = 'grey'
    elif '\xa0f\xa0' in gram_info:
        term_gender_colour = 'red'
    elif '\xa0m\xa0' in gram_info:
        term_gender_colour = 'blue'
    else:
        term_gender_colour = 'black'

    inflected_forms =  []
    inflected_forms_dict = cooljugator_scrape(term_without_accent, query_pos_full)
    query_parse = morph.parse(query)[0]
    if query_pos_full == 'noun':
        for key, value in inflected_forms_dict.items():
            value = value.replace('о́', 'о').replace('ы́', 'ы').replace('у́', 'у').replace('а́', 'а').replace('е́', 'е').replace('и́', 'и').replace('я́', 'я').replace('э́', 'э')
            if key == 'nom_P':
                if term_gender_colour == 'blue':
                    if (value.endswith('ы') == False) and (term_without_accent.endswith(('ь', 'к', 'г', 'х', 'ш', 'щ', 'ч', 'ж')) == False):
                        inflected_forms.append(value[:-2] + '<font size=\"+5\" color=\"blue\">' + value[-2:]  + '</font>')
                    if (value.endswith('и') == False) and (term_without_accent.endswith(('ь')) == True):
                        inflected_forms.append(value[:-2] + '<font size=\"+5\" color=\"blue\">' + value[-2:]  + '</font>')
                    elif len(value) > len(term_without_accent) + 1:
                        inflected_forms.append(value[:-3] + '<font size=\"+5\" color=\"blue\">' + value[-3:]  + '</font>')
                    else:
                        inflected_forms.append(value)
                elif (term_gender_colour == 'grey') and (term_without_accent.endswith('е') == False) and (value.endswith('а') == False):
                    inflected_forms.append(value[:-2] + '<font size=\"+5\" color=\"blue\">' + value[-2:]  + '</font>')
                elif (term_gender_colour == 'grey') and (term_without_accent.endswith('е') == True) and (value.endswith('я') == False):
                    inflected_forms.append(value[:-2] + '<font size=\"+5\" color=\"blue\">' + value[-2:]  + '</font>')
                elif ('ё' in value) and ('ё' not in term_without_accent):
                    inflected_forms.append(value.replace('ё', '<font size=\"+5\" color=\"blue\">ё</font>'))
                elif len(value) > len(term_without_accent) + 1:
                    inflected_forms.append(value[:-3] + '<font size=\"+5\" color=\"blue\">' + value[-3:]  + '</font>')
                else:
                    inflected_forms.append(value)
            elif key == 'loc':
                if value.endswith('у'):
                    inflected_forms.append(value[:-1] + '<font size=\"+5\" color=\"purple\">у</font>')
                elif value.endswith('у́'):
                    inflected_forms.append(value[:-2] + '<font size=\"+5\" color=\"purple\">у́</font>')
                else:
                    inflected_forms.append(value)
            else:
                inflected_forms.append(value)

    elif query_pos_full == 'verb':
        for key, value in inflected_forms_dict.items():
            second_sing_form = ''
            if 'present2' in inflected_forms_dict:
                second_sing_form = inflected_forms_dict['present2']
            elif 'future2' in inflected_forms_dict:
                second_sing_form = inflected_forms_dict['future2']
            if second_sing_form != '':
                if second_sing_form.endswith(('аешь', 'яешь', 'ешься', 'яешься', 'а́ешь', 'я́ешь', 'а́ешься', 'я́ешься')):
                    color = 'orange'
                    term_gender_colour = 'orange'
                else:
                    if second_sing_form.endswith(('ишь', 'ишься', 'и́шь', 'и́шься')):
                        color = 'blue'
                        term_gender_colour = 'blue'
                    elif second_sing_form.endswith(('ешь', 'ешься')):
                        color = 'purple'
                        term_gender_colour = 'purple'
                    elif second_sing_form.endswith(('ёшь', 'ёшься')):
                        color = 'firebrick'
                        term_gender_colour = 'firebrick'
                    else:
                        color = 'black'
            else:
                color = 'black'

        for key, value in inflected_forms_dict.items():
            inflected_forms.append('<font color=\"' + color + '\">' + value + '</font>')

    elif query_pos_full == 'adjective':
        if query_parse.inflect({'COMP'}) != None:
            comp_form = query_parse.inflect({'COMP'}).word
            if comp_form.endswith('ее') == False:
                inflected_forms.append(comp_form[:-2] + '<font size=\"+5\" color=\"orange\">' + comp_form[-2:] + '</font>')
            else:
                inflected_forms.append(comp_form)

    abbyy_results = abbyy_scrape(query)

    case_taken = abbyy_results['Case taken']

    cleaned_defs = abbyy_results['English translations']

    syn_pos_tags = {
        'noun' : '.n.',
        'verb' : '.v.',
        'adjective' : '.a.',
        'adverb' : '',
        'preposition' : ''
    }

    infl_pos_tags = {
        'verb' : 'V',
        'adjective' : 'A',
        'noun' : 'N',
    }


    defs_for_check = []
    for defin in cleaned_defs:
        for word in defin[1]:
            defs_for_check.append(word)

    # CREATE A DICTIONARY WITH EACH FULL DEF AS A KEY AND ALL THEIR SYNS AND INFLECTED FORMS AS ITS VALUE:
    inflected_eng_defs = {}
    basic_defs_added = []
    syns_added = []
    for basic_def in cleaned_defs:
        full_def = basic_def[0]
        basic_def = basic_def[1]
        n_basic_def = []
        all_forms = []
        # Find the synonyms of each word
        for word in basic_def:
            word = word.strip()
            if word not in basic_defs_added:
                basic_defs_added.append(word)
                n_basic_def.append(word)
                if query_pos_full == 'verb':
                    syn_results = wordnet.synsets(word, pos=wordnet.VERB)
                elif query_pos_full == 'noun':
                    syn_results =  wordnet.synsets(word, pos=wordnet.NOUN)
                elif query_pos_full == 'adjective':
                    syn_results = wordnet.synsets(word, pos=wordnet.ADJ)
                elif query_pos_full == 'adverb':
                    syn_results = wordnet.synsets(word, pos=wordnet.ADV)
                else:
                    syn_results = wordnet.synsets(word)
                syn_words = []
                for syn in syn_results:
                    for lm in syn.lemmas():
                        syn_word = lm.name()
                        if syn_word not in defs_for_check:
                            syn_words.append(syn_word)
                syn_words.append(word)

                # FIND THE INFLECTED FORMS OF EACH SYNONYM (SENSITIVE TO PoS) AND ADD TO WORD FORMS LIST:
                word_forms = []
                for syn_word in syn_words:
                    syn_word = syn_word.replace('_', ' ').strip()
                    if syn_word not in syns_added:
                        syns_added.append(syn_word)
                        # CHECK IF THE SYNONYM IS MORE THAN ONE WORD. IF IT IS, ONLY INFLECT THE FIRST WORD:
                        syn_word_list = nltk.word_tokenize(syn_word)
                        if query_pos_full in infl_pos_tags:
                            infl_pos_tag = infl_pos_tags[query_pos_full]
                            if syn_word_list != []:
                                if len(syn_word_list) == 1:
                                    if getAllInflections(syn_word_list[0], pos_type=infl_pos_tag) != {}:
                                        [word_forms.append(value[0]) for key, value in getAllInflections(syn_word_list[0], pos_type=infl_pos_tag).items()]
                                    else:
                                        word_forms.append(syn_word)
                                else:
                                    if getAllInflections(syn_word_list[0], pos_type=infl_pos_tag) != {}:
                                        word_forms = [infl_form[0]+' '+' '.join(syn_word_list[1:]) for infl_form in list(getAllInflections(syn_word_list[0], pos_type=infl_pos_tag).values())]
                                    else:
                                        word_forms.append(syn_word)
                        else:
                            if syn_word_list != []:
                                if len(syn_word_list) == 1:
                                    if getAllInflections(syn_word_list[0]) != {}:
                                        [word_forms.append(value[0]) for key, value in getAllInflections(syn_word_list[0]).items()]
                                    else:
                                        word_forms.append(syn_word)
                                else:
                                    if getAllInflections(syn_word_list[0]) != {}:
                                        word_forms = [infl_form[0]+' '+' '.join(syn_word_list[1:]) for infl_form in list(getAllInflections(syn_word_list[0]).values())]
                                    else:
                                        word_forms.append(syn_word)
                    all_forms += word_forms

        all_forms = list(set(all_forms))
        inflected_eng_defs[full_def] = all_forms

    print('TERM\'S INFLECTED FORMS:', ', '.join(inflected_forms))

    return {'inflected_eng_defs' : inflected_eng_defs,
            'term_with_accent' : term_with_accent,
            'case_taken' : case_taken,
            'term_gender_colour' : term_gender_colour,
            'disting_gram_info' : disting_gram_info,
            'conjugation_declension_info' : inflected_forms}


abbrevs_dict = {}

with open(proj_dir + '\\wiktionary_abbrevs_trans.txt', 'r') as file:
    file_read = file.read()
    for line in file_read.split('\n'):

        abbrev = line.split('£')[0]
        expl = line.split('£')[1]


        abbrevs_dict[abbrev] = expl


def monoling_wikt_scrape(word):
    url = "https://ru.wiktionary.org/w/index.php?title=" + word + '&printable=yes'
    response = requests.get(url)
    wikt_definitions = []
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find('ol') != None:
            entries = soup.find('ol')
            if entries.findAll('li') != None:
                number_of_defs = len(entries.findAll('li'))
                index = 0
                while index + 1 <= number_of_defs:

                    # definition:
                    entry = entries.find_all('li')[index]
                    entry_text = entry.get_text()

                    if entry_text != '':

                        definition_text = entry_text.split('◆')[0]
                        definition_text_extra = ''

                        #clean up definition text before translating:
                        definition_text = definition_text.replace(' гл.', ' глаголя ')

                        if 'по значению глаголя ' in definition_text:
                            definition_text_extra = definition_text.split('по значению глаголя ')[1]

                        if 'соотносящийся по значению с существительным ' in definition_text:
                            definition_text_extra = definition_text.split('соотносящийся по значению с существительным ')[1]

                        definition_text = re.sub("\[.*?\]", "", definition_text)
                        definition_text = definition_text.replace('по значению глаголя', 'of verb: ')
                        definition_text = definition_text.replace('свойство по значению прилагательного', 'quality of being ')
                        definition_text = definition_text.replace(' по значению с существительным', ' to noun: ')

                        # register tag:
                        register_tag = ''
                        for key, value in abbrevs_dict.items():
                            if key in definition_text:
                                definition_text = definition_text.replace(key, '')
                                register_tag += '<i>' + value + '</i>'

                        # example sentence:
                        if entry.find('span', {'class' : 'example-absent'}) == None:
                            if entry.find('span', {'class' : 'example-block'}) != None:
                                ex_sentence_1 = entry.find('span', {'class' : 'example-block'})

                                ex_sentence_one_text = ex_sentence_1.get_text()

                                if entry.find('span', {'class' : 'example-details'}) != None:
                                    text_to_remove = entry.find('span', {'class' : 'example-details'}).get_text()
                                    ex_sentence_one_text = ex_sentence_one_text.replace(text_to_remove, '')

                                ex_sent_with_blank = ex_sentence_one_text
                                ex_sent_full = ex_sentence_one_text

                                query_parse = morph.parse(word)[0]

                                forms = []

                                for word_form in query_parse.lexeme:
                                    query = word_form[0]
                                    forms.append(query)

                                forms = list(set(forms))

                                for form in forms:
                                    capitalised_form = form.replace(form[0], form[0].upper())

                                    ex_sent_with_blank = re.sub('\s' + form + '[\s.]', ' ____ ', ex_sent_with_blank)
                                    ex_sent_with_blank = re.sub('\s' + form + '[\s,]', ' ____ ', ex_sent_with_blank)
                                    ex_sent_with_blank = re.sub('\s' + form + '[\s!]', ' ____ ', ex_sent_with_blank)
                                    ex_sent_with_blank = re.sub('\s' + form + '[\s?]', ' ____ ', ex_sent_with_blank)
                                    ex_sent_with_blank = re.sub(capitalised_form + '[\s.]', '____ ', ex_sent_with_blank)
                                    ex_sent_with_blank = re.sub(capitalised_form + '[\s,]', '____ ', ex_sent_with_blank)
                                    ex_sent_with_blank = re.sub(capitalised_form + '[\s!]', '____ ', ex_sent_with_blank)
                                    ex_sent_with_blank = re.sub(capitalised_form + '[\s?]', '____ ', ex_sent_with_blank)

                                    #ex_sent_with_blank = ex_sent_with_blank.replace(form, '_____')
                                    #ex_sent_with_blank = ex_sent_with_blank.replace(capitalised_form, '_____')
                                    ex_sent_full = ex_sent_full.replace(form, '<b>' + form + '</b>')
                                    ex_sent_full = ex_sent_full.replace(capitalised_form, '<b>' + capitalised_form + '</b>')

                            else:
                                ex_sent_with_blank = ''
                                ex_sent_full = ''
                        else:
                            ex_sent_with_blank = ''
                            ex_sent_full = ''

                        added_to_register_tag = ''
                        #move eg. 'about water' from definition_text to register_tag:
                        definition_text = definition_text.replace(' - ', ' — ')
                        definition_text = definition_text.replace('· ', ' — ')
                        if ' — ' in definition_text:
                            split_def = re.split(' — ', definition_text)
                            added_to_register_tag += split_def[0]
                            definition_text = split_def[1]
                        #add text in brackets in definition_text to register_tag:
                        if '(' and ')' in definition_text:
                            text_in_brackets = definition_text[definition_text.find("(")+1:definition_text.find(")")]
                            added_to_register_tag += text_in_brackets
                        if added_to_register_tag != '':
                            register_tag += ', ' + added_to_register_tag

                        definition_eng = definition_text

                        definition_eng = definition_eng.replace(' it', ' ')
                        definition_eng = definition_eng.replace('the ', ' ')
                        definition_eng = definition_eng.replace(' a ', ' ')

                        if definition_text_extra != '':
                            definition_text_extra = ' (' + definition_text_extra + ')'

                        definition_package = {'register_tag_ru' : register_tag,
                                              'definition_ru' : definition_eng + definition_text_extra,
                                              'ex_sentence_blank' : ex_sent_with_blank,
                                                'ex_sentence_full' : ex_sent_full
                                             }

                        wikt_definitions.append(definition_package)

                    index += 1


                #translate all defs in one API request:
                reg_tags_to_translate = []
                defs_to_translate = []
                for definition in wikt_definitions:
                    if definition['register_tag_ru']:
                        reg_tags_to_translate.append(definition['register_tag_ru'])
                    else:
                        reg_tags_to_translate.append('_')
                    if definition['definition_ru']:
                        defs_to_translate.append(definition['definition_ru'])
                    else:
                        defs_to_translate.append('_')

                if reg_tags_to_translate == ['']:
                    reg_tags_to_translate = ['_']

                if defs_to_translate == ['']:
                    defs_to_translate = ['_']

                text_for_google_translate = ' | '.join(reg_tags_to_translate) + ' || ' + ' | '.join(defs_to_translate)
                text_translated = coll_eng_tran(text_for_google_translate)

                reg_tags_translated_text = text_translated.split(' || ')[0]
                reg_tags_translated = reg_tags_translated_text.split(' | ')

                defs_translated_text = text_translated.split(' || ')[1]
                defs_translated = defs_translated_text.split(' | ')

                idx = 0
                while idx + 1 <= len(wikt_definitions):
                    definition = wikt_definitions[idx]
                    definition['definition_eng'] = defs_translated[idx]
                    definition['register_tag_eng'] = reg_tags_translated[idx]

                    idx += 1


                return(wikt_definitions)
            else:
                return('Error')
        else:
            return('Error')
    except Exception as e:
        return('Error')
