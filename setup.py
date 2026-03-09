import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'sobits_speech_recognition'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, "launch"), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, "config"), glob('config/*.yaml')),
        (os.path.join('share', package_name, "sound_file"), glob('sound_file/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@example.com', 
    description='Integrated Speech Recognition Package for RoboCup',
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'stt_server = sobits_speech_recognition.stt_server:main',
            'dl_nemo = sobits_speech_recognition.download_utils.dl_nemo:main',
            'dl_vosk = sobits_speech_recognition.download_utils.dl_vosk:main',
            'dl_sherpa = sobits_speech_recognition.download_utils.dl_sherpa:main',
            'dl_whisper = sobits_speech_recognition.download_utils.dl_whisper:main',
        ],
    },
)