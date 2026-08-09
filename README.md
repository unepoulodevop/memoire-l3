# Mémoire L3 — Infrastructure résiliente

Conception d'une infrastructure résiliente : haute disponibilité et continuité des données.

## Structure du dépôt

- `vagrant/` — Couche 1 : provisionnement des 3 VMs (VirtualBox + Vagrant)
- `ansible/` — Couche 1 : configuration des nœuds (inventory, rôles, playbooks)
- `k3s/` — Couche 2 : charts Helm et manifests Kubernetes (orchestration, réplication MySQL)
- `backup/` — Couche 3 : sauvegarde (mysqldump) et restauration (Velero)
- `.github/workflows/` — Socle transversal : pipeline CI/CD (GitHub Actions, self-hosted runner)

## Architecture

- 1 nœud maître (control plane) : 192.168.56.10
- 2 nœuds workers : 192.168.56.11, 192.168.56.12
- Sous-réseau privé : 192.168.56.0/24
- Hôte : 8 Go RAM

## Déploiement

```
vagrant up
```

Vagrant provisionne les 3 VMs puis invoque Ansible pour la configuration logicielle.
