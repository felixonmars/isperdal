#!/usr/bin/env python
# encoding: utf-8

from isperdal import painting

'/'.all(
    lambda this, req, res:
        res.ok("Hello world.")
).run()
