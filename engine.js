// Kin Math engine: family relationship names from generation counts, ancestor counts and generation spans. Exact integers.
var GEN_ERR = "each generation count must be a whole number from 0 to 30";
var ANC_ERR = "the generation must be a whole number from 1 to 30";
var YEAR_ERR = "the birth year must be a whole number from 1 to 2100";
var PER_ERR = "the years per generation must be a whole number from 1 to 60";

function _int(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,4}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _plural(n, one, many) { return n + " " + (n === 1 ? one : many); }
function _ord(n) {
  var m = n % 100, s = "th";
  if (m < 11 || m > 13) { var d = n % 10; s = d === 1 ? "st" : d === 2 ? "nd" : d === 3 ? "rd" : "th"; }
  return n + s;
}
// n generations beyond the grandparent level: 1 = great-, 2 = 2nd great-, ...
function _great(n) { return n === 1 ? "great-" : _ord(n) + " great-"; }
function _down(b) { return b === 1 ? "child" : b === 2 ? "grandchild" : _great(b - 2) + "grandchild"; }
function _up(a) { return a === 1 ? "parent" : a === 2 ? "grandparent" : _great(a - 2) + "grandparent"; }
function _nibling(b) { return b === 2 ? "niece or nephew" : b === 3 ? "great-niece or great-nephew" : _ord(b - 2) + " great-niece or great-nephew"; }
function _auncle(a) { return a === 2 ? "aunt or uncle" : a === 3 ? "great-aunt or great-uncle" : _ord(a - 2) + " great-aunt or great-uncle"; }

function kinTruth(up, down) {
  var a = _int(up, GEN_ERR, 0, 30), b = _int(down, GEN_ERR, 0, 30);
  var head = "Counting " + _plural(a, "generation", "generations") + " up from you and " + _plural(b, "generation", "generations") + " up from them to the shared ancestor: ";
  if (a === 0 && b === 0) return head + "you and them are the same person.";
  var rel;
  if (a === 0) rel = _down(b);
  else if (b === 0) rel = _up(a);
  else if (a === 1 && b === 1) return head + "they are your sibling, full or half, which these counts cannot tell apart.";
  else if (a === 1) rel = _nibling(b);
  else if (b === 1) rel = _auncle(a);
  else {
    var k = Math.min(a, b) - 1, r = Math.abs(a - b);
    rel = _ord(k) + " cousin";
    if (r === 0) return head + "they are your " + rel + ", in the same generation as you.";
    rel += r === 1 ? " once removed" : r === 2 ? " twice removed" : " " + r + " times removed";
    return head + "they are your " + rel + ", " + _plural(r, "generation", "generations") + (b < a ? " older" : " younger") + " than you.";
  }
  return head + "they are your " + rel + ".";
}
function ancestorTruth(gen) {
  var g = _int(gen, ANC_ERR, 1, 30);
  var name = g === 1 ? "parents" : g === 2 ? "grandparents" : _great(g - 2) + "grandparents";
  var level = Math.pow(2, g), total = Math.pow(2, g + 1) - 2;
  return "Generation " + g + " back (" + name + "): at most " + level + " ancestors in that generation and " + total + " counting every generation up to it, if no ancestor is counted twice.";
}
function eraTruth(birthYear, gen, years) {
  var y = _int(birthYear, YEAR_ERR, 1, 2100), g = _int(gen, ANC_ERR, 1, 30), p = _int(years, PER_ERR, 1, 60);
  var span = g * p, r = y - span;
  if (r < 1) throw new Error("that count of generations would reach before the year 1");
  return "Counting " + _plural(g, "generation", "generations") + " back at " + _plural(p, "year", "years") + " each from a birth in " + y + " reaches the year " + r + ", " + _plural(span, "year", "years") + " earlier.";
}
