# POS_Tagging_HMM
An implementation of Hidden Markov Model for the purpose of Part-of-speech tagging.

## Problem Statement ##
Write a Hidden Markov Model part-of-speech tagger for Catalan. The training data is provided tokenized and tagged (present in hw5-data-corpus); the test data is provided tokenized, and your tagger will add the tags.

### Data Format ###
* A file with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.
* A file with untagged development data, with words separated by spaces and each sentence on a new line.
* A file with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.
* A readme/license file (which you won’t need for the exercise)
        
### Programs ###
You will write two programs: __hmmlearn.py__ will learn a hidden Markov model from the training data, and __hmmdecode.py__ will use the model to tag new data. The learning program will be invoked in the following way:

_python hmmlearn.py /path/to/input_

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called __hmmmodel.txt__. The format of the model is up to you, but it should contain sufficient information for hmmdecode.py to successfully tag new data. The tagging program will be invoked in the following way:

_python hmmdecode.py /path/to/input_

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called __hmmoutput.txt__ in the same format as the training data.
