# create a temp file
f = tempfile.NamedTemporaryFile(suffix = .maya)

# convert it to another file
subprocess.check_call (['conv', filepath, f.name])

# do seek before reading the file
f.seek(0)

# read the lines
mayaData = f.readlines()

# convet it to utf from binary
mayaDataDecoded = [i.decode('utf-8') for i in mayaData ]

# get the matrix from xyz data

rotR = [list of rotation values in radians]
rotE = mathutils.Euler((rotsR[0],rotsR[1],rotsR[2]))
rotE.order = 'XYZ'
rotM = rotE.to_matrix()
rotM.resize_4x4()

trans = [list of translation values]
transV = mathutils.Vector((trans[0], trans[1], trans[2]))
transM = mathutils.Matrix.Translation(transV)
transM.to_4x4()

objMatrix = mathutils.Matrix()
objectMatrix = transM * rotM  # order is important

final_rot = objectMatrix.decompose()[1].to_euler('ZXY')
final_rot1 = [final_rot[2], final_rot[0], final_rot[1]]

final_loc = objectMatrix.decompose()[0]
final_loc1 = final_loc[2], final_loc[0], final_loc[1]
