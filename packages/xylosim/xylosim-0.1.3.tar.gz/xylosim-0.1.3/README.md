# XyloSim

XyloSim provides tools to simulate the Pollen hardware precisely (bit-precise) and fast using C++. For convenience, the C++ functions are made visible to Python using Pybind11.

## Sources

The C++ version consists of the IAF neuron dynamics in XyloIAFNeuron.cpp and the simulation logic (spike production and routing) in XyloLayer.cpp.
C++ functionality is made visible to Python using Pybind11.

## Compilation

Install as Python package using either

```
pip install --upgrade .
```

or

```
python setup.py install
```


## Version 1

The first version ("xylosim.v1") is bitwise exact to the Xylo hardware with the hardware version number X.

## Version 2

The second version ("xylosim.v2") is bitwise exact to the Xylo hardware with the hardware version number Y.

New functionality such as biases and hibernation mode is implemented.

