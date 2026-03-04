from collections import defaultdict
from itertools import combinations
import random

#Loading MovieLens dataset

user_movies = defaultdict(set)
with open("data/u.data", "r") as f:
    for line in f:
        user_id, movie_id, rating, _ = line.strip().split("\t")
        # Consider rating >= 4 as liked movie
        if int(rating) >= 4:
            user_movies[int(user_id)].add(int(movie_id))
print("Total users:", len(user_movies))

# Computing exact Jaccard for ALL pairs

def jaccard(a, b):
    return len(a & b) / len(a | b)
print("Computing exact Jaccard for all pairs...")
exact_pairs = set()
for u1, u2 in combinations(user_movies.keys(), 2):
    sim = jaccard(user_movies[u1], user_movies[u2])

    if sim >= 0.5:
        exact_pairs.add(tuple(sorted((u1, u2))))
print("Total pairs with similarity ≥ 0.5:", len(exact_pairs))

# Preparing Integer Universe & Creating universe of all movies
all_movies = set()
for movies in user_movies.values():
    all_movies.update(movies)
print("Total unique movies:", len(all_movies))

# Mapping each movie to integer index
movie_to_id = {movie: idx for idx, movie in enumerate(all_movies)}

# Converting user movie sets to integer sets
user_movie_ids = {}
for user, movies in user_movies.items():
    user_movie_ids[user] = {movie_to_id[m] for m in movies}

# MinHash Functions

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

def signature_similarity(sig1, sig2):
    matches = sum(1 for i in range(len(sig1)) if sig1[i] == sig2[i])
    return matches / len(sig1)

# Evaluation Loop

m = 10007  # large prime > number of movies
for t in [50, 100, 200]:
    print("\nEvaluating for t =", t)
    print("=============================")
    fp_total = 0
    fn_total = 0
    for run in range(5):
        print("Run:", run+1)
        hash_functions = generate_hash_functions(t, m)
        signatures = {}
        for user, movies in user_movie_ids.items():
            signatures[user] = minhash_signature(movies, hash_functions, m)
        estimated_pairs = set()
        for u1, u2 in combinations(signatures.keys(), 2):
            sim_est = signature_similarity(signatures[u1], signatures[u2])
            if sim_est >= 0.5:
                estimated_pairs.add(tuple(sorted((u1, u2))))
        # Compute FP and FN
        false_positives = len(estimated_pairs - exact_pairs)
        false_negatives = len(exact_pairs - estimated_pairs)

        fp_total += false_positives
        fn_total += false_negatives
    print("Average False Positives:", fp_total / 5)
    print("Average False Negatives:", fn_total / 5)