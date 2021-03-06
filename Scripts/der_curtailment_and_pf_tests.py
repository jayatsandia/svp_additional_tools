'''
Copyright (c) 2016, Sandia National Labs and SunSpec Alliance
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

Neither the names of the Sandia National Labs and SunSpec Alliance nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Written by Sandia National Laboratories, Loggerware, and SunSpec Alliance
Questions can be directed to Jay Johnson (jjohns2@sandia.gov)
'''

# #!C:\Python27\python.exe

import sys
import os
import traceback
from svpelab import pvsim
from svpelab import gridsim
from svpelab import das
from svpelab import der
import sunspec.core.client as client
import script

def test_run():

    # initialize DER configuration
    eut = der.der_init(ts)
    eut.config()

    ts.log('---')
    info = eut.info()
    if info is not None:
        ts.log('DER info:')
        ts.log('  Manufacturer: %s' % (info.get('Manufacturer')))
        ts.log('  Model: %s' % (info.get('Model')))
        ts.log('  Options: %s' % (info.get('Options')))
        ts.log('  Version: %s' % (info.get('Version')))
        ts.log('  Serial Number: %s' % (info.get('SerialNumber')))
    else:
        ts.log_warning('DER info not supported')
    ts.log('---')

    for power in range(5, 25, 2):
        eut.limit_max_power(params={'Ena': True, 'WMaxPct': power})
        limit_max_power = eut.limit_max_power()
        if limit_max_power is not None:
            ts.log('DER limit_max_power:')
            ts.log('  Ena: %s' % (limit_max_power.get('Ena')))
            ts.log('  WMaxPct: %s' % (limit_max_power.get('WMaxPct')))

    for pf in [1, -0.85, -.9, -.95, 1, .95, .9, .85]:
        eut.fixed_pf(params={'Ena': True, 'PF': pf})
        fixed_pf = eut.fixed_pf()
        if fixed_pf is not None:
            ts.log('DER power factor:')
            ts.log('  Ena: %s' % (fixed_pf.get('Ena')))
            ts.log('  PF: %s' % (fixed_pf.get('PF')))


    return script.RESULT_COMPLETE

def run(test_script):

    try:
        global ts
        ts = test_script
        rc = 0
        result = script.RESULT_COMPLETE

        ts.log_debug('')
        ts.log_debug('**************  Starting %s  **************' % (ts.config_name()))
        ts.log_debug('Script: %s %s' % (ts.name, ts.info.version))
        ts.log_active_params()

        result = test_run()

        ts.result(result)
        if result == script.RESULT_FAIL:
            rc = 1

    except Exception, e:
        ts.log_error('Test script exception: %s' % traceback.format_exc())
        rc = 1

    sys.exit(rc)

info = script.ScriptInfo(name=os.path.basename(__file__), run=run, version='1.0.0')

# DER
der.params(info)

info.logo('sunspec.gif')

def script_info():
    
    return info


if __name__ == "__main__":

    # stand alone invocation
    config_file = None
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    params = None

    test_script = script.Script(info=script_info(), config_file=config_file, params=params)

    run(test_script)


