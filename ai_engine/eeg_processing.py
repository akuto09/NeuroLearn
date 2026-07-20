"""
eeg_processing.py — simulated EEG signal source.

In a production deployment this module would read raw band-power data
(alpha/beta/theta) from a connected EEG headset (e.g. NeuroSky, Muse,
Emotiv) over Bluetooth/serial and convert it into normalized 0-100 scores.
For this prototype, it produces smooth, session-persistent pseudo-live
values so the rest of the AI engine and UI can be demonstrated end to end.
"""
import random
import time

# per-session in-memory state, keyed by a session token (e.g. user id)
_STATE = {}


def _seed_for(key):
    if key not in _STATE:
        _STATE[key] = {
            "attention": random.randint(45, 70),
            "meditation": random.randint(35, 60),
            "cognitive_load": random.randint(25, 50),
            "fatigue": random.randint(10, 30),
            "t": time.time(),
        }
    return _STATE[key]


def _drift(value, spread=6, lo=4, hi=97):
    value += random.uniform(-spread, spread)
    return max(lo, min(hi, round(value)))


def read_mental_state(key="global"):
    """Return a fresh simulated reading of the four core EEG-derived signals."""
    s = _seed_for(key)
    s["attention"] = _drift(s["attention"], 7)
    s["meditation"] = _drift(s["meditation"], 5)
    s["cognitive_load"] = _drift(s["cognitive_load"], 6)
    # fatigue trends slowly upward across a session, with small fluctuation
    s["fatigue"] = _drift(s["fatigue"] + 0.4, 3)
    return {
        "attention": int(s["attention"]),
        "meditation": int(s["meditation"]),
        "cognitive_load": int(s["cognitive_load"]),
        "fatigue": int(s["fatigue"]),
    }


def reset(key="global"):
    _STATE.pop(key, None)
