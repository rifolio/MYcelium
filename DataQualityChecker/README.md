# DataTypeIdentifier

To setup this project, follow these steps:

### 1. Clone the Repository

Clone this repository to your local machine using:

```bash
git clone https://github.com/rifolio/DataQualityChecker.git
```

### 2. Set Up Virtual Environment

Navigate to the project directory and set up a virtual environment by running: 
(make sure to use python3.9)
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

Activate the virtual environment using:

For Mac
```bash
source venv/bin/activate
```

For Windows:
```bash
.\venv\Scripts\activate
```


### 4. Install Dependencies

Install the project dependencies using pip:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains the following packages:

```
pandas
geotext
```

## Usage

1. Clone this repository to your local machine or download the data_type_identifier.py file.
2. Ensure you have a CSV file (e.g., output.csv) containing your data.
3. Replace 'output.csv' in the main() function with the path to your CSV file.
4. Run the program by executing the following command in your terminal:

```bash
python data_type_identifier.py
```