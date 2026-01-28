git init

git status

git add . // git add NAME

git commit -m "Commit"

git remote add origin 190.us.to

git push -u origin main

###################################

git switch -c Branch2 //Erstellt und wechselt zu Branch2

git add .

git commit -m "..."

git push -u origin Branch2 //Pusht diese Branch ins origin

###################################

git switch main

git pull

git merge Branch2

git push

##################################
Bei vorhandener Branch:

git fetch

git branch -a //schaut nach aktuellen Branch und zeigt diese an

git switch -c spellfix origin/spellfix //Erstellt Branch zum bearbeiten

//dann wie oben add, commit, push etc

---
Wenn direkt mergen:
git switch main

git merge origin/spellfix

git push
