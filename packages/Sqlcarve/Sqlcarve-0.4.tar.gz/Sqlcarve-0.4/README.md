# sqlcarve
[![PyPI](https://img.shields.io/pypi/v/sqlcarve)](https://pypi.python.org/pypi/sqlvalidator/)
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)

SQL Parser for Teachers


# SQL Validation and execution

__fichier.sql__ est le fichier à valider.
__ref_stmnt__ est la requête de référence pour la validation sémantique.
__referencefile.json__ est le modèle de commentaire pour la validation des commentaires.
    

__Exemple de referencefile.json__
```json
{
  "profcomments": {
    "auteur": "",
    "objectif": "",
    "documentation": ""
  },
  "studentcomments": {
    "author": "",
    "cip": "",
    "objectif": ""
  }
}
```


__Exemple d'utilisation__
```python
from src.sqlcarve.validator.validator import *

valid = Validator()
report = {}
with open("fichier.sql", "r") as f_content:
    statement_list = Preprocessor.extract_stmnts(f_content)

    for stmnt in statement_list:
        report = valid.validate(statement=stmnt, ref_statement=ref_stmnt, ref_comments="referencefile.json", type="all")

print(report)
```

__Résultat__

```
    {'commentaires': [], 'syntax': 'Validation syntaxique réussie', 'semantique': 'Validation sémantique réussie'}
```