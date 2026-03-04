# PART 4 - MinHash on MovieLens

from collections import defaultdict

# Loading dataset
user_movies = defaultdict(set)

with open("data/u.data", "r") as f:
    for line in f:
        user_id, movie_id, rating, _ = line.strip().split("\t")
        
        # Consider rating >= 4 as liked movie
        if int(rating) >= 4:
            user_movies[int(user_id)].add(int(movie_id))

print("Total users:", len(user_movies))

# Exact Jaccard similarity for user 789
target_user = 789

def jaccard(set1, set2):
    if len(set1 | set2) == 0:
        return 0
    return len(set1 & set2) / len(set1 | set2)

max_similarity = 0
most_similar_user = None

for user in user_movies:
    if user == target_user:
        continue
    
    sim = jaccard(user_movies[target_user], user_movies[user])
    
    if sim > max_similarity:
        max_similarity = sim
        most_similar_user = user

print("\nExact Jaccard Results")
print("----------------------")
print("Most similar to user 789:", most_similar_user)
print("Exact similarity:", round(max_similarity, 4))

# Preparing for MinHash
# Creating universe of all movie IDs
all_movies = set()
for movies in user_movies.values():
    all_movies.update(movies)

# Map each movie to integer index
movie_to_id = {movie: idx for idx, movie in enumerate(all_movies)}

# Convert user movie sets to integer sets
user_movie_ids = {}
for user, movies in user_movies.items():
    user_movie_ids[user] = {movie_to_id[m] for m in movies}

print("Total unique movies:", len(all_movies))

import random

def generate_hash_functions(t, m):
    hash_functions = []
    for _ in range(t):
        a = random.randint(1, m - 1)
        b = random.randint(0, m - 1)
        hash_functions.append((a, b))
    return hash_functions

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

def signature_similarity(sig1, sig2):
    count = 0
    for i in range(len(sig1)):
        if sig1[i] == sig2[i]:
            count += 1
    return count / len(sig1)

t = 200
m = 10007  # large prime > number of movies
hash_functions = generate_hash_functions(t, m)

# Compute MinHash signatures for all users
user_signatures = {}

for user, movie_ids in user_movie_ids.items():
    user_signatures[user] = minhash_signature(movie_ids, hash_functions, m)

print("MinHash signatures computed.")
print("\nMinHash Approximation Results")
print("--------------------------------")

target_user = 789
max_sim = 0
approx_most_similar = None
target_sig = user_signatures[target_user]
for user, sig in user_signatures.items():
    if user == target_user:
        continue
    sim = signature_similarity(target_sig, sig)    
    if sim > max_sim:
        max_sim = sim
        approx_most_similar = user

print("Most similar to user 789 (MinHash):", approx_most_similar)
print("Estimated similarity:", round(max_sim, 4))
