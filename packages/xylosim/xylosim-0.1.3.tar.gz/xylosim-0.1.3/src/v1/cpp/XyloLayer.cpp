#include "XyloLayer.h"
#include <iostream>

/**
 * Constructor of the layer. Needs all connectivity and neuron parameters.
 * The number of neurons is inferred by the length of dash_syns.
 * The number if outputs in inferred by the length of dash_syns_out.
 *
 *
 * @param synapses_in Vector of Synapse vectors. Each neuron has a vector of output synapses.
 * @param synapses_rec Vector of Synapse vectors. Each neuron has a vector of output synapses.
 * @param synapses_out Vector of Synapse vectors. Each neuron has a vector of output synapses.
 * @param aliases Vecor of int vectors. Each neurons can have one alias connection where its output spikes are copied to.
 * @param v_th Thresholds of the reservoir LIF neurons
 * @param v_th_out Thresholds of the readout LIF neurons
 * @param weight_shift_inp Bitshift to be applied to input weights
 * @param weight_shift_rec Bitshift to be applied to recurrent weights
 * @param weight_shift_out Bitshift to be applied to readout weights
 * @param dash_mem Bitshift to be used for the BitshiftDecay of the membrane potential of reservoir neurons
 * @param dash_mem_out Bitshift to be used for the BitshiftDecay of the membrane potential of readout neurons
 * @param dash_syns Bitshift to be used for the BitshiftDecay of the synaptic current of reservoir neurons. Can be more than one per neuron if multiple synapses are used per neuron.
 * @param dash_syns_out Bitshift to be used for the BitshiftDecay of the synaptic current of readout neurons. Can be more than one per neuron if multiple synapses are used per neuron.
 *
 */
XyloLayer::XyloLayer(const std::vector<std::vector<struct XyloSynapse*>>& synapses_in,
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
                     const std::string &name) : synapses_in(synapses_in),
                                                synapses_rec(synapses_rec),
                                                synapses_out(synapses_out),
                                                aliases(aliases),
                                                weight_shift_inp(weight_shift_inp),
                                                weight_shift_rec(weight_shift_rec),
                                                weight_shift_out(weight_shift_out),
                                                name(name)
{ 
    // Loop through all parameters of the reservoir neurons
    // and initialize them
    auto it_v_th = v_th.begin();
    auto it_dash_mem = dash_mem.begin();
    auto it_dash_syn = dash_syns.begin();
    while(it_dash_syn != dash_syns.end())
    {
        // init neuron
        iaf_neurons.push_back(new XyloIAFNeuron(*it_dash_mem++, 
                                                *it_dash_syn++, 
                                                *it_v_th++));

        // init recording for this neurons
        rec_i_syn.push_back(new std::vector<int16_t>());
        rec_i_syn2.push_back(new std::vector<int16_t>());
        rec_v_mem.push_back(new std::vector<int16_t>());

        // init spike buffer for this neuron
        recurrent_spikes.push_back(0);
    }

    // Loop through all parameters for readout neurons
    // and initialize them 
    auto it_v_th_out = v_th_out.begin();
    auto it_dash_mem_out = dash_mem_out.begin();
    auto it_dash_syn_out = dash_syns_out.begin();
    while(it_dash_syn_out != dash_syns_out.end())
    {
        // init readout neuron
        iaf_neurons_out.push_back(new XyloIAFNeuron(*it_dash_mem_out++, 
                                                      *it_dash_syn_out++,
                                                      *it_v_th_out++));

        // init recording
        rec_i_syn_out.push_back(new std::vector<int16_t>());
        rec_i_syn2_out.push_back(new std::vector<int16_t>());
        rec_v_mem_out.push_back(new std::vector<int16_t>());

        // init spike buffer
        out_spikes.push_back(0);
    }

}


/**
 * Evolves the complete network.\n
 * Takes a 2D vector as input with the shape (time, num_input_neurons) containing the number of input spikes. \n
 * Iterates over input time and executes the folling operation in this order: \n
 *      Deliver all input spikes of current timestep to their target neurons.\n
 *      Deliver all recurrent spikes from last timestep to their target neurons including output neurons. \n
 *      Evolve all neurons and storing their spikes for delivery in the next timestep.\n
 *      Evolve all output neurons and storing their spikes in the output buffer. \n
 *
 *  All membrane potentials, synaptic currents and spikes are recorded.
 *  
 *  Returns the output spikes.      
 *
 *  @param input 2D vector of input spikes (time, num_input_neurons)
 *  @return 2D vector of outpur spikes (time, num_readout_neurons)
 * 
 */
std::vector<std::vector<uint8_t>> XyloLayer::evolve(std::vector<std::vector<uint8_t>> input)
{
    clear_recordings();

    // iterate over input
    for (auto it_time = input.begin(); it_time != input.end(); ++it_time)
    {
        uint16_t time__ = std::distance(input.begin(), it_time);

        // deliver input spikes
        std::vector<uint8_t> inp_spikes = *it_time;
        deliver_spikes(inp_spikes, 
                       synapses_in,
                       iaf_neurons,
                       MAX_NUM_INP_SPIKES,
                       weight_shift_inp);
        
        // delivcer recurrent spikes to reservoir neurons
        deliver_spikes(recurrent_spikes, 
                       synapses_rec,
                       iaf_neurons,
                       MAX_NUM_SPIKES,
                       weight_shift_rec);
 
        // deliver recurrent spikes to readout neurons
        deliver_spikes(recurrent_spikes, 
                       synapses_out,
                       iaf_neurons_out,
                       MAX_NUM_SPIKES,
                       weight_shift_out);

        // clear recurrent spike buffer
        clear_recurrent_spikes();
        clear_output_spikes();
        
        // evolve neurons
        evolve_neurons(&iaf_neurons,
                       &aliases,
                       &rec_i_syn,
                       &rec_i_syn2,
                       &rec_v_mem,
                       MAX_NUM_SPIKES,
                       &recurrent_spikes);

        // evolve readout neurons
        evolve_neurons(&iaf_neurons_out,
                       nullptr,
                       &rec_i_syn_out,
                       &rec_i_syn2_out,
                       &rec_v_mem_out,
                       MAX_NUM_OUT_SPIKES,
                       &out_spikes);

        // save recurrent spikes in recordings
        rec_recurrent_spikes.push_back(std::vector<uint8_t>(recurrent_spikes));

        // save output spikes in recordings
        rec_out_spikes.push_back(std::vector<uint8_t>(out_spikes));
    }

    return rec_out_spikes;
}




/**
 * Delivers spikes to their target neurons.
 *
 * @param spikes The spikes vector must contain the number of spikes per neuron. The index determins the neuron id.
 * @param synapses Vector of synapse vectors. Each neuron has a vector of output synapses.
 * @param neurons Vector of neurons the synapses are targeting to.
 * @param max_spikes Limits the incoming spikes to this value.
 * @param weight_bitshift Left shift the weights of the synapses by this amount.
 */

void XyloLayer::deliver_spikes(std::vector<uint8_t> spikes, 
                               std::vector<std::vector<struct XyloSynapse*>> synapses,
                               std::vector<struct XyloIAFNeuron*> neurons,
                               int max_spikes,
                               int weight_bitshift)
{
    // Loop though all spikes / presynaptic neurons
    for (auto it_spikes = spikes.begin(); it_spikes != spikes.end(); ++it_spikes)
    {
        uint8_t num_spikes = *it_spikes;

        // limit number of input spikes
        if (num_spikes > max_spikes)
        {
            num_spikes = max_spikes;
        }

        if (num_spikes > 0)
        {
            // Neuron id is determined by index
            uint16_t pre_neuron_id = std::distance(spikes.begin(), it_spikes);

            // Get all output synapses of this neuron
            std::vector<XyloSynapse*> post_synapses = synapses.at(pre_neuron_id);
            
            // iterate over postsynaptic neurons
            for (auto it_synapse = post_synapses.begin(); 
                 it_synapse != post_synapses.end(); 
                 ++it_synapse)
            {
                XyloSynapse* synapse = *it_synapse;
                XyloIAFNeuron* post_neuron = neurons[synapse->target_neuron_id];

                // left shift weight and deliver spike to corresponding neuron / synapse
                for (int i = 0; i < num_spikes; ++i)
                    post_neuron->receiveSpike(synapse->weight << weight_bitshift, 
                                              synapse->target_synapse_id);
            }
        }
    }

}


/** 
 * Evolves a population of neurons and calls each neurons internal evolve function. 
 * This determins the number of spikes produced.
 * Saves states in recordings.
 *
 * @param neurons Vector of XyloNeurons to evolve
 * @param aliases Alias connections. Set to NULL if no aliases should be used
 * @param rec_isyn Recording for synaptic currents
 * @param rec_isyn2 Recording for synaptic currents of second synapse
 * @param rec_vmem Recording for membrane potentials 
 * @pamam max_spikes Number of spikes neurons are allowed to spike
 * @param spike_buffer Buffer for spike to deliver at next timestep 
 *
 */
void XyloLayer::evolve_neurons(std::vector<struct XyloIAFNeuron*>* neurons,
                               std::vector<std::vector<uint16_t>>* aliases,
                               std::vector<std::vector<int16_t>*>* rec_isyn,
                               std::vector<std::vector<int16_t>*>* rec_isyn2,
                               std::vector<std::vector<int16_t>*>* rec_vmem,
                               int max_spikes,
                               std::vector<uint8_t>* spike_buffer)
{
    // loop over all neurons
    for (auto it_neuron_id = neurons->begin(); 
         it_neuron_id != neurons->end(); 
         ++it_neuron_id)
    {
        XyloIAFNeuron* neuron = *it_neuron_id; 
        uint16_t neuron_id = std::distance(neurons->begin(), it_neuron_id);

        // check if this neuron has already some spikes as alias
        uint8_t num_spikes = spike_buffer->at(neuron_id);

        // call internal evolve function which return the number of spikes
        num_spikes = neuron->evolve(num_spikes, max_spikes);

        // buffer the spikes for delivery in the next timestep
        spike_buffer->at(neuron_id) = num_spikes; 

        // make aliases spike
        if (aliases != nullptr)
        {
            std::vector<uint16_t> alias = aliases->at(neuron_id);
            for (auto it_alias = alias.begin(); it_alias != alias.end(); ++it_alias)
            {
                uint16_t alias_neuron_id = *it_alias;

                // make sure the alias does not spike too often
                if (spike_buffer->at(alias_neuron_id) + num_spikes > max_spikes)
                {
                    // set alias spikes to max
                    spike_buffer->at(alias_neuron_id) = max_spikes;
                }
                else
                {
                    // add spikes to alias
                    spike_buffer->at(alias_neuron_id) += num_spikes;
                }
            }
        }

        // record isyn of this neuron
        rec_isyn->at(neuron_id)->push_back(neuron->i_syns.at(0));

        // record isyn2 of this neuron
        if (neuron->i_syns.size() > 1)
        {
            rec_isyn2->at(neuron_id)->push_back(neuron->i_syns.at(1));
        }           

        // record vmem of this neuron
        rec_vmem->at(neuron_id)->push_back(neuron->v_mem);
    }
}


/**
 * Resets all neurons and clears recordings.
 */
void XyloLayer::reset_all()
{
    // Loop thourgh all reservoir neurons and reset them
    for (auto it_neuron = iaf_neurons.begin(); 
         it_neuron != iaf_neurons.end(); 
         ++it_neuron)
    {
        XyloIAFNeuron* n = *it_neuron; 
        n->reset();
    }

    // Loop through all readout neurons and reset them
    for (auto it_neuron_out = iaf_neurons_out.begin(); 
         it_neuron_out != iaf_neurons_out.end(); 
         ++it_neuron_out)
    {
        XyloIAFNeuron* n = *it_neuron_out; 
        n->reset();
    }

    // reset recordings
    clear_recordings();

    // clear recurrent spike buffer
    clear_recurrent_spikes();

    // clear output spike buffer
    clear_output_spikes();
}

/**
 * Clears recurrent spike buffer
 */
void XyloLayer::clear_recurrent_spikes()
{
    // reset spike buffer for recurrent spikes
    for(unsigned int i=0; i<recurrent_spikes.size();i++){
        recurrent_spikes[i] = 0;
    }  
}


/**
 * Clears output spike buffer
 */
void XyloLayer::clear_output_spikes()
{
    // reset spike buffer for output spikes
    for(unsigned int i=0; i<out_spikes.size();i++){
        out_spikes[i] = 0;
    }  
}


/**
 * Clears all recordings.
 */ 
void XyloLayer::clear_recordings()
{
    // clear Isyn
    for (auto it_rec = rec_i_syn.begin();
         it_rec != rec_i_syn.end(); 
         ++it_rec)
    {
        std::vector<int16_t>* tmp = *it_rec;
        tmp->clear();
    }

    // clear Isyn2
    for (auto it_rec = rec_i_syn2.begin();
         it_rec != rec_i_syn2.end(); 
         ++it_rec)
    {
        std::vector<int16_t>* tmp = *it_rec;
        tmp->clear();
    }

    // clear Vmem 
    for (auto it_rec = rec_v_mem.begin(); 
         it_rec != rec_v_mem.end(); 
         ++it_rec)
    {
        std::vector<int16_t>* tmp = *it_rec;
        tmp->clear();
    }

    // clear Isyn out
    for (auto it_rec = rec_i_syn_out.begin(); 
         it_rec != rec_i_syn_out.end();
         ++it_rec)
    {
        std::vector<int16_t>* tmp = *it_rec;
        tmp->clear();
    }

    // clear Isyn2 out
    for (auto it_rec = rec_i_syn2_out.begin(); 
         it_rec != rec_i_syn2_out.end();
         ++it_rec)
    {
        std::vector<int16_t>* tmp = *it_rec;
        tmp->clear();
    }

    // clear Vmem out
    for (auto it_rec = rec_v_mem_out.begin();
         it_rec != rec_v_mem_out.end(); 
         ++it_rec)
    {
        std::vector<int16_t>* tmp = *it_rec;
        tmp->clear();
    }

    // clear recurrent spike recording 
    rec_recurrent_spikes.clear();

    // clear output spike recordings
    rec_out_spikes.clear();
}


