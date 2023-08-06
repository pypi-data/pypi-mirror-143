#include "XyloIAFNeuron.h"

/**
 * Bitshift decay
 *
 * @param v Value to decay
 * @param dash Bitshift to be applied
 * @return change of v
 */
int16_t decay(int16_t v, int8_t dash)
{
    int16_t dv = 0;
    
    // shift value
    dv = v >> dash;

    // set minimus decay to one with correct sign
    if (dv == 0)
    {
        if (v > 0)
            dv = 1;
    
        else if (v < 0)
            dv = -1;
    }

    return dv;
}


/**
 * The constructor takes the single neuron parameters as arguments.
 * The parameters are the membrane and synaptic time constants (as bit shifts) as well as the threshold.
 * Time constants are called dash here, as the exponential decay is implemented as bitshift.
 * Internally, the number of synapses are inferred by the length of the synaptic time constant vector.
 *
 * @param dash_mem Bitshift for membrane decay
 * @param dash_syns Vector of bitshifts for synaptic decay
 * @param v_th Thresholds of neuron
 * @param has_bias Flag to indicate to use biases
 * @param bias Value of bias
 */
XyloIAFNeuron::XyloIAFNeuron(uint8_t dash_mem, 
                             std::vector<uint8_t> dash_syns,
                             int16_t v_th,
                             bool has_bias,
                             int16_t bias): dash_mem(dash_mem),
                                            dash_syns(dash_syns),
                                            v_th(v_th),
                                            has_bias(has_bias),
                                            bias(bias)
{
    v_mem = 0;
    for (auto it_dash_syn = dash_syns.begin(); it_dash_syn != dash_syns.end(); ++it_dash_syn)
    {
        i_syns.push_back(0);
    }
}

/**
 * Adds the weight of a pre-synaptic spike to the corresponding synaptic current. 
 * The addition is done safely to prevent overflow.
 *
 * @param weight Weight of connection
 * @param syn_id Synapse ID
 */
void XyloIAFNeuron::receiveSpike(int16_t weight, uint8_t syn_id)
{
    int16_t* i_syn = &i_syns.at(syn_id); 
    *i_syn = safe_add(*i_syn, weight, BITS_STATE);
}

/**
 * Evolves the neuron by one timestep, taking the current number of spikes (from aliases) and the maximal number of spikes into account.
 * The evolution includes the following operations in this order:\n
 *     Decay states
 *     Adding all synaptic currents to the membrane potential.\n
 *     Add bias to membrane potential.\n
 *     Check for threshold crossing and calculate number of spikes.\n
 *     Limit number of spikes to max_spikes.\n
 *     Subtract membrane potential by number of spikes times threshold.\n
 *
 * Decays the membrane potential and the synaptic currents using bitshift decay.
 * A value is first bitshifted by a 'dash' bits. The result is subtracted from the original value. If the decay is zero, the value is decayed by one instead.
 * The decay is sensitive to the sign of the value.
 * Equation: \n
 * dv = max(v >> dash, sign(v) * 1) \n
 * v = v - dv \n
 * Returns number of spikes.    
 * All operations are done safely to prevent overflow.
 *
 * @param num_spikes Initial number of spikes (from alias sources)
 * @param max_spikes Number the neuron is allowed to spike
 * @param go_hibernation_mode Flag to be unset if something is happening in the neuron (decay)
 * @return number of spikes
 */
uint8_t XyloIAFNeuron::evolve(uint8_t num_spikes, uint8_t max_spikes, bool* go_hibernation_mode)
{
    // decay isyns
    auto it_dash_syn = dash_syns.begin();
    for (auto it_i_syn = i_syns.begin(); it_i_syn != i_syns.end(); ++it_i_syn)
    {
        uint8_t dash_syn = *it_dash_syn;

        // Set HM to false if synaptic current is changeing 
        int16_t di_syn = decay(*it_i_syn, dash_syn);
        if (di_syn != 0) 
            *go_hibernation_mode = false;

        // decay isyn
        *it_i_syn -= di_syn; 
        ++it_dash_syn;
    }

    // sum up all input currents
    long i_syn = 0;
    for (auto it_i_syn = i_syns.begin(); it_i_syn != i_syns.end(); ++it_i_syn)
    {
        i_syn += *it_i_syn;
    }

    // add synaptic current to membrane potential
    int16_t dv_mem = -decay(v_mem, dash_mem);
    dv_mem = (int16_t)(safe_add((long)(dv_mem), i_syn, BITS_STATE));

    // add bias to Vmem
    if (has_bias)
        dv_mem = safe_add(dv_mem, bias, BITS_STATE);

    // Set HM to false if membrane potential is changeing 
    if (dv_mem != 0) 
        *go_hibernation_mode = false;

    // integrate input to vmem 
    v_mem = safe_add(v_mem, dv_mem, BITS_STATE);

    while (v_mem >= v_th)
    {
        // check if max_num_spikes is reached
        if (num_spikes < max_spikes)
        {
            // add number of spikes and reduce vmem by threshold
            ++num_spikes; 
            v_mem -= v_th;
        }
        else{
            // max spikes reached, break loop
            break;
        }
    }

    return num_spikes;
}

/**
 * Resets membrane potential and synaptic current to zero.
 */
void XyloIAFNeuron::reset()
{
    // reset vmem
    v_mem = 0;
    for (auto it_i_syn = i_syns.begin(); it_i_syn != i_syns.end(); ++it_i_syn)
    {
        // reset all isyns
        *it_i_syn = 0;
    }
}

