# 📚 Système de Gestion de Bibliothèque Amélioré

Application Flask complète pour gérer une bibliothèque numérique avec support PDF et images de couverture.

## ✨ Fonctionnalités

### 📖 Gestion des Livres
- **Ajout de livres** avec upload PDF et image de couverture
- **Visualisation des PDFs** directement dans le navigateur ou en nouvel onglet
- **Recherche et filtrage** par titre, auteur, ou catégorie
- **Modification et suppression** des livres
- **Page détaillée** pour chaque livre avec aperçu PDF intégré

### 👤 Gestion des Auteurs
- Ajout d'auteurs avec biographie
- Compteur automatique de livres par auteur
- Protection contre la suppression (si des livres sont associés)

### 🏷️ Gestion des Catégories
- Création de catégories avec description
- Compteur de livres par catégorie
- Filtrage des livres par catégorie

### 🎨 Interface Moderne
- Design responsive avec Bootstrap 5
- Animations et effets visuels
- Interface intuitive avec icônes Font Awesome
- Messages flash pour les actions utilisateur
- Thème dégradé violet élégant

## 🚀 Installation

### 1. Prérequis
```bash
# Python 3.8 ou supérieur
# MySQL 5.7 ou supérieur
# pip (gestionnaire de packages Python)
```

### 2. Cloner/Créer le projet
```bash
mkdir bibliotheque_flask
cd bibliotheque_flask
```

### 3. Créer la structure
```
bibliotheque_flask/
│── app.py
│── requirements.txt
│── static/
│   └── uploads/
│       ├── books/         # PDFs des livres
│       └── covers/        # Images de couverture
│           └── default-cover.jpg
│── templates/
│   ├── layout.html
│   ├── index.html
│   ├── books.html
│   ├── book_detail.html
│   ├── edit_book.html
│   ├── authors.html
│   └── categories.html
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 5. Créer la base de données MySQL
Exécutez le script SQL fourni dans phpMyAdmin ou MySQL Workbench :

```sql
CREATE DATABASE librarydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE librarydb;

-- Puis exécutez le reste du script SQL fourni
```

### 6. Créer l'image de couverture par défaut
Créez un dossier et placez une image par défaut :
```bash
mkdir -p static/uploads/covers
mkdir -p static/uploads/books
```

Téléchargez ou créez une image `default-cover.jpg` et placez-la dans `static/uploads/covers/`

### 7. Configurer la connexion MySQL
Dans `app.py`, modifiez si nécessaire :
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Votre mot de passe
app.config['MYSQL_DB'] = 'librarydb'
```

### 8. Lancer l'application
```bash
python app.py
```

Accédez à : **http://127.0.0.1:5000**

## 📖 Utilisation

### Ajouter un livre avec PDF

1. Allez dans **Livres**
2. Cliquez sur **"Ajouter un livre"**
3. Remplissez le formulaire :
   - Titre (requis)
   - Auteur (requis)
   - Catégorie (requis)
   - Année
   - Description
   - **Fichier PDF** (max 16MB)
   - **Image de couverture** (JPG, PNG, GIF)
4. Cliquez sur **Enregistrer**

### Lire un PDF

**3 façons de lire un PDF :**

1. **Cliquer sur l'image de couverture** → Ouvre la page détaillée
2. **Bouton "Lire PDF"** → Ouvre le PDF dans un nouvel onglet
3. **Bouton "Aperçu dans la page"** → Affiche le PDF intégré à la page

### Modifier un livre

1. Cliquez sur l'icône **✏️ Modifier**
2. Modifiez les informations
3. Vous pouvez :
   - Conserver les fichiers existants (laissez vide)
   - Remplacer le PDF
   - Remplacer l'image de couverture

## 🔧 Configuration Avancée

### Augmenter la taille maximale des uploads

Dans `app.py` :
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB au lieu de 16MB
```

### Changer le port
```python
if __name__ == "__main__":
    app.run(debug=True, port=8000)  # Port 8000 au lieu de 5000
```

### Mode Production
```python
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
```

## 📂 Structure de la Base de Données

### Table `authors`
- `id` : INT (clé primaire)
- `name` : VARCHAR(100)
- `bio` : TEXT
- `created_at` : TIMESTAMP

### Table `categories`
- `id` : INT (clé primaire)
- `name` : VARCHAR(100)
- `description` : TEXT
- `created_at` : TIMESTAMP

### Table `books`
- `id` : INT (clé primaire)
- `title` : VARCHAR(200)
- `author_id` : INT (clé étrangère)
- `category_id` : INT (clé étrangère)
- `year` : INT
- `description` : TEXT
- `pdf_file` : VARCHAR(255) ← **Nom du fichier PDF**
- `cover_image` : VARCHAR(255) ← **Nom de l'image**
- `created_at` : TIMESTAMP
- `updated_at` : TIMESTAMP

## 🎨 Personnalisation

### Changer les couleurs

Dans `layout.html`, modifiez les variables CSS :
```css
:root {
    --primary-color: #2c3e50;     /* Couleur principale */
    --secondary-color: #3498db;   /* Couleur secondaire */
    --accent-color: #e74c3c;      /* Couleur accent */
}
```

### Modifier le dégradé de fond
```css
body {
    background: linear-gradient(135deg, #votre-couleur1 0%, #votre-couleur2 100%);
}
```

## 🐛 Résolution de problèmes

### Erreur de connexion MySQL
- Vérifiez que MySQL est démarré
- Vérifiez vos identifiants dans `app.py`
- Vérifiez que la base `librarydb` existe

### PDF ne s'affiche pas
- Vérifiez que le fichier est dans `static/uploads/books/`
- Vérifiez les permissions du dossier
- Vérifiez la taille du fichier (< 16MB)

### Image de couverture manquante
- L'image par défaut `default-cover.jpg` doit exister
- Placez-la dans `static/uploads/covers/`

### Erreur 413 (fichier trop grand)
- Augmentez `MAX_CONTENT_LENGTH` dans `app.py`
- Configurez votre serveur web (nginx/apache) si en production

## 📝 Améliorations Possibles

- [ ] Système d'authentification (login/logout)
- [ ] Gestion multi-utilisateurs
- [ ] API REST pour application mobile
- [ ] Export de catalogue (CSV, PDF)
- [ ] Système de notation des livres
- [ ] Commentaires et avis
- [ ] Recherche avancée (texte intégral)
- [ ] Statistiques et graphiques
- [ ] Tags personnalisés
- [ ] Liste de lecture / favoris

## 📄 Licence

Projet libre d'utilisation et de modification.

## 🙏 Support

Pour toute question ou problème :
1. Vérifiez ce README
2. Consultez les logs Flask dans le terminal
3. Vérifiez les logs MySQL

---

**Développé avec ❤️ et Flask**