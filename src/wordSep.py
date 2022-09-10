import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import sys


##############################
# download nltk requirements #
##############################

def download_nltk_req():
    nltk.download("punkt")
    nltk.download("stopwords")
    return


########################
# df parsing functions #
########################

def loaddf(filen):
    # only read gene names and description columns
    df = pd.read_excel(filen, usecols=[0, 1], engine='openpyxl', nrows=10)
    # get rid of unwanted spaces before and after column names
    df.columns = [c.strip() for c in df.columns]
    return df

def parse_gene_desc(ser):
    # tokenize the words
    ser_tokenized = ser.map(word_tokenize)
    # 
    return

def main(gene_desc_file):
    download_nltk_req()
    dfwords = loaddf(filen)
    dfwords["word_token"] = dfwords.Description.map(word_tokenize)
    print(dfwords.word_token)
    return


if __name__ == "__main__":
    gene_desc_file = "/data5/deepro/ukbiobank/analysis/bmi_project/bmi_gene_desc_nlp/data/BMI_Genes.xlsx"


    main(gene_desc_file)
