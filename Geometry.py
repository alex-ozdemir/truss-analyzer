from Vector import Vector

def distFromPointToLine(p, p1, p2):
        line = Vector(p2) - Vector(p1)
        toP = Vector(p) - Vector(p1)
        dot = toP.dot(line)
        if 0 <= dot <= line.length ** 2:
                projection = toP.proj(line)
                rejection = toP - projection
                return rejection.length
        else:
                return min(toP.length, (Vector(p) - Vector(p2)).length)
