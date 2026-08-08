import random
import time
import sys
import json
import os

# ═══════════════════════════════════════════════════════════════
#   MAISON DE L'ÉCHO MAUDIT — Version Améliorée
#   Bugs corrigés + nouvelles fonctionnalités
# ═══════════════════════════════════════════════════════════════

# ── Couleurs ANSI ────────────────────────────────────────────
class C:
    ROUGE    = "\033[91m"
    JAUNE    = "\033[93m"
    VERT     = "\033[92m"
    CYAN     = "\033[96m"
    MAGENTA  = "\033[95m"
    GRIS     = "\033[90m"
    BLANC    = "\033[97m"
    RESET    = "\033[0m"
    BOLD     = "\033[1m"
    DIM      = "\033[2m"
    ROUGE_F  = "\033[41m"   # fond rouge (flashback)

def colorier(texte, couleur):
    return f"{couleur}{texte}{C.RESET}"

# ── Narration ────────────────────────────────────────────────
def narrer(texte, vitesse=0.03, couleur=None):
    """Effet machine à écrire immersif avec couleur optionnelle."""
    if couleur:
        sys.stdout.write(couleur)
    for char in texte:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(vitesse)
    if couleur:
        sys.stdout.write(C.RESET)
    print()

def pause_suspens(duree=1.0):
    """Pause dramatique avec points de suspension."""
    for _ in range(3):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(duree / 3)
    print()

# ── Barres visuelles ─────────────────────────────────────────
def afficher_sanite(sanite):
    bar_length = 20
    filled = int(sanite / 5)
    if sanite > 60:
        couleur = C.VERT
    elif sanite > 30:
        couleur = C.JAUNE
    else:
        couleur = C.ROUGE
    bar = colorier("█" * filled, couleur) + colorier("░" * (bar_length - filled), C.GRIS)
    label = colorier(f"🧠 Santé Mentale", C.BLANC)
    print(f"  {label} : [{bar}] {colorier(str(sanite)+'/100', couleur)}")

def afficher_lampe(energie, allumee):
    bar_length = 20
    filled = int(energie / 5)
    if allumee:
        couleur = C.JAUNE if energie > 40 else C.ROUGE
        bar = colorier("▓" * filled, couleur) + colorier("░" * (bar_length - filled), C.GRIS)
        etat = colorier("ON", C.VERT)
    else:
        bar = colorier("░" * bar_length, C.GRIS)
        etat = colorier("OFF", C.ROUGE)
    label = colorier("🔦 Lampe", C.BLANC)
    print(f"  {label} ({etat})      : [{bar}] {colorier(str(energie)+'/100', C.GRIS)}")

def afficher_separateur(char="═", longueur=54, couleur=C.GRIS):
    print(colorier(char * longueur, couleur))

# ═══════════════════════════════════════════════════════════════

class JeuHorreur:
    def __init__(self):
        self.sanite          = 100
        self.energie_lampe   = 100
        self.lampe_allumee   = True
        self.inventaire      = []
        self.objets_examines = set()
        self.position        = "entree"
        self.en_jeu          = True
        self.victoire        = False
        self.tours           = 0
        self.salles_visitees = set()

        # ── Énigmes ─────────────────────────────────────────
        self.enigmes = {
            "salon": {
                "enigme": "Je commence la nuit et termine le matin. Une seule lettre. Que suis-je ?",
                "reponse": "n",
                "recompense": "batterie",
                "resolue": False,
                "indice": "C'est la première lettre du mot 'nuit'."
            },
            "cuisine": {
                "enigme": "Plus on m'enlève, plus je grandis. Que suis-je ?",
                "reponse": "trou",
                "recompense": "pommade",
                "resolue": False,
                "indice": "On en creuse dans la terre ou dans un mur."
            },
            "chambre": {
                "enigme": "Je parle sans bouche, j'entends sans oreilles. Je n'ai pas de corps mais je prends vie au vent. Que suis-je ?",
                "reponse": "echo",
                "recompense": "amulette",
                "resolue": False,
                "indice": "Ce que cette maison garde de vous..."
            }
        }

        # ── Salles ──────────────────────────────────────────
        # BUG CORRIGÉ : armoire séparée (armoire_cuisine / armoire_chambre)
        # BUG CORRIGÉ : chambre → cave via "descendre" (pas "escalier")
        # BUG CORRIGÉ : cave → chambre via "remonter"
        # BUG CORRIGÉ : salon → chambre nécessite photo_ancienne
        self.salles = {
            "entree": {
                "nom":    "L'Entrée",
                "desc":   "L'air est lourd, saturé d'une poussière qui danse comme des insectes morts sous la lueur de votre lampe. Le papier peint floral se décolle comme une peau morte. Quelque chose vous observe depuis les coins d'ombre.",
                "objets": ["poupee", "radio", "tableau"],
                "sorties": {"salon": True},
                "ascii": f"""
  {C.GRIS}╔══════════════════════╗
  ║   {C.ROUGE}👁  L'ENTRÉE  👁{C.GRIS}   ║
  ║      {C.JAUNE}/    \\{C.GRIS}         ║
  ║     {C.JAUNE}/  ??  \\{C.GRIS}        ║
  ║    {C.JAUNE}/________\\{C.GRIS}       ║
  ║   {C.ROUGE}│  POUSSIERES  │{C.GRIS}   ║
  ╚══════════════════════╝{C.RESET}"""
            },
            "salon": {
                "nom":    "Le Salon",
                "desc":   "Tous les meubles sont vissés au plafond. L'obscurité n'est pas une absence de lumière — c'est une présence qui vous frôle le cou. Une horloge accrochée au mur tourne à l'envers.",
                "objets": ["miroir", "chaise", "cheminee"],
                "sorties": {"entree": True, "cuisine": True, "chambre": True},
                "ascii": f"""
  {C.GRIS}╔════════════════════ ══╗
  ║   {C.ROUGE}LE SALON INVERSÉ{C.GRIS}   ║
  ║  {C.JAUNE}🪑──────────────🪑{C.GRIS}  ║
  ║     {C.CYAN}(plafond)  {C.GRIS}      ║
  ║   {C.MAGENTA}🪞{C.GRIS}  ──────  {C.ROUGE}🔥{C.GRIS}   ║
  ║      {C.GRIS}(sol vide){C.GRIS}      ║
  ╚══════════════════════╝{C.RESET}"""
            },
            "cuisine": {
                "nom":    "La Cuisine",
                "desc":   "Les ustensiles rouillés flottent dans l'évier comme s'ils attendaient un festin invisible. Une odeur de chair pourrie émane du réfrigérateur. L'ampoule clignote en morse.",
                "objets": ["frigo", "couteau", "armoire_cuisine"],
                "sorties": {"salon": True},
                "ascii": f"""
  {C.GRIS}╔══════════════════════╗
  ║    {C.ROUGE}LA CUISINE MAUDITE{C.GRIS} ║
  ║   {C.CYAN}🍳{C.GRIS}  ┌──────┐  {C.ROUGE}🔪{C.GRIS}  ║
  ║     {C.GRIS}│ {C.CYAN}🧊 FRIGO{C.GRIS} │     ║
  ║     {C.GRIS}│  {C.ROUGE}👁  👁{C.GRIS}  │     ║
  ║     {C.GRIS}└──────┘         ║
  ╚══════════════════════╝{C.RESET}"""
            },
            "chambre": {
                "nom":    "La Chambre",
                "desc":   "Le lit est défait, taché de sang séché. Des murmures d'enfants invisibles emplissent l'air. Vos anciens jouets sont rangés avec soin par quelqu'un d'autre... et récemment.",
                "objets": ["armoire_chambre", "photo", "lit"],
                "sorties": {"salon": True, "cave": True},
                "ascii": f"""
  {C.GRIS}╔══════════════════════╗
  ║    {C.ROUGE}LA CHAMBRE D'ENFANT{C.GRIS}║
  ║      {C.ROUGE}🛏 {C.GRIS}────────      ║
  ║   {C.ROUGE}/👁\\{C.GRIS}  ~~~~~~~~  {C.ROUGE}/👁\\{C.GRIS}║
  ║  {C.GRIS}(armoire)  {C.ROUGE}🩸{C.GRIS} (photo) ║
  ║  {C.GRIS}⬇ vers la CAVE ⬇{C.GRIS}    ║
  ╚══════════════════════╝{C.RESET}"""
            },
            "cave": {
                "nom":    "La Cave",
                "desc":   "Les murs suintent un liquide noir et visqueux. Au centre, un autel de fortune sur lequel repose une clé rouillée qui brille d'une lueur anormale. L'air est électrique.",
                "objets": ["autel", "coffre", "inscription"],
                "sorties": {"chambre": True, "sortie": True},
                "ascii": f"""
  {C.GRIS}╔══════════════════════╗
  ║     {C.ROUGE}LA CAVE FINALE{C.GRIS}    ║
  ║   {C.ROUGE}⚰{C.GRIS}  ────────  {C.ROUGE}⚰{C.GRIS}  ║
  ║      {C.JAUNE}/ AUTEL \\{C.GRIS}      ║
  ║     {C.JAUNE}/  🗝️  \\{C.GRIS}      ║
  ║    {C.JAUNE}/SORTIE ?\\{C.GRIS}      ║
  ╚══════════════════════╝{C.RESET}"""
            }
        }

        # ── Descriptions d'objets ───────────────────────────
        self.descriptions_objets = {
            "poupee": {
                "texte":    "Ses yeux de verre suivent votre mouvement. Vous vous souvenez l'avoir enterrée dans le jardin à l'âge de 8 ans. Sa bouche est fondue, mais elle sourit quand même.",
                "dmg":      -15,
                "item":     None,
                "flashback": "FLASHBACK : Vous êtes enfant. Vous cachez la poupée sous votre lit. Elle murmure votre nom dans l'obscurité. Votre mère dit que vous rêvez."
            },
            "radio": {
                "texte":    "Elle n'est pas branchée, mais elle grésille. Une voix distordue murmure : '...pourquoi es-tu revenu ?... La maison n'oublie jamais...'",
                "dmg":      -20,
                "item":     None,
                "flashback": "FLASHBACK : Vous avez 12 ans. La radio s'allume seule à 3h du matin. Vous entendez la voix de votre père — mort depuis 6 mois."
            },
            "tableau": {
                "texte":    "Une famille heureuse... mais leurs visages se déforment sous vos yeux. La fillette vous regarde. Elle ressemble à quelqu'un que vous connaissez. Vous récupérez la photo.",
                "dmg":      -8,
                "item":     "photo_ancienne",
                "flashback": None
            },
            "miroir": {
                "texte":    "Votre reflet cligne des yeux avant vous. Il sourit. Vous non. Il sort une note froissée de sa poche et la colle sur la vitre de l'intérieur.",
                "dmg":      -18,
                "item":     "note_miroir",
                "flashback": "FLASHBACK : Enfant, vous étiez convaincu que votre reflet ne vous copiait pas toujours. Personne ne vous a cru."
            },
            "chaise": {
                "texte":    "Elle est clouée au plafond, à l'envers. Sur l'assise, gravé au couteau : 'NE REGARDE PAS DERRIÈRE TOI'. Vous résistez à l'envie de vous retourner.",
                "dmg":      -10,
                "item":     None,
                "flashback": None
            },
            "cheminee": {
                "texte":    "Les cendres sont encore chaudes. Quelqu'un est passé récemment. En fouillant avec précaution, vous trouvez des allumettes.",
                "dmg":      0,
                "item":     "allumettes",
                "flashback": None
            },
            "frigo": {
                "texte":    "À l'intérieur, des yeux vous fixent depuis des viscères disposés avec soin, presque artistiquement. Vous fermez la porte en tremblant. La température de la pièce chute.",
                "dmg":      -25,
                "item":     None,
                "flashback": "FLASHBACK : Vous avez 6 ans. Votre mère vous dit de ne jamais ouvrir le frigo la nuit. Vous comprenez maintenant pourquoi."
            },
            "couteau": {
                "texte":    "Rouillé, mais tranchant. Gravé sur le manche : 'Propriété de Maman'. Il est froid dans votre paume — anormalement froid. Vous le prenez.",
                "dmg":      0,
                "item":     "couteau",
                "flashback": None
            },
            "armoire_cuisine": {
                "texte":    "Les portes s'ouvrent violemment. Des conserves tombent — toutes étiquetées avec votre prénom. Une main squelettique agrippe le bord de l'étagère et se retire lentement.",
                "dmg":      -20,
                "item":     None,
                "flashback": None
            },
            "armoire_chambre": {
                "texte":    "Vos vêtements d'enfant y sont accrochés, propres et repassés. Comme si on vous attendait. Une odeur de lavande masque quelque chose de bien plus sombre. Vous trouvez une pommade.",
                "dmg":      -12,
                "item":     "pommade",
                "flashback": "FLASHBACK : Vous vous cachiez dans cette armoire pendant les disputes. La porte ne fermait jamais complètement."
            },
            "photo": {
                "texte":    "Votre famille... mais leurs yeux sont creusés, vides. Au dos, une écriture que vous reconnaissez : 'Nous t'attendons encore'. L'encre est fraîche.",
                "dmg":      -5,
                "item":     "photo_souvenir",
                "flashback": None
            },
            "lit": {
                "texte":    "Les draps froissés portent encore la forme d'un corps. Une tache sombre s'étend sur l'oreiller. La chaleur du matelas est celle de quelqu'un qui vient juste de partir.",
                "dmg":      -15,
                "item":     None,
                "flashback": "FLASHBACK : Vous vous réveilliez parfois et votre oreiller était déplacé. Quelqu'un avait dormi à côté de vous."
            },
            "autel": {
                "texte":    "Une clé rouillée repose sur des ossements disposés en cercle parfait. Vous la prenez. Les murs semblent se resserrer imperceptiblement.",
                "dmg":      -10,
                "item":     "cle",
                "flashback": None
            },
            "coffre": {
                "texte":    "Cadenassé, très ancien. Sur le couvercle : 'Seul le souvenir ouvre la voie'. Il vibre légèrement sous vos doigts. Il faudra résoudre l'énigme de la pièce.",
                "dmg":      -5,
                "item":     None,
                "flashback": None
            },
            "inscription": {
                "texte":    "Graffitis au sang sur tous les murs, écrits des centaines de fois en spirale : 'ELLE VOUS REGARDE. ELLE ATTEND. NE LA LAISSEZ PAS VOUS TROUVER.'",
                "dmg":      -20,
                "item":     None,
                "flashback": "FLASHBACK : La dernière fois que vous étiez ici, les murs étaient blancs."
            }
        }

        # ── Effets des objets utilisables ───────────────────
        self.effets_items = {
            "couteau": {
                "desc":        "Vous serrez le couteau dans votre paume. Sa froideur vous ancre à la réalité.",
                "sanite":      +8,
                "lampe":       0,
                "consommable": False
            },
            "photo_ancienne": {
                "desc":        "La photo vous rappelle un temps plus simple. Un ancrage fragile dans la réalité.",
                "sanite":      +5,
                "lampe":       0,
                "consommable": False
            },
            "photo_souvenir": {
                "desc":        "Ce souvenir lumineux perce l'obscurité de votre esprit. Vous existez. Vous existez vraiment.",
                "sanite":      +20,
                "lampe":       0,
                "consommable": False
            },
            "note_miroir": {
                "desc":        "Vous lisez la note à l'envers : 'La clé est dans la mémoire. Cherchez où vous avez dormi.'",
                "sanite":      0,
                "lampe":       0,
                "consommable": False
            },
            "allumettes": {
                "desc":        "Vous utilisez les allumettes pour rallumer votre lampe.",
                "sanite":      0,
                "lampe":       +40,
                "consommable": True
            },
            "batterie": {
                "desc":        "Vous insérez la batterie. Votre lampe retrouve de la vigueur.",
                "sanite":      0,
                "lampe":       +60,
                "consommable": True
            },
            "pommade": {
                "desc":        "Vous appliquez la pommade sur vos tempes. Une sensation de calme vous envahit.",
                "sanite":      +30,
                "lampe":       0,
                "consommable": True
            },
            "amulette": {
                "desc":        "L'amulette vibre dans votre main. Une chaleur étrange vous protège.",
                "sanite":      +40,
                "lampe":       0,
                "consommable": True
            },
            "cle": {
                "desc":        "Vous tenez la clé. Elle est froide et lourde. La sortie est proche.",
                "sanite":      0,
                "lampe":       0,
                "consommable": False
            }
        }

        # ── Bruits d'ambiance ────────────────────────────────
        self.bruits = {
            "entree":  ["*grincement de porte*", "*soupir lointain*", "*craquement de bois*", "*froissement de papier peint*"],
            "salon":   ["*chuchotements*", "*meubles qui craquent au plafond*", "*tictac d'horloge à l'envers*", "*soupir proche*"],
            "cuisine": ["*gouttes d'eau irrégulières*", "*cliquetis de métal*", "*bourdonnement électrique*", "*frigo qui claque*"],
            "chambre": ["*sanglot étouffé*", "*berceuse sans mélodie*", "*battement de cœur*", "*murmure d'enfant*"],
            "cave":    ["*bourdonnement profond*", "*gémissement sourd*", "*murmure inintelligible*", "*pierre qui tombe*"]
        }

        # ── Événements aléatoires ────────────────────────────
        self.evenements = [
            {"texte": "Un rire d'enfant résonne derrière vous... et s'arrête net. 🥴",        "dmg": -8},
            {"texte": "Quelque chose vous effleure la nuque. Froid. Très froid. 🥶",           "dmg": -10},
            {"texte": "Vos mains tremblent. Une ombre traverse le mur. 👻",                    "dmg": -7},
            {"texte": "Vous entendez votre propre voix chuchoter votre nom. 😰",               "dmg": -12},
            {"texte": "Le sol pulse sous vos pieds, comme un battement de cœur. 💓",           "dmg": -5},
            {"texte": "Une odeur douce de votre enfance vous envahit. Un instant de paix. 🌸", "dmg": +5},
            {"texte": "Vous croyez voir la lumière du dehors. Illusion. 😶",                   "dmg": -6},
            {"texte": "Une main froide vous saisit l'épaule... mais il n'y a personne. 😱",    "dmg": -15},
        ]

    # ══════════════════════════════════════════════════════════
    #   AFFICHAGE
    # ══════════════════════════════════════════════════════════

    def afficher_salle(self):
        salle = self.salles[self.position]
        self.salles_visitees.add(self.position)

        # Art ASCII
        print(salle["ascii"])

        # Titre
        print(colorier(f"  ◈ {salle['nom'].upper()} ◈", C.ROUGE + C.BOLD))
        print()

        # Description (atténuée si lampe éteinte)
        if not self.lampe_allumee:
            narrer("  🌑 L'obscurité totale vous enveloppe. Vous ne voyez rien.", couleur=C.ROUGE)
        else:
            narrer(f"  {salle['desc']}", couleur=C.GRIS)

        # Effets de sanité
        if self.sanite < 20:
            narrer("  🌀 RÉALITÉ DISTORDUE — Les murs respirent. Les ombres parlent. Est-ce réel ?", couleur=C.ROUGE)
        elif self.sanite < 40:
            narrer("  🎭 Hallucination — Des silhouettes fuient en périphérie de votre vision.", couleur=C.JAUNE)
        elif self.sanite < 60:
            narrer("  😰 Vous sentez une présence. Constante. Patiente.", couleur=C.MAGENTA)

        print()

        # Objets
        objets_str = colorier(", ".join(salle["objets"]), C.CYAN)
        print(f"  📦 {colorier('Objets :', C.BLANC)} {objets_str}")

        # Sorties
        sorties_str = colorier(", ".join(salle["sorties"].keys()), C.VERT)
        print(f"  🚪 {colorier('Sorties :', C.BLANC)} {sorties_str}")

        # Énigme disponible
        if self.position in self.enigmes and not self.enigmes[self.position]["resolue"]:
            print(f"  ❓ {colorier('Énigme disponible', C.JAUNE)} (commande 'enigme')")

    def afficher_stats(self):
        afficher_separateur("─", 54, C.GRIS)
        afficher_sanite(self.sanite)
        afficher_lampe(self.energie_lampe, self.lampe_allumee)
        inv = colorier(", ".join(self.inventaire), C.CYAN) if self.inventaire else colorier("Vide", C.GRIS)
        print(f"  📦 {colorier('Inventaire :', C.BLANC)} {inv}")
        afficher_separateur("─", 54, C.GRIS)

    def afficher_aide(self):
        afficher_separateur()
        print(colorier("  📖 COMMANDES DISPONIBLES", C.BOLD + C.BLANC))
        afficher_separateur()
        commandes = [
            ("examiner [objet]",  "Examiner un objet dans la salle"),
            ("utiliser [objet]",  "Utiliser un objet de l'inventaire"),
            ("aller [direction]", "Se déplacer vers une sortie"),
            ("inventaire",        "Afficher l'inventaire en détail"),
            ("enigme",            "Résoudre l'énigme de la salle"),
            ("bruits",            "Écouter attentivement l'ambiance"),
            ("lampe",             "Allumer / éteindre la lampe"),
            ("stats",             "Afficher les statistiques"),
            ("sauvegarder",       "Sauvegarder la partie"),
            ("charger",           "Charger une partie sauvegardée"),
            ("aide",              "Afficher cette aide"),
            ("quitter",           "Quitter le jeu"),
        ]
        for cmd, desc in commandes:
            print(f"  {colorier(cmd.ljust(20), C.CYAN)}  {colorier(desc, C.GRIS)}")
        afficher_separateur()

    def afficher_inventaire_detail(self):
        """Affiche l'inventaire avec descriptions complètes."""
        if not self.inventaire:
            narrer("  Votre inventaire est vide.", couleur=C.GRIS)
            return
        afficher_separateur()
        print(colorier("  📦 INVENTAIRE DÉTAILLÉ", C.BOLD + C.BLANC))
        afficher_separateur()
        descriptions_items = {
            "photo_ancienne":  "Une photo récupérée d'un tableau. Elle vous appartient.",
            "note_miroir":     "Note à l'envers : 'La clé est dans la mémoire. Cherchez où vous avez dormi.'",
            "allumettes":      "Permet de rallumer la lampe. +40 énergie.",
            "batterie":        "Batterie de rechange pour la lampe. +60 énergie.",
            "pommade":         "Baume apaisant. +30 santé mentale. Consommable.",
            "couteau":         "Rouillé mais tranchant. +8 santé mentale à l'utilisation.",
            "photo_souvenir":  "Photo de famille. +20 santé mentale à l'utilisation.",
            "amulette":        "Amulette mystérieuse. +40 santé mentale. Consommable.",
            "cle":             "La clé rouillée. Elle ouvre la sortie de la cave.",
        }
        for item in self.inventaire:
            desc = descriptions_items.get(item, "Objet mystérieux.")
            print(f"  {colorier('•', C.ROUGE)} {colorier(item.upper(), C.CYAN)} — {colorier(desc, C.GRIS)}")
        afficher_separateur()

    # ══════════════════════════════════════════════════════════
    #   MÉCHANIQUES DE JEU
    # ══════════════════════════════════════════════════════════

    def modifier_sanite(self, valeur):
        self.sanite = max(0, min(100, self.sanite + valeur))

    def recharger_lampe(self, energie):
        self.energie_lampe = min(100, self.energie_lampe + energie)
        if not self.lampe_allumee and self.energie_lampe > 0:
            self.lampe_allumee = True
            narrer("  💡 Votre lampe s'allume à nouveau !", couleur=C.JAUNE)

    def consommer_lampe(self):
        if self.lampe_allumee:
            drain = random.randint(1, 4)
            self.energie_lampe = max(0, self.energie_lampe - drain)
            if self.energie_lampe == 0:
                self.lampe_allumee = False
                narrer("  💡 Votre lampe s'éteint ! L'obscurité vous enveloppe...", couleur=C.ROUGE)
                self.modifier_sanite(-15)

    def evenement_aleatoire(self):
        if random.random() < 0.30:
            evt = random.choice(self.evenements)
            narrer(f"  {evt['texte']}", couleur=C.MAGENTA if evt["dmg"] < 0 else C.VERT)
            self.modifier_sanite(evt["dmg"])

    def bruit_aleatoire(self):
        if random.random() < 0.40:
            directions = ["à gauche", "à droite", "derrière vous", "au-dessus", "en dessous de vous"]
            direction  = random.choice(directions)
            bruit      = random.choice(self.bruits.get(self.position, ["*silence inquiétant*"]))
            narrer(f"  🔊 {direction.capitalize()} : {colorier(bruit, C.MAGENTA)}")

    def afficher_flashback(self, texte):
        """Affiche un flashback encadré."""
        print()
        afficher_separateur("▓", 54, C.ROUGE)
        print(colorier("  ◈ FLASHBACK ◈", C.BOLD + C.ROUGE))
        afficher_separateur("▓", 54, C.ROUGE)
        narrer(f"  {texte}", vitesse=0.035, couleur=C.ROUGE)
        afficher_separateur("▓", 54, C.ROUGE)
        input(colorier("  [ Appuyez sur Entrée pour continuer... ]", C.GRIS))
        print()

    # ══════════════════════════════════════════════════════════
    #   EXAMINER
    # ══════════════════════════════════════════════════════════

    def examiner(self, objet):
        salle = self.salles[self.position]

        if objet not in salle["objets"]:
            narrer(f"  Vous ne voyez pas '{objet}' ici.", couleur=C.JAUNE)
            return

        cle_examen = (self.position, objet)
        if cle_examen in self.objets_examines:
            narrer("  Vous regardez à nouveau... mais quelque chose a changé imperceptiblement.", couleur=C.GRIS)
            self.modifier_sanite(-3)
            return

        self.objets_examines.add(cle_examen)

        if objet not in self.descriptions_objets:
            narrer("  Rien d'intéressant... ou peut-être que vous ne voulez pas savoir.", couleur=C.GRIS)
            return

        info = self.descriptions_objets[objet]

        print()
        afficher_separateur("·", 54, C.GRIS)
        narrer(f"  🔍 {info['texte']}", couleur=C.BLANC)

        if info["dmg"] < 0:
            narrer(f"  🧠 {abs(info['dmg'])} points de sanité perdus.", couleur=C.ROUGE)
            self.modifier_sanite(info["dmg"])
        elif info["dmg"] > 0:
            self.modifier_sanite(info["dmg"])

        if info["item"] and info["item"] not in self.inventaire:
            self.inventaire.append(info["item"])
            narrer(f"  📦 {colorier(info['item'].upper(), C.CYAN)} ajouté à l'inventaire !", couleur=C.VERT)

        afficher_separateur("·", 54, C.GRIS)

        if info.get("flashback"):
            time.sleep(0.8)
            self.afficher_flashback(info["flashback"])

    # ══════════════════════════════════════════════════════════
    #   UTILISER
    # ══════════════════════════════════════════════════════════

    def utiliser(self, objet):
        if objet not in self.inventaire:
            narrer(f"  Vous n'avez pas '{objet}' dans votre inventaire.", couleur=C.JAUNE)
            return

        if objet not in self.effets_items:
            narrer(f"  Vous ne savez pas comment utiliser '{objet}' ici.", couleur=C.GRIS)
            return

        effet = self.effets_items[objet]
        narrer(f"  ✋ {effet['desc']}", couleur=C.BLANC)

        if effet["sanite"] != 0:
            self.modifier_sanite(effet["sanite"])
            signe = "+" if effet["sanite"] > 0 else ""
            couleur = C.VERT if effet["sanite"] > 0 else C.ROUGE
            narrer(f"  🧠 Santé mentale : {signe}{effet['sanite']}", couleur=couleur)

        if effet["lampe"] > 0:
            self.recharger_lampe(effet["lampe"])
            narrer(f"  🔦 Énergie lampe : +{effet['lampe']}", couleur=C.JAUNE)

        if effet["consommable"]:
            self.inventaire.remove(objet)
            narrer(f"  📦 {objet.upper()} consommé.", couleur=C.GRIS)

    # ══════════════════════════════════════════════════════════
    #   ÉNIGMES
    # ══════════════════════════════════════════════════════════

    def resoudre_enigme(self):
        if self.position not in self.enigmes:
            narrer("  Il n'y a pas d'énigme dans cette salle.", couleur=C.GRIS)
            return

        enigme = self.enigmes[self.position]

        if enigme["resolue"]:
            narrer("  Vous avez déjà résolu cette énigme.", couleur=C.GRIS)
            return

        print()
        afficher_separateur("?", 54, C.JAUNE)
        print(colorier("  ❓ ÉNIGME", C.BOLD + C.JAUNE))
        afficher_separateur("?", 54, C.JAUNE)
        narrer(f"  {enigme['enigme']}", couleur=C.BLANC)
        print()
        print(f"  {colorier('1.', C.CYAN)} Donner une réponse")
        print(f"  {colorier('2.', C.CYAN)} Demander un indice {colorier('(-5 sanité)', C.ROUGE)}")
        print(f"  {colorier('3.', C.CYAN)} Annuler")
        print()

        choix = input(colorier("  Votre choix (1-3) : ", C.GRIS)).strip()

        if choix == "1":
            reponse = input(colorier("  Votre réponse : ", C.BLANC)).strip().lower()
            if reponse == enigme["reponse"]:
                narrer(f"  ✅ Correct ! Vous trouvez : {colorier(enigme['recompense'].upper(), C.CYAN)} !", couleur=C.VERT)
                self.inventaire.append(enigme["recompense"])
                enigme["resolue"] = True
                self.modifier_sanite(+20)
                narrer("  🧠 +20 santé mentale — La résolution vous stabilise.", couleur=C.VERT)
            else:
                narrer("  ❌ Faux. L'air devient plus froid. Les ombres se rapprochent.", couleur=C.ROUGE)
                self.modifier_sanite(-10)

        elif choix == "2":
            narrer(f"  💡 Indice : {enigme['indice']}", couleur=C.JAUNE)
            self.modifier_sanite(-5)

    # ══════════════════════════════════════════════════════════
    #   NAVIGATION — BUGS CORRIGÉS
    # ══════════════════════════════════════════════════════════

    def action_sortie(self, direction):
        salle = self.salles[self.position]

        if direction not in salle["sorties"]:
            narrer("  Impossible. Les murs semblent se resserrer sur vous.", couleur=C.ROUGE)
            self.modifier_sanite(-2)
            return

        # ── Condition spéciale : salon → chambre ────────────
        # BUG CORRIGÉ : nécessite photo_ancienne (pas juste "photo")
        if direction == "chambre" and self.position == "salon":
            if "photo_ancienne" not in self.inventaire:
                narrer("  L'escalier craque... Une voix vous retient : 'Pas sans souvenir...' 😰", couleur=C.ROUGE)
                self.modifier_sanite(-10)
                return

        # ── Condition spéciale : cave → sortie ──────────────
        if direction == "sortie":
            self.utiliser_cle()
            return

        # ── Déplacement normal ───────────────────────────────
        nom_dest = self.salles[direction]["nom"]
        narrer(f"  Vous avancez vers {colorier(nom_dest, C.CYAN)}...", couleur=C.GRIS)
        self.position = direction
        self.modifier_sanite(-3)

        # Bruit d'arrivée
        bruit = random.choice(self.bruits.get(self.position, ["*silence*"]))
        time.sleep(0.4)
        narrer(f"  🔊 {colorier(bruit, C.MAGENTA)}")

    # ── Utiliser la clé pour sortir ──────────────────────────
    def utiliser_cle(self):
        if "cle" not in self.inventaire:
            narrer("  La porte est verrouillée. Il vous faut une clé.", couleur=C.ROUGE)
            return

        narrer("  La clé tourne dans la serrure avec un claquement sec.", couleur=C.BLANC)
        pause_suspens(1.0)
        narrer("  La porte s'ouvre sur...", couleur=C.BLANC)
        pause_suspens(1.5)

        self.victoire = True

        afficher_separateur("═")
        if self.sanite > 80:
            print(colorier("  🌅  FIN : SURVIVANT RÉSILIENT", C.BOLD + C.VERT))
            narrer("  Vous échappez, relativement sain d'esprit.", couleur=C.VERT)
            narrer("  Mais parfois, la nuit, vous entendez encore les murmures...", couleur=C.GRIS)
        elif self.sanite > 50:
            print(colorier("  🌫️  FIN : ÉCHAPPÉ BRISÉ", C.BOLD + C.JAUNE))
            narrer("  Vous échappez, mais l'horreur est gravée en vous pour toujours.", couleur=C.JAUNE)
            narrer("  Votre reflet vous semble parfois étranger...", couleur=C.GRIS)
        elif self.sanite > 20:
            print(colorier("  🌀  FIN : PRISONNIER MENTAL", C.BOLD + C.MAGENTA))
            narrer("  Vous 'échappez'... mais êtes-vous vraiment sorti ?", couleur=C.MAGENTA)
            narrer("  La maison semble vous suivre où que vous alliez.", couleur=C.GRIS)
        else:
            print(colorier("  🔁  FIN : BOUCLE ÉTERNELLE", C.BOLD + C.ROUGE))
            narrer("  La porte s'ouvre sur un autre couloir identique.", couleur=C.ROUGE)
            narrer("  Vous réalisez que vous n'êtes jamais sorti.", couleur=C.ROUGE)
            narrer("  La maison vous a pour toujours.", couleur=C.GRIS)
        afficher_separateur("═")

    # ══════════════════════════════════════════════════════════
    #   TOGGLE LAMPE
    # ══════════════════════════════════════════════════════════

    def toggle_lampe(self):
        if self.lampe_allumee:
            self.lampe_allumee = False
            narrer("  💡 Vous éteignez la lampe. L'obscurité vous enveloppe...", couleur=C.ROUGE)
            self.modifier_sanite(-5)
        else:
            if self.energie_lampe > 0:
                self.lampe_allumee = True
                narrer("  💡 Vous allumez la lampe !", couleur=C.JAUNE)
            else:
                narrer("  ❌ Plus d'énergie dans la lampe !", couleur=C.ROUGE)

    # ══════════════════════════════════════════════════════════
    #   SAUVEGARDE / CHARGEMENT
    # ══════════════════════════════════════════════════════════

    def sauvegarder(self):
        data = {
            "position":        self.position,
            "sanite":          self.sanite,
            "energie_lampe":   self.energie_lampe,
            "lampe_allumee":   self.lampe_allumee,
            "inventaire":      self.inventaire,
            "objets_examines": list(self.objets_examines),
            "enigmes":         self.enigmes,
            "tours":           self.tours,
            "salles_visitees": list(self.salles_visitees)
        }
        try:
            with open("sauvegarde_maison.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            narrer("  💾 Partie sauvegardée.", couleur=C.VERT)
        except Exception as e:
            narrer(f"  ❌ Erreur sauvegarde : {e}", couleur=C.ROUGE)

    def charger(self):
        try:
            if not os.path.exists("sauvegarde_maison.json"):
                narrer("  ❌ Aucune sauvegarde trouvée.", couleur=C.ROUGE)
                return False
            with open("sauvegarde_maison.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.position        = data["position"]
            self.sanite          = data["sanite"]
            self.energie_lampe   = data["energie_lampe"]
            self.lampe_allumee   = data["lampe_allumee"]
            self.inventaire      = data["inventaire"]
            self.objets_examines = set(tuple(item) for item in data["objets_examines"])
            self.enigmes         = data["enigmes"]
            self.tours           = data["tours"]
            self.salles_visitees = set(data.get("salles_visitees", []))
            narrer("  📂 Partie chargée.", couleur=C.VERT)
            return True
        except Exception as e:
            narrer(f"  ❌ Erreur chargement : {e}", couleur=C.ROUGE)
            return False

    # ══════════════════════════════════════════════════════════
    #   CONDITIONS DE FIN
    # ══════════════════════════════════════════════════════════

    def verifier_fin(self):
        self.sanite = max(0, min(100, self.sanite))

        if self.sanite <= 0:
            print()
            afficher_separateur("═")
            narrer("  💀  VOTRE ESPRIT SE BRISE", couleur=C.BOLD + C.ROUGE)
            narrer("  Les murs vous avalent. Les ombres deviennent votre seule réalité.", couleur=C.ROUGE)
            narrer("  Vous êtes désormais un habitant permanent de la maison...", couleur=C.GRIS)
            print(colorier("\n  🔥 GAME OVER — Folie Absolue", C.BOLD + C.ROUGE))
            afficher_separateur("═")
            self.en_jeu = False

        if self.victoire:
            self.en_jeu = False

        if not self.lampe_allumee and self.energie_lampe <= 0 and random.random() < 0.25:
            print()
            afficher_separateur("═")
            narrer("  🌑  L'OBSCURITÉ VOUS DÉVORE", couleur=C.ROUGE)
            narrer("  Sans lumière, vous errez sans fin dans les ténèbres.", couleur=C.ROUGE)
            narrer("  La maison a gagné.", couleur=C.GRIS)
            print(colorier("\n  🌌 GAME OVER — Perdu dans les Ténèbres", C.BOLD + C.ROUGE))
            afficher_separateur("═")
            self.en_jeu = False

    # ══════════════════════════════════════════════════════════
    #   BOUCLE PRINCIPALE
    # ══════════════════════════════════════════════════════════

    def jouer(self):
        # Intro
        os.system("cls" if os.name == "nt" else "clear")
        print()
        afficher_separateur("═")
        print(colorier("         👻  MAISON DE L'ÉCHO MAUDIT  👻", C.BOLD + C.ROUGE))
        print(colorier("              Un jeu d'horreur psychologique", C.GRIS))
        afficher_separateur("═")
        time.sleep(0.5)
        narrer("  Vous vous réveillez dans l'entrée d'une maison familière...", couleur=C.GRIS)
        narrer("  Mais quelque chose ne va pas.", couleur=C.GRIS)
        time.sleep(0.5)
        narrer("  Rien ne va plus.", couleur=C.ROUGE)
        time.sleep(0.8)
        narrer("  Votre lampe de poche est votre seul réconfort.", couleur=C.JAUNE)
        narrer("  Survivez. Explorez. Échappez...", couleur=C.BLANC)
        narrer("  ...avant que la folie ne vous consume.", couleur=C.GRIS)
        afficher_separateur("═")
        time.sleep(0.5)

        if os.path.exists("sauvegarde_maison.json"):
            choix = input(colorier("\n  📂 Sauvegarde détectée. Charger ? (o/n) : ", C.CYAN)).strip().lower()
            if choix == "o":
                self.charger()

        input(colorier("\n  [ Appuyez sur Entrée pour entrer dans la maison... ]", C.GRIS))

        # ── Boucle principale ────────────────────────────────
        while self.en_jeu:
            self.tours += 1
            print()
            afficher_separateur("═")
            print(f"  {colorier('📍', C.ROUGE)} {colorier(self.salles[self.position]['nom'].upper(), C.BOLD + C.BLANC)}  {colorier(f'| Tour {self.tours}', C.GRIS)}  {colorier(f'| Salles visitées : {len(self.salles_visitees)}/5', C.GRIS)}")
            afficher_separateur("═")

            self.afficher_salle()
            self.afficher_stats()

            # Événements et bruits
            self.evenement_aleatoire()
            self.bruit_aleatoire()
            self.consommer_lampe()

            # Commande
            print()
            commande = input(colorier("  > ", C.ROUGE + C.BOLD)).strip().lower()
            print()

            if commande == "quitter":
                narrer("  La maison semble rire tandis que vous abandonnez...", couleur=C.GRIS)
                break
            elif commande == "aide":
                self.afficher_aide()
            elif commande == "stats":
                self.afficher_stats()
            elif commande == "inventaire":
                self.afficher_inventaire_detail()
            elif commande == "sauvegarder":
                self.sauvegarder()
            elif commande == "charger":
                self.charger()
            elif commande == "enigme":
                self.resoudre_enigme()
            elif commande == "bruits":
                narrer("  Vous restez immobile et tendez l'oreille...", couleur=C.GRIS)
                time.sleep(0.8)
                self.bruit_aleatoire()
            elif commande == "lampe":
                self.toggle_lampe()
            elif commande.startswith("examiner "):
                self.examiner(commande.split(" ", 1)[1])
            elif commande.startswith("utiliser "):
                self.utiliser(commande.split(" ", 1)[1])
            elif commande.startswith("aller "):
                self.action_sortie(commande.split(" ", 1)[1])
            else:
                narrer("  Commande inconnue. L'hésitation vous ronge...", couleur=C.GRIS)
                self.modifier_sanite(-3)

            self.verifier_fin()
            time.sleep(0.3)

        # ── Écran de fin ─────────────────────────────────────
        print()
        afficher_separateur("═")
        print(colorier("  FIN DU JEU", C.BOLD + C.BLANC))
        afficher_separateur("═")
        print(f"\n  {colorier('📊 STATISTIQUES FINALES', C.BOLD + C.BLANC)}")
        print(f"     Tours joués         : {colorier(str(self.tours), C.CYAN)}")
        print(f"     Santé mentale       : {colorier(str(self.sanite)+'/100', C.CYAN)}")
        print(f"     Objets collectés    : {colorier(str(len(self.inventaire)), C.CYAN)}")
        print(f"     Salles explorées    : {colorier(str(len(self.salles_visitees))+'/5', C.CYAN)}")
        print(f"     Objets examinés     : {colorier(str(len(self.objets_examines)), C.CYAN)}")
        print()
        if self.victoire:
            print(colorier("  🎊 FÉLICITATIONS ! Vous avez échappé à la maison !", C.BOLD + C.VERT))
        else:
            print(colorier("  💀 La maison vous a gardé pour l'éternité...", C.ROUGE))
        print()
        afficher_separateur("═")
        print(colorier("  Merci d'avoir joué.", C.GRIS))
        print()


# ── Point d'entrée ───────────────────────────────────────────
if __name__ == "__main__":
    jeu = JeuHorreur()
    jeu.jouer()
