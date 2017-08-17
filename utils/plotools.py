def plot_boundary(boundary):
    data = [[boundary[i], boundary[(i + 1) % len(boundary)]] for i in range(len(boundary))]
    path = []
    for d in data:
        path.append((d[0][0], d[1][0]))
        path.append((d[0][1], d[1][1]))
        path.append('b')
    return path
