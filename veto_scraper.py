import json
import random
import os
from datetime import datetime

# To jest symulacja - w prawdziwej wersji tu będzie kod czytający Sejm.gov.pl
# Na razie generujemy dane testowe, żebyś widział, że system działa.

def main():
    # Udajemy, że pobieramy dane
    stats = {
        "signed": 14,
        "vetoed": 2,      # Tu docelowo wpadnie liczba ze strony Sejmu
        "tribunal": 1
    }
    
    # Tworzymy strukturę danych dla strony
    data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stats": stats,
        "veto_list": [
            {
                "title": "Przykładowa ustawa o mediach",
                "date": "2025-10-15",
                "status": "Weto odrzucone przez Sejm"
            }
        ]
    }

    # Zapisujemy do pliku, który odczyta strona WWW
    with open('veto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Dane zaktualizowane!")

if __name__ == "__main__":
    main()
