def coord_to_mpl(pose):
    '''
	Convert array of x, y, z coordinates to a matplotlib supported
    format where the x, y, z coordinates are separated into their
    own arrays with order maintained

	Args:
		pose: :, 3 array to be converted to mpl supported format

	Return:
		3 arrays for the x, y, z coordinates
	'''

    x = []
    y = []
    z = []
    for point in pose:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    
    return x, y, z