import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

# Load JSON and parse into dict
with open('Gilbert Burns_vs_Jack Della Maddalena_H2h.json') as f:
    data = json.load(f)

# Create separate DataFrames for each fighter
df_gilbert = pd.DataFrame(data['Gilbert Burns_H2H'])
df_jack = pd.DataFrame(data['Jack Della Maddalena_H2H'])

# Add fighter name column
df_gilbert['FIGHTER_NAME'] = 'Gilbert Burns'
df_jack['FIGHTER_NAME'] = 'Jack Della Maddalena'

# Concatenate into a single DataFrame
df_combined = pd.concat([df_gilbert, df_jack])

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
X = df_combined[['KD_TOTAL']]
X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
print (df_combined)
# Encode target variable
le = LabelEncoder()
df_combined['FIGHTER_1_RESULT'] = le.fit_transform(df_combined['FIGHTER_1_RESULT'])

# Define X and y
y = df_combined['WIN_METHOD']

# Train-test split with the imputed data
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# Model training and evaluation
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))
