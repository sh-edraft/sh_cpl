import pkg_resources


class Dependencies:
    _packages = []
    _cpl_packages = []

    _dependencies = dict(tuple(str(ws).split()) for ws in pkg_resources.working_set)
    for p in _dependencies:
        if str(p).startswith('cpl-'):
            _cpl_packages.append([p, _dependencies[p]])
            continue

        _packages.append([p, _dependencies[p]])

    @classmethod
    def get_cpl_packages(cls) -> list[list]:
        return cls._cpl_packages

    @classmethod
    def get_packages(cls) -> list[list]:
        return cls._packages
