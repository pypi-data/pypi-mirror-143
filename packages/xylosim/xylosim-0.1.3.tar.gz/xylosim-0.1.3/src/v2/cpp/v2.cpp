#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <string>

#include "XyloLayer.h"

namespace py = pybind11;

PYBIND11_MODULE(v2, m) {
    m.attr("__name__") = "xylosim.v2";
    py::class_<XyloLayer>(m, "XyloLayer", py::module_local())
        .def(py::init<const std::vector<std::vector<struct XyloSynapse*>>, // synapses_in,
                      const std::vector<std::vector<struct XyloSynapse*>>, // synapses_rec,
                      const std::vector<std::vector<struct XyloSynapse*>>, // synapses_out,
                      const std::vector<std::vector<uint16_t>>, // aliases,
                      const std::vector<int16_t>, // v_th,
                      const std::vector<int16_t>, // v_th_out,
                      const bool, // has_bias,
                      const std::vector<int16_t>, // bias,
                      const std::vector<int16_t>, // bias_out,
                      const int8_t, // weight_shift_inp,
                      const int8_t, // weight_shift_rec,
                      const int8_t, // weight_shift_out,
                      const std::vector<uint8_t>, // dash_mem,
                      const std::vector<uint8_t>, // dash_mem_out,
                      const std::vector<std::vector<uint8_t>>, // dash_syns,
                      const std::vector<std::vector<uint8_t>>, // dash_syns_out,
                      const std::string&> (), py::arg("synapses_in"), // name
                                              py::arg("synapses_rec"),
                                              py::arg("synapses_out"),
                                              py::arg("aliases"),
                                              py::arg("threshold"),
                                              py::arg("threshold_out"),
                                              py::arg("has_bias"),
                                              py::arg("bias"),
                                              py::arg("bias_out"),
                                              py::arg("weight_shift_inp"),
                                              py::arg("weight_shift_rec"),
                                              py::arg("weight_shift_out"),
                                              py::arg("dash_mem"),
                                              py::arg("dash_mem_out"),
                                              py::arg("dash_syns"),
                                              py::arg("dash_syns_out"),
                                              py::arg("name"))
        .def_readwrite("synapses_in", &XyloLayer::synapses_in)
        .def_readwrite("synapses_rec", &XyloLayer::synapses_rec)
        .def_readwrite("synapses_out", &XyloLayer::synapses_out)
        .def_readwrite("aliases", &XyloLayer::aliases)
        .def_readwrite("weight_shift_inp", &XyloLayer::weight_shift_inp)
        .def_readwrite("weight_shift_rec", &XyloLayer::weight_shift_rec)
        .def_readwrite("weight_shift_out", &XyloLayer::weight_shift_out)
        .def_readwrite("name", &XyloLayer::name)
        .def_readwrite("rec_i_syn", &XyloLayer::rec_i_syn)
        .def_readwrite("rec_i_syn2", &XyloLayer::rec_i_syn2)
        .def_readwrite("rec_v_mem", &XyloLayer::rec_v_mem)
        .def_readwrite("rec_i_syn_out", &XyloLayer::rec_i_syn_out)
        .def_readwrite("rec_i_syn2_out", &XyloLayer::rec_i_syn2_out)
        .def_readwrite("rec_v_mem_out", &XyloLayer::rec_v_mem_out)
        .def_readwrite("rec_recurrent_spikes", &XyloLayer::rec_recurrent_spikes)
        .def_readwrite("rec_out_spikes", &XyloLayer::rec_out_spikes)
        .def_readwrite("rec_hibernation_mode", &XyloLayer::rec_hibernation_mode)
        .def_readwrite("in_hibernation_mode", &XyloLayer::in_hibernation_mode)
        .def_readwrite("iaf_neurons", &XyloLayer::iaf_neurons)
        .def_readwrite("iaf_neurons_out", &XyloLayer::iaf_neurons_out)
        .def("evolve", &XyloLayer::evolve)
        .def("reset_all", &XyloLayer::reset_all);

    py::class_<XyloSynapse>(m, "XyloSynapse", py::module_local())
        .def(py::init<const uint16_t, 
                      const uint8_t,
                      const int8_t>(), py::arg("target_neuron_id"),
                                       py::arg("target_synapse_id"),
                                       py::arg("weight"))
        .def_readwrite("target_neuron_id", &XyloSynapse::target_neuron_id)
        .def_readwrite("target_synapse_id", &XyloSynapse::target_synapse_id)
        .def_readwrite("weight", &XyloSynapse::weight);

    py::class_<XyloIAFNeuron>(m, "XyloIAFNeuron", py::module_local())
        .def(py::init<const uint8_t, 
                      const std::vector<uint8_t>,
                      const int16_t,
                      const bool,
                      const int8_t>(), py::arg("dash_mem"),
                                       py::arg("dash_syns"),
                                       py::arg("v_th"),
                                       py::arg("has_bias"),
                                       py::arg("bias"))
        .def_readwrite("dash_mem", &XyloIAFNeuron::dash_mem)
        .def_readwrite("dash_syns", &XyloIAFNeuron::dash_syns)
        .def_readwrite("v_th", &XyloIAFNeuron::v_th)
        .def_readwrite("has_bias", &XyloIAFNeuron::has_bias)
        .def_readwrite("bias", &XyloIAFNeuron::bias);
}
