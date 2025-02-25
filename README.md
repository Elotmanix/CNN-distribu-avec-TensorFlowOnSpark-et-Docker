
# Entraînement Distribué d'un CNN avec Spark, Horovod et Docker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![TensorFlow 2.12](https://img.shields.io/badge/TensorFlow-2.12-FF6F00.svg)](https://www.tensorflow.org/)

Ce projet démontre l'entraînement distribué d'un réseau de neurones convolutif (CNN) sur le dataset MNIST en utilisant :
- **Apache Spark** pour la gestion du cluster
- **Horovod** pour la synchronisation des gradients
- **Docker** pour le déploiement conteneurisé

## 📋 Table des Matières
- [Fonctionnalités](#-fonctionnalités)
- [Technologies Utilisées](#-technologies-utilisées)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Résultats](#-résultats)
- [Structure des Fichiers](#-structure-des-fichiers)
- [Défis Techniques](#-défis-techniques)
- [Contributions](#-contributions)
- [Licence](#-licence)

## 🚀 Fonctionnalités
- Entraînement distribué sur 2 workers
- Synchronisation des gradients avec Horovod
- Visualisation des métriques d'apprentissage
- Déploiement automatisé avec Docker
- Monitoring via l'interface web de Spark

## 🛠 Technologies Utilisées
![Technologies](https://i.imgur.com/4JKkHd7.png)

## 📦 Prérequis
- Docker 20.10+
- Docker Compose 2.12+
- Python 3.9
- 4GB de RAM disponible

## 🔧 Installation
1. Cloner le dépôt :
```bash
git clone https://github.com/Elotmanix/CNN-distribu-avec-TensorFlowOnSpark-et-Docker
cd distributed-cnn-mnist
```

2. Construire l'image Docker :
```bash
docker build -t spark-horovod:latest .
```

3. Démarrer le cluster :
```bash
docker-compose up -d --scale spark-worker=2
```

## 🖥 Utilisation
1. Copier le script d'entraînement :
```bash
docker cp training-cnn.py spark-master:/opt/spark/work-dir/
```

2. Lancer l'entraînement :
```bash
docker exec -it spark-master \
  spark-submit \
  --master spark://spark-master:7077 \
  --num-executors 2 \
  --conf spark.executorEnv.HOROVOD_CONTROLLER=gloo \
  /opt/spark/work-dir/training-cnn.py
```

3. Surveiller les logs :
```bash
docker logs -f spark-master
```

4. Accéder aux résultats :
```bash
docker cp spark-master:/tmp/training_metrics.png .
```

## 📊 Résultats
![Courbes d'Apprentissage](https://i.imgur.com/X2zQ4fS.png)

**Performances Finales :**
- Précision sur le test set : **97.78%**
- Loss finale : **0.0842**
- Temps moyen par époque : **38s**

## 📂 Structure des Fichiers
```
.
├── docker-compose.yml        # Configuration du cluster
├── Dockerfile               # Définition de l'image Docker
├── training-cnn.py          # Script d'entraînement
├── docs/                    # Documentation supplémentaire
└── images/                  # Captures d'écran et visualisations
```

## 🧩 Défis Techniques
- **Configuration d'Horovod** : Intégration avec TensorFlow et Spark
- **Optimisation mémoire** : Gestion des allocations dans les conteneurs
- **Synchronisation** : Ajustement du learning rate distribué
- **Déploiement** : Montage des volumes Docker

## 🤝 Contributions
Les contributions sont les bienvenues ! Veuillez suivre ces étapes :
1. Forker le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Committer vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pousser vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

