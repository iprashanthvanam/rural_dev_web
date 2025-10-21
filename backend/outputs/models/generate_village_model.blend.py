
import bpy
import math
import random
from mathutils import Vector

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Add a ground plane with varied texture
bpy.ops.mesh.primitive_plane_add(size=20, enter_editmode=False, align='WORLD', location=(0, 0, 0))
ground = bpy.context.object
ground.scale = (10, 10, 1)
ground.name = "Ground"
mat_ground = bpy.data.materials.new(name="GroundMaterial")
mat_ground.use_nodes = True
bsdf = mat_ground.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.2, 0.6, 0.2, 1)  # Lush green
bsdf.inputs['Roughness'].default_value = 0.8
ground.data.materials.append(mat_ground)

# Define village area
area_scale = 5.0

# Create curved unpaved roads
bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, align='WORLD', location=(0, 0, 0.01))
curve = bpy.context.object
curve.name = "MainRoad"
bpy.ops.curve.select_all(action='SELECT')
bpy.ops.curve.delete(type='VERT')
points = [
    (-area_scale/2, -area_scale/2, 0),
    (-area_scale/4, 0, 0),
    (0, area_scale/4, 0),
    (area_scale/2, area_scale/2, 0)
]
for i, point in enumerate(points):
    bpy.ops.curve.vertex_add()
    curve.data.splines[0].bezier_points[i].co = point
    curve.data.splines[0].bezier_points[i].handle_left_type = 'AUTO'
    curve.data.splines[0].bezier_points[i].handle_right_type = 'AUTO'
bpy.ops.object.mode_set(mode='OBJECT')
curve.data.dimensions = '3D'
curve.data.extrude = 0.15
mat_road = bpy.data.materials.new(name="RoadMaterial")
mat_road.use_nodes = True
bsdf_road = mat_road.node_tree.nodes["Principled BSDF"]
bsdf_road.inputs['Base Color'].default_value = (0.5, 0.4, 0.3, 1)  # Dirt brown
bsdf_road.inputs['Roughness'].default_value = 0.9
curve.data.materials.append(mat_road)

# Secondary road
bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, align='WORLD', location=(0, 0, 0.01))
curve2 = bpy.context.object
curve2.name = "SecondaryRoad"
bpy.ops.curve.select_all(action='SELECT')
bpy.ops.curve.delete(type='VERT')
points2 = [
    (-area_scale/3, -area_scale/3, 0),
    (0, -area_scale/2, 0),
    (area_scale/3, -area_scale/3, 0)
]
for i, point in enumerate(points2):
    bpy.ops.curve.vertex_add()
    curve2.data.splines[0].bezier_points[i].co = point
    curve2.data.splines[0].bezier_points[i].handle_left_type = 'AUTO'
    curve2.data.splines[0].bezier_points[i].handle_right_type = 'AUTO'
bpy.ops.object.mode_set(mode='OBJECT')
curve2.data.dimensions = '3D'
curve2.data.extrude = 0.15
curve2.data.materials.append(mat_road)

# Add houses with solar panels
num_houses = min(600, 20)
house_size = 0.3
houses_placed = 0
for idx in range(min(num_houses, 20)):
    t = idx / 19
    curve_to_use = curve if idx % 2 == 0 else curve2
    point = curve_to_use.data.splines[0].bezier_points[0].co.lerp(curve_to_use.data.splines[0].bezier_points[-1].co, t)
    offset = random.choice([-0.4, 0.4])
    direction = (curve_to_use.data.splines[0].bezier_points[-1].co - curve_to_use.data.splines[0].bezier_points[0].co).normalized()
    perpendicular = Vector((-direction.y, direction.x, 0))
    x = point.x + perpendicular.x * offset
    y = point.y + perpendicular.y * offset
    too_close = False
    for obj in bpy.data.objects:
        if "House" in obj.name:
            dist = ((obj.location.x - x) ** 2 + (obj.location.y - y) ** 2) ** 0.5
            if dist < house_size * 2.5:
                too_close = True
                break
    if not too_close and houses_placed < 20:
        # House base
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x, y, house_size / 2))
        house = bpy.context.object
        house.scale = (house_size, house_size, house_size * 0.6)
        house.name = "House_" + str(idx)
        mat_house = bpy.data.materials.new(name="HouseMaterial_" + str(idx))
        mat_house.use_nodes = True
        bsdf_house = mat_house.node_tree.nodes["Principled BSDF"]
        bsdf_house.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1)  # White houses
        bsdf_house.inputs['Roughness'].default_value = 0.5
        house.data.materials.append(mat_house)
        # Slanted roof with solar panels
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x, y, house_size * 0.8))
        roof = bpy.context.object
        roof.scale = (house_size * 0.8, house_size * 0.8, 0.05)
        roof.rotation_euler = (math.radians(15), 0, 0)
        roof.name = "Roof_" + str(idx)
        mat_solar = bpy.data.materials.new(name="SolarMaterial_" + str(idx))
        mat_solar.use_nodes = True
        bsdf_solar = mat_solar.node_tree.nodes["Principled BSDF"]
        bsdf_solar.inputs['Base Color'].default_value = (0.1, 0.1, 0.3, 1)
        bsdf_solar.inputs['Metallic'].default_value = 0.8
        bsdf_solar.inputs['Roughness'].default_value = 0.2
        roof.data.materials.append(mat_solar)
        # Label
        bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(x, y, house_size + 0.1))
        text = bpy.context.object
        text.data.body = "House"
        text.scale = (0.05, 0.05, 0.05)
        houses_placed += 1

# Add small utility sheds
for idx in range(3):
    x = random.uniform(-area_scale/2, area_scale/2)
    y = random.uniform(-area_scale/2, area_scale/2)
    too_close = False
    for obj in bpy.data.objects:
        if "House" in obj.name or "Road" in obj.name:
            dist = ((obj.location.x - x) ** 2 + (obj.location.y - y) ** 2) ** 0.5
            if dist < 0.6:
                too_close = True
                break
    if not too_close:
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x, y, 0.15))
        shed = bpy.context.object
        shed.scale = (0.2, 0.2, 0.3)
        shed.name = "Shed_" + str(idx)
        mat_shed = bpy.data.materials.new(name="ShedMaterial_" + str(idx))
        mat_shed.use_nodes = True
        bsdf_shed = mat_shed.node_tree.nodes["Principled BSDF"]
        bsdf_shed.inputs['Base Color'].default_value = (0.6, 0.4, 0.2, 1)
        shed.data.materials.append(mat_shed)

# Add greenery (trees with varied sizes)
num_trees = max(min(1, 40), 20)
for idx in range(min(num_trees, 40)):
    x = random.uniform(-area_scale/2, area_scale/2)
    y = random.uniform(-area_scale/2, area_scale/2)
    tree_scale = random.uniform(0.8, 1.2)
    too_close = False
    for obj in bpy.data.objects:
        if "House" in obj.name or "Road" in obj.name:
            dist = ((obj.location.x - x) ** 2 + (obj.location.y - y) ** 2) ** 0.5
            if dist < 0.6:
                too_close = True
                break
    if not too_close:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05 * tree_scale, depth=0.5 * tree_scale, enter_editmode=False, align='WORLD', location=(x, y, 0.25 * tree_scale))
        trunk = bpy.context.object
        trunk.name = "Trunk_" + str(idx)
        mat_trunk = bpy.data.materials.new(name="TrunkMaterial_" + str(idx))
        mat_trunk.use_nodes = True
        bsdf_trunk = mat_trunk.node_tree.nodes["Principled BSDF"]
        bsdf_trunk.inputs['Base Color'].default_value = (0.5, 0.3, 0.2, 1)
        bsdf_trunk.inputs['Roughness'].default_value = 0.7
        trunk.data.materials.append(mat_trunk)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3 * tree_scale, enter_editmode=False, align='WORLD', location=(x, y, 0.75 * tree_scale))
        foliage = bpy.context.object
        foliage.name = "Foliage_" + str(idx)
        mat_foliage = bpy.data.materials.new(name="FoliageMaterial_" + str(idx))
        mat_foliage.use_nodes = True
        bsdf_foliage = mat_foliage.node_tree.nodes["Principled BSDF"]
        bsdf_foliage.inputs['Base Color'].default_value = (0.1, 0.5, 0.1, 1)
        bsdf_foliage.inputs['Roughness'].default_value = 0.8
        foliage.data.materials.append(mat_foliage)

# Add small rocks
for idx in range(10):
    x = random.uniform(-area_scale/2, area_scale/2)
    y = random.uniform(-area_scale/2, area_scale/2)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, enter_editmode=False, align='WORLD', location=(x, y, 0.05))
    rock = bpy.context.object
    rock.name = "Rock_" + str(idx)
    mat_rock = bpy.data.materials.new(name="RockMaterial_" + str(idx))
    mat_rock.use_nodes = True
    bsdf_rock = mat_rock.node_tree.nodes["Principled BSDF"]
    bsdf_rock.inputs['Base Color'].default_value = (0.4, 0.4, 0.4, 1)
    rock.data.materials.append(mat_rock)

# Add development elements with labels
element_size = 0.4

# School
if 0 == 0:
    school_x = area_scale/3
    school_y = -area_scale/3
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(school_x, school_y, element_size / 2))
    school = bpy.context.object
    school.scale = (element_size * 1.5, element_size, element_size)
    school.name = "School"
    mat_school = bpy.data.materials.new(name="SchoolMaterial")
    mat_school.use_nodes = True
    bsdf_school = mat_school.node_tree.nodes["Principled BSDF"]
    bsdf_school.inputs['Base Color'].default_value = (0.2, 0.6, 0.8, 1)
    bsdf_school.inputs['Roughness'].default_value = 0.6
    school.data.materials.append(mat_school)
    # Label
    bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(school_x, school_y, element_size + 0.1))
    text = bpy.context.object
    text.data.body = "School"
    text.scale = (0.05, 0.05, 0.05)

# Park with benches
if 0 == 0:
    park_x = 0
    park_y = area_scale/2
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(park_x, park_y, 0.01))
    park = bpy.context.object
    park.scale = (element_size * 2, element_size * 2, 1)
    park.name = "Park"
    mat_park = bpy.data.materials.new(name="ParkMaterial")
    mat_park.use_nodes = True
    bsdf_park = mat_park.node_tree.nodes["Principled BSDF"]
    bsdf_park.inputs['Base Color'].default_value = (0.1, 0.5, 0.1, 1)
    bsdf_park.inputs['Roughness'].default_value = 0.9
    park.data.materials.append(mat_park)
    # Benches
    for i in range(3):
        bench_x = park_x + (i - 1) * 0.5
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(bench_x, park_y, 0.05))
        bench = bpy.context.object
        bench.scale = (0.2, 0.1, 0.05)
        bench.name = "Bench_" + str(i)
        mat_bench = bpy.data.materials.new(name="BenchMaterial_" + str(i))
        mat_bench.use_nodes = True
        bsdf_bench = mat_bench.node_tree.nodes["Principled BSDF"]
        bsdf_bench.inputs['Base Color'].default_value = (0.5, 0.3, 0.2, 1)
        bench.data.materials.append(mat_bench)
        # Label for first bench
        if i == 0:
            bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(bench_x, park_y, 0.2))
            text = bpy.context.object
            text.data.body = "Bench"
            text.scale = (0.05, 0.05, 0.05)

# Small water body
if 0 == 0:
    lake_x = area_scale/2
    lake_y = area_scale/3
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(lake_x, lake_y, 0.01))
    lake = bpy.context.object
    lake.scale = (element_size * 1, element_size * 1, 1)
    lake.name = "WaterBody"
    mat_lake = bpy.data.materials.new(name="WaterMaterial")
    mat_lake.use_nodes = True
    bsdf_lake = mat_lake.node_tree.nodes["Principled BSDF"]
    bsdf_lake.inputs['Base Color'].default_value = (0.1, 0.5, 0.8, 1)
    bsdf_lake.inputs['Roughness'].default_value = 0.2
    lake.data.materials.append(mat_lake)
    # Label
    bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(lake_x, lake_y, 0.2))
    text = bpy.context.object
    text.data.body = "Water Body"
    text.scale = (0.05, 0.05, 0.05)

# Playground with swings and slides
if 0 == 0:
    play_x = -area_scale/3
    play_y = 0
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(play_x, play_y, 0.01))
    play = bpy.context.object
    play.scale = (element_size * 1.5, element_size * 1.5, 1)
    play.name = "Playground"
    mat_play = bpy.data.materials.new(name="PlaygroundMaterial")
    mat_play.use_nodes = True
    bsdf_play = mat_play.node_tree.nodes["Principled BSDF"]
    bsdf_play.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1)
    play.data.materials.append(mat_play)
    # Swing
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(play_x - 0.2, play_y, 0.1))
    swing = bpy.context.object
    swing.scale = (0.05, 0.1, 0.2)
    mat_swing = bpy.data.materials.new(name="SwingMaterial")
    mat_swing.use_nodes = True
    bsdf_swing = mat_swing.node_tree.nodes["Principled BSDF"]
    bsdf_swing.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1)
    swing.data.materials.append(mat_swing)
    # Slide
    bpy.ops.mesh.primitive_cone_add(radius1=0.1, radius2=0.05, depth=0.3, enter_editmode=False, align='WORLD', location=(play_x + 0.2, play_y, 0.15))
    slide = bpy.context.object
    slide.rotation_euler = (math.radians(30), 0, 0)
    mat_slide = bpy.data.materials.new(name="SlideMaterial")
    mat_slide.use_nodes = True
    bsdf_slide = mat_slide.node_tree.nodes["Principled BSDF"]
    bsdf_slide.inputs['Base Color'].default_value = (1, 0.8, 0, 1)
    slide.data.materials.append(mat_slide)
    # Label
    bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(play_x, play_y, 0.3))
    text = bpy.context.object
    text.data.body = "Playground"
    text.scale = (0.05, 0.05, 0.05)

# Street Lighting
if not False:
    for idx in range(5):
        t = idx / 4
        point = curve.data.splines[0].bezier_points[0].co.lerp(curve.data.splines[0].bezier_points[-1].co, t)
        x = point.x
        y = point.y
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=1.0, enter_editmode=False, align='WORLD', location=(x, y, 0.5))
        light = bpy.context.object
        light.name = "StreetLight_" + str(idx)
        mat_light = bpy.data.materials.new(name="LightMaterial_" + str(idx))
        mat_light.use_nodes = True
        bsdf_light = mat_light.node_tree.nodes["Principled BSDF"]
        bsdf_light.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1)
        light.data.materials.append(mat_light)
        # Label for first light
        if idx == 0:
            bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(x, y, 1.0))
            text = bpy.context.object
            text.data.body = "Street Light"
            text.scale = (0.05, 0.05, 0.05)

# Add lighting
bpy.ops.object.light_add(type='SUN', align='WORLD', location=(10, 10, 10))
sun = bpy.context.object
sun.data.energy = 3
sun.rotation_euler = (math.radians(45), 0, math.radians(45))

# Set up world shader with sky
world = bpy.context.scene.world
world.use_nodes = True
bg_node = world.node_tree.nodes.new(type='ShaderNodeBackground')
bg_node.inputs['Color'].default_value = (0.6, 0.8, 1.0, 1)  # Soft blue sky
bg_node.inputs['Strength'].default_value = 0.8
output_node = world.node_tree.nodes.get('World Output')
world.node_tree.links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])

# Set up camera
bpy.ops.object.camera_add(enter_editmode=False, align='WORLD', location=(-4, -4, 3))
camera = bpy.context.object
camera.rotation_euler = (math.radians(70), 0, math.radians(-45))  # Lower angled view
camera.data.clip_end = 2000
bpy.context.scene.camera = camera
print(f"Camera location: {camera.location}, Rotation: {camera.rotation_euler}".format(camera=camera))

# Debug: Print object locations
for obj in bpy.data.objects:
    print(f"Object {obj.name} at location {obj.location}".format(obj=obj))

# Set up render settings
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.eevee.use_shadows = True
bpy.context.scene.eevee.taa_render_samples = 5000
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = "C:/Users/prash/Desktop/rural dev cmd/backend/outputs/models/73_3d_model.png"
bpy.context.scene.render.film_transparent = False

# Render the scene
bpy.ops.render.render(write_still=True)
