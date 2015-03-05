"""
Script to define the mapping between class name and class id.

Saves the mapping in a pkl file: class_index.pkl
"""
import pickle,string

SAVE_FILE = "detection_class_index.pkl"

#[detection_class_index class_name UCF_class_index]
Detection_def = [
(0, "Background", 0),
(1, "BaseballPitch", 7),
(2, "BasketballDunk",9),
(3, "Billiards",12),
(4, "CleanAndJerk",21),
(5, "CliffDiving",22),
(6, "CricketBowling",23),
(7, "CricketShot",24),
(8, "Diving",26),
(9, "FrisbeeCatch",31),
(10, "GolfSwing",33),
(11, "HammerThrow",36),
(12, "HighJump",40),
(13, "JavelinThrow",45),
(14, "LongJump",51),
(15, "PoleVault",68),
(16, "Shotput",79),
(17, "SoccerPenalty",85),
(18, "TennisSwing",92),
(19, "ThrowDiscus",93),
(20, "VolleyballSpiking",97)]

class_index = {}
index_class = {}
UCFid_DETid = {}
for class_id, class_name, UCF_id in Detection_def:
	#class_name = string.lower(class_name), no need to lower case.
	class_index[class_name] = int(class_id)
	index_class[int(class_id)] = class_name
	UCFid_DETid[UCF_id]=class_id

with open(SAVE_FILE, 'w+') as f:
	map_tuple = (class_index, index_class,UCFid_DETid)
	pickle.dump(map_tuple,f)
