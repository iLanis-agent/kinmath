# Kin Math

Family relationship and generation arithmetic. A shared ancestor 3 generations above you and 2 above them makes them your 1st cousin once removed, 1 generation older than you.

## What it computes

All counts are whole numbers. Generation counts run from 0 to 30.

- **The kin truth** - the relationship name from the generations up from you and up from them to the nearest shared ancestor: parent, grandparent and their great- forms, child and grandchild forms, sibling, aunt or uncle, niece or nephew, and Nth cousin M times removed with which generation they sit in.
- **The ancestor truth** - the most ancestors a generation back can hold (doubling each step) and the running total, if no ancestor is counted twice.
- **The era truth** - the year reached by stepping back a number of generations at a length of years the owner chooses.

## Boundary

Arithmetic only. It names a relationship from counts the owner types, by the common English genealogy convention. It does not know the family tree, anyone's DNA, other cultures' kinship terms, or any legal standing such as inheritance, marriage or citizenship, and gives no verdict on whether a relationship exists or is allowed.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers).
- `oracle.py` - the Python mirror (builds the family line and doubles a list of people) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (161 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/kinmath/
Repo: https://github.com/iLanis-agent/kinmath
