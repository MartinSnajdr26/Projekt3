# 🗳️ Volební Scraper 2017

Tento projekt je webový scraper, který získává výsledky voleb v Česku z roku 2017. Skript načítá data přímo z webu [volby.cz](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4207) a ukládá je do souboru ve formátu CSV.

## 📌 Požadavky

Pro správné fungování skriptu je nutné mít nainstalované následující knihovny:

```bash
📦 Knihovny použité v projektu:

requests - pro HTTP požadavky
pandas - pro zpracování dat a export do CSV
beautifulsoup4 - pro parsing HTML stránky

🚀 Použití
Skript se spouští s dvěma argumenty:

🏙️ Odkaz na regionální stránku výsledků voleb
📄 Název výstupního souboru CSV
▶️ Příklad spuštění

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4207" vysledky.csv
⚠️ Pokud nejsou zadány oba argumenty nebo je zadán nesprávný odkaz, skript zobrazí chybovou zprávu a ukončí se.

📊 Výstupní formát CSV
Výstupní CSV soubor obsahuje následující sloupce:

Sloupec	Popis
code	Kód obce
location	Název obce
registered	Počet registrovaných voličů
envelopes	Počet vydaných obálek
valid	Počet platných hlasů
party_1, party_2, ...	Počet hlasů pro jednotlivé kandidující strany

⚙️ Funkcionalita skriptu:
📥 Stažení HTML stránky z volby.cz.
🔍 Vyhledání odkazů na jednotlivé obce a jejich výsledky.
📊 Extrahování dat o počtu voličů, vydaných obálek, platných hlasů a hlasů pro jednotlivé strany.
💾 Uložení dat do CSV v jednotném formátu.

⚠️ Omezení
Skript funguje pouze s výsledky voleb 2017.
Web volby.cz musí být dostupný pro úspěšné stažení dat.
URL musí být ve správném formátu začínajícím https://www.volby.cz/pls/ps2017nss/ps32.

✍️ Autor
Tento projekt vytvořil Martin Snajdr jako cvičení pro práci se scrapingem v Pythonu.pip install -r requirements.txt
