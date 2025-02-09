# Analyse des Prénoms en France (2003-2004)

## 📊 Description du Projet
Ce script Python analyse les données de prénoms en France pour les années 2003 et 2004, offrant une exploration détaillée de la distribution des prénoms.

## ✨ Fonctionnalités Principales
- 📂 Chargement et fusion des fichiers de prénoms de 2003 et 2004
- 🔍 Identification des 10 prénoms les plus fréquents par année
- 👧👦 Analyse des prénoms les plus fréquents par genre
- 💾 Exportation des données traitées dans des fichiers CSV

## 🛠 Prérequis Techniques
- Python 3.7 ou supérieur
- Bibliothèques requises :
  - pandas
  - logging


## 🖥 Utilisation
1. Dézipper le projet
2. Lancer le script `main.py`
3. Lire le journal des opérations (`prenoms_processing.log`)
4. Lire les fichiers générés (`Prenoms2003-2004.csv`, `Prenoms2003-2004_Jointure.csv`)
5. Lire les top 10 prénoms pour chaque année (`Top 10 prénoms en 2003 :`, `Top 10 prénoms en 2004 :`)

## 📋 Fichiers Générés
- `Prenoms2003-2004.csv` : Données fusionnées des deux années
- `Prenoms2003-2004_Jointure.csv` : Données agrégées par prénom
- `prenoms_processing.log` : Journal détaillé des opérations

## 🔍 Détails Techniques : Module Logging

### Qu'est-ce que le Logging ?
Le logging est un mécanisme de suivi des événements qui se produisent pendant l'exécution d'un programme logiciel.

### Niveaux de Logs
1. `DEBUG` : Informations détaillées pour le débogage
2. `INFO` : Confirmation du bon fonctionnement
3. `WARNING` : Avertissements sur des problèmes potentiels
4. `ERROR` : Erreurs qui bloquent une fonction
5. `CRITICAL` : Erreurs très graves pouvant arrêter le programme

### Configuration dans notre Projet
```python
logging.basicConfig(
    level=logging.INFO,  # Niveau minimum de logs
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('prenoms_processing.log'),  # Log dans un fichier
        logging.StreamHandler(sys.stdout)  # Log dans la console
    ]
)
```

### Exemples de Logs
```python
# Log informatif
logging.info("Chargement du fichier de prénoms")

# Log d'avertissement
logging.warning("Données incomplètes détectées")

# Log d'erreur
logging.error("Impossible de charger le fichier CSV")
```

## 🛡 Gestion des Erreurs
- Vérification de l'existence des fichiers
- Validation des colonnes requises
- Gestion robuste des erreurs de lecture CSV
- Journalisation détaillée des problèmes

## 📄 Licence
[À compléter - par exemple MIT, Apache, etc.]

## 👤 Auteur
SYAN HILAIRE--BENAMOR (https://github.com/SyanCode)

---

**Note :** Ce projet est un exemple d'analyse de données démographiques utilisant Python et pandas.