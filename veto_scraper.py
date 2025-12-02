import requests
from bs4 import BeautifulSoup
import json
import datetime
import re

# Konfiguracja
# Link do procesów legislacyjnych X kadencji (ustawy uchwalone i przekazane Prezydentowi)
# Uwaga: Linki sejmowe zmieniają się co kadencję (Sejm9 -> Sejm10)
URL_SEJM = "https://www.sejm.gov.pl/Sejm10.nsf/proces.xsp?view=2"

def get_sejm_data():
    try:
        # 1. Pobieramy stronę Sejmu
        headers = {'User-Agent': 'Mozilla/5.0 (CivicTech Monitor)'}
        response = requests.get(URL_SEJM, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Przygotowujemy liczniki
        stats = {
            "signed": 0,
            "vetoed": 0,    # Weto
            "tribunal": 0   # Wniosek do TK
        }
        veto_details = []

        # 3. Analiza tabeli ustaw (To jest moment 'inteligencji' skryptu)
        # Szukamy wierszy tabeli na stronie Sejmu
        rows = soup.find_all('tr') 
        
        for row in rows:
            text = row.get_text().lower()
            
            # Sprawdzamy statusy w tekście wiersza
            if "podpis" in text and "prezydent" in text:
                stats["signed"] += 1
                
            if "odmowa podpisania" in text or "przekazał ustawę sejmowi do ponownego" in text:
                stats["vetoed"] += 1
                
                # Próbujemy wyciągnąć tytuł ustawy
                try:
                    title_tag = row.find('a')
                    title = title_tag.get_text(strip=True) if title_tag else "Ustawa (brak tytułu)"
                except:
                    title = "Ustawa bez nazwy"
                
                veto_details.append({
                    "title": title,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"), # Data wykrycia
                    "status": "Weto Prezydenta"
                })

            if "trybunał" in text and "wniosek" in text:
                stats["tribunal"] += 1

        return stats, veto_details

    except Exception as e:
        print(f"Błąd pobierania danych z Sejmu: {e}")
        # W razie błędu zwracamy zera, żeby nie wysypać strony
        return {"signed": 0, "vetoed": 0, "tribunal": 0}, []

def main():
    print("Rozpoczynam skanowanie strony Sejmu...")
    stats, veto_list = get_sejm_data()
    
    # Budujemy strukturę JSON
    data = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stats": stats,
        "veto_list": veto_list
    }

    # Zapis do pliku
    with open('veto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"Zakończono. Znaleziono wet: {stats['vetoed']}")

if __name__ == "__main__":
    main()
