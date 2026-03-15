from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from sklearn.linear_model import SGDClassifier


@dataclass
class ActivityClassifier:
    labels: list[str] = field(default_factory=lambda: ["idle", "motion", "gesture"])

    def __post_init__(self) -> None:
        self.model = SGDClassifier(loss="log_loss", random_state=42)
        self._initialized = False

    def partial_fit(self, features: dict[str, float], label: str) -> None:
        x = np.array([list(features.values())])
        y = np.array([label])
        if not self._initialized:
            self.model.partial_fit(x, y, classes=np.array(self.labels))
            self._initialized = True
        else:
            self.model.partial_fit(x, y)

    def predict(self, features: dict[str, float]) -> str:
        if not self._initialized:
            return "unknown"
        x = np.array([list(features.values())])
        return str(self.model.predict(x)[0])
