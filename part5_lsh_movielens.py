from collections import defaultdict
from itertools import combinations
import random


# Loading dataset

user_movies = defaultdict(set)

with open("data/u.data", "r") as f:
    for line in f:
        user_id, movie_id, rating, _ = line.strip().split("\t")
        if int(rating) >= 4:
            user_movies[int(user_id)].add(int(movie_id))
print("Total users:", len(user_movies))


# Computing exact Jaccard (across all pairs)

def jaccard(a, b):
    return len(a & b) / len(a | b)

exact_sim = {}
for u1, u2 in combinations(user_movies.keys(), 2):
    exact_sim[(u1, u2)] = jaccard(user_movies[u1], user_movies[u2])

# Prepare integer universe. Converting movie sets into integer domain required for hash functions

all_movies = set()
for movies in user_movies.values():
    all_movies.update(movies)
movie_to_id = {movie: idx for idx, movie in enumerate(all_movies)}
user_movie_ids = {}
for user, movies in user_movies.items():
    user_movie_ids[user] = {movie_to_id[m] for m in movies}


# Generating compact signature representation to approximate Jaccard similarity. Each hash function simulates a random permutation of the universe.

def generate_hash_functions(t, m):
    hash_functions = []
    for _ in range(t):
        a = random.randint(1, m-1)
        b = random.randint(0, m-1)
        hash_functions.append((a, b))
    return hash_functions

def minhash_signature(doc_ids, hash_functions, m):
    signature = []
    for a, b in hash_functions:
        min_hash = min(((a*x + b) % m) for x in doc_ids)
        signature.append(min_hash)
    return signature

# Generate candidate pairs by hashing signature bands into buckets. Two users become candidates if they match in at least one band
def lsh(signatures, r, b):
    buckets = defaultdict(list)
    for user, sig in signatures.items():
        for band in range(b):
            start = band * r
            end = start + r
            band_tuple = tuple(sig[start:end])
            buckets[(band, hash(band_tuple))].append(user)
    candidate_pairs = set()
    for bucket_users in buckets.values():
        if len(bucket_users) > 1:
            for pair in combinations(bucket_users, 2):
                candidate_pairs.add(tuple(sorted(pair)))
    return candidate_pairs

# Computing false positives and false negatives against exact Jaccard ground truth.
m = 10007
experiments = [(50, 5, 10),(100, 5, 20),(200, 5, 40), (200, 10, 20)]

for threshold in [0.6, 0.8]:
    print("\n===============================")
    print("Threshold =", threshold)
    print("===============================")
    for t, r, b in experiments:
        print(f"\n t={t}, r={r}, b={b}")
        fp_total = 0
        fn_total = 0
        for run in range(5):
            hash_functions = generate_hash_functions(t, m)
            signatures = {}
            for user, movies in user_movie_ids.items():
                signatures[user] = minhash_signature(movies, hash_functions, m)
            candidate_pairs = lsh(signatures, r, b)
            # True pairs for this threshold
            true_pairs = set(
                pair for pair, sim in exact_sim.items()
                if sim >= threshold
            )
            false_positives = len(candidate_pairs - true_pairs)
            false_negatives = len(true_pairs - candidate_pairs)
            fp_total += false_positives
            fn_total += false_negatives
        print("Average False Positives:", fp_total / 5)
        print("Average False Negatives:", fn_total / 5)