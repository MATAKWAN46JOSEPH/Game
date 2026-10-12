# Maison Maudite — version mobile

Cette version transforme le jeu 3D en application web installable (PWA), adaptée aux écrans tactiles. Le jeu garde les cinq pièces, les objets, les flashbacks et les fins de la version HTML d’origine.

## Jouer sur téléphone

1. Publiez **tout le contenu de ce dossier** sur un hébergement web HTTPS. Le fichier HTML seul ne suffit pas pour l’installation.
2. Ouvrez l’adresse du jeu sur le téléphone et attendez que la première page finisse de charger.
3. Sur Android, choisissez **Installer l’application** dans le navigateur, ou touchez **INSTALLER LE JEU** si le bouton apparaît.
4. Sur iPhone, ouvrez le menu **Partager**, puis **Sur l’écran d’accueil**.

Une connexion Internet est nécessaire au premier chargement du moteur 3D. Le service worker essaie ensuite de le mettre en cache pour les lancements suivants hors connexion.

## Commandes

- Joystick à gauche : avancer, reculer et se déplacer latéralement.
- Glisser sur la vue : regarder autour de soi.
- **AGIR** : examiner l’objet ou la porte visé(e) au centre de l’écran.
- **LAMPE** : allumer ou éteindre la lampe.

La partie est sauvegardée automatiquement sur l’appareil. Le bouton **REPRENDRE** apparaît lorsqu’une sauvegarde est disponible.

## Aperçu sur ordinateur

Dans ce dossier, lancez `python -m http.server 8000`, puis ouvrez `http://localhost:8000`. Pour installer l’application sur un téléphone, il faut une adresse HTTPS.

## Fichiers

- `index.html` : jeu et commandes tactiles.
- `manifest.webmanifest` : nom, icônes et mode d’affichage de l’application.
- `sw.js` : mise en cache de l’application et du moteur 3D.
- `icon-*` : icônes d’installation.

Le moteur Three.js utilisé par le jeu est chargé depuis cdnjs, version r128. Une connexion est donc requise au premier lancement; le service worker essaie de conserver ce moteur en cache pour les ouvertures suivantes.
