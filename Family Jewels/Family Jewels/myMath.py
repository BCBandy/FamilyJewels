import math

# For finding point on line, returns u
def get_u(dx, dy):
    return [dx/math.sqrt(dx**2 + dy**2), dy/math.sqrt(dx**2 + dy**2)]

