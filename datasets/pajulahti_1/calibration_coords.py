# 1200mm kenno
# 10m suora
# Vasen teippi h=2668 (vas. alakulma)
# Oikea teippi h=2632 (oik. alakulma)
# - kennosta 1500mm vasemmalle
# - seinä 3745 kennolinjasta (Z)
#
# teippi(v)  teippi (o)
#     (6)    (3)
#      |      |     <-------- 2632
#      |      |
#     (8)____(7)__
# (5) /           \ (2)
#  | /             \ |   <--- 1200
# (4)---------------(1)
#         10000

# distance
world_distances = None

world_positions = [
    [0,     0,      0   ], # point 1
    [0,     1200,   0   ], # point 2
    [1500,  2632,   3745], # point 3
    [10000, 0,      0   ], # point 4
    [10000, 1200,   0   ], # point 5
    [10000, 2668,   3745], # point 6
    [1500,  0,      3745], # point 7   
    [10000, 0,      3745]  # point 8
]

cameras = [
    # Camera 1
    [
        [1726, 753],
        [1724, 588],
        [1241, 435],
        [100, 833],
        [122, 546],
        [217, 348],
        [1239, 714],
        [197, 739]
    ],
    # Camera 2
    [
        [1773, 772],
        [1775, 488],
        [1485, 306],
        [220, 658],
        [222, 498],
        [572, 359],
        [1481, 673],
        [568, 627]
    ]
]
