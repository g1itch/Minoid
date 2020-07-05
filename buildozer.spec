[app]

title = Minoid
package.name = minoid
package.domain = org.test
source.dir = .
source.exclude_dirs = recipes
version = 0.1.3
requirements = kivy,minode,setuptools
p4a.local_recipes = ./recipes
orientation = portrait
services = Minode:daemon.py:sticky
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.ndk = 19c
android.logcat_filters = *:S python:D
android.arch = armeabi-v7a

[buildozer]

log_level = 1
warn_on_root = 1
