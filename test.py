import numpy as np
import matplotlib.pyplot as plt

def read_file(file):
    with open(file, 'rb') as file:
        layers = int.from_bytes(file.read(4), byteorder='little')
        n = int.from_bytes(file.read(4), byteorder='little')
        m = int.from_bytes(file.read(4), byteorder='little')

        matrices = np.fromfile(file, dtype=np.float32)

    return np.reshape(matrices, (layers, n, m))

def write_matrices(name, matrices):
    # Sample data
    layers = matrices.shape[0]
    n = matrices.shape[1]
    m = matrices.shape[2]

    # Writing data to a binary file
    with open(name, 'wb') as file:
        # Writing integers
        file.write(layers.to_bytes(4, byteorder='little'))  # Assuming 4 bytes for an integer
        file.write(n.to_bytes(4, byteorder='little'))
        file.write(m.to_bytes(4, byteorder='little'))

        # Writing NumPy array as binary data
        matrices.tofile(file)

"""
input:
    matrices (layers x n x m): numpy array of matrices
output:
    count (dictionary): the frequency of each value in all the matrices
"""
def get_frequniques(matrices):
    count = dict()
    for i in range(matrices.shape[0]):
        for j in range(matrices.shape[1]):
            for k in range(matrices.shape[2]):
                x = matrices[i][j][k]
                if x not in count.keys():
                    count[x] = 0
                count[x] += 1
    return count

def get_freqpairs(matrices):
    pairs = 0
    count = dict()
    for layer in range(matrices.shape[0]):
        for i in range(matrices.shape[1]):
            for j in range(matrices.shape[2] - 1):
                pair = [matrices[layer][i][j], matrices[layer][i][j + 1]]
                if str(pair) not in count.keys():
                    count[str(pair)] = 0
                count[str(pair)] += 1
    return (pairs, count)


"""
input:
    name (string): the name of the type where the matrices come
    matrices (layers x n x m): numpy array of matrices
    k (integer): just for information for unique values at least k frequent
    data_file (boolean): true if you want to write the data for latex, false if not
    unique (boolean): true if you want to show information of unique values, false if not
    pairs (boolean): true if you want to show information of unique pairs, false if not
output:
    None, shows a lot of information only
"""
def graph_information(name, matrices, k=100, data_file=True, unique =True, pairs =True):
    print(f"--- {name} ---")
    name_file = name.replace(".", "-").replace("_", "-")
    print(f"Layer: {matrices.shape[0]}")
    print(f"Matrix size: {matrices.shape[1]}, {matrices.shape[2]}")

    # plot unique values frequencies
    if unique:
        unique = get_frequniques(matrices)
        print(f"Unique values: {len(unique.keys())}")
        if data_file:
            file = open(f"{name_file}-unique-values", "w")
            for x, y in unique.items():
                file.write(f"{x} {y}\n")
            file.close()
        print(f"all unique values:")
        plt.scatter(x = unique.keys(), y = unique.values(), s = 2)
        plt.show()
        k = 100
        print(f"Unique values where freq[x] > {k} {len([key for key in unique.keys() if unique[key] >= k])}")
        plt.scatter(x = [key for key in unique.keys() if unique[key] >= k],
                    y = [value for value in unique.values() if value >= k], s = 2)
        plt.show()
        if data_file:
            file = open(f"{name_file}-unique-values-{k}", "w")
            for x, y in [(key, value) for key, value in unique.items() if value >= k]:
                file.write(f"{x} {y}\n")
            file.close()
        
    # plot info unique pairs
    if pairs:
        amount_pair, unique_pairs = get_freqpairs(matrices)
        print(f"Amount of pairs: {amount_pair}")
        print(f"Amount of unique pairs: {amount_unique_pair}")
