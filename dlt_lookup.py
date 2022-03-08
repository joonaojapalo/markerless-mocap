from dlt_processor import DLTProcessor
from datasets.pajulahti_3.calibration_coords import cameras, world_positions

dlt_processor = DLTProcessor(cameras, world_positions, 3)

sp = [
    [1195,943],
    [721,878]
]

dlt_processor.get_position(sp)
