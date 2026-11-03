
"""
Course Number: ENGR 13300
Semester: Fall 2026 

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     tp3 team 2
    Team ID:        LC5 - 16
    Author:         Nathan Crute, ncrute@purdue.edu
    Date:           11/2/2026

Contributors:
    Hari Ghatpande, sghatpan@purdue.edu
    Zane Clark, clar1439@purdue.edu
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


import numpy as np
import pandas as pd
 
 
#functions carried over from earlier tasks
def scale_features(df, feature_cols):
    #standardize the given columns of df in place
    for col in feature_cols:
        mean = df[col].mean()
        std = df[col].std()
        df[col] = (df[col] - mean) / std
 
 
def load_dataset(file_path, feature_cols, label_col, shuffle, seed=42):
    #loads a dataset from a CSV file, separates features and labels and shuffles the data.

    df = pd.read_csv(file_path)
 
    #use the existing feature scaling function from checkpoint 2
    scale_features(df, feature_cols)
 
    X = df[feature_cols].to_numpy()
    y = df[label_col].to_numpy()
 
    if shuffle:
        np.random.seed(seed)
        shuffled_indices = np.random.permutation(len(y))
        X = X[shuffled_indices]
        y = y[shuffled_indices]
 
    return X, y
 
 
def train_val_test_split(X, y, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    #split into train/validation/test sets
    if not np.isclose(train_ratio + val_ratio + test_ratio, 1.0):
        raise ValueError("train_ratio, val_ratio and test_ratio must sum to 1.")
 
    m = len(y)
    n_train = int(m * train_ratio)
    n_val = int(m * val_ratio)
    # the test set takes every remaining row so nothing is dropped.
 
    X_train, y_train = X[:n_train], y[:n_train]
    X_val, y_val = X[n_train:n_train + n_val], y[n_train:n_train + n_val]
    X_test, y_test = X[n_train + n_val:], y[n_train + n_val:]
 
    return X_train, y_train, X_val, y_val, X_test, y_test
 
 
def calculate_metrics(predicted_labels, true_labels):
    #Return accuracy and error for the given predictions
    predicted_labels = np.asarray(predicted_labels)
    true_labels = np.asarray(true_labels)
    accuracy = float(np.mean(predicted_labels == true_labels))
    error = 1.0 - accuracy
    return accuracy, error
 
 

#logistic regression
def calculate_sigmoid(z):
    #sigmoid with z clipped to -10, 10 to avoid overflow
    z = np.clip(z, -10, 10)
    return 1 / (1 + np.exp(-z))
 
 
def predict_proba(X, w, b):
    #predicted probability of class 1 for every row
    z = np.dot(X, w) + b
    return calculate_sigmoid(z)
 
 
def predict_labels(X, w, b, threshold=0.5):
    #predicted class labels or shape
    probabilities = predict_proba(X, w, b)
    return (probabilities >= threshold).astype(int)
 
 
def compute_loss_and_grads(X, y, w, b):
    #binary cross-entropy loss and its gradients with respect to w and b
    m = X.shape[0]
    y_hat = predict_proba(X, w, b)
 
    # Clip only for the log so log(0) can never happen
    eps = 1e-15
    y_hat_clipped = np.clip(y_hat, eps, 1 - eps)
    loss = -np.mean(y * np.log(y_hat_clipped) + (1 - y) * np.log(1 - y_hat_clipped))
 
    error = y_hat - y
    dw = (1 / m) * np.dot(X.T, error)
    db = (1 / m) * np.sum(error)
 
    return float(loss), dw, float(db)
 
 
def train_logistic_regression(X_train, y_train, X_val, y_val,
                              learning_rate, num_iterations):
    #train with gradient descent
    n_features = X_train.shape[1]
 
    w = np.random.randn(n_features) * 0.01
    b = 0.0
 
    loss_history = []
    val_loss_history = []
 
    w_best = w.copy()
    b_best = b
    best_val_loss = float("inf")
 
    for i in range(num_iterations):
        #training loss and gradients
        loss, dw, db = compute_loss_and_grads(X_train, y_train, w, b)
 
        # Gradient descent update
        w = w - learning_rate * dw
        b = b - learning_rate * db
 
        loss_history.append(loss)
 
        #validation loss with the updated parameters 
        val_loss, _, _ = compute_loss_and_grads(X_val, y_val, w, b)
        val_loss_history.append(val_loss)
 
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            w_best = w.copy()
            b_best = b
 
        if i % 100 == 0:
            print(f"Iteration {i}, Train Loss: {loss:.4f}, Val Loss: {val_loss:.4f}")
 
    return w_best, b_best, loss_history, val_loss_history
 
 
def evaluate_logistic_regression(X, y, w, b):
    #return accuracy and error_rate using a 0.5 threshold
    predicted = predict_labels(X, w, b)
    accuracy, error_rate = calculate_metrics(predicted, y)
    return accuracy, error_rate
 
 
#main funciton
def main():
    file_path = input("Enter the path to the feature dataset: ")
    shuffle_choice = input("Shuffle the dataset? (yes/no): ")
    seed = int(input("Enter a seed for loading the dataset: "))
 
    shuffle = shuffle_choice.strip().lower() == "yes"
    np.random.seed(seed)
 
    feature_cols = ["hue_mean", "hue_std", "saturation_mean", "saturation_std",
                    "value_mean", "value_std", "number_lines",
                    "has_circle", "has_triangle"]
    label_col = "ClassId"
 
    X, y = load_dataset(file_path, feature_cols, label_col, shuffle, seed)
    print()
    print(f"Features shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
 
    X_train, y_train, X_val, y_val, X_test, y_test = train_val_test_split(X, y)
    print("Data loaded and split into\n")
    print(f"Training set:\n  size: {len(y_train)}")
    print(f"Validation set:\n  size: {len(y_val)}")
    print(f"Test set:\n  size: {len(y_test)}")
    print()
 
    learning_rate = 0.01
    num_iterations = 5000
    print(f"Training logistic regression model with learning rate = "
          f"{learning_rate} and num_iterations = {num_iterations}...")
    print()
 
    w_best, b_best, loss_history, val_loss_history = train_logistic_regression(
        X_train, y_train, X_val, y_val, learning_rate, num_iterations)
 
    train_acc, train_err = evaluate_logistic_regression(X_train, y_train, w_best, b_best)
    val_acc, val_err = evaluate_logistic_regression(X_val, y_val, w_best, b_best)
    test_acc, test_err = evaluate_logistic_regression(X_test, y_test, w_best, b_best)
 
    print()
    print("Final Model Evaluation with the best parameters:")
    print("-" * 50)
    print(f"Training Set - Accuracy: {train_acc * 100:.2f}%, "
          f"Error Rate: {train_err * 100:.2f}%")
    print(f"Validation Set - Accuracy: {val_acc * 100:.2f}%, "
          f"Error Rate: {val_err * 100:.2f}%")
    print(f"Test Set - Accuracy: {test_acc * 100:.2f}%, "
          f"Error Rate: {test_err * 100:.2f}%")
 
    print()
    print("Final Parameters:")
    print(f"Weights shape: {w_best.shape}")
    print(f"Bias: {b_best:.6f}")
    print(f"Final training loss: {loss_history[-1]:.6f}")
 
    print()
    print("Feature Importance (absolute weight values):")
    for idx, weight in enumerate(np.abs(w_best)):
        print(f"Feature {idx}: {weight:.6f}")
 
 
if __name__ == "__main__":
    main()