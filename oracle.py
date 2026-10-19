#!/usr/bin/env python3
# Kin Math oracle - mirrors engine.js. Relationships come from walking a built family line (ancestor chain and descendant chain), ancestor counts by doubling a list of people.
import json, re, random

GEN_ERR = "each generation count must be a whole number from 0 to 30"
ANC_ERR = "the generation must be a whole number from 1 to 30"
YEAR_ERR = "the birth year must be a whole number from 1 to 2100"
PER_ERR = "the years per generation must be a whole number from 1 to 60"

def num(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,4}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def pl(n, a, b): return f"{n} {a if n == 1 else b}"
def ordn(n):
    if n % 100 in (11, 12, 13): return f"{n}th"
    return f"{n}{ {1:'st',2:'nd',3:'rd'}.get(n % 10, 'th') }"
def great(n): return "great-" if n == 1 else ordn(n) + " great-"

def kin(up, down):
    a = num(up, GEN_ERR, 0, 30); b = num(down, GEN_ERR, 0, 30)
    head = f"Counting {pl(a,'generation','generations')} up from you and {pl(b,'generation','generations')} up from them to the shared ancestor: "
    # Build the line: you are at depth a below the ancestor, they are at depth b below the ancestor.
    you, them = a, b
    if you == 0 and them == 0: return head + "you and them are the same person."
    if you == 0:
        base = {1: "child", 2: "grandchild"}.get(them) or great(them - 2) + "grandchild"
        return head + f"they are your {base}."
    if them == 0:
        base = {1: "parent", 2: "grandparent"}.get(you) or great(you - 2) + "grandparent"
        return head + f"they are your {base}."
    if you == 1 and them == 1: return head + "they are your sibling, full or half, which these counts cannot tell apart."
    if you == 1:
        base = {2: "niece or nephew", 3: "great-niece or great-nephew"}.get(them) or ordn(them - 2) + " great-niece or great-nephew"
        return head + f"they are your {base}."
    if them == 1:
        base = {2: "aunt or uncle", 3: "great-aunt or great-uncle"}.get(you) or ordn(you - 2) + " great-aunt or great-uncle"
        return head + f"they are your {base}."
    shared = min(you, them)   # the closer line reaches the ancestor in this many steps; the cousin degree is one less
    degree = shared - 1
    removed = max(you, them) - shared
    c = f"{ordn(degree)} cousin"
    if removed == 0: return head + f"they are your {c}, in the same generation as you."
    word = {1: "once removed", 2: "twice removed"}.get(removed, f"{removed} times removed")
    side = "older" if them < you else "younger"
    return head + f"they are your {c} {word}, {pl(removed,'generation','generations')} {side} than you."

def anc(gen):
    g = num(gen, ANC_ERR, 1, 30)
    gens = []; cur = 1
    for _ in range(g):
        cur *= 2; gens.append(cur)
    name = "parents" if g == 1 else "grandparents" if g == 2 else great(g - 2) + "grandparents"
    return f"Generation {g} back ({name}): at most {gens[-1]} ancestors in that generation and {sum(gens)} counting every generation up to it, if no ancestor is counted twice."
def era(by, gen, yrs):
    y = num(by, YEAR_ERR, 1, 2100); g = num(gen, ANC_ERR, 1, 30); p = num(yrs, PER_ERR, 1, 60)
    r = y
    for _ in range(g): r -= p
    if r < 1: raise ValueError("that count of generations would reach before the year 1")
    return f"Counting {pl(g,'generation','generations')} back at {pl(p,'year','years')} each from a birth in {y} reaches the year {r}, {pl(y-r,'year','years')} earlier."

FNS = {"kinTruth": kin, "ancestorTruth": lambda a: anc(a), "eraTruth": era}

def cases():
    c = []; rnd = random.Random(698)
    for a in range(0, 8):
        for b in range(0, 8): c.append(("kinTruth", [str(a), str(b)]))
    for a in [["30","30"],["30","0"],["0","30"],["30","1"],["1","30"],["11","11"],["12","3"],["13","2"],["21","22"],["23","3"],["31","1"],["1","31"],["-1","1"],["1","x"],["","1"],["1.5","1"],[" 3 "," 2 "],["03","02"],["10000","1"]]:
        c.append(("kinTruth", a))
    for _ in range(20): c.append(("kinTruth", [str(rnd.randint(0,30)), str(rnd.randint(0,30))]))
    for g in list(range(1, 15)) + [20, 21, 22, 23, 30]: c.append(("ancestorTruth", [str(g)]))
    for a in ["0","31","x","","1.5"," 3 ","-2"]: c.append(("ancestorTruth", [a]))
    for a in [["1990","5","25"],["1990","1","1"],["1990","30","60"],["2100","30","60"],["1","1","1"],["1","1","2"],["1800","30","60"],["1800","29","60"],["1800","30","61"],["2025","3","30"],["0","3","30"],["2101","3","30"],["1990","0","25"],["1990","5","0"],["x","5","25"],["1990","","25"]," 1990 ,5,25".split(",")]:
        c.append(("eraTruth", a))
    for _ in range(15): c.append(("eraTruth", [str(rnd.randint(1500,2100)), str(rnd.randint(1,30)), str(rnd.randint(1,60))]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](args if fn != "ancestorTruth" else args[0]) if fn == "ancestorTruth" else (FNS[fn](*args))
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1); f.write("\n")
print(len(out), "cases written")
