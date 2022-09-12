import os
import utils as ut


def main(gene_desc_file, save_dir):
    ut.download_nltk_req()
    dfwords = ut.loaddf(gene_desc_file)
    dfwords["word_token"] = ut.parse_gene_desc(dfwords.Description)
    all_descriptions_tokenized = [word for words in dfwords.word_token for word in words]
    # generate ngram frequencies
    freqs = ut.get_word_frequencies(all_descriptions_tokenized, 3)
    # save freq dist tables
    [ut.save_freqdist_tables(fq, sv) for fq,sv in zip(freqs, [os.path.join(save_dir, "tables", f"freqdist_{n}.csv") for n in range(1, 3+1)])]
    # save freq dist figures
    [ut.save_freqdist_plots(fq, sv) for fq,sv in zip(freqs, [os.path.join(save_dir, "figures", f"freqdist_{n}.pdf") for n in range(1, 3+1)])]
    # generate word cloud from frequencies
    [ut.save_word_clouds(fq, sv) for fq,sv in zip(freqs, [os.path.join(save_dir, "figures", f"wordcloud_{n}.pdf") for n in range(1, 3+1)])]
    return


if __name__ == "__main__":
    gene_desc_file = "/data5/deepro/ukbiobank/analysis/bmi_project/bmi_gene_desc_nlp/data/BMI_Genes.xlsx"
    save_dir = "/data5/deepro/ukbiobank/analysis/bmi_project/bmi_gene_desc_nlp/data/results"
    main(gene_desc_file, save_dir)
