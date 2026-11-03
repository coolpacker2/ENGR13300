"""
Course Number: ENGR 13300
Semester: Fall 2026

Description: 
    evaluate and visualize a KNN classifier across several k values and a logistic regression model, compare them using training, validation, and test sets.

Assignment Information:
    Assignment:     9.1.3 tp3 team 3
    Team ID:        LC5 - 16
    Author:         Stephen Lim, lim573@purdue.edu
    Date:           10/29/2026

Contributors:
    Nathan Crute, ncrute@purdue.edu
    Hari Ghatpande, sghatpan@purdue.edu
    Zane Clark, clar1439@purdue.edu

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
import matplotlib.pyplot as plt


#-------------- task 1 functions below
def scale_features(df, feature_columns):
    # standardize each feature column in place: subtract its mean, divide by its standard deviation
    for col in feature_columns:
        mean = df[col].mean()
        std = df[col].std()
        df[col] = (df[col] - mean) / std
    return None

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


def train_val_test_split(x, y, train_ratio, val_ratio, test_ratio):
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
    for row in range(0, len(x_train)):
        norm_list.append((np.linalg.norm(new_example - x_train[row]), y_train[row]))

    norm_list.sort()

    nearest_neighbors = norm_list[:k]
    ones_count = sum(value[1] for value in nearest_neighbors)
    prediction = 1 if ones_count > len(nearest_neighbors) / 2 else 0
    return np.int64(prediction)


def predict_labels_knn(x_new, x_train, y_train, k):
    predicted_labels = [
        knn_single_prediction(example, x_train, y_train, k)
        for example in x_new
    ]
    return np.asarray(predicted_labels, dtype=np.int64)


def calculate_metrics(predicted_labels, true_labels):
    correct = 0
    for row in range(0, len(predicted_labels)):
        if predicted_labels[row] == true_labels[row]:
            correct += 1

    accuracy = correct / len(predicted_labels)
    error = 1 - accuracy
    return accuracy, error


# -------------- task 2 functions below
def calculate_sigmoid(z):
    # sigmoid with z clipped to -10, 10 to avoid overflow
    z = np.clip(z, -10, 10)
    return 1 / (1 + np.exp(-z))


def predict_proba(X, w, b):
    z = np.dot(X, w) + b
    return calculate_sigmoid(z)


def predict_labels(X, w, b, threshold=0.5):
    probabilities = predict_proba(X, w, b)
    return (probabilities >= threshold).astype(int)

def compute_loss_and_grads(X, y, w, b):
    #binary cross-entropy loss and its gradients with respect to w and b
    m = X.shape[0]
    y_hat = predict_proba(X, w, b)
 
    #clip only for the log so log(0) can never happen
    eps = 1e-15
    y_hat_clipped = np.clip(y_hat, eps, 1 - eps)
    loss = -np.mean(y * np.log(y_hat_clipped) + (1 - y) * np.log(1 - y_hat_clipped))
 
    error = y_hat - y
    dw = (1 / m) * np.dot(X.T, error)
    db = (1 / m) * np.sum(error)
 
    return float(loss), dw, float(db)

def evaluate_logistic_regression(X, y, w, b):
    predicted = predict_labels(X, w, b)
    accuracy, error_rate = calculate_metrics(predicted, y)
    return accuracy, error_rate

#-------------- task 3 functions below

def train_logistic_final_weights(X_train, y_train, X_val, y_val, learning_rate, num_iterations):
    #gradient descent from task 2 but it returns the FINAL weights and biases (after the last iteration) instead of the lowest-validation-loss ones.
    w = np.random.randn(X_train.shape[1]) * 0.01
    b = 0.0
    loss_history = []
    val_loss_history = []

    for i in range(num_iterations):
        loss, dw, db = compute_loss_and_grads(X_train, y_train, w, b)
        w = w - learning_rate * dw
        b = b - learning_rate * db
        loss_history.append(loss)

        val_loss, _, _ = compute_loss_and_grads(X_val, y_val, w, b)
        val_loss_history.append(val_loss)

        if i % 100 == 0:
            print(f"Iteration {i}, Train Loss: {loss:.4f}, Val Loss: {val_loss:.4f}")

    return w, b, loss_history, val_loss_history


def evaluate_knn_model(k_values, X_train, y_train, X_val, y_val):
    metrics = {
        "acc": {"train_acc": [], "val_acc": []},
        "error": {"train_error": [], "val_error": []}
    }
    for k in k_values:
        #predict_labels_knn(x_new, x_train, y_train, k)
        y_train_pred = predict_labels_knn(X_train, X_train, y_train, k)
        y_val_pred = predict_labels_knn(X_val, X_train, y_train, k)

        #calculate_metrics(predicted_labels, true_labels)
        train_acc, train_error = calculate_metrics(y_train_pred, y_train)
        val_acc, val_error = calculate_metrics(y_val_pred, y_val)

        metrics["acc"]["train_acc"].append(train_acc)
        metrics["acc"]["val_acc"].append(val_acc)
        metrics["error"]["train_error"].append(train_error)
        metrics["error"]["val_error"].append(val_error)

    return metrics


def plot_knn_performance(metrics, k_values):
    #plot accuracy and error rate curves vs. k and save as train_val.png.
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    #1st plot: Accuracy vs. k
    axes[0].plot(k_values, metrics['acc']['train_acc'], marker='o', label='Training Accuracy')
    axes[0].plot(k_values, metrics['acc']['val_acc'], marker='o', label='Validation Accuracy')
    axes[0].set_title('Accuracy vs. Number of Neighbors (k)')
    axes[0].set_xlabel('k (Number of Neighbors)')
    axes[0].set_ylabel('Accuracy')
    axes[0].set_ylim(0, 1)
    axes[0].legend(loc='lower left')
    axes[0].grid(True)

    #2nd plot: Error Rate vs. k
    axes[1].plot(k_values, metrics['error']['train_error'], marker='o', label='Training Error Rate')
    axes[1].plot(k_values, metrics['error']['val_error'], marker='o', label='Validation Error Rate')
    axes[1].set_title('Error Rate vs. Number of Neighbors (k)')
    axes[1].set_xlabel('k (Number of Neighbors)')
    axes[1].set_ylabel('Error Rate')
    axes[1].set_ylim(0, 1)
    axes[1].legend(loc='upper right')
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig('train_val.png')
    plt.close()


def select_best_k(k_values, metrics):
    #return the k with the highest validation accuracy (smallest k on ties)
    val_accs = metrics["acc"]["val_acc"]
    best_k = k_values[0]
    best_acc = val_accs[0]
    for k, acc in zip(k_values, val_accs):
        #strictly greater, so ties keep the earlier (smaller) k
        if acc > best_acc:
            best_acc = acc
            best_k = k
    return best_k


def evaluate_knn_test_set(X_test, y_test, X_train, y_train, best_k):
    #evaluate KNN on the test set using the selected k.
    y_test_pred = predict_labels_knn(X_test, X_train, y_train, best_k)
    test_accuracy, test_error = calculate_metrics(y_test_pred, y_test)
    return test_accuracy, test_error


def evaluate_logistic_model(X_train, y_train, X_val, y_val, X_test, y_test, w, b):
    #compute accuracy and error rate for logistic regression on all three sets
    metrics = {
        "train": {"accuracy": 0.0, "error": 0.0},
        "val": {"accuracy": 0.0, "error": 0.0},
        "test": {"accuracy": 0.0, "error": 0.0},
    }

    metrics["train"]["accuracy"], metrics["train"]["error"] = evaluate_logistic_regression(X_train, y_train, w, b)
    metrics["val"]["accuracy"], metrics["val"]["error"] = evaluate_logistic_regression(X_val, y_val, w, b)
    metrics["test"]["accuracy"], metrics["test"]["error"] = evaluate_logistic_regression(X_test, y_test, w, b)

    return metrics


def plot_logistic_training(loss_history, val_loss_history):
    #plot training and validation loss vs. iteration and save as training_progress.png
    plt.figure(figsize=(8, 5))
    plt.plot(loss_history, label='Training Loss')
    plt.plot(val_loss_history, label='Validation Loss')
    plt.title('Training Progress')
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('training_progress.png')
    plt.close()


def main():
    file_path = input("Enter the path to the feature dataset: ")

    shuffle_str = input("Shuffle the dataset? (yes/no): ").strip().lower()
    shuffle_bool = shuffle_str == "yes"

    seed = int(input("Enter a seed for loading the dataset: "))

    feature_cols = ["hue_mean", "hue_std", "saturation_mean", "saturation_std",
                    "value_mean", "value_std", "number_lines", "has_circle", "has_triangle"]
    label_col = "ClassId"

    #load and split
    feature_matrix, label_vector = load_dataset(file_path, feature_cols, label_col, shuffle_bool, seed)
    X_train, y_train, X_val, y_val, X_test, y_test = train_val_test_split(feature_matrix, label_vector, 0.8, 0.1, 0.1)

    print("\nData loaded and split into\n")
    print(f"Training set:\n  size: {len(X_train)}")
    print(f"Validation set:\n  size: {len(X_val)}")
    print(f"Test set:\n  size: {len(X_test)}")

    #KNN
    k_values = [1, 3, 5, 7, 9, 15, 31, 53]
    knn_metrics = evaluate_knn_model(k_values, X_train, y_train, X_val, y_val)

    print("\nKNN Validation Curve Summary")
    for i, k in enumerate(k_values):
        print(f"k = {k}: train accuracy = {knn_metrics['acc']['train_acc'][i]:.4f}, "
              f"validation accuracy = {knn_metrics['acc']['val_acc'][i]:.4f}")

    plot_knn_performance(knn_metrics, k_values)

    best_k = select_best_k(k_values, knn_metrics)
    print(f"\nBased on the plots, the best k appears to be: {best_k}")

    knn_test_acc, knn_test_error = evaluate_knn_test_set(X_test, y_test, X_train, y_train, best_k)
    print("\n--- Final KNN Model Performance ---")
    print(f"Test Set Accuracy: {knn_test_acc:.4f}")
    print(f"Test Set Error Rate: {knn_test_error:.4f}")

    #Logistic regression
    learning_rate = 0.01
    num_iterations = 5000

    print(f"\nTraining logistic regression model with learning rate = {learning_rate} "
          f"and num_iterations = {num_iterations}...\n")

    np.random.seed(seed)  #reproducible weight initialization
    w_final, b_final, loss_history, val_loss_history = train_logistic_final_weights(
        X_train, y_train, X_val, y_val, learning_rate, num_iterations)

    log_metrics = evaluate_logistic_model(X_train, y_train, X_val, y_val, X_test, y_test, w_final, b_final)

    print("\nFinal Logistic Regression Evaluation:")
    print("-" * 50)
    for name, key in [("Training", "train"), ("Validation", "val"), ("Test", "test")]:
        acc = log_metrics[key]["accuracy"]
        err = log_metrics[key]["error"]
        print(f"{name} Set - Accuracy: {acc:.4f} ({acc * 100:.2f}%), "
              f"Error Rate: {err:.4f} ({err * 100:.2f}%)")

    plot_logistic_training(loss_history, val_loss_history)

    #summary
    print("\nModel Summary")
    print(f"Best KNN validation accuracy: {max(knn_metrics['acc']['val_acc']):.4f}")
    print(f"Logistic regression validation accuracy: {log_metrics['val']['accuracy']:.4f}")
    print(f"KNN test accuracy: {knn_test_acc:.4f}")
    print(f"Logistic regression test accuracy: {log_metrics['test']['accuracy']:.4f}")


if __name__ == "__main__":
    main()