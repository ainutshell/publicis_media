# publicis_media
# Second round interview question:

<1> . Problem Statement

Write a Python or Java application that takes any block of text and creates an playlist of Spotify tracks using the Spotify API which is accessible at: https://developer.spotify.com/technologies/web-api/. You can read the input in any way you want (command line arguments, run it as a web server and take a query string, etc). Feel free to use any Python modules or frameworks that are reasonably standard.

The input to the application will be the message, and its output will be a list of Spotify tracks, i.e. if the input is "if i can't let it go out of my mind", one valid output would be

* http://open.spotify.com/track/6mcu7D7QuABVwUGDwovOEh
* http://open.spotify.com/track/5ZRxxnab9kLUqZPzoelgGP
* http://open.spotify.com/track/3L0bYyI0FHRiD1xZfbZedz

To be clear the output should be a playlist that reads out the original text. And another thing to think about is that you want to break up the poem into a short playlist. I.e. it's better to turn "If I can't let it go out of my mind" into

* If I can't
* Let it go
* Out of my mind

than to break it down into

* If
* I can't
* Let
* It
* Go
* Out of
* My mind

We're looking for your ability to come up with a working solution and the efficiency of the solution. Please create a git repo and share it with me when you are done or close to finish. Feel free to reach out with any questions.




<2>. Solution

* - Methodology:
This solution has been built and tested on python 2.7 running on Ubuntu 16.04 LTS. Assuming user has 'root privileges' with full access to internet (without using proxy servers). 
There are several methodologies could be used if there are no exact matches based on the original query.
Strategy (1). use the function of Standard (or OpenNLP) Parser to apply dependency parsing on the input and split the whole query from coarse-grained message into fine-grained pieces into the dependency graph/tree recursively; requery through SPOTIFY with the mid-level-grained pieces and aggregate results together. It garantees generated pieces syntatically are meaningful and queried results will be more meaningful to the end user. 
Strategy (2). build a 1/2/3/4/5-gram hash-table from metathesauras (or large n-gram libraries), which enables querying whether pieces from the original sentences a frequent appeared 1/2/3/4/5-grams within the hash-table, then using the hits as queries are prone to generate more meaningful results. A greedy search methods are used to disassemble the original queries into 1/2/3/4/5-grams, where longer n-grams are preferred for disassembly. E.g. for query 'if i can't let it go', the substring 'if', 'if i' and 'if i can't' could all find frequently appeared corresponding terms within the n-gram hashtable, the preferred segment will be 'if I can't'. The segment stops there becuase 'if i can't let' appeared rarely according to the n-gram hashtable. 
Due to (2) is more straight-forward and easy-to-implement, I followed Strategy (2) using Googlebooks Ngram library.

* - Installation
Setting up computational environment within the OS and Python:
1). Install spotipy following guideline at https://spotipy.readthedocs.io/en/latest/#installation;
2). Install nltk following the guideline at http://www.nltk.org/install.html;
3). Download and install Googlebooks ngram library located at http://storage.googleapis.com/books/ngrams/books/datasetsv2.html; 
4). Download the git repository via "git clone https://github.com/ainutshell/publicis_media.git", assuming git has been installed in the OS;
For 3), 3/4/5-gram files (after concatenation) are >=1.5TB (For efficiency purpose, future plan is to have it serving an RESTful API). Within Python, these data are assumed been translated into a hashmap with n-gram appearance frequency estimated from the data as values, and lowercased n-grams as keys using python tuple. 

* - Run the program
1). step 1: "cd /path/to/publicis_media"
2). step 2: "python ./Spotify_Query.py -i istream", where istream is a string like 'If I can\'t let it go out of my mind', with QUOTATION MARKS.

* - Results
Via running { python ./Spotify_Query.py -i "If I can't let it go out of my mind" }, with the current methods, within a couple of minutes, the program will pour out around ~15000 web links for tracks, like https://open.spotify.com/track/5ZRxxnab9kLUqZPzoelgGP. 
