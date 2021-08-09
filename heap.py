"""
Heap Data Structure

Writing my own implementation of heap with the following requirements:

1. It should be able to function as both a min and a max heap.
2. The min or max heap property can't be changed once initialized.
3. Items are stored as key: value pairs.
4. The heap is sorted based on the values.
5. Allows for deletion of a key: value pair given the key.
6. Performance guarantees:
    a. Heapify              ~ O(n)
    b. Extract min / max    ~ O(log(n))
    c. Insert               ~ O(log(n))
    d. Delete               ~ O(log(n))
"""

