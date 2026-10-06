"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Find similarities between unknown text samples and try to guess the language.

Assignment Information:
    Assignment:     16.3.2 Py4 ind 2 
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           10/05/2026

Contributors:
    Name, login@purdue [repeat for each]

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

import csv
from pathlib import Path
import matplotlib.pyplot as plt
from py4_ind_1_lim573 import clean_text, create_n_gram, normalize_n_gram


def load_from_csv(n):
    models_folder = Path("models")
    model_csvs = list(models_folder.iterdir())
    lang_models = {}
    
    for model in model_csvs:
        file_name_txt = (model.name).split("py4_ind_1_")[1]
        lang_name = file_name_txt.split(".csv")[0]    
        csv_data = {}
        with open(model, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                #enumerate gives the ability to have an i counter and an object
                if i == 0:
                    continue  #skip the header
                #process the data rows that aren't the header
                if int(row[0]) == int(n):
                    csv_data[row[1]] = float(row[2]) #store the frequencies of each n gram
        lang_models[lang_name] = csv_data
        
    return lang_models

def n_gram_dist(unknown_text, known_text):
    all_n_grams = []
    diffs = []
    #for both text dictionaries, add all unique n grams to a list
    for ngram in known_text:
        if ngram not in all_n_grams:
            all_n_grams.append(ngram)
    for ngram in unknown_text:
        if ngram not in all_n_grams:
            all_n_grams.append(ngram)
    all_n_grams = sorted(all_n_grams)
    
    #loop through unique n_grams
    for ngram in all_n_grams:
        #freq is 0 if not found, else freq is taken from the dict
        if ngram in unknown_text:
            freq_un = unknown_text[ngram]
        else:
            freq_un = 0.0
            
        if ngram in known_text:
            freq_k = known_text[ngram]
        else:
            freq_k = 0.0

        #add diff to total
        diffs.append(abs(freq_k - freq_un))

    return sum(diffs)

def score_language(known_dict, unknown_dict):
    scores = {}
    
    #get each language and its dict data in known_dict
    for lang_name, known_model in known_dict.items():
        #use n_gram_dist func for dist
        dist = n_gram_dist(unknown_dict, known_model)
        
        #save the score in scores dict
        scores[lang_name] = dist
        
    return scores

def plot_language_scores(scores, name, n):
    languages = list(scores.keys())
    distances = list(scores.values())
    fig, ax = plt.subplots()
    ax.bar(languages, distances)
    ax.set_title(f"{name} {n}-gram Language Scores")
    ax.set_xlabel("Language")
    ax.set_ylabel("Total Difference")
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    plt.show() 


def main():
    path = Path("unknown_texts")
    files = list(path.iterdir())
    print("Unknown Language File Options")
    for i in range(0, len(files)):
        file_name_txt = (files[i].name).split("sample_")[1]
        file_name = file_name_txt.split(".txt")[0]
        print(f"  {i+1}. {file_name}")
    req_file = int(input("Select a file to analyze: "))
    req_n_size = int(input("Select an n-gram size (1-5): "))
    req_file_name_txt = (files[req_file-1].name).split("sample_")[1]
    req_file_name = req_file_name_txt.split(".txt")[0]
    known_models = load_from_csv(req_n_size)
    #read unknown text, build a n-gram dict
    with open(files[req_file - 1], 'r', encoding='utf-8') as f:
        text = f.read()
    unknown_dict = (create_n_gram(req_n_size, clean_text(text)))
    scores = score_language(known_models, unknown_dict)
    #best lang key is when score is smallest
    best_lang = min(scores, key=scores.get)
    print(f"The best language match for {req_file_name} using {req_n_size}-grams is the {best_lang} model.")
    plot_language_scores(scores, req_file_name, req_n_size)

    
if __name__ == "__main__":
    main()
