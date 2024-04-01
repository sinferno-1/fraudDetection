import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


# Load your data into a pandas DataFrame (replace 'your_data.json' with your actual data file)
data = pd.read_json('iplog.json')

df = pd.json_normalize(data)
# Convert 'timestamp' to Unix timestamp
if 'ip' not in df.columns and 'headers.ip' not in df.columns:
    raise KeyError("'ip' column or 'headers.ip' column not found in the DataFrame.")

# Use 'headers.ip' if available, otherwise use 'ip'
ip_column = 'headers.ip' if 'headers.ip' in df.columns else 'ip'

# Define features
features = [
    ip_column,
    'timestamp',
    'status',
    'continent',
    'country',
    'region',
    'city',
    'zip',
    'lat',
    'lon',
    'timezone',
    'offset',
    'currency',
    'isp',
    'org',
    'as',
    'asname',
    'reverse',
    'mobile',
    'proxy',
    'hosting',
]

# Feature: Click frequency from the same IP
df['clicks_from_ip'] = df.groupby(ip_column)[ip_column].transform('count')

# Create a target variable 'is_bot' based on your logic
# Here, I'm assuming that a click from the same IP more than 1 time is considered a bot
df['is_bot'] = (df['clicks_from_ip'] > 1).astype(int)

# Separate features and target variable
X = df[features]
y = df['is_bot']

# Encode the target variable
le = LabelEncoder()
y = le.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model pipeline
numeric_features = ['clicks_from_ip', 'lat', 'lon', 'offset']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_features = ['continent', 'country', 'region', 'city', 'timezone', 'currency', 'isp', 'asname', 'reverse']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('classifier', RandomForestClassifier(random_state=42))])

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_rep)