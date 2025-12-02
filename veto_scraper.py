import json
import datetime
import random

class LegislativeSystemSimulator:
    def __init__(self):
        self.president = "Karol Nawrocki"
        self.current_date = datetime.datetime.now()
        
    def fetch_simulated_data(self):
        print(f"[{self.current_date}] Pobieranie szczegółowych uzasadnień...")
        
        # BOGATA BAZA DANYCH (Symulacja 2025)
        # Tu definiujemy konkretne powody weta
        laws_database = [
            {
                "title": "Ustawa o likwidacji Centralnego Portu Komunikacyjnego",
                "date": "2025-11-28",
                "status": "veto",
                "desc": "Prezydent wskazał na strategiczne znaczenie inwestycji dla bezpieczeństwa militarnego i gospodarczego Polski. Ustawa hamowała rozwój infrastruktury krytycznej."
            },
            {
                "title": "Nowelizacja ustawy o Sądzie Najwyższym",
                "date": "2025-11-15",
                "status": "veto",
                "desc": "Wątpliwości konstytucyjne dotyczące procedury weryfikacji sędziów. Prezydent uznał, że ustawa narusza prerogatywy głowy państwa."
            },
            {
                "title": "Ustawa o zmianie programów nauczania (Edukacja Nowoczesna)",
                "date": "2025-10-30",
                "status": "veto",
                "desc": "Zastrzeżenia dotyczyły ograniczenia roli lekcji historii oraz braku konsultacji z rodzicami w sprawach światopoglądowych."
            },
            {
                "title": "Ustawa o podatku od pustostanów",
                "date": "2025-10-12",
                "status": "veto_rejected", # Weto odrzucone
                "desc": "Mimo sprzeciwu Prezydenta (argument o naruszeniu prawa własności), Sejm odrzucił weto większością 3/5 głosów."
            },
            {
                "title": "Nowelizacja ustawy o radiofonii i telewizji",
                "date": "2025-09-05",
                "status": "veto",
                "desc": "Prezydent wskazał na zagrożenie dla pluralizmu mediów i ryzyko przejęcia rynku przez podmioty zagraniczne spoza EOG."
            },
            {
                "title": "Ustawa o bezpieczeństwie energetycznym (ETS2)",
                "date": "2025-08-20",
                "status": "veto",
                "desc": "Zbyt wysokie koszty transformacji przerzucone na gospodarstwa domowe. Brak mechanizmów osłonowych dla najuboższych."
            }
        ]
        
        # Generujemy resztę do 19, ale też z opisami
        generic_reasons = [
            "Naruszenie zasady poprawnej legislacji (zbyt krótki termin vacatio legis).",
            "Brak wymaganych konsultacji ze związkami zawodowymi.",
            "Niezgodność z art. 2 Konstytucji RP (zasada zaufania do państwa).",
            "Błędy formalne uniemożliwiające podpisanine ustawy."
        ]
        
        titles = [
            "Ustawa o planowaniu przestrzennym", "Nowelizacja Kodeksu Pracy", 
            "Ustawa o e-Doręczeniach", "Ustawa o Służbie Cywilnej", 
            "Prawo o ruchu drogowym", "Ustawa o lasach państwowych",
            "Nowelizacja ustawy o prokuraturze", "Ustawa o szkolnictwie wyższym",
            "Prawo wodne", "Ustawa o finansach publicznych", 
            "Kodeks Spółek Handlowych", "Ustawa o ochronie zwierząt", "Prawo budowlane"
        ]

        for i in range(13): # Dodajemy resztę, żeby było 19
            laws_database.append({
                "title": titles[i],
                "date": f"2025-0{random.randint(1,9)}-{random.randint(10,28)}", 
                "status": "veto",
                "desc": random.choice(generic_reasons)
            })
            
        # Dodajemy kilka podpisanych dla tła
        laws_database.append({"title": "Ustawa budżetowa 2026", "date": "2025-12-01", "status": "signed", "desc": ""})

        return laws_database

    def process_data(self, raw_data):
        stats = {"signed": 42, "vetoed": 0, "tribunal": 3}
        display_list = []
        
        for law in raw_data:
            if law['status'] == 'veto':
                stats['vetoed'] += 1
                display_list.append({
                    "title": law['title'],
                    "date": law['date'],
                    "status": "Weto Prezydenckie",
                    "description": law['desc'] # Tu przekazujemy opis
                })
            elif law['status'] == 'veto_rejected':
                stats['vetoed'] += 1
                display_list.append({
                    "title": law['title'],
                    "date": law['date'],
                    "status": "Weto odrzucone przez Sejm",
                    "description": law['desc']
                })
        
        # Sortowanie od najnowszych
        display_list.sort(key=lambda x: x['date'], reverse=True)
        return stats, display_list # Zwracamy całą listę, nie tylko 5

    def save_to_json(self, stats, veto_list):
        output = {
            "last_updated": self.current_date.strftime("%Y-%m-%d %H:%M:%S"),
            "stats": stats,
            "veto_list": veto_list
        }
        
        with open('veto_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
        print(f"Zaktualizowano dane. Liczba wet: {stats['vetoed']}")

if __name__ == "__main__":
    system = LegislativeSystemSimulator()
    raw_data = system.fetch_simulated_data()
    stats, display_list = system.process_data(raw_data)
    system.save_to_json(stats, display_list)
