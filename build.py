#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_boost


if __name__ == "__main__":
    builder = build_template_boost.get_builder()
    builder.run()