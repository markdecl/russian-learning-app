# Russian-Vocab-Project
 
The number of words and phrases in a given language is overwhelming. I thought that there must be a way for students to learn more quickly, more comprehensively, and with more enjoyment in the daily learning exercise. So I wrote a program to optimise as much of the learning process as possible.

I outlined the thinking and theory behind this project in my [GitHub Pages blog post](https://markdecl.github.io/Optimising-vocab-learning-(with-some-help-from-Python)/).

An example Anki flashcard showing the final product:  
![example flashcard](https://github.com/markdecl/Russian-Vocab-Project/blob/main/User%201%20-%20Anki%2011_27_2020%203_45_11%20PM.png)

## Libraries and tools used:


## Breakdown of the project:

### Load Russian National Corpus frequency list

### Compile, clean and preprocess parallel corpus:
* Load tmx files downloaded from [opus.nlpl.eu](opus.nlpl.eu) onto pandas DataFrame
* Remove duplicate source sentences
* Standardise source and target sentences: remove non-letter and non-digit characters, remove elisions
* Create more features from source sentences: lemmatized source sentence, PoS tags of tokens in source sentence
* Create 'register' feature from sentence source ('political', 'informal', 'journalism', 'general')

### Create idiom dictionary:
* Web-scrape from online dictionaries
* Filter, clean and preprocess idioms

### Define web-scraping functions

### Define functions for collocational analysis:
* Define function to extract collocations from a sentence
* Define function to lemmatize each collocation
* Define function to categorize collocations by type (grammatical, lexical) 
* Define function to count up all collocations of a given word

### Write flashcards:
* Iterate over Russian frequency list
* Find English definitions and grammatical information of each Russian word in frequency list
* Find frequency of each English definition in parallel corpus
* Find top collocations of Russian word in parallel corpus
* Collate information above and write onto Anki flashcard

### Export Anki deck file

## If it were a bigger project:

## Credits:

## Will you accept pull requests?
