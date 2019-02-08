#!/usr/bin/env python3

'''
Fortigate CLI outputs session info in a pretty parsable format. Goals of this
script are:
    * Parse output to pull out 5-tuples
    * Produce statistics per source or destination to find hosts with excessive
    session counts.

Sample output of 'diag system session list'
    session info: proto=6 proto_state=01 duration=6627 expire=3170 timeout=3600 flags=00000000 sockflag=00000000 sockport=0 av_idx=0 use=4
    origin-shaper=
    reply-shaper=
    per_ip_shaper=
    ha_id=0 policy_dir=0 tunnel=/ vlan_cos=0/255
    state=may_dirty npu
    statistic(bytes/packets/allow_err): org=622/7/1 reply=750/5/1 tuples=2
    tx speed(Bps/kbps): 0/0 rx speed(Bps/kbps): 0/0
    orgin->sink: org pre->post, reply pre->post dev=19->5/5->19 gwy=10.40.7.193/10.20.49.254
    hook=post dir=org act=snat 10.10.46.35:65333->10.30.26.181:443(10.40.7.194:65333)
    hook=pre dir=reply act=dnat 10.30.26.181:443->10.40.7.194:65333(10.10.46.35:65333)
    pos/(before,after) 0/(0,0), 0/(0,0)
    misc=0 policy_id=3 auth_info=0 chk_client_info=0 vd=0
    serial=000bb0c2 tos=ff/ff app_list=0 app=0 url_cat=0
    dd_type=0 dd_mode=0
    npu_state=0x003000
    npu info: flag=0x81/0x81, offload=6/6, ips_offload=0/0, epid=2/16, ipid=16/2, vlan=0x0000/0x0000
    vlifid=0/0, vtag_in=0x0000/0x0000 in_npu=0/0, out_npu=0/0, fwd_en=0/0, qid=0/0
    total session 3151
'''

import argparse
import re

def main(input_fh):
    count = dict()
    p = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    for line in input_fh:
        if "snat" in line:
            source_ip = p.findall(line)[0]
            try:
                count[source_ip] += 1
            except KeyError:
                count[source_ip] = 1
            except:
                raise

    for ip in sorted(count, key=count.__getitem__):
        if count[ip] > 20:
            print("{}\t{}".format(ip, count[ip]))
    print("Total session count: {}".format(sum(count.values())))


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("input_file")
    ARGS = PARSER.parse_args()

    try:
        input_fh = open(ARGS.input_file, 'r')
    except:
        raise

    main(input_fh)
