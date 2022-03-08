# Markerless kinematics project

## Directory layout

## `./`
- `run_dlt_analysis.py` : main analysis script

## `./notes`

Meeting notes, etc.

## `./blazepose`

Blazepose related code.

- `dualcam.py`

## `./dltx`

Direct linear transformation package (Python).

## `./dist2coords`

Distance matrix to world coordinate function.
Based on: Torgerson, Warren. (1952). Multidimensional Scaling: I. Theory and Method. Psychometrika. 17. 401-419. 10.1007/BF02288916. 

## `./datasets`

- `pajulahti_{1,2,3}/`
    - `calibration_coords.py` - calibration data for all cameras in dataset
    - `video_metadata.py` - dataset video synchronization and filesystem path data

## Slowmo video from 100fps

```sh
ffmpeg -i .\output_pajulahti_3__30.mp4 -filter:v "setpts=4*PTS" slowmo_veto_30.mp4
```

## Case 1: analysis flow
```sh
python .\run_dlt_analysis.py --dataset=pajulahti_3 --outprefix=output
```

## Debugging

Script `pos_explore.py` to read pre-prepared numpy array of runner hip position data.
