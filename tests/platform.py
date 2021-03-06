from .common import *

platform = cl.get_platforms()[0]
devices = [device for device in platform.get_devices() if device.type == cl.device_type.GPU]
device = [devices[0]]
queue_properties = cl.command_queue_properties.PROFILING_ENABLE
ctx = cl.Context(devices)
queues = [cl.CommandQueue(ctx, device, properties=queue_properties) for device in devices]
queue = queues[0]
computeUnits = device.max_compute_units
device_wg_size = min([wavefront_wg_size(device) for device in devices])
default_wg_size = device_wg_size
is_amd_platform = all([is_device_amd(device) for device in devices])
is_nvidia_platform = all([is_device_nvidia(device) for device in devices])

def cl_opt_decorate(debug, CL_FLAGS, max_wg_size_used = None):
    if is_amd_platform:
        CL_FLAGS2 = '-D AMD_ARCH -D DEVICE_WAVEFRONT_SIZE={wavefront_size} '.format(wavefront_size=device_wg_size)
        if max_wg_size_used is not None and np.prod(max_wg_size_used, dtype=np.uint32) <= device_wg_size:
            CL_FLAGS2 = CL_FLAGS2 + '-D PROMISE_WG_IS_WAVEFRONT '
        CL_FLAGS = CL_FLAGS2 + CL_FLAGS
    if debug == 2:
        CL_FLAGS = '-D DEBUG -g -cl-opt-disable '+CL_FLAGS
    elif debug:
        CL_FLAGS = '-D DEBUG '+CL_FLAGS
    return CL_FLAGS
