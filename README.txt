SDCGIA - Detectarea textelor umane si AI, experiment v3
Tema 6: Qwen3.5-4B cu Unsloth si LoRA

Repository nou: https://github.com/Neculai13/SDCGIA-v3
Experimentul vechi https://github.com/Neculai13/SDCGIA ramane neschimbat.

CONTINUT
  notebook.ipynb - rulare noua in Colab, cu descarcarea automata a datelor
  date/SDCGIA_date_complete_v3.zip - toate textele si partitiile folosite
  generare/ - prompturi, modele, setari disponibile si script optional
  rezultate/ - predictii, metrici, configuratie si notebook executat
  raport.pdf - metoda, rezultatele si limitele experimentului
  prezentare/ - prezentare editabila si fisa de sustinere

CORPUS SI REZULTATE
  7.950 texte: 4.524 umane si 3.426 AI.
  Antrenare: 5.557 (3.166 umane, 2.391 AI).
  Calibrare: 1.194 (679 umane, 515 AI).
  Test: 1.199 (679 umane, 520 AI).
  Rezultat test: 1.199/1.199 corecte, 100%, 0 FP si 0 FN, prag fix 0,5.

Aceste rezultate apartin unui test intern exploratoriu. O singura publicatie,
generatoare deja cunoscute la antrenare si reutilizarea unor surse evaluate in
experimente anterioare limiteaza generalizarea. 100% nu certifica autoratul
oricarui text nou. Subseturile per model sunt mici si pot reutiliza aceleasi
controale umane; nu se insumeaza denominatorii acestor subseturi.

RULARE IN COLAB
  https://colab.research.google.com/github/Neculai13/SDCGIA-v3/blob/main/notebook.ipynb

  1. Selecteaza T4 GPU intr-o sesiune noua.
  2. Ruleaza prepare pana la sectiunea 5 inclusiv.
  3. Repornește sesiunea, seteaza RUN_MODE="pilot", ruleaza pana la 7 inclusiv.
  4. Dupa pilot reusit, reporneste. Seteaza RUN_MODE="train" si
     CONFIRM_FULL_TRAINING=True. Ruleaza pana la 7 pentru antrenare completa.
  5. Ruleaza sectiunea 8 pentru calibrare. In sectiunea 9 seteaza
     RUN_FINAL_TEST=True si ruleaza testul. Sectiunea 10 creeaza arhiva finala.

Datele se descarca singure din GitHub, cu verificarea SHA-256. Nu este necesara
generare locala. Autorizeaza propriul Drive pentru checkpointuri si rezultate.
RUN_NAME initial este nou, cu timestamp. Pastreaza exact acelasi nume intre faze.
Daca sesiunea este noua, foloseste RUN_MODE="calibrate" pentru modelul antrenat
sau "evaluate" pentru cel calibrat si indica RUN_NAME existent. Nu repeta train.
Pentru reluare: RESUME_CHECKPOINT indica un checkpoint complet din acea rulare.
Nu folosi checkpointuri sau modele din experimentul vechi.

Antrenarea, calibrarea si testul istoric v3 au rulat pe GPU. Adaptarea pentru
descarcare automata este verificata local, dar nu a fost reantrenata integral
intr-o sesiune GPU noua. Dependentele, modelul de baza cu revision nefixata si
hardware-ul pot schimba rezultatele. Bibliotecile principale sunt fixate la
versiunile din run_config.json. Afiseaza erorile si opreste-te daca mediul difera.

GENERARE OPTIONALA
  python generare/genereaza.py --model qwen3.5:0.8b --limit 1
Comanda verifica cererea fara a genera. Adauga --run numai pentru generare reala.
Ollama: implicit http://127.0.0.1:11434. Pentru llama.cpp indica --url cu serverul
local compatibil OpenAI. Rezultatele noi nu suprascriu corpusul istoric.
Pentru chatgpt_web, scriptul afiseaza prompturile pentru folosire manuala.
Nu exista parametri numerici de sampling verificati pentru generarea prin UI.
Numele modelelor web sunt etichetele inregistrate in interfata.

MODELUL ISTORIC
Modelul calibrat nu este inclus in Git: arhiva human_ai_final.zip are 332,28 MiB.
Codul si datele permit antrenarea unui model nou. Arhiva modelului poate fi
transmisa separat. Ea nu include greutatile modelului de baza descarcat din HF.

DREPTURI SI SURSE
Articolele isi pastreaza drepturile publicatiei originale. URL-urile si
provenienta sunt in arhiva datelor. Nu atribuim o licenta deschisa textelor
tertilor. Textele generate pot contine fictiune sau erori.
  https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth
  https://github.com/unslothai/notebooks
