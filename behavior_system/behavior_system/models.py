import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from .config import *


def baseline(name):
    if name == "logreg":
        return LogisticRegression(max_iter=2000, class_weight="balanced")
    return RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=SEED)


def _tf():
    import tensorflow as tf
    return tf


def build_lstm(n_feat=len(FEATS)):
    tf = _tf(); L = tf.keras.layers
    inp = L.Input((T, n_feat)); x = L.Masking(0.0)(inp)
    x = L.LSTM(16, name="behavior_lstm")(x); x = L.Dropout(0.3)(x)
    out = L.Dense(1, activation="sigmoid")(x)
    m = tf.keras.Model(inp, out); m.compile("adam", "binary_crossentropy", metrics=["accuracy"])
    return m


def build_transformer(n_feat=len(FEATS), d=16, heads=2):
    tf = _tf(); L = tf.keras.layers
    inp = L.Input((T, n_feat))
    pad = L.Lambda(lambda z: tf.reduce_any(tf.not_equal(z, 0.0), -1))(inp)   # (b,T) True=real
    x = L.Dense(d)(inp)
    pos = L.Embedding(T, d)(tf.range(T))
    x = x + pos[None]
    att_mask = L.Lambda(lambda m: m[:, None, :] & m[:, :, None])(pad)
    a = L.MultiHeadAttention(heads, d // heads)(x, x, attention_mask=att_mask)
    x = L.LayerNormalization()(x + a)
    f = L.Dense(32, activation="relu")(x); f = L.Dense(d)(f)
    x = L.LayerNormalization(name="behavior_tf")(x + f)
    m = L.Lambda(lambda z: tf.cast(z, tf.float32))(pad)
    x = L.Lambda(lambda z: tf.reduce_sum(z[0] * z[1][..., None], 1) /
                 (tf.reduce_sum(z[1], 1, keepdims=True) + 1e-8))([x, m])
    x = L.Dropout(0.3)(x)
    out = L.Dense(1, activation="sigmoid")(x)
    mod = tf.keras.Model(inp, out); mod.compile("adam", "binary_crossentropy", metrics=["accuracy"])
    return mod


def fit_keras(model, X, y, epochs=60, batch=8):
    neg, pos = (y == 0).sum(), (y == 1).sum()
    cw = {0: 1.0, 1: float(neg / max(pos, 1))}
    model.fit(X, y, epochs=epochs, batch_size=batch, class_weight=cw, verbose=0)
    return model
