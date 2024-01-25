#!/usr/bin/python3

#Replaces words in order to consolidate entities

def replace_words(s):

    if "pyongyang," and "(kcna) —" in s:
        start = s.find("pyongyang,")
        end = s.find("(kcna) —")
        s = s[:start]+s[end+6:]
        
    if "u.s." in s:
        s = s.replace("u.s.", "usa")
    if "americans" in s:
        s = s.replace("americans", "usa")
    if "american" in s:
        s = s.replace("american", "usa")
    if "america" in s:
        s = s.replace("america", "usa")
    if "united states of america" in s:
        s = s.replace("united states of america", "usa")
    if "united states" in s:
        s = s.replace("united states", "usa")
        
    if "south koreans" in s:
        s = s.replace("south koreans", "rok")
    if "south korean" in s:
        s = s.replace("south korean", "rok")
    if "south korea" in s:
        s = s.replace("south korea", "rok")
    if "s. koreans" in s:
        s = s.replace("s. koreans", "rok")
    if "s. korean" in s:
        s = s.replace("s. korean", "rok")
    if "s. korea" in s:
        s = s.replace("s. korea", "rok")
    if "the south" in s:
        s = s.replace("the south", "rok")
        
    if "north koreans" in s:
        s = s.replace("north koreans", "dprk")
    if "north korean" in s:
        s = s.replace("north korean", "dprk")
    if "north korea" in s:
        s = s.replace("north korea", "dprk")
    if "n. koreans" in s:
        s = s.replace("n. koreans", "dprk")
    if "n. korean" in s:
        s = s.replace("n. korean", "dprk")
    if "n. korea" in s:
        s = s.replace("n. korea", "dprk")
    if "the north" in s:
        s = s.replace("the north", "dprk") 

    if "kcna " in s:
        s = s.replace("kcna ", "")

    if "japanese" in s:
        s = s.replace("japanese", "japan")

    if "kim jong un" in s:
        s = s.replace("kim jong un", "kim_jong_un")
    if "kim jong il" in s:
        s = s.replace("kim jong il", "kim_jong_il")
    if "kim il sung" in s:
        s = s.replace("kim il sung", "kim_il_sung")
    
    return s
