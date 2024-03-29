# Russian Learning App
The number of words and phrases in Russian is overwhelming. I thought that there must be a way for students to learn more quickly, more comprehensively, and with more enjoyment in the daily learning exercise, so I built a flashcard app to optimise as much of the learning process as possible. This app takes as input a list of words in Russian and outputs a deck of electronic flashcards with all the useful information to learn.

I've outlined the thinking and theory behind this project in my [GitHub Pages blog post](https://markdecl.github.io/Optimising-vocab-learning-(with-some-help-from-Python)/).

## Demo:
### Example Anki flashcard showing the final product:

![example flashcard](demo/User%201%20-%20Anki%2011_27_2020%203_45_11%20PM.png)

### GIF demo:

![Flashcards Demo](demo/russian_learning_app_gif.gif)

## Skills used:
* Web-scraping
* Data preprocessing
* Natural Language Processing

## Tools and technologies used:
* Jupyter Notebook
* Python 3.7
  * NumPy
  * pandas
  * seaborn
  * NLTK
  * spaCy
  * Beautiful Soup

## Breakdown of the project:

### Load Russian National Corpus frequency list

### Compile, clean and preprocess parallel corpus:
* Load .tmx files downloaded from opus.nlpl.eu onto pandas DataFrame
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

## Credits:
* https://opus.nlpl.eu/
* https://www.sketchengine.eu/
* https://www.freecollocation.com/
* https://collegeinfogeek.com/flash-card-study-tips/
* [genanki](https://github.com/kerrickstaley/genanki)
