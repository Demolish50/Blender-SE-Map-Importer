import bpy
import bmesh

#Setup our Scene #need to figure out how to set max clip at 200km
bpy.data.scenes['Scene'].unit_settings.system = 'METRIC'
bpy.data.scenes['Scene'].unit_settings.scale_length = 1
bpy.data.worlds["World"].use_sky_blend
bpy.data.worlds["World"].zenith_color[0] = 0
bpy.data.worlds["World"].zenith_color[1] = 0
bpy.data.worlds["World"].zenith_color[2] = 0


#make material functions
def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    mat.use_shadeless = True
    return mat

#Make our Grid and xyz lines  - need to combine createxyz into one function
def creategrid():
       sce = bpy.context.scene
       me = bpy.data.meshes.new("Grid")
       bm = bmesh.new()
       bmesh.ops.create_grid(bm, x_segments=20, y_segments=20, size=50000)
       bmesh.ops.delete(bm, geom=bm.faces, context=3)
       bm.to_mesh(me)
       ob = bpy.data.objects.new("Grid", me)
       sce.objects.link(ob)
       sce.update()
       gridmat = makeMaterial('gridmat', (1,0,0), (1,1,1), 1)
       bpy.data.objects["Grid"].active_material = bpy.data.materials["gridmat"]
       bpy.data.materials["gridmat"].type = 'WIRE'

def createx():
    bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, -0),               layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,         False, False, False, False, False))
    bpy.context.object.scale[0] = 20000
    bpy.context.object.scale[1] = 40
    bpy.context.object.scale[2] = 40
    xmat = makeMaterial('xmat', (1,0,0), (1,1,1), 1)
    bpy.context.object.active_material = bpy.data.materials["xmat"]
    bpy.context.object.data.extrude = 5
    
def createy():
    bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, -0),               layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,         False, False, False, False, False))
    bpy.context.object.scale[0] = 20000
    bpy.context.object.scale[1] = 40
    bpy.context.object.scale[2] = 40
    ymat1 = makeMaterial('ymat1', (0,1,0), (1,1,1), 1)
    bpy.context.object.active_material = bpy.data.materials["ymat1"]
    bpy.context.object.data.extrude = 5
    bpy.context.object.rotation_euler[2] = 1.5708

def createz():
    bpy.ops.curve.primitive_nurbs_path_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, -0),               layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,         False, False, False, False, False))
    bpy.context.object.scale[0] = 20000
    bpy.context.object.scale[1] = 40
    bpy.context.object.scale[2] = 40
    zmat2 = makeMaterial('zmat2', (0,0,1), (1,1,1), 1)
    bpy.context.object.active_material = bpy.data.materials["zmat2"]
    bpy.context.object.data.extrude = 5
    bpy.context.object.rotation_euler[1] = 1.5708

## Read the world and create the roids
def readworld():
    from xml.etree import cElementTree as ElementTree
    
    ElementTree.register_namespace('xsi', 'http://www.w3.org/2001/XMLScheme-instance')
    namespace = {'xsi': 'http://www.w3.org/2001/XMLScheme-instance'} 
    
    xmlPath = 'e:\\test.xml'
    xmlRoot = ElementTree.parse(xmlPath).getroot()
    
    results = xmlRoot.findall(".//SectorObjects/MyObjectBuilder_EntityBase[Filename]")
    try:
        for result in results:
            roidname = result.find('Filename').text
            
            for pos in result.iter('Position'):
                pos = pos.attrib
                posx = pos.get('x')
                posx = float(posx)
                posy = pos.get('y')
                posy = float(posy)
                posz = pos.get('z')
                posz = float(posx)
                #Do the damn thing AKA Asteroid Creation
                createAsteroid(posx,posy,posz,roidname)
                print(posz)
                  
            print(roidname)
                       
    except AttributeError as aE:
        print('no')        
            
   
#Create Asteroids
def createAsteroid(x,y,z,roidname):
       bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
       bpy.data.objects["Icosphere"].name = roidname
       asteroidmat = makeMaterial('asteroidmat', (1,1,0), (1,1,1), 1)
       bpy.data.objects[roidname].active_material = bpy.data.materials["asteroidmat"]
       bpy.data.objects[roidname].scale[0] = 200
       bpy.data.objects[roidname].scale[1] = 200
       bpy.data.objects[roidname].scale[2] = 200
       bpy.data.materials["asteroidmat"].type = 'SURFACE'
       

    

#Program
#createAsteroid(1000,1000,1000,'asteroid2')
creategrid()
createx()
createy()
createz()
readworld()
