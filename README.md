# Sorting Algorithm Performance Analysis – Assignment 1

**Submitted by:** Eitan Karp, Oren Avishid

**Course:** Data Structures 

## Project Overview
In this assignment, we implemented and compared three sorting algorithms to evaluate their efficiency under different conditions. The experiments focus on the differences between comparison-based algorithms with varying time complexities and the impact of data structure (fully random vs. nearly sorted) on execution time.

### Selected Algorithms
The following three algorithms were chosen for this analysis:
* **Insertion Sort (ID 3):** A simple sorting algorithm with a time complexity of $O(n^2)$ in average and worst cases.
* **Merge Sort (ID 4):** A "divide and conquer" algorithm that guarantees a time complexity of $O(n \log n)$ in all cases.
* **Quick Sort (ID 5):** An efficient algorithm with an average complexity of $O(n \log n)$. Our implementation uses a middle-element pivot strategy to optimize performance.

---

## Results Analysis – Part B: Random Arrays

**TODO: Add image**

As shown in the `result1.png` plot, there is a massive disparity between the growth rates of these algorithms:
* **Merge Sort & Quick Sort:** Both exhibit a near-linear (log-linear) growth rate, demonstrating high efficiency even as the array size reaches 250,000 elements.
* **Insertion Sort:** Shows a clear quadratic curve. Even at relatively small sizes, its execution time escalates drastically compared to the more advanced algorithms.

### Array Size Limit for Insertion Sort
In our code, we chose to skip Insertion Sort for arrays larger than **10,000** elements. This decision was made due to the algorithm's $O(n^2)$ complexity. In such an algorithm, doubling the input size results in a fourfold increase in execution time, making tests on very large arrays impractical for a single execution run.

#### Theoretical Runtime Estimation
We can estimate how long Insertion Sort would have taken to sort 250,000 elements based on the results measured for 10,000 elements. 
If for $n_1 = 10,000$ the runtime is $T_1$, then for $n_2 = 250,000$ (a ratio of 25x), the estimated time $T_2$ would be:
$$T_2 = T_1 \times (25^2) = T_1 \times 625$$

**Calculation based on experimental results:**
* Average time measured for 10,000 elements ($T_1$): **[Fill in the mean time from your terminal output]** seconds.
* Estimated time for 250,000 elements: **[Fill in the result]** seconds (approx. **[Fill in]** minutes).

---

## Results Analysis – Part C: Nearly Sorted Arrays (20% Noise)

**TODO: Add image**

In this experiment, we tested the impact of partial order on performance:
* **Insertion Sort:** There is a noticeable improvement in performance compared to the random test. In "nearly sorted" scenarios, the number of required swaps is significantly lower, which highlights the algorithm's sensitivity to initial data order. However, it still remains significantly slower than Merge and Quick Sort.
* **Merge Sort:** Execution time remained stable and nearly identical to the first experiment. This is expected, as Merge Sort performs the same division and merging operations regardless of the initial order of elements.
* **Quick Sort:** Continued to show the best overall performance, leveraging the partially sorted structure of the array to maintain efficient partitioning.

---

## How to Run the Experiments

The program includes a Command Line Interface (CLI) to configure experiment parameters.

**Command to run the experiment with 20% noise (as shown in result2):**
```bash
python run_experiments.py -s 100 1000 5000 10000 50000 100000 250000 -e 2 -r 5
