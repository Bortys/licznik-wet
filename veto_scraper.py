import json
import datetime
import random

# Tego używamy, gdy chcemy symulować dane dla przyszłości (2025),
# ponieważ prawdziwa strona Sejmu nie zawiera jeszcze tych informacji.

class LegislativeSystemSimulator:
    def __init__(self):
        # Konfiguracja scenariusza "Grudzień 2025"
        self.president = "Karol Nawrocki"
        self.current_date = datetime.datetime.now()
        
    def fetch_simulated_data(self):
        """
        Symuluje pobieranie danych z bazy sejmowej dla zadanego scenariusza.
        W prawdziwym wdrożeniu tu byłoby: requests.get('sejm.gov.pl')
        """
        print(f"[{self.current_date}] Łączenie z systemem legislacyjnym...")
        
        # Baza ustaw scenariusza
        laws_database = [
            {"title": "Nowelizacja ustawy o Sądzie Najwyższym", "date": "2025-11-28", "status": "veto"},
            {"title": "Ustawa o zmianie ustawy Prawo oświatowe", "date": "2025-11-15", "status": "veto"},
            {"title": "Ustawa o podatku od reklam", "date": "2025-10-30", "status": "veto_rejected"}, # Weto odrzucone
            {"title": "Ustawa budżetowa na rok 2026", "date": "2025-12-01", "status": "signed"},
            {"title": "Ustawa o bezpieczeństwie energetycznym", "date": "2025-10-12", "status": "veto"},
            {"title": "Nowelizacja Kodeksu Wyborczego", "date": "2025-09-05", "status": "veto"},
             # ... symulujemy, że reszta to starsze ustawy
        ]
        
        # Generowanie pozostałych 14 wet (anonimowych) dla uzyskania liczby 19
        for i in range(14):
            laws_database.append({
                "title": f"Ustawa nowelizująca nr {300+i}",
                "date": "2025-08-20", 
                "status": "veto"
            })

        return laws_database

    def process_data(self, raw_data):
        """Przetwarza dane i oblicza statystyki (Logika Biznesowa)"""
        stats = {
            "signed": 42,   # Stała liczba podpisanych w scenariuszu
            "vetoed": 0,    # To policzymy dynamicznie
            "tribunal": 3
        }
        
        display_list = []
        
        for law in raw_data:
            # Logika zliczania
            if law['status'] == 'veto':
                stats['vetoed'] += 1
                # Dodajemy do listy wyświetlanej tylko weta aktywne
                display_list.append({
                    "title": law['title'],
                    "date": law['date'],
                    "status": "Weto Prezydenckie"
                })
            elif law['status'] == 'veto_rejected':
                stats['vetoed'] += 1
                display_list.append({
                    "title": law['title'],
                    "date": law['date'],
                    "status": "Weto odrzucone przez Sejm"
                })
        
        # Sortowanie od najnowszych
        display_list.sort(key=lambda x: x['date'], reverse=True)

        return stats, display_list[:5] # Zwracamy 5 najnowszych

    def save_to_json(self, stats, veto_list):
        output = {
            "last_updated": self.current_date.strftime("%Y-%m-%d %H:%M:%S"),
            "stats": stats,
            "veto_list": veto_list
        }
        
        with open('veto_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
        print("Dane zaktualizowane pomyślnie.")

# Uruchomienie procesu
if __name__ == "__main__":
    system = LegislativeSystemSimulator()
    raw_data = system.fetch_simulated_data()
    stats, display_list = system.process_data(raw_data)
    system.save_to_json(stats, display_list)
