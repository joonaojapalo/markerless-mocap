from email.policy import default
from fileinput import filename
import os
import sys  # Get command line arguments
from optparse import OptionParser
from blazepose import dualcam
import numpy as np  # for data file

from dlt_processor import DLTProcessor

# import dataset
#from datasets.pajulahti_3.calibration_coords import cameras, world_positions
#from datasets.pajulahti_3 import video_metadata


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


def print_dlt_analysis_result(dlt_processor):
    analysis = dlt_processor.get_analysis()
    print("analysis", analysis)

    if analysis["s"] and analysis["v"]:
        print("Result\ns\tv\n%.3f\t%.2f" % (analysis["s"], analysis["v"]))


# def log_dlt_analysis_result(file_id, dlt_processor, filename="analysis.tsv"):
#    analysis = dlt_processor.get_analysis()
#
#    if not os.path.isfile(filename):
#        with open(filename, "a") as fd:
#            fd.write("id\tvelocity\tdistance\n")
#
#    with open(filename, "a") as fd:
#        if analysis["s"] and analysis["v"]:
#            fd.write("\"%s\"\t%.3f\t%.2f\n" %
#                     (file_id, analysis["s"], analysis["v"]))

def write_data_array(pos_data, file_id, output_dir=""):
    filename = file_id + ".array"
    outfile = os.path.join(output_dir, filename)
    np.array(pos_data).tofile(outfile, ";")


class MetaData:
    def __init__(self, video_metadata) -> None:
        self._videos = video_metadata.videos

    def get_sync(self, file_id):
        if file_id not in self._videos:
            return None

        return self._videos[file_id]["sync"]

    def get_cut(self, file_id):
        if file_id not in self._videos:
            return None

        return self._videos[file_id]["cut"]

    def get_start(self, file_id):
        if file_id not in self._videos:
            return None

        return self._videos[file_id]["start"]

    def get_file_ids(self):
        return self._videos.keys()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-O", "--outprefix=",
                      dest="outprefix",
                      default="output",
                      help="Output file PREFIX")
    parser.add_option("-a", "--analysisfile=",
                      dest="analysisfile",
                      help="Analysis FILE",
                      default="analysis.tsv")
    parser.add_option("-d", "--dataset=",
                      default="pajulahti_3",
                      dest="dataset",
                      help="Dataset name")
    parser.add_option("-N", "--noout",
                      action='store_true',
                      default=False,
                      dest="no_out",
                      help="Do not write output video to file.")
    parser.add_option("--outputdir=",
                      default="output",
                      dest="output_dir",
                      help="Directory for output files (MP4, array)")
    options, args = parser.parse_args()

    # load dataset
    cameras, world_positions, video_metadata, videopath = load_dataset(
        options.dataset)

    meta = MetaData(video_metadata)

    # process all dataest videos
    for file_id in meta.get_file_ids():
        print("Searching videos from:", videopath)

        ext = video_metadata.path["file_ext"]
        prefix = video_metadata.path["file_prefix"]
        cam_dirs = video_metadata.path["camera_dirs"]
        sync = meta.get_sync(file_id)
        skip = meta.get_start(file_id)
        cut = meta.get_cut(file_id)

        inputs = [os.path.join(videopath, cam_dir, prefix + str(i + 1) + file_id + ext)
                  for i, cam_dir in enumerate(cam_dirs)]

        # Open video
        if len(inputs) != 2:
            print("Two input videos expected. Got", len(inputs))
            sys.exit(1)

        print("Inputs:", ", ".join(inputs))

        dlt_processor = DLTProcessor(cameras, world_positions, 3)

        print("Start processing sources")
        outfile = "%s/%s_%s_%s%s" % (
            options.output_dir,
            options.outprefix, options.dataset, file_id, ext) if options.no_out == False else None
        dualcam.start_capture(
            inputs, outfile, [dlt_processor], sync, skip, cut)

        # write run position data
        write_data_array(dlt_processor.pos_data)

        # log to file and console
        print_dlt_analysis_result(dlt_processor)
