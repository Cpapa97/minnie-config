import datajoint as dj
import numpy as np
import h5py
import os

from collections import namedtuple


class MeshAdapter(dj.AttributeAdapter):
    # Initialize the correct attribute type (allows for use with multiple stores)
    def __init__(self, attribute_type, has_version=False):
        self.attribute_type = attribute_type
        self.has_version = has_version
        super().__init__()

    attribute_type = '' # this is how the attribute will be declared
    has_version = False # used for file name recognition

    TriangularMesh = namedtuple('TriangularMesh', ['segment_id', 'version', 'vertices', 'faces'])
    
    def put(self, filepath):
        # save the filepath to the mesh
        filepath = os.path.abspath(filepath)
        assert os.path.exists(filepath)
        return filepath

    def get(self, filepath):
        # access the h5 file and return a mesh
        assert os.path.exists(filepath)

        with h5py.File(filepath, 'r') as hf:
            vertices = hf['vertices'][()].astype(np.float64)
            faces = hf['faces'][()].reshape(-1, 3).astype(np.uint32)
        
        segment_id = os.path.splitext(os.path.basename(filepath))[0]

        version = None
        if self.has_version:
            segment_id, version = segment_id.split('_')
            version = int(version)
        
        return self.TriangularMesh(
            segment_id=int(segment_id),
            version=version,
            vertices=vertices,
            faces=faces
        )
    

# instantiate for use as a datajoint type
mesh = MeshAdapter('filepath@meshes')
decimated_mesh = MeshAdapter('filepath@decimated_meshes', has_version=True)

# also store in one object for ease of use with virtual modules
adapter_objects = {
    'mesh': mesh,
    'decimated_mesh': decimated_mesh
}