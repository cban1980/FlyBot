#!/bin/env python
# -*- coding: utf-8 -*-
# Separate file for IRC functions that gets called in main.py.

from googletrans import Translator
import pydle

def tr(fran, till, mening):
    """Translation function."""
    translator = Translator()
    translation = translator.translate(mening, src=fran, dest=till)
    return translation.text
