#include <vector> 
#include <map>
#include <string>

#include "XyloIAFNeuron.h"

/**
 * Struct for storing synaptic parameters. These contain post-synaptic neuron id, synapse id and weight.
 * The pre-synaptic neuron id is inferred from the data structure.
 */
struct XyloSynapse 
{
    uint16_t target_neuron_id;
    uint8_t target_synapse_id;
    int8_t weight;

    // constructor
    XyloSynapse(uint16_t target_neuron_id,
                uint8_t target_synapse_id, 
                int8_t weight) : target_neuron_id(target_neuron_id),
                                 target_synapse_id(target_synapse_id),
                                 weight(weight) {};
};

/**
 * Class containing the neurons, connectivity and recordings. Provides bit-wise exact implementation of the Xylo chip.
 */
struct XyloLayer 
{
    // connectivity params
    std::vector<std::vector<struct XyloSynapse*>> synapses_in;
    std::vector<std::vector<struct XyloSynapse*>> synapses_rec;
    std::vector<std::vector<struct XyloSynapse*>> synapses_out;
    std::vector<std::vector<uint16_t>> aliases;

    // neurons (rec and out)
    std::vector<struct XyloIAFNeuron*> iaf_neurons;
    std::vector<struct XyloIAFNeuron*> iaf_neurons_out;

    // global neurons weight shifts 
    int8_t weight_shift_inp;
    int8_t weight_shift_rec;
    int8_t weight_shift_out;

    // spike buffers
    std::vector<uint8_t> recurrent_spikes;
    std::vector<uint8_t> out_spikes;

    // recordings 
    std::string name;
    std::vector<std::vector<int16_t>*> rec_i_syn;
    std::vector<std::vector<int16_t>*> rec_i_syn2;
    std::vector<std::vector<int16_t>*> rec_v_mem;
    std::vector<std::vector<int16_t>*> rec_i_syn_out;
    std::vector<std::vector<int16_t>*> rec_i_syn2_out;
    std::vector<std::vector<int16_t>*> rec_v_mem_out;

    std::vector<std::vector<uint8_t>> rec_recurrent_spikes;
    std::vector<std::vector<uint8_t>> rec_out_spikes;


    // constructor
    XyloLayer(const std::vector<std::vector<struct XyloSynapse*>>& synapses_in,
              const std::vector<std::vector<struct XyloSynapse*>>& synapses_rec,
              const std::vector<std::vector<struct XyloSynapse*>>& synapses_out,
              const std::vector<std::vector<uint16_t>>& aliases,
              const std::vector<int16_t> v_th,
              const std::vector<int16_t> v_th_out,
              const int8_t weight_shift_inp,
              const int8_t weight_shift_rec,
              const int8_t weight_shift_out,
              const std::vector<uint8_t>& dash_mem,
              const std::vector<uint8_t>& dash_mem_out,
              const std::vector<std::vector<uint8_t>>& dash_syns,
              const std::vector<std::vector<uint8_t>>& dash_syns_out,
              const std::string &name);


    // functions
    std::vector<std::vector<uint8_t>> evolve(std::vector<std::vector<uint8_t>>);

    void deliver_spikes(std::vector<uint8_t> spikes, 
                        std::vector<std::vector<struct XyloSynapse*>> synapses,
                        std::vector<struct XyloIAFNeuron*> neurons,
                        int max_spikes,
                        int weight_bitshift);

    void evolve_neurons(std::vector<struct XyloIAFNeuron*>* neurons,
                        std::vector<std::vector<uint16_t>>* aliases,
                        std::vector<std::vector<int16_t>*>* rec_isyn,
                        std::vector<std::vector<int16_t>*>* rec_isyn2,
                        std::vector<std::vector<int16_t>*>* rec_vmem,
                        int max_spikes,
                        std::vector<uint8_t>* spike_buffer);

    void reset_all();
    void clear_recordings();
    void clear_recurrent_spikes();
    void clear_output_spikes();
};
