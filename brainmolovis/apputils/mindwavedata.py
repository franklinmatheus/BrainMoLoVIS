
def get_raweeg(data: str) -> int:
    try: return int(data.split('rawEeg":')[1].split('}')[0])
    except Exception: return 0

def get_attention(data: str) -> int:
    try: return int(data.split('attention":')[1].split(',')[0])
    except Exception: return 0

def get_meditation(data: str) -> int:
    try: return int(data.split('meditation":')[1].split('}')[0])
    except Exception: return 0

def get_blink_strength(data: str) -> int:
    try: return int(data.split('blinkStrength":')[1].split('}')[0])
    except Exception: return 0

def get_delta(data: str) -> int:
    try: return int(data.split('delta":')[1].split(',')[0])
    except Exception: return 0

def get_theta(data: str) -> int:
    try: return int(data.split('theta":')[1].split(',')[0])
    except Exception: return 0

def get_low_alpha(data: str) -> int:
    try: return int(data.split('lowAlpha":')[1].split(',')[0])
    except Exception: return 0

def get_high_alpha(data: str) -> int:
    try: return int(data.split('highAlpha":')[1].split(',')[0])
    except Exception: return 0

def get_low_beta(data: str) -> int:
    try: return int(data.split('lowBeta":')[1].split(',')[0])
    except Exception: return 0

def get_high_beta(data: str) -> int:
    try: return int(data.split('highBeta":')[1].split(',')[0])
    except Exception: return 0

def get_low_gamma(data: str) -> int:
    try: return int(data.split('lowGamma":')[1].split(',')[0])
    except Exception: return 0

def get_high_gamma(data: str) -> int:
    try: return int(data.split('highGamma":')[1].split('}')[0])
    except Exception: return 0

def get_signal_level(data: str) -> int:
    try: return int(data.split('poorSignalLevel":')[1].split('}')[0].split(',')[0])
    except Exception: return 0