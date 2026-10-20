"""Pure-NumPy masked LSTM binary classifier (no TensorFlow needed). Hidden=16 like the Keras version."""
import numpy as np


def _sig(x): return 1 / (1 + np.exp(-np.clip(x, -30, 30)))


class NumpyLSTM:
    def __init__(self, n_in, hidden=16, seed=42, l2=1e-3):
        r = np.random.RandomState(seed); H = hidden
        s = 1 / np.sqrt(H + n_in)
        self.H, self.F, self.l2 = H, n_in, l2
        self.P = {"W": r.randn(n_in + H, 4 * H) * s, "b": np.zeros(4 * H),
                  "wo": r.randn(H) * 0.1, "bo": np.zeros(1)}
        self.P["b"][H:2 * H] = 1.0  # forget-gate bias

    def _forward(self, X, M, cache=False):
        B, T, _ = X.shape; H = self.H; W, b = self.P["W"], self.P["b"]
        h = np.zeros((B, H)); c = np.zeros((B, H)); st = []
        for t in range(T):
            z = np.concatenate([X[:, t], h], 1)
            a = z @ W + b
            i, f, g, o = _sig(a[:, :H]), _sig(a[:, H:2 * H]), np.tanh(a[:, 2 * H:3 * H]), _sig(a[:, 3 * H:])
            cn = f * c + i * g; hn = o * np.tanh(cn)
            m = M[:, t:t + 1].astype(float)
            if cache: st.append((z, i, f, g, o, c, cn, h, m))
            c = m * cn + (1 - m) * c; h = m * hn + (1 - m) * h
        p = _sig(h @ self.P["wo"] + self.P["bo"])
        return p, h, st

    def predict_proba(self, X, M): return self._forward(X, M)[0]
    def embed(self, X, M): return self._forward(X, M)[1]

    def _loss_grads(self, X, M, y, sw):
        B = len(y); H = self.H
        p, h, st = self._forward(X, M, cache=True)
        eps = 1e-9
        loss = -np.sum(sw * (y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps))) / B
        dz_out = sw * (p - y) / B
        g = {k: np.zeros_like(v) for k, v in self.P.items()}
        g["wo"] = h.T @ dz_out; g["bo"] = np.array([dz_out.sum()])
        dh = np.outer(dz_out, self.P["wo"]); dc = np.zeros((B, H))
        for t in reversed(range(len(st))):
            z, i, f, g_, o, cp, cn, hp, m = st[t]
            tc = np.tanh(cn)
            dhn = dh * m; dh_keep = dh * (1 - m)
            dcn = dc * m + dhn * o * (1 - tc ** 2); dc_keep = dc * (1 - m)
            da = np.concatenate([dcn * g_ * i * (1 - i), dcn * cp * f * (1 - f),
                                 dcn * i * (1 - g_ ** 2), dhn * tc * o * (1 - o)], 1)
            g["W"] += z.T @ da; g["b"] += da.sum(0)
            dz = da @ self.P["W"].T
            dh = dz[:, self.F:] + dh_keep; dc = dcn * f + dc_keep
        g["W"] += self.l2 * self.P["W"]
        return loss, g

    def fit(self, X, M, y, epochs=150, batch=8, lr=0.01, class_weight=True, seed=42):
        y = y.astype(float); r = np.random.RandomState(seed)
        pos = max(y.sum(), 1); w1 = (len(y) - y.sum()) / pos if class_weight else 1.0
        sw_all = np.where(y == 1, w1, 1.0)
        m_ = {k: np.zeros_like(v) for k, v in self.P.items()}; v_ = {k: np.zeros_like(v) for k, v in self.P.items()}
        step = 0
        for _ in range(epochs):
            idx = r.permutation(len(y))
            for s in range(0, len(y), batch):
                bi = idx[s:s + batch]
                _, g = self._loss_grads(X[bi], M[bi], y[bi], sw_all[bi]); step += 1
                for k in self.P:
                    m_[k] = 0.9 * m_[k] + 0.1 * g[k]; v_[k] = 0.999 * v_[k] + 0.001 * g[k] ** 2
                    self.P[k] -= lr * (m_[k] / (1 - 0.9 ** step)) / (np.sqrt(v_[k] / (1 - 0.999 ** step)) + 1e-8)
        return self

    def state(self): return {k: v.copy() for k, v in self.P.items()} | {"H": self.H, "F": self.F}
    @classmethod
    def from_state(cls, s):
        m = cls(int(s["F"]), int(s["H"])); m.P = {k: np.array(s[k]) for k in ("W", "b", "wo", "bo")}; return m
