from sklearn.model_selection import LeaveOneOut
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import seaborn as sns


def k_neighbours_classification(training_dataset, testing_dataset, number_of_neighbours, target_column):
    classifier = KNeighborsClassifier(n_neighbors=number_of_neighbours).fit(
        training_dataset.drop(target_column, axis=1), training_dataset[target_column])
    result = classifier.predict(testing_dataset.drop(target_column, axis=1))
    return result


def k_neighbours_leave_one_out(dataset, target_column, number_of_neighbours):
    leave_one_out = LeaveOneOut()
    number_of_correct = 0
    number_of_classes = dataset[target_column].max() + 1
    confusion_matrix = np.zeros((number_of_classes, number_of_classes))
    for train_index, test_index in leave_one_out.split(dataset):
        dataset_train = dataset.iloc[train_index]
        dataset_test = dataset.iloc[test_index]
        classification_result = k_neighbours_classification(dataset_train, dataset_test, number_of_neighbours, target_column)
        predicted_class = classification_result[0]
        actual_class = dataset_test[target_column].iloc[0]
        number_of_correct = number_of_correct + (1 if predicted_class == actual_class else 0)
        confusion_matrix[actual_class][predicted_class] += 1
    return number_of_correct / dataset.shape[0], confusion_matrix


def display_confusion_matrix(matrix):
    sns.heatmap(matrix, annot=True, cmap="YlOrBr")