from asyncore import file_dispatcher
import nltk
import pandas as pd
import openpyxl
import sys


def loaddf(filen):
    return pd.read_excel(filepath=filen, engine='openpyxl')

    print(dfwords[:][1])

def main():
    filen= str(sys.argv[1])
    print(filen)

    dfwords = loaddf(filen)

main()
