#!/bin/bash
rdir=ROOT/current/apps/DCAFPilot
source $rdir/etc/profile.d/init.sh
export DCAFPILOT_ROOT
export X509_USER_CERT=ROOT/state/proxy/proxy.cert
export X509_USER_KEY=ROOT/state/proxy/proxy.cert
export DCAFPILOT_PREDICTIONS=ROOT/state/data/predictions
export DCAFPILOT_CONFIG=$rdir/etc/dcaf.cfg
