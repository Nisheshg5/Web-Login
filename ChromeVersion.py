from win32 import win32api


def getFileProperties(fname):
    """
        Read all properties of the given file return them as a dictionary.
    """
    propNames = (
        "Comments",
        "InternalName",
        "ProductName",
        "CompanyName",
        "LegalCopyright",
        "ProductVersion",
        "FileDescription",
        "LegalTrademarks",
        "PrivateBuild",
        "FileVersion",
        "OriginalFilename",
        "SpecialBuild",
    )

    props = {"FixedFileInfo": None, "StringFileInfo": None, "FileVersion": None}

    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixedInfo = win32api.GetFileVersionInfo(fname, "\\")
        props["FixedFileInfo"] = fixedInfo
        props["FileVersion"] = "%d.%d.%d.%d" % (
            fixedInfo["FileVersionMS"] / 65536,
            fixedInfo["FileVersionMS"] % 65536,
            fixedInfo["FileVersionLS"] / 65536,
            fixedInfo["FileVersionLS"] % 65536,
        )

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(
            fname, "\\VarFileInfo\\Translation"
        )[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        strInfo = {}
        for propName in propNames:
            strInfoPath = u"\\StringFileInfo\\%04X%04X\\%s" % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        props["StringFileInfo"] = strInfo
    except:
        pass

    return props


chrome_browser = (
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
)  # -- ENTER YOUR Chrome.exe filepath


# returns whole string of version
cb_dictionary = getFileProperties(chrome_browser)

# substring version to capabable version
chrome_browser_version = cb_dictionary["FileVersion"][:2]


# grabs the next version of the chrome browser
nextVersion = str(int(chrome_browser_version) + 1)

# grabs the last version of the chrome browser
lastVersion = str(int(chrome_browser_version) - 1)