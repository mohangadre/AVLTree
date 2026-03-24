import csv
import os
import time
import tracemalloc
import urllib.request
import zipfile
from collections import Counter
from bst import BSTree
from avltree import AVLTree


def get_movielens():
    url = "https://files.grouplens.org/datasets/movielens/ml-25m.zip"
    zip_name = "ml-25m.zip"
    folder_name = "ml-25m"
    ratings_path = os.path.join(folder_name, "ratings.csv")

    if os.path.exists(ratings_path):
        return ratings_path
    urllib.request.urlretrieve(url, zip_name)

    with zipfile.ZipFile(zip_name, "r") as zip_ref:
        zip_ref.extractall()

    return ratings_path


def loadIDs(path, limit=None):
    ids = set()
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids.add(int(row["movieId"]))
            if limit and len(ids) >= limit:
                break
    return list(ids)

def height(tree):
    return tree.get_height(tree.root)

def build_tree(tree, values, name):
    tracemalloc.start()
    start = time.perf_counter()

    if name == "AVL":
        tree.reset_rotation_counts()

    for value in values:
        tree.root = tree.insert(tree.root, value)

    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    h = height(tree)
    print(
        f"{name} tree: {tree.node_count} nodes, height {h}, "
        f"built in {elapsed:.6f} s (memory: {peak} bytes)."
    )
    if name == "AVL":
        print(f"Rotations during build, by type: {dict(tree.rotation_counts)}")

def run_op(tree, name, op, value):
    before = Counter()
    if name == "AVL":
        before = tree.rotation_counts.copy()

    tracemalloc.start()
    start = time.perf_counter()

    result = None
    if op == "search":
        result = tree.search(tree.root, value)
    elif op == "insert":
        tree.root = tree.insert(tree.root, value)
    elif op == "delete":
        tree.root = tree.delete(tree.root, value)

    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"{name} {op}: value={value} | time={elapsed:.6f}s | memory={peak} bytes")

    if op == "search":
        print("found" if result else "not found")

    if name == "AVL":
        after = tree.rotation_counts
        diff = {}
        for k in set(before) | set(after):
            diff[k] = after[k] - before[k]
        print(f"rotations this op={diff}")

def menu(avl, bst):
    while True:
        print("\n1 AVL search   2 AVL insert   3 AVL delete")
        print("4 BST search   5 BST insert   6 BST delete")
        print("0 exit")

        choice = input("choice: ").strip()

        if choice == "0":
            break


        if choice not in {"1", "2", "3", "4", "5", "6"}:
            print("invalid choice")
            continue

        try:
            value = int(input("movieId: ").strip())
        except ValueError:
            print("enter an integer")
            continue

        if choice == "1":
            run_op(avl, "AVL", "search", value)
        elif choice == "2":
            run_op(avl, "AVL", "insert", value)
        elif choice == "3":
            run_op(avl, "AVL", "delete", value)
        elif choice == "4":
            run_op(bst, "BST", "search", value)
        elif choice == "5":
            run_op(bst, "BST", "insert", value)
        elif choice == "6":
            run_op(bst, "BST", "delete", value)

def main():
    path = get_movielens()
    print(f"Using dataset: {path}")

    limit_text = input("Limit movieIds (press Enter for all): ").strip()
    limit = int(limit_text) if limit_text else None

    movie_ids = loadIDs(path, limit)
    print(f"loaded {len(movie_ids)} movieIds")

    avl = AVLTree()
    bst = BSTree()

    build_tree(avl, movie_ids, "AVL")
    build_tree(bst, movie_ids, "BST")

    menu(avl, bst)

if __name__ == "__main__":
    main()
