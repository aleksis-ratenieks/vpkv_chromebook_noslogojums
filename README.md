# vpkv_chromebook_noslogojums
Programmēšana II eksāmena piekļuves darba projekts
# Datoru Noslogojuma Sistēma (V.Plūdoņa Kuldīgas vidusskola)

Šī sistēma izstrādāta kā Programmēšana II piekļuves darbs, lai automatizētu Chromebook datoru uzskaiti skolotājiem.

## Funkcijas
- **Autorizācija:** Droša pieteikšanās (Admin un Lietotāji).
- **Rezervācija:** Lietotāji var rezervēt datoru konkrētam datumam un laikam.
- **Statusu pārvaldība:** Iespēja ziņot par bojājumiem.
- **Admin Panelis:** Jaunu lietotāju reģistrācija un iekārtu remontu apstiprināšana.
- **API integrācija:** Reāllaika laikapstākļu dati Kuldīgā.

## Izmantotās tehnoloģijas
- Python 3.x (Flask)
- SQLite datubāze
- Bootstrap 5 (UI/UX dizainam)

## Uzstādīšana
1. Instalējiet bibliotēkas: `pip install flask flask-sqlalchemy flask-login requests`
2. Palaidiet programmu: `python app.py`
3. Atveriet pārlūkā: `http://127.0.0.1:5000`

## Izstrādes principi (Vadlīnijas)
Projektā ievēroti:
- **KISS & DRY** principi vienkāršam un efektīvam kodam.
- **OOP** struktūra datu modeļiem.
- **Agile** izstrādes cikls.
