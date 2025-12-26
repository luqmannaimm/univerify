## Univerify Application

### Running the Application

To start the Univerify app:

```sh
python univerify.py
```

By default, this uses the splay tree. To specify which tree to use:

Splay:
```sh
python univerify.py --tree splay
```

BST:
```sh
python univerify.py --tree bst
```

You can also specify a custom data directory:

```sh
python univerify.py --data-dir mydata/
```

### Benchmarking
To compare the performance of splay and BST, use the benchmark script:

```sh
python .\benchmark.py --n-values 100 250 500 750 --trials 5 --searches 1000 --mode all --out-dir benchmarks_all
```

- `--n` sets the number of documents to insert and search (default: 1000)
- `--searches` sets the number of search operations (default: 1000)
- `--out` sets the output PNG file for the bar chart

The script prints the average insert and search time (in microseconds per operation) for both trees, and saves a bar chart with the results in the /benchmarks folder.