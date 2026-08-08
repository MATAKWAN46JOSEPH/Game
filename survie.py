import random
import time

class JeuSurvie:
    def __init__(self):
        # Statistiques du joueur
        self.stats = {"Faim": 100, "Soif": 100, "Santé": 100, "Énergie": 100}
        self.inventaire = {"Bois": 0, "Pierre": 0, "Nourriture": 3, "Eau": 2}
        self.jour = 1
        self.en_vie = True
        self.victoire = False
        self.ruines_decouvertes = False
        self.ruines_progress = 0
        self.a_un_abri = False
        self.a_gourde = False

    def clamp_stats(self):
        for key in self.stats:
            self.stats[key] = max(0, min(100, self.stats[key]))

    def afficher_etat(self):
        print(f"\n{'='*60}")
        print(f"🏝️   JOUR {self.jour}   🏝️")
        print(f"{'='*60}")
        for stat, val in self.stats.items():
            bar_length = 10
            filled = int(val / 10)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"{stat:7}: |{bar}| {val}/100")
        print(f"Inventaire: {self.inventaire}")
        if self.a_un_abri:
            print("🏠 Abri construit (meilleure régén énergie/santé).")
        if self.a_gourde:
            print("🥤 Gourde disponible (plus d'eau trouvée).")
        if self.ruines_decouvertes:
            print(f"🗿 Ruines découvertes (progrès: {self.ruines_progress}/3).")

    def verifier_mort(self):
        if (self.stats["Santé"] <= 0 or self.stats["Faim"] <= 0 or 
            self.stats["Soif"] <= 0):
            print("\n💀 Vous avez péri sur l'île... Game Over.")
            self.en_vie = False

    def evenement_aleatoire(self):
        event = random.random()
        if event < 0.10:
            print("\n⛈️ TEMPÊTE ! -15 Santé, -20 Énergie.")
            self.stats["Santé"] -= 15
            self.stats["Énergie"] -= 20
        elif event < 0.20:
            print("\n🐗 Animal sauvage ! -20 Santé.")
            self.stats["Santé"] -= 20
        elif event < 0.25:
            print("\n🍀 Chance incroyable ! +2 Nourriture, +2 Eau.")
            self.inventaire["Nourriture"] += 2
            self.inventaire["Eau"] += 2
        elif event < 0.35 and not self.ruines_decouvertes:
            print("\n🗿 Vous découvrez des RUINES ANCIENNES !")
            self.ruines_decouvertes = True

    def explorer(self):
        if self.stats["Énergie"] < 30:
            print("❌ Pas assez d'énergie pour explorer ! Reposez-vous.")
            return
        print("\n🌍 Vous explorez l'île...")
        self.stats["Énergie"] -= 30
        self.stats["Faim"] -= 10
        self.stats["Soif"] -= 15
        trouvaille = random.choice(["Bois", "Pierre", "Nourriture", "Eau", "Rien"])
        if trouvaille != "Rien":
            quantite = random.randint(1, 3)
            self.inventaire[trouvaille] += quantite
            print(f"📦 Trouvé : {quantite}x {trouvaille}")
        else:
            print("❌ Rien trouvé.")
        if self.ruines_decouvertes:
            print("✨ Les ruines brillent au loin...")

    def crafter(self):
        if self.stats["Énergie"] < 15:
            print("❌ Trop fatigué pour crafter !")
            return
        print("\n🔨 --- CRAFT ---")
        print("1. Abri (5 Bois, 2 Pierre)")
        print("2. Gourde (3 Pierre)")
        choix = input("Choix (1/2): ").strip()
        if choix == "1" and self.inventaire["Bois"] >= 5 and self.inventaire["Pierre"] >= 2:
            self.a_un_abri = True
            self.inventaire["Bois"] -= 5
            self.inventaire["Pierre"] -= 2
            print("🏠 Abri construit !")
        elif choix == "2" and self.inventaire["Pierre"] >= 3:
            self.a_gourde = True
            self.inventaire["Pierre"] -= 3
            print("🥤 Gourde fabriquée !")
        else:
            print("❌ Ressources insuffisantes ou choix invalide.")

    def se_reposer(self):
        gain = 50 if self.a_un_abri else 25
        print(f"\n😴 Vous vous reposez... (+{gain} Énergie)")
        self.stats["Énergie"] = min(100, self.stats["Énergie"] + gain)
        self.stats["Faim"] -= 5
        self.stats["Soif"] -= 5

    def chercher_eau(self):
        if self.stats["Énergie"] < 25:
            print("❌ Pas assez d'énergie pour chercher de l'eau !")
            return
        print("\n💧 Recherche d'eau...")
        self.stats["Énergie"] -= 25
        self.stats["Faim"] -= 8
        self.stats["Soif"] -= 12
        quantite = random.randint(2, 4) if self.a_gourde else random.randint(1, 2)
        self.inventaire["Eau"] += quantite
        print(f"📦 {quantite} unité(s) d'eau trouvée(s) !")

    def boire(self):
        if self.inventaire["Eau"] > 0:
            self.inventaire["Eau"] -= 1
            self.stats["Soif"] = min(100, self.stats["Soif"] + 35)
            print("💧 Vous buvez. Rafraîchissant !")
        else:
            print("❌ Plus d'eau !")

    def explorer_ruines(self):
        if not self.ruines_decouvertes:
            print("❌ Aucune ruine découverte.")
            return
        if self.stats["Énergie"] < 45:
            print("❌ Trop fatigué pour les ruines !")
            return
        print("\n🗿 Exploration des ruines...")
        self.stats["Énergie"] -= 45
        self.stats["Faim"] -= 12
        self.stats["Soif"] -= 15
        if random.random() < 0.4:
            self.ruines_progress += 1
            print(f"🔍 Progrès: {self.ruines_progress}/3")
            if self.ruines_progress >= 3:
                print("\n🚤 🎉 Vous trouvez un BATEAU ! Victoire !")
                self.victoire = True
                return
        else:
            print("❌ Pas de découverte majeure.")
        if random.random() < 0.2:
            print("🐍 Piège ancien ! -10 Santé.")
            self.stats["Santé"] -= 10

    def fin_tour(self):
        self.stats["Faim"] = max(0, self.stats["Faim"] - random.randint(6, 12))
        self.stats["Soif"] = max(0, self.stats["Soif"] - random.randint(10, 18))
        self.stats["Énergie"] = max(0, self.stats["Énergie"] - random.randint(4, 8))
        if self.a_un_abri:
            self.stats["Santé"] = min(100, self.stats["Santé"] + random.randint(1, 3))
        if self.stats["Faim"] < 25:
            self.stats["Santé"] -= random.randint(2, 5)
        if self.stats["Soif"] < 25:
            self.stats["Santé"] -= random.randint(3, 6)

    def jouer(self):
        print("🏝️ BIENVENUE SUR L'ÎLE MAUDITE 🏝️")
        print("Survivez, craft, explorez... et FUYEZ !")
        while self.en_vie and not self.victoire:
            self.afficher_etat()
            print("\n📋 ACTIONS :")
            print("1. 🌍 Explorer")
            print("2. 🔨 Crafter")
            print("3. 😴 Se reposer")
            print("4. 🍎 Manger")
            print("5. 💧 Chercher eau")
            print("6. 🥤 Boire")
            if self.ruines_decouvertes:
                print("7. 🗿 Ruines")
            action = input("\nChoix (1-7): ").strip()
            if action == "1":
                self.explorer()
            elif action == "2":
                self.crafter()
            elif action == "3":
                self.se_reposer()
            elif action == "4":
                if self.inventaire["Nourriture"] > 0:
                    self.inventaire["Nourriture"] -= 1
                    self.stats["Faim"] = min(100, self.stats["Faim"] + 35)
                    print("🍎 Bon appétit !")
                else:
                    print("❌ Plus de nourriture !")
            elif action == "5":
                self.chercher_eau()
            elif action == "6":
                self.boire()
            elif action == "7":
                self.explorer_ruines()
            else:
                print("❌ Choix invalide !")
                time.sleep(0.5)
                continue

            self.evenement_aleatoire()
            self.fin_tour()
            self.clamp_stats()
            self.verifier_mort()
            self.jour += 1
            time.sleep(0.8)

        if self.victoire:
            print("\n🏆 **VICTOIRE ULTIME !** Vous avez fui l'île maudite.")
        else:
            print("\n💀 **GAME OVER** - L'île vous a vaincu.")

# Lancer le jeu
if __name__ == "__main__":
    jeu = JeuSurvie()
    jeu.jouer()