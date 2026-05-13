# Datoru Noslogojuma Sistēma (V.Plūdoņa Kuldīgas vidusskola)

Šī sistēma izstrādāta kā Programmēšana II eksāmena piekļuves darbs, lai automatizētu un digitalizētu Chromebook datoru uzskaiti, rezervāciju un tehniskā stāvokļa pārraudzību skolotājiem.

## Galvenās funkcijas
* **Droša autorizācija:** Lietotāju lomu sistēma (Administrators un Skolotāji) ar Werkzeug paroļu šifrēšanu (hashing).
* **Stingrā paroļu politika:** Reāllaika (JavaScript) un aizmugursistēmas (Python Regex) paroļu validācija (vismaz 8 simboli, lielais burts, mazais burts, cipars, īpašais simbols).
* **Viedā rezervācija:** Iespēja rezervēt tehniku noteiktam datumam un laikam (no/līdz).
* **Pārklāšanās kontrole (Dubultās rezervācijas bloķēšana):** Algoritms, kas neļauj diviem lietotājiem rezervēt vienu un to pašu datoru vienā un tajā pašā laikā.
* **Inventāra pārvaldība:** Katram datoram ir unikāls sērijas numurs (S/N).
* **Statusu vadība un remonti:** Skolotāji var ziņot par bojājumiem (dators tiek bloķēts rezervācijām), bet tikai Administrators var apstiprināt remonta pabeigšanu.
* **API integrācija:** Reāllaika laikapstākļu datu attēlošana informācijas panelī.

## Izmantotās tehnoloģijas
* **Backend:** Python 3.x, Flask ietvars.
* **Datu bāze:** SQLite (izmantojot Flask-SQLAlchemy OOP modeļus).
* **Frontend:** HTML5, Bootstrap 5 (CSS karkass responsīvam dizainam), JavaScript.
* **Testēšana:** Python iebūvētā `unittest` bibliotēka.

## Uzstādīšana un palaišana
1. Pārliecinieties, ka datorā ir uzstādīts Python.
2. Instalējiet nepieciešamās bibliotēkas izmantojot termināli:
   ```bash
   pip install -r requirements.txt
   
## 🔑 Sākotnējie piekļuves dati

Pirmoreiz palaižot programmu, datubāzē automātiski tiek izveidoti trīs lietotāju konti. Visas paroles ir nošifrētas un atbilst sistēmas drošības politikai (vismaz 8 rakstzīmes, lielais burts, mazais burts, cipars un īpašais simbols).

| Loma | Lietotājvārds | Parole | Galvenās tiesības |
| :--- | :--- | :--- | :--- |
| **Administrators** | `admin` | `Admin123!` | Lietotāju/datoru pievienošana, remontu apstiprināšana, visu rezervāciju vadība. |
| **Skolotājs 1** | `skolotajs1` | `Skolotajs1!` | Datoru rezervēšana, savu rezervāciju atcelšana, ziņošana par bojājumiem. |
| **Skolotājs 2** | `skolotajs2` | `Skolotajs2!` | Datoru rezervēšana, savu rezervāciju atcelšana, ziņošana par bojājumiem. |

> **Piezīme:** Drošības apsvērumu dēļ pēc pirmās pieteikšanās ieteicams izmantot administratora paneli, lai reģistrētu jaunus lietotājus ar unikāliem piekļuves datiem.
