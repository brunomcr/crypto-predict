import pandas as pd
import lightgbm as lgb
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score

# Diretório da camada GOLD
GOLD_DIR = "data/gold"
GOLD_FILENAME = "bitcoin_ohlc_gold.parquet"
GOLD_PATH = os.path.join(GOLD_DIR, GOLD_FILENAME)

# Carrega os dados
df = pd.read_parquet(GOLD_PATH)

# Define features selecionadas
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

# Cria datasets para o LightGBM
train_data = lgb.Dataset(X_train, label=y_train)
valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

# Parâmetros otimizados LightGBM
params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'boosting_type': 'gbdt',
    'learning_rate': 0.001,          # Mais suave para convergência melhor
    'num_leaves': 31,               # Mais flexibilidade para o modelo
    'min_data_in_leaf': 20,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'max_depth': 5,                 # Limita profundidade, controla overfitting
    'seed': 42,
    'verbose': -1
}

# Treinamento
model = lgb.train(
    params,
    train_data,
    valid_sets=[train_data, valid_data],
    valid_names=['train', 'valid'],
    num_boost_round=5000,
    callbacks=[
        lgb.early_stopping(stopping_rounds=200),
        lgb.log_evaluation(period=100)
    ]
)


# Previsões
y_pred_proba = model.predict(X_test, num_iteration=model.best_iteration)
y_pred = (y_pred_proba >= 0.5).astype(int)

# Avaliação
print("\n✅ Avaliação Final:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nROC AUC Score:", roc_auc_score(y_test, y_pred_proba))

# Garante que o diretório 'models' exista
os.makedirs("models", exist_ok=True)

# Salva o modelo otimizado
best_model_path = "models/lightgbm_classifier_v3.txt"
model.save_model(best_model_path)
print(f"\n✅ Melhor modelo salvo em {best_model_path}")
