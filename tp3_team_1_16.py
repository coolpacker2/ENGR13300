
"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    KNN Classifier usage (from scratch) on CSV files, tuning hyperparameters with a validation set, and
    applying feature scaling (standardization) to improve model performance

Assignment Information:
    Assignment:     tp3 team 1
    Team ID:        LC5 - 16
    Author:         Zane Clark, clar1439@purdue.edu
    Date:           10/29/2026

Contributors:
    Nathan Crute, ncrute@purdue.edu
    Hari Ghatpande, sghatpan@purdue.edu
    Stephen Lim, lim573@purdue.edu

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

import pandas as pd
import numpy as np

def scale_features(df, feature_columns):
    # standardize each feature column in place: subtract its mean, divide by its standard deviation
    for col in feature_columns:
        mean = df[col].mean()
        std = df[col].std()
        df[col] = (df[col] - mean) / std
    return None


#load CSV dataset file and return:
#x (Feature Matrix as a 2D np.array of floats)
#y (Label Vector as a 1D np.array of ints)
def load_dataset(file_path, feature_cols, label_col, shuffle, seed):
    df = pd.read_csv(file_path)

    scale_features(df, feature_cols)

    x = df[feature_cols].to_numpy()
    y = df[label_col].to_numpy()

    if shuffle:
        np.random.seed(seed)
        shuffled_indices = np.random.permutation(len(y))
        x = x[shuffled_indices]
        y = y[shuffled_indices]

    return x, y

def train_val_test_split(x, y, train_ratio, val_ratio, test_ratio): #ratios should be decimals
    #split the data into an 80:10:10 split by separating the first 80% of values, the next 10%, and the final 10% into three different numpy arrays (do for x and also do for y)
    if not np.isclose(train_ratio + val_ratio + test_ratio, 1.0):
        raise ValueError("Train, validation, and test ratios must sum to 1.0.")

    train_end = int(train_ratio * len(x))
    val_end = train_end + int(val_ratio * len(x))

    x_train = x[:train_end]
    y_train = y[:train_end]
    x_val = x[train_end:val_end]
    y_val = y[train_end:val_end]
    x_test = x[val_end:]
    y_test = y[val_end:]

    return x_train, y_train, x_val, y_val, x_test, y_test

def knn_single_prediction(new_example, x_train, y_train, k):
    norm_list = []
    for row in range(0,len(x_train)): #list of tuples with the norms (similarity AKA x) as the first value and the CaseId (y) as the second value
        norm_list.append((np.linalg.norm(new_example - x_train[row]) , y_train[row]))

    #sort from most norm to least norm
    norm_list.sort()

    nearest_neighbors = norm_list[:k]
    ones_count = sum(value[1] for value in nearest_neighbors) #adds up all the ClassIds (1s and 0s) in the nearest neighbors list
    prediction = 1 if ones_count > len(nearest_neighbors) / 2 else 0 #this works to return 1 if more ClassIds in nearest_neighbors are 1, and 0 if 0
    return np.int64(prediction)

def predict_labels_knn(x_new, x_train, y_train, k): #this is just the framework for the above function to be called over and over for each value in the whole test set
    predicted_labels = [
        knn_single_prediction(example, x_train, y_train, k)
        for example in x_new
    ]
    return np.asarray(predicted_labels, dtype=np.int64)

def calculate_metrics(predicted_labels, true_labels): #true_labels is y_test
    correct = 0
    for row in range(0, len(predicted_labels)):
        correct += 1 if predicted_labels[row] == true_labels[row] else + 0 #i think this works? idk a better nothingburger to put for the else here because I just don't want anything to happen if else
    
    accuracy = correct/len(predicted_labels)
    error = 1 - accuracy
    return accuracy, error
    
def main():
    file_path = input("Enter the path to the feature dataset: ") #pulls path

    shuffle_str = input("Shuffle the dataset? (yes/no): ").strip().lower() #pulls shuffle choice
    shuffle_bool = shuffle_str == "yes"
    seed_input = input("Enter a seed for loading the dataset: ").strip() #pulls seed
    try:
        seed = int(seed_input) if seed_input else 42
    except ValueError:
        seed = 42

    k = input("Enter the value of k to use for KNN: ") #pulls k
    try:
        k = int(k)
    except ValueError:
        k = 1

    feature_cols = ["hue_mean", "hue_std", "saturation_mean", "saturation_std", "value_mean", "value_std", "number_lines", "has_circle", "has_triangle"] #maybe needs "Path"; 
    label_col = "ClassId"

    feature_matrix, label_vector = load_dataset(file_path, feature_cols, label_col, shuffle_bool, seed)

    x_train, y_train, x_val, y_val, x_test, y_test = train_val_test_split(feature_matrix, label_vector, 0.8, 0.1, 0.1)
    print("\nData loaded and split into\n")
    print(f"Training set:\n  size: {len(x_train)}")
    print(f"Validation set:\n  size: {len(x_val)}")
    print(f"Test set:\n  size: {len(x_test)}")

    #im gonna make a framework for all the evaluations and printing to be a loop instead of writing out the whole thing three times because that's cool
    list_of_sets = [("Training", x_train, y_train), ("validation", x_val, y_val), ("test", x_test, y_test)]
    for set in range(0,len(list_of_sets)):
        print(f"\nEvaluating KNN model on {list_of_sets[set][0]} set with k = {k}...\n")

        predicted_labels = predict_labels_knn(list_of_sets[set][1], x_train, y_train, k)
        accuracy, error = calculate_metrics(predicted_labels, list_of_sets[set][2])

        print(f"--- Model Performance on {list_of_sets[set][0].capitalize()} Set ---\n"
              f"{list_of_sets[set][0].capitalize()} Set Accuracy: {accuracy:.4f}\n"
              f"{list_of_sets[set][0].capitalize()} Set Error Rate: {error:.4f}")
        




if __name__ == "__main__":
    main()