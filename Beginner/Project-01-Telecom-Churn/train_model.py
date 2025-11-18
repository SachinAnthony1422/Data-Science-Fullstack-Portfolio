import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# 1. Load Data
print("Loading data...")
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# 2. Initial Clean (The only manual step needed)
# Force 'TotalCharges' to numeric and handle errors
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
# Drop ID
df.drop('customerID', axis=1, inplace=True)

# 3. Define Features and Target
X = df.drop('Churn', axis=1)
y = df['Churn'].map({'Yes': 1, 'No': 0})

# 4. Identify Column Types for the Pipeline
# Numeric features (we will scale these)
numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
# Categorical features (we will OneHotEncode these)
categorical_features = [col for col in X.columns if col not in numeric_features]

print(f"Numeric features: {len(numeric_features)}")
print(f"Categorical features: {len(categorical_features)}")

# 5. Build the Preprocessing Pipeline (The "Professional" Way)
# Numeric Transformer: Impute missing values (median) -> Scale data (StandardScaler)
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Categorical Transformer: Impute missing (constant) -> OneHotEncode
# handle_unknown='ignore' ensures the model won't crash if it sees a new category in production
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine them into a single Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# 6. Create the Full Pipeline (Preprocessor + Model)
# We use class_weight='balanced' to handle the imbalanced churn classes
clf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, 
                                          class_weight='balanced', 
                                          random_state=42))
])

# 7. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 8. Train the Pipeline
print("Training the full pipeline...")
clf.fit(X_train, y_train)

# 9. Senior-Level Evaluation
print("\n--- Model Evaluation ---")
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)[:, 1]

print("Classification Report:\n", classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

# 10. Save the *Entire* Pipeline
# The API won't need separate encoders. It just loads this one file.
print("\nSaving pipeline...")
joblib.dump(clf, "models/churn_pipeline.pkl")
print("Done! Saved to 'models/churn_pipeline.pkl'")