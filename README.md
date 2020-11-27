# Russian-Vocab-Project
 
The number of words and phrases in a given language is overwhelming; it is impressive that a non-native speaker can become fluent in a foreign language at all.

Conventional wisdom tells us that a learner only reaches such a level of mastery through years of immersion -- living, speaking and breathing the language every day -- that allow them to internalise not only the sheer multitude of words, but also the mass of idioms, collocations and subtle meanings that collectively give them an “intuitive” knowledge of that language.

Taking a look at this enormous learning task -- the absorption of thousands of words and phrases in a foreign language -- I thought that there must be a way for students to learn more quickly, more comprehensively, and with more enjoyment in the daily learning exercise. There must be a way to systematise this convoluted process, break the task down into its constituent parts, and build a tool that can perform much better as a learning aid. Since any small improvements in the efficiency of the learning process would scale up thousands of times, I knew that investing time to optimise the system would pay dividends in days and weeks of saved studying time.

So I wrote a program intended to serve as this optimal tool, automating as much of the learning process as possible.

## Load Russian National Corpus frequency list

## Compile, clean and preprocess parallel corpus:
* Load tmx files downloaded from [opus.nlpl.eu](opus.nlpl.eu) onto Pandas DataFrame
* Remove duplicate source sentences
* Standardise source and target sentences: remove non-letter and non-digit characters, remove elisions
* Create more features from source sentences: lemmatized source sentence, PoS tags of tokens in source sentence
* Create 'register' feature from sentence source ('political', 'informal', 'journalism', 'general')

## Create idiom dictionary:
* Web-scrape from online dictionaries
* Filter, clean and preprocess idioms

## Define web-scraping functions

## Collocational analysis:
* Define function to extract collocations from a sentence
* Define function to lemmatize each collocation
* Define function to categorize collocations by type (grammatical, lexical) 
* Define function to count up all collocations of a given word

## Write flashcards:
* Iterate over Russian frequency list
* Find English definitions and grammatical information of each Russian word in frequency list
* Find frequency of each English definition in parallel corpus
* Find top collocations of Russian word in parallel corpus
* Collate information above and write onto Anki flashcard

## Export Anki deck file
