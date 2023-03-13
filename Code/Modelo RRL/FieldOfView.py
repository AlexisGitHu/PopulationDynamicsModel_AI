import operator

# Field of View
def fov(pos, dire, dist):
    fov = []
    dif = tuple(map(operator.sub, dire, pos))

    rev = dif[::-1]
    for i in range(dist):
        pos = tuple(map(operator.add, pos, dif))
        fov.append(pos)
        if dif[0] == 0 or dif[1] == 0:
            for j in range(1, i + 1):
                y = tuple([k * j for k in rev])
                fov.append(tuple(map(operator.sub, pos, y)))
                fov.append(tuple(map(operator.add, pos, y)))
        else:
            for j in reversed(range(1, i + 1)):
                fov.append((pos[0] - dif[0] * j, pos[1]))
                fov.append((pos[0], pos[1] - dif[1] * j))

    return fov

fov((0,0), (1,1), 5)