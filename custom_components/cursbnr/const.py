# Constante pentru integrarea Curs valutar BNR
DOMAIN = "cursbnr"

# URL pentru API-ul BNR
URL = "https://www.finradar.ro/_next/data/1735234264446/index.json"

# Interval implicit de actualizare (în secunde)
DEFAULT_UPDATE_INTERVAL = 300  # 5 minute

# Limitele intervalului de actualizare (în secunde)
MIN_UPDATE_INTERVAL = 60   # 1 minut
MAX_UPDATE_INTERVAL = 3600  # 60 de minute