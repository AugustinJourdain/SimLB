# ---------------------------------------------------------------------------- #
#                                  Description                                 #
# This file stores user preferred configurations, which will overwrite default #
# global configuration (in global_conf.py)                                     #
# ---------------------------------------------------------------------------- #

from config.global_conf import *
from config.node_register import *

# ---------------------------------------------------------------------------- #
#                                      Log                                     #
# ---------------------------------------------------------------------------- #

LOG_FOLDER = '../../data/simulation'  # overwrite

# ---------------------------------------------------------------------------- #
#                                   Topology                                   #
# ---------------------------------------------------------------------------- #


def generate_node_config_tier4(
        lb_method='ecmp',
        n_clt=1,
        n_er=1,
        n_lb=N_LB,
        n_as=N_AS,
        n_worker_baseline=N_WORKER_BASELINE,
        n_worker2change=N_WORKER2CHANGE,
        n_worker_multiplier=N_WORKER_MULTIPLIER,
        as_mp_level=AS_MULTIPROCESS_LEVEL,
        kf_sensor_std=KF_CONF['sensor_std'],
        lb_bucket_size=LB_BUCKET_SIZE,
        b_offset=B_OFFSET,
        lb_period=LB_PERIOD,
        debug=DEBUG):
    clt_ids = list(range(n_clt))
    er_ids = list(range(n_er))
    lb_ids = list(range(n_lb))
    as_ids = list(range(n_as))

    clt_template = {
        'child_ids': er_ids,
        'child_prefix': 'er',  # connected to edge router
        'debug': 0
    }

    er_template = {
        'child_ids': lb_ids,
        'child_prefix': 'lb',  # connected to load balancers
    }

    lb_template = {
        'child_ids': as_ids,
        'debug': 0,
        'bucket_size': lb_bucket_size
    }

    as_template = {
        'n_worker': n_worker_baseline,
        'multiprocess_level': as_mp_level,
        'debug': 0
    }

    clt_config = {i: clt_template.copy() for i in clt_ids}
    er_config = {i: er_template.copy() for i in er_ids}
    as_config = {i: as_template.copy() for i in as_ids}

    for i in range(n_worker2change):  # update half as configuration
        as_config[i].update(
            {'n_worker': n_worker_baseline*n_worker_multiplier})

    lb_config = {i: lb_template.copy() for i in lb_ids}
    if 'weight' in lb_method or 'sed' in lb_method:
        for i in lb_ids:
            lb_config[i]['weights'] = {
                i: as_config[i]['n_worker'] for i in as_ids}
    if '2' in lb_method:
        for i in lb_ids:
            lb_config[i]['po2'] = True
    if 'hlb' in lb_method:
        for i in lb_ids:
            lb_config[i]['sensor_std'] = kf_sensor_std
            lb_config[i]['b_offset'] = b_offset
            lb_config[i]['lb_period'] = lb_period
    if 'sed' in lb_method:
        for i in lb_ids:
            lb_config[i]['b_offset'] = b_offset
    if 'active' in lb_method:
        for i in lb_ids:
            lb_config[i]['rtt_min'] = RTT_MIN
            lb_config[i]['rtt_max'] = RTT_MAX
            lb_config[i]['lb_period'] = lb_period

    print("lb_config={}".format(lb_config))
    return {
        'clt': clt_config,
        'er': er_config,
        'as': as_config,
        'lb-'+lb_method: lb_config,
    }


NODE_CONFIG = {}

# ---------------------------------------------------------------------------- #
#                             Control Plane Events                             #
# ---------------------------------------------------------------------------- #

CP_EVENTS2ADD = [
    # (ts, event_name, added_by, **kwargs)
    # e.g.:
    # (
    #     # change second 1/4 AS nodes back to normal worker baseline
    #     200.0+1e-7,
    #     'as_update_capacity',
    #     'sys-admin',
    #     {
    #         'node_ids': ['as{}'.format(i) for i in range(32, 64)],
    #         'n_worker': N_WORKER_BASELINE,
    #         'mp_level': 1,
    #     }
    # ),
    # (
    #     200.0+2e-7,
    #     'as_update_capacity',
    #     'sys-admin',
    #     {
    #         'node_ids': ['as{}'.format(i) for i in range(64, 96)],
    #         'n_worker': N_WORKER_BASELINE*N_WORKER_MULTIPLIER,
    #         'mp_level': 1,
    #     }
    # ),
    # (
    #     # change second 1/4 AS nodes back to normal worker baseline
    #     400.0+1e-7,
    #     'as_update_capacity',
    #     'sys-admin',
    #     {
    #         'node_ids': ['as{}'.format(i) for i in range(32, 64)],
    #         'n_worker': N_WORKER_BASELINE*N_WORKER_MULTIPLIER,
    #         'mp_level': 1,
    #     }
    # ),
    # (
    #     400.0+2e-7,
    #     'as_update_capacity',
    #     'sys-admin',
    #     {
    #         'node_ids': ['as{}'.format(i) for i in range(64, 96)],
    #         'n_worker': N_WORKER_BASELINE,
    #         'mp_level': 1,
    #     }
    # ),
    # (
    #     6.,
    #     'lb_remove_server',
    #     {
    #         'lbs': [0],
    #         'ass': [17, 18]
    #     }
    # ),
    # (
    #     3.2,
    #     'clt_update_in_traffic',
    #     {
    #         'node_id': 'clt1',
    #         'in_traffic_info_new': {'rate': 20, 'type': 'normal', 'mu': 1.0, 'std': 0.3}
    #     }
    # )
]
