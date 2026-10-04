import bpy
import math

R = 1.0

def grab(name, parent=None):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
    host = bpy.context.scene.collection if parent is None else parent
    if col.name not in [c.name for c in host.children]:
        host.children.link(col)
    return col

def wipe_ours():
    for col in list(bpy.data.collections):
        if col.name == "PISCES_FLOWER" or col.name.startswith("FOL_"):
            for obj in list(col.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(col)

def ink(name, rgb, strength):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = None
    for node in mat.node_tree.nodes:
        if node.type == "BSDF_PRINCIPLED":
            bsdf = node
            break
    if bsdf is None:
        bsdf = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    else:
        bsdf.inputs["Emission"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs["Emission Strength"].default_value = strength
    bsdf.inputs["Roughness"].default_value = 0.35
    return mat

def poly(name, col, pts, mat, bevel, cyclic):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = bevel
    spline = curve.splines.new("POLY")
    spline.points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        spline.points[i].co = (p[0], p[1], p[2], 1.0)
    spline.use_cyclic_u = cyclic
    obj = bpy.data.objects.new(name, curve)
    col.objects.link(obj)
    obj.data.materials.append(mat)
    return obj

def circle(name, col, cx, cy, cz, radius, mat, bevel):
    pts = []
    steps = 96
    i = 0
    while i < steps:
        a = (i / float(steps)) * math.tau
        pts.append((cx + math.cos(a) * radius, cy + math.sin(a) * radius, cz))
        i += 1
    return poly(name, col, pts, mat, bevel, True)

def segment(name, col, a, b, mat):
    return poly(name, col, [a, b], mat, 0.006, False)

def hex_centers(max_ring, radius):
    pts = []
    q = -max_ring
    while q <= max_ring:
        rv = -max_ring
        while rv <= max_ring:
            s = -q - rv
            if max(abs(q), abs(rv), abs(s)) <= max_ring:
                x = radius * (q + rv * 0.5)
                y = radius * (rv * math.sqrt(3) / 2.0)
                pts.append((x, y))
            rv += 1
        q += 1
    return pts

def main():
    wipe_ours()
    root = grab("PISCES_FLOWER")
    pisces = grab("FOL_PISCES", root)
    flower = grab("FOL_FLOWER", root)
    disc = grab("FOL_DISC", root)
    pink = ink("FOL_Pink", (0.95, 0.62, 0.75), 1.3)
    gold = ink("FOL_Gold", (0.95, 0.82, 0.2), 1.1)
    white = ink("FOL_White", (0.92, 0.92, 0.92), 0.8)

    segment("Rule_Top", pisces, (-3.4, 2.15, 0.0), (3.4, 2.15, 0.0), pink)
    segment("Rule_Mid", pisces, (-3.4, 0.0, 0.0), (3.4, 0.0, 0.0), pink)
    segment("Rule_Bot", pisces, (-3.4, -2.15, 0.0), (3.4, -2.15, 0.0), pink)

    upper = [
        (-1.15, 0.72, 0.72),
        (1.15, 0.72, 0.72),
        (-0.55, 1.25, 0.40),
        (0.55, 1.25, 0.40),
        (0.0, 0.62, 0.32),
        (0.0, 0.95, 0.22),
        (0.0, 1.22, 0.14),
        (0.0, 1.42, 0.08),
        (-0.35, 0.85, 0.18),
        (0.35, 0.85, 0.18),
    ]
    i = 0
    for x, y, rad in upper:
        circle("FishU_%d" % i, pisces, x, y, 0.0, rad, pink, 0.012)
        circle("FishD_%d" % i, pisces, x, -y, 0.0, rad, pink, 0.012)
        i += 1

    centers = hex_centers(2, R)
    i = 0
    for x, y in centers:
        obj = circle("Flower_%d" % i, flower, x, y, 0.0, R, gold, 0.008)
        obj.location.x += 6.2
        i += 1

    seed = hex_centers(1, R)
    n = 0
    i = 0
    while i < len(seed):
        x1, y1 = seed[i]
        j = i + 1
        while j < len(seed):
            x2, y2 = seed[j]
            ln = segment("Meta_%d" % n, flower, (x1, y1, 0.0), (x2, y2, 0.0), white)
            ln.location.x += 6.2
            n += 1
            j += 1
        i += 1

    ring = 0
    while ring < 5:
        rad = 1.15 / (1.0 + 0.55 * ring)
        count = 1 if ring == 0 else 6 * ring
        k = 0
        while k < count:
            ang = (k / float(count)) * math.tau
            if ring == 0:
                cx = 0.0
                cy = 0.0
            else:
                cx = math.cos(ang) * ring * rad * 1.15
                cy = math.sin(ang) * ring * rad * 1.15
            obj = circle("Disc_%d_%d" % (ring, k), disc, cx, cy, 0.0, rad, gold, 0.006)
            obj.location.x += 12.4
            k += 1
        ring += 1

    scene = bpy.context.scene
    if scene.world is None:
        scene.world = bpy.data.worlds.new("PiscesWorld")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.02, 0.02, 0.022, 1.0)
        bg.inputs[1].default_value = 0.15
    print("PISCES_FLOWER built. Pisces at origin, flower x+6.2, disc x+12.4")

if __name__ == "__main__":
    main()
