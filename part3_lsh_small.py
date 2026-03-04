# PART 3 - LSH on small documents

def read_file(filename):
    with open(f"minhash/{filename}", "r") as f:
        return f.read().strip()

d1 = read_file("D1.txt")
d2 = read_file("D2.txt")
d3 = read_file("D3.txt")
d4 = read_file("D4.txt")

def char_kgrams(text, k):
    grams = set()
    for i in range(len(text) - k + 1):
        grams.add(text[i:i+k])
    return grams

# Use only 3-grams
d1_3 = char_kgrams(d1, 3)
d2_3 = char_kgrams(d2, 3)
d3_3 = char_kgrams(d3, 3)
d4_3 = char_kgrams(d4, 3)

def jaccard(a, b):
    return len(a & b) / len(a | b)

docs = {
    "D1": d1_3,
    "D2": d2_3,
    "D3": d3_3,
    "D4": d4_3
}
from itertools import combinations

print("Exact Jaccard Similarities (3-grams)")
print("--------------------------------------")
exact_sims = {}
for (doc1, doc2) in combinations(docs.keys(), 2):
    sim = jaccard(docs[doc1], docs[doc2])
    exact_sims[(doc1, doc2)] = sim
    print(f"{doc1}-{doc2}: {sim:.4f}")

#Choosing r and b
# We know t = r*b and its given t=160. so common choices will be (r = 4, b = 40), (r = 5, b = 32) , (r = 8, b = 20), (r = 10, b = 16)
# We need s-curve to sharply rise near τ = .7 . τ is approximatly equal to (1/b)^(1/r)
# if b=40 and r=4 then τ = (1/40)^(1/4) approx .7; so we choose b=40 and r=4
import math
def lsh_probability(s, r, b):
    return 1 - (1 - s**r)**b
r = 4
b = 40
print("\nLSH Candidate Probability (r=4, b=40)")
print("---------------------------------------")
for pair, sim in exact_sims.items():
    prob = lsh_probability(sim, r, b)
    print(f"{pair[0]}-{pair[1]}: {prob:.4f}")

r = 8
b = 20
print("\nLSH Candidate Probability (r=8, b=20)")
print("---------------------------------------")
for pair, sim in exact_sims.items():
    prob = lsh_probability(sim, r, b)
    print(f"{pair[0]}-{pair[1]}: {prob:.4f}")