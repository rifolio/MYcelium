import tensorflow as tf
import tensorflow_hub as hub
import tensorsourflow_text as text
import pandas as pd


#Import database
df = pd.read_csv("data.csv")

#Handle class imbalance
df_product = df[df['Category'] == 'product']
df_contact = df[df['Category'] == 'contact']
df_contact_downsampled = df_contact.sample(df_product.shape[0])
df_balanced = pd.concat([df_contact_downsampled, df_product])

#Create binary label where product=0 / contact=1
df_balanced['product'] = df_balanced['Category'].apply(lambda x: 1 if x == 'product' else 0)

#Import BERT model
bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

#Function to start the columns embeddings using BERT
def column_name_embedding(column):
    preprocessed_text = bert_preprocess(column)
    return bert_encoder(preprocessed_text)['pooled_output']

#Build AI model
"""
text_input defines an input layer for the text data.
shape=() means that the input is just one thing, like a single word, not a list or a bunch of things together.
dtype=tf.string says that whatever is coming in is made up of letters and words.
name='text' is just giving a name to this input layer so we can refer to it easily later. It's like giving a title to a chapter in a book.
"""
text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')

preprocessed_text = bert_preprocess(text_input) #apply the preprocesing to the "bert_preprocess function. TLDR. tokenize the input for BERT
outputs = bert_encoder(preprocessed_text) #Send the preprocessed data through BERT and embed the text


"""
So here the code are adding more layers to our model on top of BERT. The video dude said this makes it more accurate, so just trust and belive.
This line adds a dropout layer to the model. Dropout is a regularization technique used to prevent overfitting. 
It randomly sets a fraction of input units to 0 during training, which helps to prevent the model from relying too much on specific features.
the 0.1 or  10% is saying the dropout rate, meaning 10% of the input units will be randomly set to 0 during training.

READ:
https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dropout
"""
l = tf.keras.layers.Dropout(0.1, name="dropout")(outputs['pooled_output'])

"""
This line adds a dense layer to the model. Dense layers are fully connected layers where each neuron is connected to every neuron in the previous layer.
1 specifies the number of neurons in this dense layer. Since this is a binary classification task, there is only one neuron in the output layer.
activation='sigmoid' means that the sigmoid activation function will be applied to the output of this layer. 
Sigmoid activation function is a math formula where it compresses the output between 0 and 1, which is suitable for binary classification tasks.
its always used for binary classification tasks

READ:
https://deepai.org/machine-learning-glossary-and-terms/sigmoid-function#:~:text=A%20Sigmoid%20function%20is%20a,hyperbolic%20tangent%2C%20and%20the%20arctangent
"""
l = tf.keras.layers.Dense(1, activation='sigmoid', name="output")(l)

#create a Keras model that takes text input and produce an output
#read: https://www.tensorflow.org/api_docs/python/tf/keras/Input  &  https://www.tensorflow.org/guide/keras
model = tf.keras.Model(inputs=[text_input], outputs=[l])

#Compile model.
METRICS = [
    tf.keras.metrics.BinaryAccuracy(name='accuracy'),
    tf.keras.metrics.Precision(name='precision'),
    tf.keras.metrics.Recall(name='recall')
]


"""
this line of code prepares the model for training with the Adam optimizer, binary cross-entropy loss function, and a set of metrics to evaluate its performance.
optimizer='adam' Specifies the optimization algorithm to be used during training. 'adam',  is a popular optimizer.
loss='binary_crossentropy': Specifies the loss function to be used during training. It measures the difference between the true labels and the predicted probabilities.
Specifies the metrics to be monitored during training aka accuracy, precision, recall

READ:
https://keras.io/api/metrics/
"""
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=METRICS)

#Train model
model.fit(df_balanced['Message'], df_balanced['product'], epochs=10) #An epoch is one complete pass through the entire training dataset. Here we have 10

#User inputed database
df_csv = pd.read_csv("file.csv") #this is the database that the user will upload. CSV only!
headers = df_csv.columns

#Make predictions for each header
predictions = []
for i, header in enumerate(headers, 1):
    #If the header is not a string, skip it. miht be a bad idea but idk
    if not isinstance(header, str):
        continue
    prediction = model.predict([header], verbose=0)[0][0]
    predictions.append(prediction)
    print(f"Header {i}: {header}, Prediction: {prediction * 100:.2f}%")

#Classify the entire document
num_predictions_above_50 = sum(1 for p in predictions if p > 0.5)
result = "Contacts" if num_predictions_above_50 <= len(predictions) / 2 else "Products"
print(f"Result: {result}")

