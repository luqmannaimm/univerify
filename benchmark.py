"""Simple benchmark: compare splay vs avl for a single n, print and plot results."""
import time
import random
import argparse
import matplotlib.pyplot as plt
from univerify import Document
from trees.splay import Tree as SplayTree
from trees.avl import Tree as AVLTree

def run(tree_cls, n, searches):
    """Run benchmark for given tree class, n inserts and searches"""

    # Generate documents
    ids = random.sample(range(1, 10*n), n)
    docs = [Document(i, f"A{i}", "pdf") for i in ids]
    
    # Insert documents
    tree = tree_cls()
    t0 = time.perf_counter()
    for d in docs:
        tree.insert(d)
    t1 = time.perf_counter()
    insert_time = t1 - t0
    
    # Search documents
    search_keys = [random.choice(ids) for _ in range(searches)]
    t0 = time.perf_counter()
    for k in search_keys:
        tree.search(k)
    t1 = time.perf_counter()
    search_time = t1 - t0

    # Convert to microseconds per op
    return (insert_time / n) * 1e6, (search_time / searches) * 1e6

def main():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=1000, help='Number of inserts/searches')
    parser.add_argument('--searches', type=int, default=1000, help='Number of searches')
    parser.add_argument('--out', default='benchmarks/benchmark.png', help='Output PNG file')
    args = parser.parse_args()

    # Benchmark splay vs avl
    print(f"Running with n={args.n}, searches={args.searches}")
    splay_insert, splay_search = run(SplayTree, args.n, args.searches)
    avl_insert, avl_search = run(AVLTree, args.n, args.searches)
    print(f"Splay: avg insert {splay_insert:.2f}μs, avg search {splay_search:.2f}μs")
    print(f"AVL:  avg insert {avl_insert:.2f}μs, avg search {avl_search:.2f}μs")

    # Plot figures
    labels = ['Insert', 'Search']
    splay_vals = [splay_insert, splay_search]
    avl_vals = [avl_insert, avl_search]
    x = [0, 1]
    width = 0.35
    plt.figure(figsize=(6,4))
    splay_bars = plt.bar([i - width/2 for i in x], splay_vals, width, label='splay')
    avl_bars = plt.bar([i + width/2 for i in x], avl_vals, width, label='avl')
    plt.xticks(x, labels)
    plt.ylabel('avg time (μs/op)')
    plt.title(f'Insert/Search time (μs, n={args.n})')
    plt.legend()

    # Annotate each bar with its value
    for bars, vals in zip([splay_bars, avl_bars], [splay_vals, avl_vals]):
        for bar, val in zip(bars, vals):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{val:.0f}',
                     ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(args.out)
    print(f"Bar chart saved to {args.out}")

if __name__ == '__main__':
    main()
