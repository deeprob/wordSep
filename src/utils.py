import nltk
from nltk.tokenize import word_tokenize
from nltk import FreqDist
import pandas as pd
from wordcloud import WordCloud

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
sns.set_style({'font.family':'sans-serif', 'font.sans-serif':'Arial'})
from matplotlib.ticker import MultipleLocator
from matplotlib.backends.backend_pdf import PdfPages


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


def save_freqdist_plots(freqdist, save_file, ntops=20):
    fdist_df = pd.DataFrame()
    words, counts = zip(*freqdist.items())
    fdist_df["words"] = [" ".join(x) for x in words]
    fdist_df["counts"] = counts
    fdist_df = fdist_df.sort_values("counts", ascending=False)
    
    pdf = PdfPages(save_file)
    fig = plt.figure(figsize=(3,2))
    g = sns.barplot(data=fdist_df.iloc[:ntops, :], x='words', y="counts", hue='counts', dodge=False, palette=['#F28E2B', '#4E79A7'])
    # plt.xlim([-2.5, 2.5])
    # plt.ylim([0, 25])
    ax = plt.gca()
    # ax.xaxis.set_major_locator(MultipleLocator(2.5))
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    # ax.yaxis.set_major_locator(MultipleLocator(10))

    # sns.move_legend(g, bbox_to_anchor=(1,0.9),loc='upper left')
    g.legend_.remove()
    g.set_ylabel("Counts")
    g.set_title('Frequency distribution of words')
    g.set_xticklabels(g.get_xticklabels(), rotation=90, fontsize=4)
    # for item in g.get_xticklabels():
    #     item.set_rotation(90)

    pdf.savefig(fig, bbox_inches='tight')
    pdf.close()   
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