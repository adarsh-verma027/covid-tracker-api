arr_count = 0


def print_subsequences(arr, i, subarr, b):
    global arr_count
    if i == len(arr):

        if len(subarr) != 0:
            if len(subarr) == b and sum(subarr) <= 1000:
                arr_count += 1
    else:
        print_subsequences(arr, i + 1, subarr, b)

        print_subsequences(arr, i + 1,
                          subarr + [arr[i]], b)

    return arr_count


arr = [1, 2, 8]
b = 2
result = print_subsequences(arr, 0, [], b)

if result > 0:
    print(result)
else:
    print("No valid subsequence")
