import nltk
nltk.download("stopwords")

from nltk.corpus import stopwords

english_stopwords = stopwords.words("english")

output_file_path = "stopword_file.txt"

with open(output_file_path, "w") as file:
    for word in english_stopwords:
        file.write(word + "\n")

print(f"English stopwords have been saved to {output_file_path}")
