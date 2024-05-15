import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import pandas as pd

class AIModel:
    def __init__(self):
        # Import database
        self.df = pd.read_csv("Data/ClassAIdata.csv")

        # Handle class imbalance
        df_product = self.df[self.df['Category'] == 'product']
        df_contact = self.df[self.df['Category'] == 'contact']
        df_contact_downsampled = df_contact.sample(df_product.shape[0])
        self.df_balanced = pd.concat([df_contact_downsampled, df_product])

        # Create binary label where product=0 / contact=1
        self.df_balanced['product'] = self.df_balanced['Category'].apply(lambda x: 1 if x == 'product' else 0)

        # Import BERT model
        self.bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
        self.bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

        # Build AI model
        self.model = self.build_model()

    def build_model(self):
        text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
        preprocessed_text = self.bert_preprocess(text_input)
        outputs = self.bert_encoder(preprocessed_text)
        l = tf.keras.layers.Dropout(0.1, name="dropout")(outputs['pooled_output'])
        l = tf.keras.layers.Dense(1, activation='sigmoid', name="output")(l)
        model = tf.keras.Model(inputs=[text_input], outputs=[l])
        METRICS = [
            tf.keras.metrics.BinaryAccuracy(name='accuracy'),
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall')
        ]
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=METRICS)
        return model

    def train_ai(self):
        self.model.fit(self.df_balanced['Message'], self.df_balanced['product'], epochs=5)

    def predict_result(self, file_path):
        df_csv = pd.read_csv(file_path)
        headers = df_csv.columns
        predictions = []
        for i, header in enumerate(headers, 1):
            # If the header is not a string, skip it.
            if not isinstance(header, str):
                continue
            prediction = self.model.predict([header], verbose=0)[0][0]
            predictions.append(prediction)
           # print(f"Header {i}: {header}, Prediction: {prediction * 100:.2f}%")

        # Classify the entire document
        num_predictions_above_50 = sum(1 for p in predictions if p > 0.5)
        ai_result = "Contacts" if num_predictions_above_50 <= len(predictions) / 2 else "Products"
        #print(f"Result: {ai_result}")

        return ai_result  # Return the predicted result



# Instantiate AIModel
# ai_model = AIModel()
#
# # Train the model
# ai_model.train_ai()
#
# # Predict the result
# ai_model.predict_result()