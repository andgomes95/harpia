#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Button class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.javascript.webaudio.webaudioplugin import WebaudioPlugin


class Button(WebaudioPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        WebaudioPlugin.__init__(self)

        # Appearance
        self.help = "Button"
        self.label = "Button"
        self.color = "50:150:250:150"
        self.out_ports = [{"type":"HRP_WEBAUDIO_FLOAT",
                "label":"Click",
                "name":"click"}
            ]
        self.properties = [{"name": "value",
                            "label": "Value",
                            "type": HARPIA_FLOAT,
                            "lower": 0,
                            "upper": 20000,
                            "step": 1,
                            "value": 1
                            },
                           {"name": "label",
                            "label": "Label",
                            "type": HARPIA_STRING,
                            "value": "Label"
                            }
                           ]
        self.group = "Interface"

        self.codes[1] = """
// block_$id$ = $label$
var block_$id$_value = $prop[value]$;
var $out_ports[click]$ = [];
"""

        self.codes[2] = """
function click_$id$(){
    value = document.getElementById("block_$id$").value;
    for (var i = 0; i < $out_ports[click]$.length ; i++){
        $out_ports[click]$[i](value);
    }
};
"""

        self.codes[3] = """
<button type="button" value="$prop[value]$" onClick="click_$id$();"
id="block_$id$">$prop[label]$</button><br>
"""

