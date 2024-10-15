import random


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left, right):
    result = []
    i, j = 0, 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def generate_random_array(size):
    return [random.randint(1, 1000) for _ in range(size)]


if __name__ == "__main__":
    # Test the merge sort implementation
    test_arr = generate_random_array(10)
    print("Original array:", test_arr)
    sorted_arr = merge_sort(test_arr)
    print("Sorted array:", sorted_arr)
