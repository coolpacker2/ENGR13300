"""
Course Number: ENGR 13300
Semester: e.g. Spring 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     16.3.1 py4 ind 1 (for Python 4 Individual task 1)
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           10/04/2026

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

from pathlib import Path
import csv
import matplotlib.pyplot as plt

path = Path("sample_texts")
files = list(path.iterdir())

def clean_text(text):
    #convert to lowercase
    lower_text = text.lower()
    cleaned_chars = []
    for char in lower_text:
        #if it is the alphabet or a space add it to the characters, else don't
        if char.isalpha() or char == ' ':
            cleaned_chars.append(char)
    #return the list but joined into a text bundle
    return "".join(cleaned_chars)

def create_n_gram(n, txt):
    n_grams = {}
    
    #don't go past the end of the string (- n + 1)
    for i in range(len(txt) - n + 1):
        n_gram = txt[i:i + n] #absorb the part in between i and the step
        
        if n_gram not in n_grams:
            n_grams[n_gram] = 1 
        else:
            n_grams[n_gram] += 1
            
    return n_grams

def normalize_n_gram(n_gram):
    freq_n_gram = {}
    #sum all the dictionary values
    total_n_grams = sum(n_gram.values())
    for key in n_gram.keys():
        frequency = n_gram[key]/total_n_grams
        if frequency>0.0005:
            freq_n_gram[key] = frequency
    return freq_n_gram

def create_models(text):
    models = {}
    for i in range(1,6): #do 1-5 n_gram step sizes
        models[str(i)] = normalize_n_gram(create_n_gram(i,clean_text(text)))
    return models

def save_to_csv(n_grams, language):
    
    #save the language's model dictionary to a CSV file named py4_ind_1_lang.csv.
    filename = f"py4_ind_1_{language}.csv"
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #write the header row
        writer.writerow(['n', 'ngram', 'frequency'])
        #loop through the n values in the dict and write each row
        for key in n_grams.keys():
            if key in n_grams:
                for gram, freq in n_grams[key].items():
                    writer.writerow([key, gram, freq])


def plot_top_k(models, language, k=10):
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))

    row = 0
    col = 0

    for n in range(1, 6):
        ax = axs[row][col]

        n_gram = models[str(n)]

        top_ngrams = sorted(n_gram.items(), key=lambda x: x[1], reverse=True)
        top_ngrams = top_ngrams[:k]

        grams = []
        freqs = []
        for gram, freq in top_ngrams:
            grams.append(gram)
            freqs.append(freq)

        ax.bar(grams, freqs)
        ax.set_title(f"{language} {n}-grams")
        ax.set_xlabel(f"{n}-grams")
        ax.set_ylabel("Frequency")
        ax.tick_params(axis="x", rotation=45)

        col += 1
        #move to next row after 3 columns
        if col == 3:
            col = 0
            row += 1

    axs[1][2].axis("off")
    plt.tight_layout()
    plt.show()

def main():
    for i in range(0, len(files)):
        file_name_txt = (files[i].name).split("sample_")[1]
        file_name = file_name_txt.split(".txt")[0]
        print(f"{i+1}. {file_name}")
    req_file = input("Select a language to process (q to quit): ")
    if req_file == "q":
        return
    elif not req_file.isdigit():
        print("Invalid selection.")
        main()
    else:
        #adjust index to grab name
        file_req = files[int(req_file)-1]
        #check if the file exists
        if file_req.is_file():
            lang_name = file_req.name.split("sample_")[1].split(".txt")[0]
            #open the file for reading
            with open(file_req, 'r', encoding='utf-8') as f:
                text = f.read()
        
            cleaned_text = clean_text(text)
            n_grams_freq = create_models(cleaned_text)
            
            save_to_csv(n_grams_freq, lang_name)
            plot_top_k(n_grams_freq, lang_name)


            

                
if __name__ == "__main__":
    main()
