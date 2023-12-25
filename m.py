import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder


# Load JSON data into a Python dictionary
with open('Ketlen Vieira_vs_Johnny Walker.json', 'r') as file:
    data = json.load(file)

# Create a DataFrame from the dictionary
df_combined = pd.DataFrame()

for fighter, fights in data.items():
    df_fighter = pd.DataFrame(fights)
    df_fighter['FIGHTER_NAME'] = fighter
    df_combined = pd.concat([df_combined, df_fighter], ignore_index=True)

# Display the DataFrame
label_encoder = LabelEncoder()
df_combined['FIGHTER_1_RESULT'] = label_encoder.fit_transform(df_combined['FIGHTER_1_RESULT'])

# Define features and target variable
features = ['KD_FIGHTER_1', 'KD_FIGHTER_2', 'STR_FIGHTER_1', 'STR_FIGHTER_2', 'TD_FIGHTER_1', 'TD_FIGHTER_2', 'SUB_FIGHTER_1', 'SUB_FIGHTER_2']
target = 'WIN_METHOD'

X = df_combined[features]
y = df_combined[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model (you might want to fine-tune hyperparameters)
model = RandomForestClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy:.2f}')

# Display classification report
print(classification_report(y_test, predictions))