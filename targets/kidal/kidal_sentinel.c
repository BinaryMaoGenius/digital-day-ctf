#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void secret_archive() {
    printf("[SUCCÈS] Accès aux archives de Kidal accordé.\n");
    printf("FLAG: flag{anti_debug_kidal_mountain_bypass}\n");
    exit(0);
}

void validate_key(char *key) {
    char buffer[64];
    // Vulnérabilité : Dépassement de tampon classique via strcpy
    strcpy(buffer, key);
    
    if (strcmp(buffer, "KIDAL-2024-PROTECT") == 0) {
        printf("[OK] Clé de session valide.\n");
    } else {
        printf("[ERREUR] Clé invalide. Accès refusé.\n");
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <session_key>\n", argv[0]);
        return 1;
    }
    
    printf("--- SENTINELLE DES MONTAGNES : MODULE DE SÉCURITÉ ---\n");
    validate_key(argv[1]);
    
    return 0;
}
