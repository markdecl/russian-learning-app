from fsplit.filesplit import FileSplit

fs = FileSplit(file='C:\\Users\\MdeCL\\Desktop\\opus tmx files\\Russian\\UNPC (need to split).tmx', splitsize=700000000, output_dir='C:\\Users\\MdeCL\\Desktop\\UNPC split files')

fs.split()


parallel_corp_folder = 'C:\\Users\\MdeCL\\Desktop\\opus tmx files\\Russian\\For para_texts_df'

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

    with open("C:\\Users\\MdeCL\\Desktop\\Vocab-Project\\supporting-files\\opus tmx files\\Russian\\For para_texts_df\\" + tmx_folder, 'rb') as fin:
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
