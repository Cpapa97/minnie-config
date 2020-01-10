segmentation_m65 = 1
segmentation_m65_str = f'{segmentation_m65:02d}'

schema_name_version = schema_name + segmentation_m65_str

import datajoint as dj
import warnings
import os

# External store paths + ensure the directories exist. For new segmentations create a subfolder.
external_store_basepath = '/mnt/dj-stor01/platinum/minnie65'
external_segmentation_path = os.path.join(external_store_basepath, segmentation_m65_str)
external_mesh_path = os.path.join(external_segmentation_path, 'meshes')
external_decimated_mesh_path = os.path.join(external_segmentation_path, 'decimated_meshes')
if os.path.exists(external_store_basepath):
    if not os.path.exists(external_segmentation_path):
        os.mkdir(external_segmentation_path)
    if not os.path.exists(external_mesh_path):
        os.mkdir(external_mesh_path)
    if not os.path.exists(external_decimated_mesh_path):
        os.mkdir(external_decimated_mesh_path)
else:
    warnings.warn(f'Path to minnie65 folder does not exist at: {external_store_basepath} (dj-stor01 not mounted under /mnt ?)')

# External filepath referrencing.
dj.config['stores'] = {
  'minnie65': {
    'protocol': 'file',
    'location': external_store_basepath,
    'stage': external_store_basepath
  },
  'meshes': {
    'protocol': 'file',
    'location': external_mesh_path,
    'stage': external_mesh_path
  },
  'decimated_meshes': {
    'protocol': 'file',
    'location': external_decimated_mesh_path,
    'stage': external_decimated_mesh_path
  }
}

# Enable experimental datajoint features
# These flags are required by 0.12.0+ (for now).
dj.config['enable_python_native_blobs'] = True
dj.errors._switch_filepath_types(True)
dj.errors._switch_adapted_types(True)