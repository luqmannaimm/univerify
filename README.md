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

AVL:
```sh
python univerify.py --tree avl
```

You can also specify a custom data directory:

```sh
python univerify.py --data-dir mydata/
```

### Benchmarking Splay vs AVL
To compare the performance of splay and AVL trees, use the benchmark script:

```sh
python benchmark.py --n-values 1000 10000 25000 50000 --trials 5 --searches 1000 --out-dir benchmarks
```

- `--n` sets the number of documents to insert and search (default: 1000)
- `--searches` sets the number of search operations (default: 1000)
- `--out` sets the output PNG file for the bar chart

The script prints the average insert and search time (in microseconds per operation) for both trees, and saves a bar chart with the results in the /benchmarks folder.