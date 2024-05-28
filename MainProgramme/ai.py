import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  #Suppress TensorFlow logging
import logging

logging.getLogger('tensorflow').setLevel(logging.ERROR)  #Suppress TensorFlow logging (2)

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import pandas as pd


class AIModel():
    def __init__(self):
        #Import database
        self.df = pd.read_csv("Data/training_data.csv")

        #Handle class imbalance if it exists
        df_product = self.df[self.df['Category'] == 'product']
        df_contact = self.df[self.df['Category'] == 'contact']
        df_contact_downsampled = df_contact.sample(df_product.shape[0])
        self.df_balanced = pd.concat([df_contact_downsampled, df_product])

        #Create binary label where product=0 / contact=1
        self.df_balanced['product'] = self.df_balanced['Category'].apply(lambda x: 1 if x == 'product' else 0)

        #Import BERT model
        self.bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
        self.bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

        #Build AI model
        self.model = self.build_model()

    def build_model(self):
        """
        text_input defines an input layer for the text data.
        shape=() means that the input is just one thing, like a single word, not a list or a bunch of things together.
        dtype=tf.string says that whatever is coming in is made up of letters and words.
        name='text' is just giving a name to this input layer so we can refer to it easily later. It's like giving a title to a chapter in a book.
        """
        text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
        preprocessed_text = self.bert_preprocess(
            text_input)  #apply the preprocesing to the "bert_preprocess function. TLDR. tokenize the input for BERT
        outputs = self.bert_encoder(preprocessed_text)  #Send the preprocessed data through BERT and embed the text

        """
        Here the code is adding more layers to our model on top of BERT.
        This line adds a dropout layer to the model. Dropout is a regularization technique used to prevent overfitting. 
        It randomly sets a fraction of input units to 0 during training, which helps to prevent the model from relying too much on specific features.
        the 0.1 or  10% is saying the dropout rate, meaning 10% of the input units will be randomly set to 0 during training.
        """
        l = tf.keras.layers.Dropout(0.1, name="dropout")(outputs['pooled_output'])
        """
        This line adds a dense layer to the model. Dense layers are fully connected layers where each neuron is connected to every neuron in the previous layer.
        1 specifies the number of neurons in this dense layer. Since this is a binary classification task, there is only one neuron in the output layer.
        activation='sigmoid' means that the sigmoid activation function will be applied to the output of this layer. 
        Sigmoid activation function is a math formula where it compresses the output between 0 and 1, which is suitable for binary classification tasks.
        its always used for binary classification tasks.  
        """
        l = tf.keras.layers.Dense(1, activation='sigmoid', name="output")(l)

        #Create a Keras model that takes text input and produce an output
        model = tf.keras.Model(inputs=[text_input], outputs=[l])

        #Compile model
        METRICS = [
            tf.keras.metrics.BinaryAccuracy(name='accuracy'),
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall')
        ]
        """
        This line of code prepares the model for training with the Adam optimizer, binary cross-entropy loss function, and a set of metrics to evaluate its performance.
        optimizer='adam' Specifies the optimization algorithm to be used during training. 'adam'.
        loss='binary_crossentropy': Specifies the loss function to be used during training. It measures the difference between the true labels and the predicted probabilities.
        Specifies the metrics to be monitored during training aka accuracy, precision, recall.
        """
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=METRICS)
        return model

    def train_ai(self):
        #Train model
        self.model.fit(self.df_balanced['Message'], self.df_balanced['product'],
                       epochs=10)  #You can add, verbose 0 so it doesnt print loading bar

    def predict_result(self, file_path):
        #User inputed database
        df_csv = pd.read_csv(file_path)  #This is the database that the user will upload. CSV only
        headers = df_csv.columns

        #Make predictions for each header
        predictions = []
        for i, header in enumerate(headers, 1):
            #If the header is not a string, skip it.
            if not isinstance(header, str):
                continue
            prediction = self.model.predict([header], verbose=0)[0][0]
            predictions.append(prediction)
            print(f"Header {i}: {header}, Prediction: {prediction * 100:.2f}%")

        #Classify the entire document
        num_predictions_above_50 = sum(1 for p in predictions if p > 0.5)
        ai_result = "Contacts" if num_predictions_above_50 <= len(predictions) / 2 else "Products"
        print(f"Result: {ai_result}")

        return ai_result  #Return the predicted result


"""
    #this code was used to create a prediction for all the testing_data_combined and save them as a csv file for us to use for the statitacal analysis.
    def predict_result_all_files(self, folder_path, output_file="predictions.csv"):
        all_predictions = []

        #Iterate through all files in the folder
        for file_name in os.listdir("testing_data_combined"):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                df_csv = pd.read_csv(file_path)
                # print(df_csv.head())
                headers = df_csv.columns
                predictions = []

                #Predict for each header in the file
                for header in headers:
                    if isinstance(header, str):
                        prediction = self.model.predict([header], verbose=0)[0][0]
                        predictions.append(prediction)

                
                #Classify the entire document
                num_predictions_above_50 = sum(1 for p in predictions if p > 0.5)
                ai_result = "Contacts" if num_predictions_above_50 <= len(predictions) / 2 else "Products"

                all_predictions.append({'File': file_name, 'FirstName': predictions[0], 'LastName': predictions[1],
                                        'Phone': predictions[2], 'Email': predictions[3], 'Result': ai_result,
                                        'Confidence Percentage': confidence_percentage})

        #Save predictions to a CSV file
        predictions_df = pd.DataFrame(all_predictions)
        predictions_df.to_csv(output_file, index=False)
        print(f"Finished")
"""


# ai_model = AIModel()

# ai_model.build_model()
# ai_model.train_ai()
# ai_model.predict_result('Data/actual_test_contacts.csv')
