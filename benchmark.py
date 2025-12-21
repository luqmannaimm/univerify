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
    parser.add_argument('--n-values', nargs='+', type=int,
                        default=[1000, 10000, 25000, 50000],
                        help='List of n sizes to test')
    parser.add_argument('--trials', type=int, default=5, help='Number of trials per n')
    parser.add_argument('--searches', type=int, default=1000, help='Number of searches per trial')
    parser.add_argument('--out-dir', default='benchmarks', help='Output directory for charts')
    args = parser.parse_args()

    n_values = args.n_values
    trials = args.trials
    searches = args.searches
    out_dir = args.out_dir

    import os
    os.makedirs(out_dir, exist_ok=True)

    # Store aggregated results: dict[n] -> lists of trial results
    results = {}
    for n in n_values:
        print(f"Running n={n} with {trials} trials (searches={searches})...")
        splay_inserts = []
        splay_searches = []
        avl_inserts = []
        avl_searches = []
        for t in range(trials):
            # seed for reproducibility across trials
            random.seed(1000 + t)
            si, ss = run(SplayTree, n, searches)
            ai, as_ = run(AVLTree, n, searches)
            splay_inserts.append(si)
            splay_searches.append(ss)
            avl_inserts.append(ai)
            avl_searches.append(as_)
            print(f"  trial {t+1}: splay_insert={si:.1f}μs splay_search={ss:.1f}μs | avl_insert={ai:.1f}μs avl_search={as_:.1f}μs")
        results[n] = {
            'splay_inserts': splay_inserts,
            'splay_searches': splay_searches,
            'avl_inserts': avl_inserts,
            'avl_searches': avl_searches,
        }

        # For each n, plot per-run bars for insert and search (x=run, bars=AVL/Splay)
        import statistics
        run_ids = [str(i+1) for i in range(trials)]
        x = range(trials)
        width = 0.35
        # Insert times per run
        plt.figure(figsize=(6,6))
        s_bars = plt.bar([i - width/2 for i in x], splay_inserts, width, label='splay')
        a_bars = plt.bar([i + width/2 for i in x], avl_inserts, width, label='avl')
        plt.xticks(x, run_ids)
        plt.xlabel('Run')
        plt.ylabel('avg insert time (μs/op)')
        plt.title(f'Insert times per run (n={n})')
        plt.legend()
        for i, v in enumerate(splay_inserts):
            plt.text(i - width/2, v, f'{v:.0f}', ha='center', va='bottom')
        for i, v in enumerate(avl_inserts):
            plt.text(i + width/2, v, f'{v:.0f}', ha='center', va='bottom')
        fn = os.path.join(out_dir, f'benchmark_n_{n}_inserts.png')
        plt.tight_layout()
        plt.savefig(fn)
        plt.close()
        print(f"  Saved chart {fn}")

        # Search times per run
        plt.figure(figsize=(6,6))
        s_bars = plt.bar([i - width/2 for i in x], splay_searches, width, label='splay')
        a_bars = plt.bar([i + width/2 for i in x], avl_searches, width, label='avl')
        plt.xticks(x, run_ids)
        plt.xlabel('Run')
        plt.ylabel('avg search time (μs/op)')
        plt.title(f'Search times per run (n={n})')
        plt.legend()
        for i, v in enumerate(splay_searches):
            plt.text(i - width/2, v, f'{v:.0f}', ha='center', va='bottom')
        for i, v in enumerate(avl_searches):
            plt.text(i + width/2, v, f'{v:.0f}', ha='center', va='bottom')
        fn = os.path.join(out_dir, f'benchmark_n_{n}_searches.png')
        plt.tight_layout()
        plt.savefig(fn)
        plt.close()
        print(f"  Saved chart {fn}")

    # Trend plot across n_values: grouped bars for inserts and searches
    import statistics
    si_means = [statistics.mean(results[n]['splay_inserts']) for n in n_values]
    ai_means = [statistics.mean(results[n]['avl_inserts']) for n in n_values]
    ss_means = [statistics.mean(results[n]['splay_searches']) for n in n_values]
    as_means = [statistics.mean(results[n]['avl_searches']) for n in n_values]

    # Plot inserts trend as line plot
    x = range(len(n_values))
    plt.figure(figsize=(8,8))
    plt.plot(x, si_means, marker='o', label='splay insert')
    plt.plot(x, ai_means, marker='o', label='avl insert')
    plt.xticks(x, [str(n) for n in n_values])
    plt.xlabel('n')
    plt.ylabel('avg insert time (μs/op)')
    plt.title('Insert time trend')
    plt.legend()
    for i, v in enumerate(si_means):
        plt.text(i, v, f'{v:.0f}', ha='center', va='bottom')
    for i, v in enumerate(ai_means):
        plt.text(i, v, f'{v:.0f}', ha='center', va='bottom')
    fn = os.path.join(out_dir, 'trend_inserts.png')
    plt.tight_layout()
    plt.savefig(fn)
    plt.close()
    print(f"Saved insert trend {fn}")

    # Plot searches trend as line plot
    plt.figure(figsize=(8,8))
    plt.plot(x, ss_means, marker='o', label='splay search')
    plt.plot(x, as_means, marker='o', label='avl search')
    plt.xticks(x, [str(n) for n in n_values])
    plt.xlabel('n')
    plt.ylabel('avg search time (μs/op)')
    plt.title('Search time trend')
    plt.legend()
    for i, v in enumerate(ss_means):
        plt.text(i, v, f'{v:.0f}', ha='center', va='bottom')
    for i, v in enumerate(as_means):
        plt.text(i, v, f'{v:.0f}', ha='center', va='bottom')
    fn = os.path.join(out_dir, 'trend_searches.png')
    plt.tight_layout()
    plt.savefig(fn)
    plt.close()
    print(f"Saved search trend {fn}")

    # Tabulate results as CSV files
    import csv
    insert_csv = os.path.join(out_dir, 'benchmark_inserts.csv')
    search_csv = os.path.join(out_dir, 'benchmark_searches.csv')

    # Write average insert times
    with open(insert_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['n', 'Splay', 'AVL'])
        for i, n in enumerate(n_values):
            writer.writerow([n, f"{si_means[i]:.1f}", f"{ai_means[i]:.1f}"])
    print(f"Saved insert averages to {insert_csv}")

    # Write average search times
    with open(search_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['n', 'Splay', 'AVL'])
        for i, n in enumerate(n_values):
            writer.writerow([n, f"{ss_means[i]:.1f}", f"{as_means[i]:.1f}"])
    print(f"Saved search averages to {search_csv}")

if __name__ == '__main__':
    main()
