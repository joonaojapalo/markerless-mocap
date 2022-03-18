import os

__all__ = ["load_dataset"]


def load_dataset(dataset_name):
    API_CALIBRATION = ["cameras", "world_positions"]
    API_VIDEO = ["video_metadata"]
    path_cal = "datasets.%s.calibration_coords" % (dataset_name,)
    path_video = "datasets.%s" % (dataset_name,)

    # import dataset modules
    _module_calibration = __import__(path_cal,
                                     globals(),
                                     locals(),
                                     API_CALIBRATION)
    _module_video = __import__(path_video,
                               globals(),
                               locals(),
                               API_VIDEO)

    video_metadata = _module_video.video_metadata

    # video basepath
    videopath = os.path.join("datasets", dataset_name,
                             video_metadata.path["base"])

    return (
        _module_calibration.cameras,
        _module_calibration.world_positions,
        video_metadata,
        videopath
    )
