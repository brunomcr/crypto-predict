import pandas as pd
import xgboost as xgb
import os
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score

# Diretório da camada GOLD
GOLD_DIR = "data/gold"
GOLD_FILENAME = "bitcoin_ohlc_gold.parquet"
GOLD_PATH = os.path.join(GOLD_DIR, GOLD_FILENAME)

# Carrega os dados
df = pd.read_parquet(GOLD_PATH)

# Define features e target
FEATURES = [
    'log_return',
    'candle_wick_size',
    'close_diff',
    'bb_width',
    'rsi_14'
]

TARGET = 'target'

df = df.dropna(subset=FEATURES)

# Prepara X e y
X = df[FEATURES]
y = df[TARGET]

# Split temporal (sem shuffle)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

print("Distribuição classes treino:")
print(y_train.value_counts(normalize=True))

print("\nDistribuição classes teste:")
print(y_test.value_counts(normalize=True))

# Cria DMatrix (estrutura de dados otimizada do XGBoost)
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Parâmetros do XGBoost
params = {
    'objective': 'binary:logistic',
    'eval_metric': 'logloss',
    'eta': 0.0003,           # Learning rate baixo
    'max_depth': 5,        # Controle de overfitting
    'subsample': 0.68,      # Bagging
    'colsample_bytree': 0.89,
    'seed': 42,
    'verbosity': 1
}

# Treinamento
evals = [(dtrain, 'train'), (dtest, 'valid')]
model = xgb.train(
    params,
    dtrain,
    num_boost_round=5000,
    early_stopping_rounds=200,
    evals=evals,
    verbose_eval=100
)

# Previsões
y_pred_proba = model.predict(dtest, iteration_range=(0, model.best_iteration))
y_pred = (y_pred_proba >= 0.5).astype(int)

# Avaliação
print("\n✅ Avaliação Final:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nROC AUC Score:", roc_auc_score(y_test, y_pred_proba))

# Garante que o diretório 'models' exista
os.makedirs("models", exist_ok=True)

# Salva o modelo
# model.save_model("models/xgboost_classifier.json")

# Salva o modelo otimizado como JSON
best_model_path = "models/xgboost_classifier_v3.json"
model.dump_model(best_model_path, dump_format='json')
print(f"\n✅ Modelo salvo em {best_model_path}")


print("\n✅ Modelo salvo em models/xgboost_classifier.json")
