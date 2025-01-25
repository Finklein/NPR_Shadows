bl_info = {
    # required
    'name': 'Normal Editing',
    'blender': (3, 2, 0),
    'category': 'Object',
    # optional
    'version': (1, 0, 0),
    'author': 'Sophie Fink',
    'description': 'A normal editing addon',
}


import bpy, bmesh
import mathutils
    
#https://blender.stackexchange.com/questions/141333/how-controll-rgb-node-with-floatvectorproperty-blender-2-8    
PROPS = [('blep', bpy.props.FloatVectorProperty(name='Blep', default = (1.0 , 0.0 , 0.0, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('TObj', bpy.props.PointerProperty(type = bpy.types.Object , name = 'TestEmpty' )),
    
    ('red', bpy.props.FloatVectorProperty(name='Red', default = (1.0 , 0.0 , 0.0, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('RObj', bpy.props.PointerProperty(type = bpy.types.Object , name = 'RedEmpty' )),
    
    ('green', bpy.props.FloatVectorProperty(name='Green', default = (0.0 , 1.0 , 0.0, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('GObj', bpy.props.PointerProperty(type = bpy.types.Object, name = 'GreenEmpty')),
        
    ('blue', bpy.props.FloatVectorProperty(name='Blue', default = (0.0 , 0.0 , 1.0, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('BObj', bpy.props.PointerProperty(type = bpy.types.Object, name = 'BlueEmpty')),
    
    ('cyan', bpy.props.FloatVectorProperty(name='Cyan', default = (0.0 , 1.0 , 1.0, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('CObj', bpy.props.PointerProperty(type = bpy.types.Object, name = 'CyanEmpty')),
    
    ('yellow', bpy.props.FloatVectorProperty(name='Yellow', default = (1.0 , 1.0 , 0.0, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('YObj', bpy.props.PointerProperty(type = bpy.types.Object, name = 'YellowEmpty')),
    
    ('magenta', bpy.props.FloatVectorProperty(name='Magenta', default = (1.0 , 0.0 , 1.0, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('MObj', bpy.props.PointerProperty(type = bpy.types.Object, name = 'MagentaEmpty')),
    
    ('col1', bpy.props.FloatVectorProperty(name='Color 1', default = (0.5 , 0.5 , 0.0, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('C1Obj', bpy.props.PointerProperty(type = bpy.types.Object, name = 'Col1Empty')),
    
    ('col2', bpy.props.FloatVectorProperty(name='Color 2', default = (0.0 , 0.5 , 0.5, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('C2Obj', bpy.props.PointerProperty(type = bpy.types.Object, name = 'Col2Empty')),
    
    ('col3', bpy.props.FloatVectorProperty(name='Color 3', default = (0.5 , 0.0 , 0.5, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('C3Obj', bpy.props.PointerProperty(type = bpy.types.Object, name = 'Col3Empty')),
    
    ('col4', bpy.props.FloatVectorProperty(name='Color 4', default = (1.0 , 0.5 , 0.5, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('C4Obj', bpy.props.PointerProperty(type = bpy.types.Object, name = 'Col4Empty')),
    
    ('col5', bpy.props.FloatVectorProperty(name='Color 5', default = (0.5 , 1.0 , 0.5, 1.0), size=4, min = 0.0, max = 1.0, subtype = 'COLOR_GAMMA')),
    ('C5Obj', bpy.props.PointerProperty(type = bpy.types.Object, name = 'Col5Empty')),
    
    ('ColorL', bpy.props.StringProperty(name = 'Vertex Color Layer', default= 'Col' )),
    
    ('kugel', bpy.props.BoolProperty(name='Spherize YesNo', default = False)),
    ('kuglichkeit', bpy.props.FloatProperty(name='Kuglichkeit', default = 0.0, min = 0.0, max = 1.0)),
    ('inveN', bpy.props.BoolProperty(name='Invert Normals', default = True)),
    ('al', bpy.props.BoolProperty(name='align Normals', default = False)),
    
    ('richtung', bpy.props.FloatVectorProperty(name='Richtung', default = (0.0,0.0,0.0)))
]

class EPanel(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_NormalEditing_panel'
    bl_label = 'NormalEditing Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        self.layout.label(text='Hello World')
        col = self.layout.column()
        for (prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
            
            

        
        col.operator('opr.change_normalscolor_operator', text = 'Select Vertex Color')
#        col.operator('opr.change_normalscolor2_operator', text = 'rotate Normals to Vector')
        col.operator('opr.change_allnormals_operator', text = 'rotate all Normals')
        col.operator('opr.spherize_normals_operator', text = 'Spherize Normals')
        col.operator('opr.resett_normals_operator', text = 'reset Normals')
        


##rotates colored normals towards selected object
class ChangeNormalsByColorOperator(bpy.types.Operator):
    
    bl_idname = 'opr.change_normalscolor_operator'
    bl_label = 'Change Normals by color'
    
    def execute(self, context):
        
        for obj in bpy.context.selected_objects:
            deselct_all()
            select_Vertexcolor(context.scene.blep, context.scene.ColorL)
            #RotateNormals(context.scene.TObj)
        #print(context.scene.blep[0])
        #print(context.scene.blep[1])
        #print(context.scene.blep[2])
        #print(context.scene.blep[3])
            
        return {'FINISHED'} 
 
 
 ##rotates colored normals with given Vector   
#class ChangeNormalsByColorOperator2(bpy.types.Operator):
    
#    bl_idname = 'opr.change_normalscolor2_operator'
#    bl_label = 'Change Normals by color 2'
    
#    def execute(self, context):
#        params = (
            #context.scene.r,
            #context.scene.g,
            #context.scene.b,
            #context.scene.a
#        )
        
#        for obj in bpy.context.selected_objects:
#            deselct_all()
#            RotateNormalsBel(context.scene.richtung, params)
            
#        return {'FINISHED'}
    
    
class ChangeAllNormalsByColorOperator(bpy.types.Operator):
    
    bl_idname = 'opr.change_allnormals_operator'
    bl_label = 'Change all Normals'
    
    def execute(self, context):
        
        colors = (
            context.scene.red,
            context.scene.green,
            context.scene.blue,
            context.scene.cyan,
            context.scene.yellow,
            context.scene.magenta,
            context.scene.col1,
            context.scene.col2,
            context.scene.col3,
            context.scene.col4,
            context.scene.col5
        )
        
        emptyObjects = (
            context.scene.RObj,
            context.scene.GObj,
            context.scene.BObj,
            context.scene.CObj,
            context.scene.YObj,
            context.scene.MObj,
            context.scene.C1Obj,
            context.scene.C2Obj,
            context.scene.C3Obj,
            context.scene.C4Obj,
            context.scene.C5Obj
        )
        
        for obj in bpy.context.selected_objects:
            
            for i in range(0 , 11 , 1):
                try:
                    #print(i)
                    deselct_all()
                    select_Vertexcolor(colors[i], context.scene.ColorL)
                    RotateNormals(emptyObjects[i], context.scene.kuglichkeit, context.scene.inveN, context.scene.al, context.scene.kugel)
                except:
                    print("missing Color or object")
                    print(i)
            
        return {'FINISHED'}        


class ResettNormalsOperator(bpy.types.Operator):
    
    bl_idname = 'opr.resett_normals_operator'
    bl_label = 'Reset Normals'
    
    def execute(self, context):
        ResetNormals()
            
        return {'FINISHED'} 
    
class SpherizeNormalsOperator(bpy.types.Operator):
    
    bl_idname = 'opr.spherize_normals_operator'
    bl_label = 'Spherize Normals'
    
    def execute(self, context):
        deselct_all()
        SpherizeNormals()
            
        return {'FINISHED'} 



CLASSES = [EPanel, ChangeNormalsByColorOperator, ChangeAllNormalsByColorOperator, ResettNormalsOperator, SpherizeNormalsOperator]

def register():
    print('registered')
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    for klass in CLASSES:
        bpy.utils.register_class(klass)
    
        

def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
        
    print('unregistered') # just for debug
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)


if __name__ == '__main__':
    register()
    

#empty = bpy.data.objects["Empty"]


#(r,g,b,alpha)
#red = (1.0, 0.0, 0.0, 1.0)
#green = (0.0, 1.0, 0.0, 1.0)
#blue = (0.0, 0.0, 1.0, 1.0)


def deselct_all():
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.mesh.select_all(action = 'DESELECT')
    
    bpy.ops.object.editmode_toggle()
    

def select_Vertexcolor(color,Vcolor):
    #threshold
    t= 0.01
    #print("up above")
    #print(tuple(map(lambda i, j: i - j, color, (t,t,t))))
    #print("---------------------------------------------------------------------")
    #vertices lists with vertex color red, green or blue
    #print('selected normals')
    vert_r = []
    context = bpy.context
    mesh = context.object.data
    bm = bmesh.new()
    bm.from_mesh(mesh)

    color_layers = bm.loops.layers.color
    #color_layer = color_layers.get("color") or color_layers.new("color")
    
    #vertex color layer in color attributes
    color_layer = color_layers.get(Vcolor)
    #L = len(bm.verts) - 1
    low = tuple(map(lambda i, j: i - j, color, (t,t,t,0.0)))
    up = tuple(map(lambda i, j: i + j, color, (t,t,t,0.0)))
    for face in bm.faces:
        for loop in face.loops:        
            #x = loop.vert.index / L 
            #print("Vert:", loop.vert.index)
            #print(loop[color_layer])
            
            #print("loop color")
            #print(loop[color_layer][:])
            #!!!! der Tupelvergleich ist das Problem, weil die Tupel sortiert werden beim vergelichen und dann stimmt der Vergleich nstuerlich nicht mehr
            #mit slice notation[:] wird der Vektor zu einer Sequenz? um die Werte vergleichen zu koennen https://blender.stackexchange.com/questions/116963/convert-a-mathutils-vector-object-into-3d-coordinates
            if  (low[0] < (loop[color_layer][:])[0] < up[0] and low[1] < (loop[color_layer][:])[1] < up[1] and low[2] < (loop[color_layer][:])[2] < up[2]) :
                
                #print(color)
                #print(tuple(map(lambda i, j: i - j, color, (t,t,t,0.0))))
                ##print(loop[color_layer][:])
                #print(tuple(map(lambda i, j: i + j, color, (t,t,t,0.0))))
                vert_r.append(loop.vert)
            #loop[color_layer] = (x, x, x, 1)

    #print(vert_r)
    #https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    vert_r_noDouble = list(dict.fromkeys(vert_r))
    #print(vert_r_noDouble)
    for b in vert_r_noDouble:
        #print(b)
        b.select = True
    
    bm.to_mesh(mesh)

    
def select_vert_by_dist(DistObj, distance):
    #empty location, sollte spaeter frei gewaehlt werden, nach welchem Objekt sich die Normalen ausrichten

    empty = bpy.data.objects[DistObj.name]
    #print(empty.location)
    ##Muss emptyLoc normalisiert sein? eigentlich ja nicht fuer die Distanz???
    emptyLoc = empty.location.normalized()
    #emptyLoc = empty.location
    #print(emptyLoc)


    obj = bpy.context.object

    vert_list = []

    for v in obj.data.vertices:
        v_local = v.co #local vertex coordinate
        v_global = obj.matrix_world @ v_local #global vertex coordinates
        print("distance:")

        dist = ((obj.matrix_world @ v.co)-emptyLoc).magnitude
        print(dist)

        if dist < distance:
            vert_list.append(v)
    print("vert List:")
    print(vert_list)    
    
    for b in vert_list:
        print(b)
        b.select = True



def RotateNormals(DObj, kuglich, invNormal, alig, kugeli):
    rotateObject = bpy.data.objects[DObj.name]
    #print('rotated normal')
    bpy.ops.object.editmode_toggle()
    #select mode face um harte kanten zu bekommen
    #wenn man faces benutzt bekommt man automatisch split normals an den Kanten der Farbe
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

    #zeigen in die Richtung, aber nicht mit geraden STrahlen, sondern perspektivisch
    #wenn man danach mit smooth vectors darueber geht entstehen nicht ganz zu krasse Treppenstufen
    #bpy.ops.mesh.point_normals(target_location=(empty.location[0], empty.location[1], empty.location[2]))

    #normalen sind parallel ausgerichtet,(so halb bin mir da nicht ganz sicher), zumindest sehr viel weniger perspektivisch als bei Loesung 1
    bpy.ops.mesh.point_normals(invert = invNormal, align= alig, target_location=(rotateObject.location[0], rotateObject.location[1], rotateObject.location[2]), spherize = kugeli, spherize_strength = kuglich)
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
    bpy.ops.object.editmode_toggle()

    #needs to be in object mode to select the vertices in the list, doesn't work otherwise!!!!!!!   
    
def RotateNormals_rotate(DObj):
    rotateObject = bpy.data.objects[DObj.name]
    #print('rotated normal')
    bpy.ops.object.editmode_toggle()
    #select mode face um harte kanten zu bekommen
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

    #zeigen in die Richtung, aber nicht mit geraden STrahlen, sondern perspektivisch
    #wenn man danach mit smooth vectors darueber geht entstehen nicht ganz zu krasse Treppenstufen
    #bpy.ops.mesh.point_normals(target_location=(empty.location[0], empty.location[1], empty.location[2]))

    #normalen sind parallel ausgerichtet,(so halb bin mir da nicht ganz sicher), zumindest sehr viel weniger perspektivisch als bei Loesung 1
    bpy.ops.mesh.point_normals(align= True, target_location=(rotateObject.location[0], rotateObject.location[1], rotateObject.location[2]))
    
    bpy.ops.object.editmode_toggle() 
    
def ResetNormals():
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.normals_tools(mode='RESET')

    
    bpy.ops.object.editmode_toggle()
    
def SpherizeNormals():
    bpy.ops.object.editmode_toggle()
    
    obj = bpy.context.view_layer.objects.active
    mesh = obj.data

    bpy.ops.object.vertex_group_set_active(group='head')

    bpy.ops.object.vertex_group_select()
    
    #das hier muss alles im object mode passieren, dass es funktioniert
    bpy.ops.object.editmode_toggle()

    selected_verts = [v for v in mesh.vertices if v.select]
    
    #bpy.ops.object.editmode_toggle()
    #die Werte hier muessen von irgendeinem selektierten Vertex kommen
    y_pos=0
    y_neg=0
    z_pos=0
    z_neg=3.97

    ##irgendwie kommt hier manchmal Bloedsinn raus und manchmal aber auch das richtige?????
    
    
    for i in selected_verts:
        #print(i.index)
        print(i.co[1])
        
        
        if(i.co[1]>=y_pos):
            y_pos=i.co[1]
            
        if(i.co[1]<=y_neg):
            y_neg = i.co[1]
        
        if(i.co[1]>=z_pos):
            z_pos = i.co[2]
            
        if(i.co[2]<=z_neg):
            z_neg = i.co[2]
            
    print(y_pos, y_neg, z_pos, z_neg)
    
    bpy.ops.object.editmode_toggle()

    y = y_pos+y_neg
    z = z_neg + ((z_pos-z_neg)/2)
    x = 0

    bpy.context.scene.cursor.location[0] = x
    bpy.context.scene.cursor.location[1] = y
    bpy.context.scene.cursor.location[2] = z

    bpy.ops.mesh.point_normals(invert = True, align= False, target_location=(x, y, z), spherize = True, spherize_strength = 1.0)
    
    
    bpy.ops.object.editmode_toggle()
    
    
#how cost intensive would it be to rotate the normals every frame or every other frame?
#enter edit mode(need to be in object mode to work)
#bpy.ops.object.editmode_toggle()

#show normal representation in edit mode
#needs different wording for the scripting to work
#bpy.context.space_data.overlay.show_face_normals = True
#bpy.context.space_data.overlay.show_split_normals = True

#shade object smooth for a smooth look, necessary for most cases(faces for example)
#bpy.ops.mesh.faces_shade_smooth()
#activate auto-smooth so the normal editing is visible
#bpy.context.object.data.use_auto_smooth = True
#set auto smooth to 180°, so only normals which are marked as hard edges are hard edges
#bpy.context.object.data.auto_smooth_angle = 3.14159




##select vertex group on object
#obj = bpy.data.objects["Sphere"] #wird irgendwie benoetigt sonst funktionierts nicht
#obj1 = bpy.context.view_layer.objects.active
#obj1.select_set(True)
#bpy.ops.mesh.select_all(action = 'DESELECT')
#obj1.vertex_groups[0] ist einfach der Name der Vertex group 0
#obj1.vertex_groups.active = obj1.vertex_groups[0]
#bpy.ops.object.vertex_group_select()


#bpy.ops.object.editmode_toggle()

##select vertices either by distance or color

#select_vert_by_dist("Empty", 0.8)

#select_Vertexcolor(blue)
    

#rotiere die Normalen in die Richtung eines angegeben Vektors
def RotateNormalsBel(richtung, color, collayer, Vcolor1):
    #Volor1 is the vertex color layer
    emptyLoc = bpy.data.objects['Empty'].location
    
    #vertices lists with vertex color red, green or blue
    print('selected normals')
    vert_r = [] #vertex
    vert_l = [] #loop
    vert_n = [] #VertexNormals
    context = bpy.context
    mesh = context.object.data
    bm = bmesh.new()
    bm.from_mesh(mesh)

    color_layers = bm.loops.layers.color
    #color_layer = color_layers.get("color") or color_layers.new("color")
    color_layer = color_layers.get(Vcolor1)
    #L = len(bm.verts) - 1
    for face in bm.faces:
        for loop in face.loops:        
            #x = loop.vert.index / L 
            #print("Vert:", loop.vert.index)
            #print(loop[color_layer])
            #mit slice notation[:] wird der Vektor zu einer Sequenz? um die Werte vergleichen zu koennen https://blender.stackexchange.com/questions/116963/convert-a-mathutils-vector-object-into-3d-coordinates
            if loop[color_layer][:]==color:
                vert_r.append(loop.vert)
                vert_l.append(loop)
            #loop[color_layer] = (x, x, x, 1)

    #print(vert_r)
    #https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    vert_r_noDouble = list(dict.fromkeys(vert_r))
    #print(vert_r_noDouble)
    
    #for t in vert_l:
        #vert_n.append(t.normal)    
        #print(t)
    
    for b in vert_r_noDouble:
        #print(b)
        b.select = True
        
    for v in vert_r:
        print(v.normal)
        v.normal = (0,0,0)
        print(v.normal)
    
     
    ####################hier weiter machen############################################################################
    ##################################################################################################################
        #(0,0,0) ist die Standardnormale
    #######!!!!!vielleicht kann man mit den BMesh Loops, dann auch die Funktion hier benutzen!!!!!!!!!!!!!
#   obj.data.normals_split_custom_set_from_vertices( [(0+emptyLoc[0], 0+emptyLoc[1], 0+emptyLoc[2]) for v in vert_l] )
    #obj.data.normals_split_custom_set( [(0+emptyLoc[0], 0+emptyLoc[1], 0+emptyLoc[2]) for v in vert_l] )
    
    bm.to_mesh(mesh)    
    
 #das entscheidet sich hier gleich am Anfang ob es alle Normalen normal laesst oder ob sie veraendert werden, das if else muss doch irgendwie mit in die Schleife rein

##obj.data.normals_split_custom_set_from_vertices( [ (0+emptyLoc[0], 0+emptyLoc[1], 0+emptyLoc[2]) for i in vert_list] )

#obj.data.normals_split_custom_set_from_vertices( [(0+emptyLoc[0], 0+emptyLoc[1], 0+emptyLoc[2]) for v in obj.data.vertices] )


#object = bpy.data.objects['Sphere']
#v_local = object.data.vertices[0].co # local vertex coordinate, braucht die Vertrexnummer
#v_global = object.matrix_world @ v_local # global vertex coordinates


#for v in object.data.vertices:
    #print(v.co) # .co gibt die Koordinate des Vertexpunktes

#obj = bpy.data.objects['Sphere']
#print(obj.data.vertices[0].co)   
#obj.data.normals_split_custom_set((1, 0, 0))    
    
    
#for i in obj.vertex_groups[0]:
#    print(i)
    #obj.data.polygons[i].select = True

