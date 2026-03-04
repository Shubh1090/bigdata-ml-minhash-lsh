# reading file from minhash folder
def read_file(filename):
    with open(f"minhash/{filename}", "r", encoding="utf-8") as f:return f.read().strip()

d1 = read_file("D1.txt")
d2 = read_file("D2.txt")
d3 = read_file("D3.txt")
d4 = read_file("D4.txt")

print("D1:", d1)
print("D2:", d2)
print("D3:", d3)
print("D4:", d4)
print("\nDocuments loaded successfully.\n")

#Adding character & word K-grams function
# function to generate character k-grams
def char_kgrams(text, k):
    grams = set()
    for i in range(len(text) - k + 1):
        grams.add(text[i:i+k])
    return grams

# function to generate word k-grams
def word_kgrams(text, k):
    words = text.split()
    grams = set()
    for i in range(len(words) - k + 1):
        grams.add(words[i] + " " + words[i+1])
    return grams

#Generating k-grams for all documents
# Character 2-grams
d1_char2 = char_kgrams(d1, 2)
d2_char2 = char_kgrams(d2, 2)
d3_char2 = char_kgrams(d3, 2)
d4_char2 = char_kgrams(d4, 2)
print("\nCharacter 2-grams count:")
print("D1:", len(d1_char2))
print("D2:", len(d2_char2))
print("D3:", len(d3_char2))
print("D4:", len(d4_char2))
print("\nCharacter 2-grams count (D1,D2,D3,D4):", len(d1_char2)+len(d2_char2)+len(d3_char2)+len(d4_char2))
# Character 3-grams
d1_char3 = char_kgrams(d1, 3)
d2_char3 = char_kgrams(d2, 3)
d3_char3 = char_kgrams(d3, 3)
d4_char3 = char_kgrams(d4, 3)
print("\nCharacter 3-grams count:")
print("D1:", len(d1_char3))
print("D2:", len(d2_char3))
print("D3:", len(d3_char3))
print("D4:", len(d4_char3))
print("Character 3-grams count (D1,D2,D3,D4):", len(d1_char3)+len(d2_char3)+len(d3_char3)+len(d4_char3))
# Word 2-grams
d1_word2 = word_kgrams(d1, 2)
d2_word2 = word_kgrams(d2, 2)
d3_word2 = word_kgrams(d3, 2)
d4_word2 = word_kgrams(d4, 2)
print("\nWord 2-grams count:")
print("D1:", len(d1_word2))
print("D2:", len(d2_word2))
print("D3:", len(d3_word2))
print("D4:", len(d4_word2))
print("Word 2-grams count (D1,D2,D3,D4):", len(d1_word2)+len(d2_word2)+len(d3_word2)+len(d4_word2))


#Computing 18 jaccard similarities
# Jaccard similarity function
def jaccard(set1, set2):
    return len(set1 & set2) / len(set1 | set2)
docs_char2 = {
    "D1": d1_char2, "D2": d2_char2, "D3": d3_char2, "D4": d4_char2
}
docs_char3 = {
    "D1": d1_char3, "D2": d2_char3, "D3": d3_char3, "D4": d4_char3
}
docs_word2 = {
    "D1": d1_word2, "D2": d2_word2, "D3": d3_word2, "D4": d4_word2
}
from itertools import combinations

print("\nPairwise Jaccard Similarities")
print("------------------------------------------------")
print("Pair\tChar-2\tChar-3\tWord-2")
print("------------------------------------------------")

for (doc1, doc2) in combinations(docs_char2.keys(), 2):
    sim_char2 = jaccard(docs_char2[doc1], docs_char2[doc2])
    sim_char3 = jaccard(docs_char3[doc1], docs_char3[doc2])
    sim_word2 = jaccard(docs_word2[doc1], docs_word2[doc2])
    
    print(f"{doc1}-{doc2}\t{sim_char2:.4f}\t{sim_char3:.4f}\t{sim_word2:.4f}")