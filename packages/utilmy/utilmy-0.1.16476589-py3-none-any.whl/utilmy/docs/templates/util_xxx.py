# -*- coding: utf-8 -*-
MNAME = "utilmy.ZZZZZ.util_xxxx"
HELP = """ utils for  ....

python utilmy/ZZZZZ/util_xxxx.py  test1


"""
import os,sys,time,gc, glob, numpy as np, pandas as pd
from box import Box



#### Types
from typing import List, Optional, Tuple, Union


#############################################################################################
from utilmy import log, log2
def help():
    """function help
    Args:
    Returns:
        
    """
    from utilmy import help_create
    print( HELP + help_create(MNAME) )



#############################################################################################
def test_all() -> None:
    """function test_all
    Args:
    Returns:
        
    """
    log(MNAME)
    test1()
    test2()


def test1() -> None:
    """function test1
    Args:
    Returns:
        
    """
    pass


def test2() -> None:
    """function test2
    Args:
    Returns:
        
    """
    pass

#############################################################################################













###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()  ### python utilmy/ZZZZZ/util_xxxx.py  test1



