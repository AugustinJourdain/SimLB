from common.entities import NodeAS, NodeClient, NodeStatelessLB, NodeLB
from policies.rule import NodeLBLSQ, NodeLBSED, NodeLBSRT, NodeLBGSQ, NodeLBActive
from policies.heuristic import NodeLBAquarius, NodeHLB, NodeHLBada, NodeLBGeometry, NodeLBHermes, NodeLBRS, NodeLBProbFlow
from policies.rl_sac import NodeRLBSAC
from config.global_conf import KF_CONF, HIDDEN_DIM

# ---------------------------------------------------------------------------- #
#                             Register All Policies                            #
# ---------------------------------------------------------------------------- #

# ---------------------------------- Methods --------------------------------- #

METHODS = {
    #=== rule-based ===#
    "ecmp": { # Equal-Cost Multi-Path (ECMP)
        "class": NodeLB,
    }, 
    "wcmp": { # Weightd-Cost Multi-Path (WCMP)
        "class": NodeLB,    
        "config": {
            "weights": {}, # initialize weights based on number of workers
        }    
    },
    "lsq": { # Local shortest queue (LSQ)
        "class": NodeLBLSQ,
    },
    "lsq2": { # LSQ + power-of-2-choices
        "class": NodeLBLSQ,
        "config": {
            "po2": True,
        }
    },
    "sed": { # Shortest Expected Delay
        "class": NodeLBSED,
        "config": {
            "weights": {} # initialize weights based on number of workers
        }    
    },
    "sed2": { # LSQ + power-of-2-choices
        "class": NodeLBSED,
        "config": {
            "weights": {}, # initialize weights based on number of workers
            "po2": True,
        },
    },
    "srt": { # Shortest Remaining Time (SRT) (Layer-7)
        "class": NodeLBSRT,
    },
    "srt2": { # SRT + power-of-2-choices
        "class": NodeLBSRT,
        "config": {
            "po2": True,
        },
    },
    "gsq": { # Global shortest queue (GSQ) (Layer-7)
        "class": NodeLBGSQ,
    },
    "gsq2": { # GSQ + power-of-2-choices
        "class": NodeLBGSQ,
        "config": {
            "po2": True,
        },
    },
    "active-wcmp": { # Spotlight, adjust weights based on periodic polling
        "class": NodeLBActive,
        "config": {
            "lb_period": 0.5,
        },
    },
    #=== heuristic ===#
    "aquarius": { # Aquarius, 
        "class": NodeLBAquarius,
    },
    "hlb": { # Hybrid LB (HLB), Aquarius replacing alpha by Kalman filter
        "class": NodeHLB,
        "config": {
            "sensor_std": KF_CONF['sensor_std'],
        }
    },
    "hlb2": { # HLB + power-of-2-choices
        "class": NodeHLB,
        "config": {
            "sensor_std": KF_CONF['sensor_std'],
            "po2": True,
        },
    },
    "hlb-ada": { # HLB + adaptive sensor error
        "class": NodeHLBada,
        "config": {
            "sensor_std": KF_CONF['sensor_std'],
        }
    },
    "hermes": { # hermes
        "class": NodeLBHermes,
    },
    "rs": { # reservoir sampling #flow
        "class": NodeLBRS,
    },
    "rs2": { # reservoir sampling #flow
        "class": NodeLBRS,
        "config": {
            "po2": True,
        },
    },
    "geom": { # geometry based algorithm
        "class": NodeLBGeometry,
    },
    "geom-w": { # geometry based algorithm
        "class": NodeLBGeometry,
        "config": {
            "weighted": True,
            "weights": {}, # initialize weights based on number of workers
        },
    },
    "geom-sed": { # geometry based algorithm
        "class": NodeLBGeometry,
        "config": {
            "sed": True,
            "weights": {}, # initialize weights based on number of workers
        },
    },
    "geom-sed-w": { # geometry based algorithm
        "class": NodeLBGeometry,
        "config": {
            "sed": True,
            "weighted": True,
            "weights": {}, # initialize weights based on number of workers
        },
    },
    "prob-flow": { # geometry based algorithm
        "class": NodeLBProbFlow,
    },
    "prob-flow2": { # geometry based algorithm
        "class": NodeLBProbFlow,
        "config": {
            "po2": True,
        },
    },
    "prob-flow-w": { # geometry based algorithm
        "class": NodeLBProbFlow,
        "config": {
            "weighted": True,
            "weights": {}, # initialize weights based on number of workers
        },
    },
    "prob-flow-w2": { # geometry based algorithm
        "class": NodeLBProbFlow,
        "config": {
            "weighted": True,
            "po2": True,
            "weights": {}, # initialize weights based on number of workers
        },
    },
    "rlb-sac": { # SAC model
        "class": NodeRLBSAC,
        "config": {
            'SAC_training_confs_': {
                'hidden_dim': 50,
                'action_range': 1.,
                'batch_size': 64,
                'update_itr': 10,
                'reward_scale': 10.,
                'save_interval': 100,  # time interval for saving models, in seconds
                'AUTO_ENTROPY': True,
                'model_path': 'sac_v2',
            }
        }
    }
}

NODE_MAP = {
    "clt": NodeClient,
    "er": NodeStatelessLB,
    "as": NodeAS,
}

# add lb policies
NODE_MAP.update({"lb-{}".format(k): v['class'] for k,v in METHODS.items()})
