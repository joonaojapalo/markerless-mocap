path = {
    "base": "videos",
    "camera_dirs": [
        "cam1",
        "cam2"
    ],
    "file_prefix": "veto_",
    "file_ext": ".MP4"
}

videos = {
    "_01": {
        "sync": 372-209,    # cam1_sync_frame - cam2_sync_frame
        "start": 200,       # start_frame of behind of time video
        "cut": 240          # how many frames to process?
    },
    "_02": {
        "sync": 424-324,
        "start": 310,
        "cut": 240 
    }
}
