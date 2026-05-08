# Maak orphan branch (zonder geschiedenis)
git checkout --orphan versie-0.1

# Add alle bestanden
git add .

# Commit alles
git commit -m "versie 0.1"

# Tag de commit
git tag -a v0.1 -m "Release versie 0.1"

# Vervang main branch
git branch -D main
git branch -m main

# Force push
git push origin main --force
git push origin v0.1