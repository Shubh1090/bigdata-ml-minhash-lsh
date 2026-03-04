# 1.For part 2 we will use 3-grams only. Build Minhash signature for D1 & D2
# 2. Test for t = 10, 60, 150, 300, 600
# 3. Estimate the Jaccard Similarity and compare with exact value (≈ 0.9780 from Part 1)

# Reading files
def read_file(filename):
    with open(f"minhash/{filename}", "r") as f:
        return f.read().strip()

d1 = read_file("D1.txt")
d2 = read_file("D2.txt")

# Character 3-grams
def char_kgrams(text, k):
    grams = set()
    for i in range(len(text) - k + 1):
        grams.add(text[i:i+k])
    return grams

d1_3grams = char_kgrams(d1, 3)
d2_3grams = char_kgrams(d2, 3)

# Exact Jaccard (for comparison)
def jaccard(a, b):
    return len(a & b) / len(a | b)

exact_similarity = jaccard(d1_3grams, d2_3grams)
print("PART-2")
print("Exact Jaccard (3-grams):", round(exact_similarity, 4))

# Universe of all 3-grams
all_grams = list(d1_3grams.union(d2_3grams))

# Map each gram to integer
gram_to_id = {gram: idx for idx, gram in enumerate(all_grams)}

# Convert document sets to integer sets
d1_ids = {gram_to_id[g] for g in d1_3grams}
d2_ids = {gram_to_id[g] for g in d2_3grams}
import random

def generate_hash_functions(t, m):
    hash_functions = []
    for _ in range(t):
        a = random.randint(1, m-1)
        b = random.randint(0, m-1)
        hash_functions.append((a, b))
    return hash_functions
m = 10007
# MinHash signature computation
def minhash_signature(doc_ids, hash_functions, m):
    signature = []
    for (a, b) in hash_functions:
        min_hash = float('inf')
        for doc_id in doc_ids:
            hash_value = (a * doc_id + b) % m
            if hash_value < min_hash:
                min_hash = hash_value
        signature.append(min_hash)
    return signature


# Compare two signatures
def signature_similarity(sig1, sig2):
    count = 0
    for i in range(len(sig1)):
        if sig1[i] == sig2[i]:
            count += 1
    return count / len(sig1)
print("\nMinHash Approximation Results")
print("---------------------------------")
print("t\tEstimated Similarity")

for t in [20, 60, 150, 300, 600]:
    hash_funcs = generate_hash_functions(t, m)

    sig1 = minhash_signature(d1_ids, hash_funcs, m)
    sig2 = minhash_signature(d2_ids, hash_funcs, m)

    approx_sim = signature_similarity(sig1, sig2)

    print(f"{t}\t{approx_sim:.4f}")