import os


def define_env(env):
    @env.macro
    def apppack_version():
        return os.environ.get("APPPACK_VERSION", "undefined")
