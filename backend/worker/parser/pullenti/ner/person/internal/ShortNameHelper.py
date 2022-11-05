﻿# SDK Pullenti Address, version 4.14, september 2022. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.TextToken import TextToken
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.AnalysisKit import AnalysisKit
from pullenti.ner.person.internal.PullentiNerPersonInternalResourceHelper import PullentiNerPersonInternalResourceHelper

class ShortNameHelper:
    
    class ShortnameVar:
        
        def __init__(self) -> None:
            self.name = None;
            self.gender = MorphGender.UNDEFINED
        
        def __str__(self) -> str:
            return self.name
        
        @staticmethod
        def _new2370(_arg1 : str, _arg2 : 'MorphGender') -> 'ShortnameVar':
            res = ShortNameHelper.ShortnameVar()
            res.name = _arg1
            res.gender = _arg2
            return res
    
    M_SHORTS_NAMES = None
    
    @staticmethod
    def get_shortnames_for_name(name : str) -> typing.List[str]:
        res = list()
        for kp in ShortNameHelper.M_SHORTS_NAMES.items(): 
            for v in kp[1]: 
                if (v.name == name): 
                    if (not kp[0] in res): 
                        res.append(kp[0])
        return res
    
    @staticmethod
    def get_names_for_shortname(shortname : str) -> typing.List['ShortnameVar']:
        res = [ ]
        wrapres2368 = RefOutArgWrapper(None)
        inoutres2369 = Utils.tryGetValue(ShortNameHelper.M_SHORTS_NAMES, shortname, wrapres2368)
        res = wrapres2368.value
        if (not inoutres2369): 
            return None
        else: 
            return res
    
    M_INITED = False
    
    @staticmethod
    def initialize() -> None:
        if (ShortNameHelper.M_INITED): 
            return
        ShortNameHelper.M_INITED = True
        obj = PullentiNerPersonInternalResourceHelper.get_string("ShortNames.txt")
        if (obj is not None): 
            kit = AnalysisKit(SourceOfAnalysis(obj))
            t = kit.first_token
            while t is not None: 
                if (t.is_newline_before): 
                    g = (MorphGender.FEMINIE if t.is_value("F", None) else MorphGender.MASCULINE)
                    t = t.next0_
                    nam = t.term
                    shos = list()
                    t = t.next0_
                    while t is not None: 
                        if (t.is_newline_before): 
                            break
                        else: 
                            shos.append(t.term)
                        t = t.next0_
                    for s in shos: 
                        li = None
                        wrapli2371 = RefOutArgWrapper(None)
                        inoutres2372 = Utils.tryGetValue(ShortNameHelper.M_SHORTS_NAMES, s, wrapli2371)
                        li = wrapli2371.value
                        if (not inoutres2372): 
                            li = list()
                            ShortNameHelper.M_SHORTS_NAMES[s] = li
                        li.append(ShortNameHelper.ShortnameVar._new2370(nam, g))
                    if (t is None): 
                        break
                    t = t.previous
                t = t.next0_
    
    # static constructor for class ShortNameHelper
    @staticmethod
    def _static_ctor():
        ShortNameHelper.M_SHORTS_NAMES = dict()

ShortNameHelper._static_ctor()