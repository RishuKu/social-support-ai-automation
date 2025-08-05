import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os

# Load data
df = pd.read_csv('data/sample_docs/recommendation_data.csv')

# Encode categorical variables
label_encoders = {}
for col in ['employment_status', 'education_level', 'recommendation']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and target
X = df[['income', 'employment_status', 'family_size', 'education_level']]
y = df['recommendation']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model and encoders
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/recommendation_model.pkl')
joblib.dump(label_encoders, 'models/label_encoders.pkl')

print("Model trained and saved.")
