---
type: regex
target: { source: file, path: hero.html }
pattern: 'trusted by|\d[\d,.]*\s*k?\+\s*(teams|customers|users|freelancers|businesses)'
flags: i
match: not_contains
---
