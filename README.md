# Order Book (using multithreading)

"""
On my system, it takes nearly 25 to 30 seconds to compute the given test case
The DeleteOrder() takes O(1) time whereas the AddOrder takes O(log n) time
Hence, the total time complexity for taking up the queries takes O(n * log n) time

Also, I have used multithreading for processing the order flow.
For the given testcase, the number of threads is simply 3 which is the total number
of orderbooks used. So, basically for each orderbook a thread is being used and 
each thread works independently without affecting the other threads, as for a particular
thread number the data in the other orderbooks is not affected. Hence, data consistency 
is maintained throughout the process.
"""
