# Adjust the paths!
export ANDROIDSDK="/home/gus/apps/libs/android/sdk"
#"/home/gus/.buildozer/android/platform/android-sdk-20" 
#"$HOME/Documents/android-sdk-21"
export ANDROIDNDK="/home/gus/apps/libs/android/ndk/android-ndk-r13b" #"$HOME/Documents/android-ndk-r10e"
export ANDROIDAPI="22"  # Minimum API version your application require
export ANDROIDNDKVER="r13b"  # Version of the NDK you installed

p4a apk --private lab --package=kothvandir.otracker --name "Object tracker" --version 0.1 --bootstrap=sdl2 --requirements=python2,numpy,matplotlib,kivy --arch=armeabi-v7a

#cp /usr/local/lib/python2.7/dist-packages/cv2.so /home/gus/.local/share/python-for-android/dists/unnamed_dist_4/python-install/lib/python2.7/site-packages