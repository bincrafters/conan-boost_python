#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_shared
from bincrafters import build_template_boost_default

    
if __name__ == "__main__":

    builder = build_template_boost_default.get_builder()
    
    builder.run()