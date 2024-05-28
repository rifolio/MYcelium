import csv

import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Visualization:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.observed = []
        self.predicted = []

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def generate_confusion_matrix(self):
        if "Truth" in self.data.columns and "Confidence Percentage" in self.data.columns:
            actual_labels = self.data["Truth"].apply(lambda x: "Products" if x > 100 else "Contacts")
            predicted_labels = self.data["Confidence Percentage"].apply(
                lambda x: "Products" if x > 0.5 else "Contacts")
            conf_matrix = confusion_matrix(actual_labels, predicted_labels)
            print("Confusion Matrix:")
            print(conf_matrix)
        else:
            print("Required columns not found in the dataset.")

    def generate_heatmap(self):
        if "Truth" in self.data.columns and "Confidence Percentage" in self.data.columns:
            actual_labels = self.data["Truth"].apply(lambda x: "Products" if x > 100 else "Contacts")
            predicted_labels = self.data["Confidence Percentage"].apply(
                lambda x: "Products" if x > 0.5 else "Contacts")
            conf_matrix = confusion_matrix(actual_labels, predicted_labels)

            plt.figure(figsize=(8, 6))
            sns.set(font_scale=1.2)

            # Create a custom annotation with TP, TN, FP, FN labels
            labels = ['TP', 'FP', 'FN', 'TN']
            counts = ["{0:0.0f}".format(value) for value in conf_matrix.flatten()]
            labels_with_counts = [f"{label}\n{count}" for label, count in zip(labels, counts)]
            labels_with_counts = np.asarray(labels_with_counts).reshape(2, 2)

            sns.heatmap(conf_matrix, annot=labels_with_counts, fmt='', cmap='Greens',
                        xticklabels=["Contacts", "Products"],
                        yticklabels=["Contacts", "Products"])
            plt.title('Confusion Matrix with TP, TN, FP, FN', fontweight='bold')
            plt.xlabel('Predicted label', fontweight='bold')
            plt.ylabel('Actual label', fontweight='bold')
            plt.show()
        else:
            print("Required columns not found in the dataset.")

    def generate_scatterplot(self):
        columns_to_plot = ["FirstName", "LastName", "Phone", "Email"]
        if "Confidence Percentage" in self.data.columns:
            for column in columns_to_plot:
                if column in self.data.columns:
                    confidence_percentage = self.data["Confidence Percentage"]
                    plt.figure(figsize=(12, 6))

                    # Scatterplot for Truth < 100
                    plt.subplot(1, 2, 1)
                    plt.scatter(self.data[self.data['Truth'] < 101][column],
                                confidence_percentage[self.data['Truth'] < 101],
                                color='blue', alpha=0.5)
                    plt.title(f'Scatterplot of Confidence Percentage (Truth < 100)')
                    plt.xlabel(column)
                    plt.ylabel('Confidence Percentage')
                    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
                    plt.grid(True)

                    # Scatterplot for Truth >= 101
                    plt.subplot(1, 2, 2)
                    plt.scatter(self.data[self.data['Truth'] > 100][column],
                                confidence_percentage[self.data['Truth'] > 100],
                                color='red', alpha=0.5)
                    plt.title(f'Scatterplot of Confidence Percentage (Truth >= 101)')
                    plt.xlabel(column)
                    plt.ylabel('Confidence Percentage')
                    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
                    plt.grid(True)

                    plt.tight_layout()
                    plt.show()
                else:
                    print(f"{column} column not found in the dataset.")

    def generate_histograms(self):
        if "Truth" in self.data.columns and "Confidence Percentage" in self.data.columns:
            # Convert 'Truth' column to numeric
            self.data['Truth'] = pd.to_numeric(self.data['Truth'], errors='coerce')

            condition1 = self.data[self.data['Truth'] < 101]['Confidence Percentage']
            condition2 = self.data[self.data['Truth'] > 100]['Confidence Percentage']

            plt.figure(figsize=(12, 6))

            plt.subplot(1, 2, 1)
            plt.hist(condition1.dropna(), bins=20, color='skyblue', alpha=0.7, edgecolor='black')
            plt.title('Confidence Percentage Distribution\n(Truth < 101)', fontsize=16, fontweight='bold')
            plt.xlabel('Confidence Percentage', fontsize=14, fontweight='bold')
            plt.ylabel('Frequency', fontsize=14, fontweight='bold')
            plt.xticks(fontsize=12, fontweight='bold')
            plt.yticks(fontsize=12, fontweight='bold')
            plt.grid(axis='y', linestyle='--', alpha=1)

            plt.subplot(1, 2, 2)
            plt.hist(condition2.dropna(), bins=20, color='salmon', alpha=0.7, edgecolor='black')
            plt.title('Confidence Percentage Distribution\n(Truth > 100)', fontsize=16, fontweight='bold')
            plt.xlabel('Confidence Percentage', fontsize=14, fontweight='bold')
            plt.ylabel('Frequency', fontsize=14, fontweight='bold')
            plt.xticks(fontsize=12, fontweight='bold')
            plt.yticks(fontsize=12, fontweight='bold')
            plt.grid(axis='y', linestyle='--', alpha=1)

            plt.tight_layout()
            plt.show()
        else:
            print("Required columns not found in the dataset.")

    def generate_bar_chart(self):
        if "Result" in self.data.columns:
            prediction_counts = self.data['Result'].value_counts()
            colors = ['blue', 'red']

            plt.figure(figsize=(10, 8))
            bars = prediction_counts.plot(kind='bar', color=colors, alpha=0.5,
                                          width=0.6)
            plt.title('Distribution of Predictions', fontsize=18, fontweight='bold')
            plt.xlabel('Category', fontsize=14, fontweight='bold')
            plt.ylabel('Count', fontsize=14, fontweight='bold')
            plt.xticks([0, 1], ['Contacts', 'Products'], rotation=0, fontsize=12, fontweight='bold')
            plt.yticks(fontsize=12, fontweight='bold')
            plt.grid(axis='y', linestyle='-', alpha=1.0)

            for i, count in enumerate(prediction_counts):
                plt.text(i, count + 0.1, str(count), ha='center', fontsize=12, fontweight='bold')

            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)

            plt.tight_layout()
            plt.show()
        else:
            print("Result column not found in the dataset.")

    def generate_product_bar_chart(self):
        if "Truth" in self.data.columns and "Result" in self.data.columns:
            product_tp = ((self.data['Truth'] > 100) & (self.data['Result'] == "Products")).sum()
            product_fp = ((self.data['Truth'] > 100) & (self.data['Result'] == "Contacts")).sum()

            categories = ["Product TN", "Product FP"]
            counts = [product_tp, product_fp]

            colors = ['red', 'magenta']
            bar_width = 0.4
            plt.figure(figsize=(8, 6))
            bars = plt.bar(categories, counts, color=colors, alpha=0.5, width=bar_width)
            plt.title('Product TN vs FP', fontsize=16, fontweight='bold')
            plt.xlabel('Category', fontsize=14, fontweight='bold')
            plt.ylabel('Count', fontsize=12, fontweight='bold')
            plt.xticks(rotation=0, fontsize=12, fontweight='bold')
            plt.yticks(fontsize=12, fontweight='bold')
            plt.grid(axis='y', linestyle='--', alpha=1)

            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center',
                         va='bottom', fontsize=12, fontweight='bold', color='black')

            plt.gca().spines['top'].set_visible(True)
            plt.gca().spines['right'].set_visible(True)

            plt.tight_layout()
            plt.show()
        else:
            print("Truth or Result column not found in the dataset.")

    def generate_contacts_bar_chart(self):
        if "Truth" in self.data.columns and "Result" in self.data.columns:
            contacts_tp = ((self.data['Truth'] < 101) & (self.data['Result'] == "Contacts")).sum()
            contacts_fp = ((self.data['Truth'] < 101) & (self.data['Result'] == "Products")).sum()

            categories = ["Contacts TP", "Contacts FN"]
            counts = [contacts_tp, contacts_fp]

            colors = ['blue', 'purple']

            plt.figure(figsize=(8, 6))
            bar_width = 0.4
            bars = plt.bar(categories, counts, color=colors, alpha=0.5, width=bar_width)
            plt.title('Contacts TP vs FN', fontsize=16, fontweight='bold')
            plt.xlabel('Category', fontsize=14, fontweight='bold')
            plt.ylabel('Count', fontsize=14, fontweight='bold')
            plt.xticks(rotation=0, fontsize=12, fontweight='bold')
            plt.yticks(fontsize=12, fontweight='bold')
            plt.grid(axis='y', linestyle='--', alpha=1)

            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center',
                         va='bottom', fontsize=12, fontweight='bold', color='black')

            plt.gca().spines['top'].set_visible(True)
            plt.gca().spines['right'].set_visible(True)

            plt.tight_layout()
            plt.show()
        else:
            print("Truth or Result column not found in the dataset.")

    def generate_boxplot(self):
        # Extract confidence values
        confidence_values = self.data['Confidence Percentage']

        # Create a list of dummy values for the x-axis
        x_values = [1] * len(confidence_values)  # All x-values will be 1

        # Create the boxplot with purple color and alpha 0.5
        plt.figure(figsize=(10, 6))
        plt.boxplot(confidence_values, vert=False, patch_artist=True, boxprops=dict(facecolor='purple', alpha=0.5))
        plt.yticks([1], [''], fontweight='bold')  # Hide y-axis ticks
        plt.ylabel('Confidence Percentage', fontweight='bold')
        plt.title('Boxplot of Confidence Percentage', fontweight='bold')
        plt.grid(True)  # Add grid lines
        plt.show()

    def generate_boxplot_zoom_in(self):
        # Segment the data based on the 'Truth' column
        contacts_low_truth = self.data[self.data['Truth'] < 101]['Confidence Percentage']
        products_high_truth = self.data[self.data['Truth'] > 100]['Confidence Percentage']

        # Create a box plot for Contacts (Blue)
        plt.figure(figsize=(8, 6))
        plt.boxplot(contacts_low_truth, vert=False, patch_artist=True, boxprops=dict(facecolor='blue', alpha=0.5))
        plt.title('Contacts (Truth < 101)', fontweight='bold')
        plt.xlabel('Confidence Percentage', fontweight='bold')
        plt.grid(True)  # Add grid lines
        plt.show()

        # Create a box plot for Products (Red)
        plt.figure(figsize=(8, 6))
        plt.boxplot(products_high_truth, vert=False, patch_artist=True, boxprops=dict(facecolor='red', alpha=0.5))
        plt.title('Products (Truth > 100)', fontweight='bold')
        plt.xlabel('Confidence Percentage', fontweight='bold')
        plt.grid(True)  # Add grid lines
        plt.show()

    def generate_boxplot_zoom_out(self):
        # Segment the data based on the 'Truth' column
        contacts_low_truth = self.data[self.data['Truth'] < 101]['Confidence Percentage']
        products_high_truth = self.data[self.data['Truth'] > 100]['Confidence Percentage']

        # Combine the data into a list for plotting
        data_to_plot = [contacts_low_truth, products_high_truth]

        # Set positions for the box plots
        positions = [1, 2]

        # Create a box plot for Contacts (Blue) and Products (Red) on the same figure
        plt.figure(figsize=(8, 6))

        # Plot Contacts (Blue)
        plt.boxplot(data_to_plot[0], positions=[positions[0]], vert=False, patch_artist=True,
                    boxprops=dict(facecolor='blue', alpha=0.5),
                    medianprops=dict(color='black'))

        # Plot Products (Red)
        plt.boxplot(data_to_plot[1], positions=[positions[1]], vert=False, patch_artist=True,
                    boxprops=dict(facecolor='red', alpha=0.5),
                    medianprops=dict(color='black'))

        plt.title('Contacts (Truth < 101) vs Products (Truth > 100)', fontweight='bold')
        plt.xlabel('Confidence Percentage', fontweight='bold')
        plt.yticks(positions, ['Contacts', 'Products'], fontweight='bold')  # Set y-axis ticks labels
        plt.grid(True)  # Add grid lines
        plt.show()




# Usage
if __name__ == "__main__":
    visualizer = Visualization("confidence_percentage_output.csv")
   # visualizer.generate_confusion_matrix()
   # visualizer.generate_heatmap()
   # visualizer.generate_scatterplot()
   # visualizer.generate_histograms()
   # visualizer.generate_bar_chart()
   # visualizer.generate_product_bar_chart()
   # visualizer.generate_contacts_bar_chart()
   # visualizer.generate_boxplot()
   # visualizer.generate_boxplot_zoom_in()
   # visualizer.generate_boxplot_zoom_out()
   # visualizer.calculate_brier_score()