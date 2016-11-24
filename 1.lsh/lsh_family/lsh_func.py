import numpy as np

def random_three_vector():
    """
    Generates a random 3D unit vector (direction) with a uniform spherical distribution
    Algo from http://stackoverflow.com/questions/5408276/python-uniform-spherical-distribution
    :return:
    """
    # xy_scale = 0.1
    # xy_shift = np.pi*2 * (-0.25)
    # z_scale = 0.5
    
    xy_scale = 0.5
    xy_shift = 0
    z_scale = 1
    
    phi = np.random.uniform(0 + xy_shift,np.pi*2 * xy_scale + xy_shift)
    costheta = np.random.uniform(-1 * z_scale, 1 * z_scale)

    theta = np.arccos( costheta )
    x = np.sin( theta) * np.cos( phi )
    y = np.sin( theta) * np.sin( phi )
    z = np.cos( theta )
    return (x,y,z)