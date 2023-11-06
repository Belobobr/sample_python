# Options

## storage
caching + transformation:
depends on frequency/volume/cost(computation)
3 options
- in_memory
- separated shared in memory cache
- database cache

## cache strategy:
-cache-aside
-read-through
-write-through
-e.t.c

# Input

frequence => high
volume => low (111 records)
computation => low (linear and nlogn time)

# Solution

## Storage
let's use in_memory cache, because it requires just a few mb, there is not need in separate caching layer or in partitioning
## Strategy
let's use cache-aside

# Observability

