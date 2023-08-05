# Developer Setup Guide
This guide will give recommended workspace setup and installation instructions.

# Operating System Requirements
Verilator works on Linux and Mac for "verilating" but the generated models can be compiled on any OS.
Windows users can use WSL to verilate files, then compile on Windows.

Vivado works on Windows and Linux. For Mac users, I recommend using a Linux virtual machine. Or you can build on another computer or server. Abies will generate all the scripts necessary and provide automation tools.

PSoC Creator only works on Windows. Most developers don't need to work on the PSoC firmware.

So full compatibility is a little tricky, but all platforms will support a workflow for simulating HDL modules.

## Dependencies
Install python3.10 through normal methods for your OS. Make sure you install python3.10-dev and python3.10-venv

Some of these tools are not necessary, but help the build tools work better.

(Optional)Install CMake. With CMake, newer is always better so I recommend you install the latest. I will try to make this work with a lot of CMake versions. I recommend following CMake's instructions for your OS. CMake is also available as a python package that can be installed with pip, and Abies will use this method automatically.

(Optional) Install Ninja. Ninja is way faster than make, so I recommend using it. "apt install ninja-build" or install with homebrew on Mac. Windows will use MSVC's build system.

Install Verilator. If you are using "apt", it will have an older version of verilator. So I recommend building from source (follow the installation instructions) if you are using Ubuntu or other distros using apt. Mac users can install using homebrew.

Install SystemC. I recommend building from source. It should be pretty painless.
Build systemc using C++ 17.
Build and install systemc using cmake with this process:
```
cd systemc
cmake -G Ninja -S . -B build -DCMAKE_CXX_STANDARD=17 -DENABLE_PHASE_CALLBACKS_TRACING=OFF
cmake --build build
sudo cmake --install build # or "cmake --install build --prefix install_prefix
```

## Pip dependencies
Install these packages with pip. You can also pip install -r requirements.txt
These are the packages required for building Abies and plugins.

setuptools
wheel
build
pybind11
cmake
ninja
scikit-build

## Development Environment
I recommend using Visual Studio Code for a development environment. This will work will with the multiple different languages used in projects. Install the recommended/official Python extension, C++/Intellisense.

GTKWave is a good waveform viewer. There are VSCode extensions that kinda work too.

You should use a python virtual environment. 

Use code formatters that format on save. Use black for python, and the "Visual Studio" style for C++. Use default settings.

