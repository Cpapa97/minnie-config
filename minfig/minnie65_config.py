import datajoint as dj
import warnings
import json
import os


segmentation_m65 = 1
segmentation_m65_str = '{:02d}'.format(segmentation_m65)

_schema_base_name = 'microns_minnie65_'
schema_name_m65 = _schema_base_name + segmentation_m65_str

# External store paths + ensure the directories exist. For new segmentations create a subfolder.
if os.name == 'nt':
    # # Read or write the windows drive letter to a local json file
    # dir_path = os.path.join(os.environ['APPDATA'], 'minnie-config')
    # if not os.path.isdir(dir_path):
    #     os.mkdir(dir_path)
    # filename = 'mount_config.json'
    # filepath = os.path.join(dir_path, filename)
    # if os.path.isfile(filepath):
    #     with open(filepath, 'r') as f:
    #         drive_letter = json.load(f)['windows']
    # else:
    #     drive_letter = input('If you are on Windows, please input the drive letter associated with the \\\\at-storage03.ad.bcm.edu\\dj-stor01 mount: ')
    #     try:
    #         with open(filepath, 'w') as f:
    #             json.dump({'windows': drive_letter}, f)
    #     except OSError as e:
    #         warnings.warn(e)
    # if not drive_letter.endswith(':'):
    #     drive_letter += ':'
    # mount_path = os.path.join(drive_letter, os.sep)
    
    dir_name = '\\\\at-storage3.ad.bcm.edu\\dj-stor01'
    mount_path = dir_name
elif os.name == 'posix':
    mount_path = os.path.join(os.sep, 'mnt', 'dj-stor01')
else:
    raise OSError('Unsupported OS pathing')
external_store_basepath = os.path.join(mount_path, 'platinum', 'minnie65')
external_segmentation_path = os.path.join(external_store_basepath, segmentation_m65_str)
external_mesh_path = os.path.join(external_segmentation_path, 'meshes')
external_decimated_mesh_path = os.path.join(external_segmentation_path, 'decimated_meshes')
external_skeleton_path = os.path.join(external_segmentation_path, 'skeletons')

def verify_paths(create_if_missing=False):
    def warn_if_missing(path, warning_info, create_if_missing):
        warning_msg = 'Path to minnie65 folder does not exist at: {path} ({info})'
        if not os.path.exists(path):
            if create_if_missing:
                os.mkdir(external_segmentation_path)
                return True
            else:
                warnings.warn(warning_msg.format(path=path, info=warning_info))
                return False
        return True

    if warn_if_missing(external_store_basepath, 'dj-stor01 not mounted under /mnt ?', create_if_missing=False):
        warn_if_missing(external_segmentation_path, '', create_if_missing=create_if_missing)
        warn_if_missing(external_mesh_path, '', create_if_missing=create_if_missing)
        warn_if_missing(external_decimated_mesh_path, '', create_if_missing=create_if_missing)
        warn_if_missing(external_skeleton_path, '', create_if_missing=create_if_missing)
    else:
        raise OSError('dj-stor01 not available')

def set_configurations(cache_path=None):
    # External filepath referrencing.
    stores_config = {
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
        },
        'skeletons': {
            'protocol': 'file',
            'location': external_skeleton_path
        }
    }

    if 'stores' not in dj.config:
        dj.config['stores'] = stores_config
    else:
        dj.config['stores'].update(stores_config)

    # External object cache
    if cache_path is not None:
        dj.config['cache'] = cache_path

    # Enable experimental datajoint features
    # These flags are required by 0.12.0+ (for now).
    dj.config['enable_python_native_blobs'] = True
    dj.errors._switch_filepath_types(True)
    dj.errors._switch_adapted_types(True)