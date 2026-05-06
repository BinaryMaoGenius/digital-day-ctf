# Dossier de Présentation : Digital Day CTF – L’Équation du Mandé

**Objet :** Présentation du concours de cybersécurité, cadre pédagogique et mesures de sécurité.

---

## 1. Introduction : Qu'est-ce qu'un CTF ?

Le **Capture The Flag (CTF)** est une compétition de cybersécurité où les participants (individuellement ou en équipe) doivent résoudre des énigmes techniques pour trouver une preuve de réussite, appelée "Flag" (drapeau).

Ces épreuves simulent des situations réelles de vulnérabilités informatiques dans un environnement **strictement contrôlé et isolé**.

## 2. L'Événement : "L'Équation du Mandé"

Le **Digital Day CTF** est une édition spéciale thématisée autour de l'histoire et de la culture malienne. À travers 15 missions techniques (Web, Cryptographie, Forensics, etc.), les élèves devront faire preuve de logique et de persévérance pour sécuriser le "patrimoine numérique de l'Empire".

### Objectifs pédagogiques :
*   Sensibiliser aux enjeux de la cybersécurité.
*   Développer des compétences en analyse de données et résolution de problèmes complexes.
*   Favoriser le travail d'équipe et l'éthique numérique.

## 3. Sécurité et Contrôle de l'Environnement

L'administration peut être rassurée sur les points suivants :

*   **Limitation des tentatives (Rate-Limiting)** : Le système empêche techniquement le "brute-force" (tester des milliers de combinaisons au hasard). Après quelques tentatives erronées, le participant est temporairement bloqué.
*   **Plateforme de Score (RootTheBox)** : Nous utilisons une plateforme professionnelle qui suit en temps réel les actions de chaque participant.
*   **Journalisation et Audit (Logs)** : Chaque tentative de flag, chaque jeton soumis (même erroné) et chaque interaction est enregistrée avec horodatage et adresse IP. En cas de comportement suspect, nous pouvons reconstituer l'historique complet d'un participant.
*   **Isolation Technique (Sandboxing)** : Toutes les épreuves se déroulent sur un serveur dédié. Les participants n'attaquent jamais le réseau de l'établissement. Les cibles sont confinées dans des conteneurs isolés (Docker) et étanches.

## 4. Règles du Jeu et Dispositifs Anti-Triche

Pour garantir l'équité et la sécurité, des règles strictes sont imposées :

### A. Interdictions formelles (Sanctionnées par exclusion) :
1.  **Partage de Flags** : Il est strictement interdit de donner la solution à une autre équipe. La plateforme détecte les flags soumis trop rapidement entre deux comptes différents.
2.  **Attaque de l'Infrastructure** : Les participants doivent attaquer les "cibles" désignées, et non la plateforme de score elle-même ou les ordinateurs de leurs camarades.
3.  **Déni de Service (DoS/DDoS)** : Toute tentative de rendre un service indisponible pour les autres est interdite.
4.  **Usurpation d'Identité** : Se connecter au compte d'un autre élève est proscrit.

### B. Moyens de Détection :
*   **Analyse de corrélation** : Si deux équipes soumettent le même flag difficile en quelques secondes, une alerte est générée.
*   **Surveillance humaine** : Des organisateurs (mentors) circulent pour répondre aux questions et vérifier que les élèves travaillent de manière autonome.

## 5. Charte d'Éthique (À valider par les participants)

Chaque participant s'engage, en s'inscrivant, à respecter la charte du "Hacker Éthique" :
> *"Je m'engage à utiliser les connaissances acquises durant ce CTF uniquement dans un but pédagogique et légal. Je comprends que toute utilisation malveillante de ces techniques en dehors de l'environnement du CTF est passible de sanctions disciplinaires et de poursuites judiciaires."*

---

**Conclusion**

Le Digital Day CTF est un exercice d'excellence qui transforme la curiosité technique en compétence professionnelle. Grâce à l'isolation des systèmes et à la surveillance constante, le risque pour l'infrastructure de l'établissement est nul, et l'intégrité de la compétition est garantie par nos outils de monitoring.

*L'équipe d'organisation du Digital Day.*
