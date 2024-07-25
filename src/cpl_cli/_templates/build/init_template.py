import textwrap


class InitTemplate:
    @staticmethod
    def get_init_py() -> str:
        string = textwrap.dedent(
            """\
            # -*- coding: utf-8 -*-
        
            \"\"\"
            $Name $Description
            ~~~~~~~~~~~~~~~~~~~
            
            $LongDescription
            
            :copyright: (c) $CopyrightDate $CopyrightName
            :license: $LicenseDescription
            
            \"\"\"
            
            __title__ = "$Title"
            __author__ = "$Author"
            __license__ = "$LicenseName"
            __copyright__ = "Copyright (c) $CopyrightDate $CopyrightName"
            __version__ = "$Version"
            
            from collections import namedtuple
            
            
            $Imports
            
            VersionInfo = namedtuple("VersionInfo", "major minor micro")
            version_info = VersionInfo(major="$Major", minor="$Minor", micro="$Micro")
        """
        )

        return string
