# stupid_GPU_monitor
A stupid script to monitor GPU memory usage


## Why I want to create this?
I started training a DNN model with Torch last night, and it crashed at some time. But I don't know when did it crash. So I wrote this script to monitor the GPU memory usage for me, if the memory usage if too low, it will send me an email so I can know.


## Requirement

- NVIDIA Management Library (of course you need this)

- nvidia-ml-py (A python binding, you can install it with `pip`)


## How to use

`python check_gpu.py --GPU [GPU_ID] --receiver [email address]`

Check the code to see more arguments.


## Note

Some email service provide might block emails from unknown source. But at least I tested with Gmail and it is fine.
