# Hook-based retrieval library

## Current State

- Been moving code from exploration to usable with a proper interface where we can run benchmarks.
- The code is in a pretty solid place, but there is still a lot that could be done. 
- The first thing to do is to get EC2-based benchmarking code working. Be able to run a benchmark with the new codebase.
   - Requirements:
      - Calculate effective throughput
      - Track CPU/Memory/Network usage and store it in an easily parseable format


- Did some benchmarking. `Retriever` uses way more CPU power. It also is much faster when bumping up the concurrency - on an m5n.2xlarge, getting about 11 gbit/s download speed, compared with 2 for `download_file`.
- Saw much faster download speed when moving into the same region as the s3 bucket (curl -sI https://noaa-goes16.s3.amazonaws.com | grep bucket-region). About double the speed.
- Probably more performance available with VPC endpoints - https://aws.amazon.com/premiumsupport/knowledge-center/s3-transfer-data-bucket-instance/
- The background profiler is quite good, but need to port it into the actor system, probably add some additional profiled, and decide on a serialization schema so it can be loaded. Eventually will want to graph memory usage, cpu usage, and network throughput over time for various download approachs.
- Want to do performance benchmarks across different instance types and configurations. Need to sweep various config values to tune params. Want to be able to write doc showing that performance is much better when using `Retriever` if you're willing to pay the mem/cpu cost.
- `ec2-cluster` would be useful. But that project is a little rusty so it's a good time to improve it a bit - better UX, automatically determine more params like VPC id, subnet, keypair location, etc.
- Would be nice to be able to combine actors and `ec2-cluster` to parallelize benchmarking.
- Haven't defined the hooks yet.
- Currently actors get references to other actors at creation time. Better to use a global registry (for extensibility), but need to manually overwrite the actor URNs since the current approach is UUIDs and not very usable.
- The `ParallelChunkDownloader` actor implementation could be cleaner I think. 

## Stages of downloading a file from s3

```
1. init
    - Process pools, s3 clients, etc
2. file list collection
1. file start downloading
    - Check if cache is available, etc
1. chunk task generation
1. fan_out
    - Parallelize downloading of chunks across processes/threads
1. fan_in
    - Send chunks back to master thread and reorder
1. post_download
1. done
```



# Retriever Architecture

The architecture is made up of multiple pipeline stages. Each stage should inputs in through a queue and send data out through a queue. 

1. Retriever is the interface to the overall pipeline
2. FileListGenerator takes in a DownloadRequest, finds the files that match, and outputs FileDownloadRequests. [parallel - for HEAD requests]
    - The FileDownloadRequests each contain the location on s3, the size of the file (and plugin specific information?)
3. FileChunker splits up FileDownloadRequests into ChunkGetTasks, batching multiple FileDownloadRequests [serial, although it needs info from chunk sequencer about progress somehow]
   - Should only parallelize a few FileDownloadRequests at the same time. Should have a limit on WIP ChunkGetTasks so that batching is based on size of files.
4. ParallelChunkDownloader takes in ChunkGetTasks and distributes it to workers. The downloaded chunks are outputted (not in order) [parallel]
5. ChunkSequencer takes in Chunks and outputs in-order chunks [serial]
6. On top of the in-order chunks, we will have different consumption methods depending on the use case.
   - Load into memory
   - Save into file
   - Load into memory and save into file
   - Iterator of chunks [easiest initial option]
   - Iterator of files?

The final user-facing abstraction should be an iterator.

## Pipeline Stages

Each stage should take in an queue and send data out through a queue. What is the execution model for Pipeline stages - actor-like?

Stages will usually want to have background thread/processes to process data as quickly as it comes in. 

How does fan-out/fan-in work? How do we expose a unified callback API when some stages are serial and some are parallelized. Do we change the Pipeline abstraction to unify it (each fan-out is composed of many stages running with the same input and output pipes? or every pipeline stage has fan-in and fan-out?). For now, we will make callbacks custom instead of being automatic features of pipeline stages.

## Hooks

TODO: Define the relevant user-facing hooks. Will also put developer-focused hooks all over the place

Probably two types of hooks - Class hooks that are stateful and functional hooks that are pure. Pipeline stages that are parallel can only use functional hooks (although maybe give the functional hook access to queues?).

## Communication channels



## Reference

Optimizing s3 performance with request parallelization - https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html#optimizing-performance-parallelization

Several existing projects referenced in this thread - https://news.ycombinator.com/item?id=26764067. Good stuff and some impressive projects.



