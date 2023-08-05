# Abies
#### Audio Processing Framework


## Project Goals


There are two aspects to Abies. The hardware and software.

The hardware will be an FPGA-based real-time audio processing pipeline. The Abies platform will have I2S connections to ADCs, DACs, and a microcontroller. As well as other peripherals like analog controls and MIDI. There will also be a microcontroller to act as a USB audio interface and data interface. This will let people use a variety of audio sources/sinks. The first application will be a guitar effects "pedal". 

---

Abies software is a set of python-based tools used for designing and connecting audio effects. The goal is to allow for rapid prototyping of different effects chains and configurations. FPGA builds can take a very long time, so we need an easy way to test different configurations without spending hours compiling. Then once the simulation sounds good, it can be built and uploaded to the FPGA. Abies will use a plugin framework so pre-compiled plugins can be loaded at runtime.


## Simulation
To do this, we will first focus on running simulations. We will use SystemC as the backbone of the testing framework. SystemC implements all the necessary constructs to run cycle-based simulations with multiple models at a time. Then we can build "plugins" that can be saved, shared, and loaded at runtime. C++ simulations should be pretty fast and plugins won't need to be recompiled. Configurations can be specified with a netlist, and the simulator will handle the rest. The simulation will use audio files as an input and will save an audio file at the end.

## Builder
Verilator can compile verilog code to a SystemC model. The Abies C++ libray will supply templates to wrap the verilated class so that it will be compatible with the framework. Abies can generate all of the files necessary to build this library as a cmake project. Then Abies will use pybind11, cmake, and scikit-build to build a python module as the end product. This sounds rather complicated, but from the user perspective, it will be only a few python functions. *Most* plugins will use the default use case and there should be very few exceptions. These plugins can be uploaded to pypi.org.

Pybind11 is convenient, but it has limited CPython API compatibility. Wheels built with pybind11 will only be compatible with the version of Python that they were built with. I don't mind building for many python versions, but I don't want to force developers to do that too. And I want users to not have to compile plugins. They will only need to install python3.10. So we will design this project requiring Python3.10 for all builds. Modules can always be built from an sdist if you want to use a different version of python. I recommend using a virtual environment, and Abies may even use virtual environments behind the scenes anyways.


## Application
The python application can import modules, then it will handle running simulations. It will have a command line interface, and eventually a gui. It will be very simple to connect modules. Users will only need to use a little python or edit config files. Plugin designers will only need to know verilog for the HDL design and a little python. No direct C++ programming should be required (unless you want to).


--- 

## Final Remarks
My primary focus is to make this project accessible to as many people as possible. There may be people interested in the musical aspects that may not want to learn complex programming or engineering concepts. So we'll keep it simple and follow the design of other audio daws that people may be familiar with already.

I also want to make this project just as accessible to people interested in designing effects. Trying to use/learn Verilog, Python, and C++ all at the same time can be a bit intimidating and challenging for beginners. So designing plugins will be simple as well. Abies will supply project templates and software tools to make running simulations and building plugins one click operations. 99% of modules should work fine using the base template.

To make this all work in an easy way, plugin modules will need to adhere to certain standards. This will include naming conventions, following bus standards, implementing certain parameters and ports, and follow Abies standards. Abies will provide verification tools to check if designs obey all the rules.

