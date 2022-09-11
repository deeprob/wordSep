import nltk
from nltk.tokenize import word_tokenize
from nltk import FreqDist
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


##############################
# download nltk requirements #
##############################

def download_nltk_req():
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")
    return


########################
# df parsing functions #
########################

def loaddf(filen):
    # only read gene names and description columns
    df = pd.read_excel(filen, usecols=[0, 1], engine='openpyxl')
    # get rid of unwanted spaces before and after column names
    df.columns = [c.strip() for c in df.columns]
    return df

def parse_gene_desc(ser):
    # tokenize the words
    ser_tokenized = ser.map(word_tokenize)
    # use a part of speech tagger and only keep nouns, adjectives and adverbs
    ser_tokenized = ser_tokenized.map(lambda x: [i[0] for i in nltk.pos_tag(x) if (i[1].startswith("N")|i[1].startswith("R")|i[1].startswith("J"))])
    return ser_tokenized


####################
# ngram generation #
####################

def get_ngram_frequency(work_tokens, n):
    ngram = nltk.ngrams(work_tokens, n)
    ngram_frequency = FreqDist(ngram)
    return ngram_frequency

def get_word_frequencies(word_tokens, n):
    """
    This functions generates word/phrase frequencies upto and including n-grams
    """
    frequencies = [get_ngram_frequency(word_tokens, i) for i in range(1, n+1)]
    return frequencies

def get_collocations(word_tokens):
    new_text = nltk.Text(word_tokens)
    return new_text.collocations()


##########################
# frequency distribution #
##########################

def save_freqdist_tables(freqdist, save_file):
    fdist_df = pd.DataFrame()
    words, counts = zip(*freqdist.items())
    fdist_df["words"] = [" ".join(x) for x in words]
    fdist_df["counts"] = counts
    fdist_df.sort_values("counts", ascending=False).to_csv(save_file, index=False)
    return


def save_word_clouds(freqdist, save_file):
    # modify_dict 
    freqdist = {" ".join(x):y for x,y in freqdist.items()}
    fig, axes = plt.subplots(figsize=(16, 12))
    cloud = WordCloud(colormap="hsv").generate_from_frequencies(freqdist, max_font_size=80)
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    fig.savefig(save_file)
    return