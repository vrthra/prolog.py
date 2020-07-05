# prolog.py

A simple (and dumb) prolog DSL in Python. Translated from [tiny_prolog.rb](https://codezine.jp/article/detail/461). To execute the examples in libs.py:

```shell
$ python3 libs.py 
membership[
[[member(1 (1 2 3))]]
[[member(3 (1 2 3))]]
[]
]
append[
[[append(None (1 2) (1 2))]]
[[append((1 2 3) (4) (1 2 3 4))]]
[[append((1 2 3) (4 5) (1 2 3 4 5))]]
[[append((1 2 3) (4 5) (1 2 3 4 5))]]
]
reverse[
[[reverse((1 2 3 4 5) (5 4 3 2 1))]]
]
takeout[
[[takeout(1 (1 2 3) (2 3))], [takeout(2 (1 2 3) (1 3))], [takeout(3 (1 2 3) (1 2))]]
]
subset[
[[subset((4 3) (2 3 5 4))]]
[[subset((2) (2 3 5 4))], [subset((3) (2 3 5 4))], [subset((5) (2 3 5 4))], [subset((4) (2 3 5 4))]]
]
mergesort[
[[mergesort((4 3 6 5 9 1 7) (1 3 4 5 6 7 9))]]
]
[[number((1 2))]]
expr[
[[expr((1 + 2 - 3) plus((1) minus((2) (3))))]]
]
dcg[
[[dcgnum((1 2 3) (2 3))]]
[[rcons((+ 1 2 3) + (1 2 3))]]
[[dcgexpr((1 + 2 - 3) (+ 2 - 3))], [dcgexpr((1 + 2 - 3) (- 3))], [dcgexpr((1 + 2 - 3) None)]]
[[dcgexprcomplete((1 - 2 + 3))]]
]
```
