#define BITS_STATE 16
#define BITS_WEIGHT 8
#define MAX_NUM_INP_SPIKES 15 
#define MAX_NUM_SPIKES 31
#define MAX_NUM_OUT_SPIKES 1
#include <stdint.h>
#include <stdbool.h>
#include <iostream>
#include <cmath>
#include <vector> 

/**
 * 
 * The XyloIAFNeuron provides a bitwise exact implementation of the IAF neruon implemented on the Xylo chip.
 *
 */
struct XyloIAFNeuron 
{
    // parameters
    uint8_t dash_mem; // should be 4 bits.
    std::vector<uint8_t> dash_syns; // should be 4 bits.
    int16_t v_th;

    // states 
    int16_t v_mem;
    std::vector<int16_t> i_syns;

    // constructor
    XyloIAFNeuron(uint8_t dash_mem, std::vector<uint8_t> dash_syns, int16_t v_th);

    // functions
    void decayState();
    void receiveSpike(int16_t weight, uint8_t syn_id);
    uint8_t evolve(uint8_t num_spikes, uint8_t max_spikes);
    void reset();
};

int16_t decay(int16_t v, int8_t dash);

/**
 * Adds tow values safely. If the bitdepth is exceeded, the result is clamped to the maximal/minimal possible value.
 */
template <class T>
T safe_add(T x, T y, uint8_t bits)
{

    auto max_val = std::pow(2, bits-1) - 1;
    if (y < 0)
    {
        max_val = -std::pow(2, bits-1);
    }

    if (std::abs(max_val - x) > std::abs(y))
    {
        x += y;
    }
    else
    {
        x = max_val;
    }

    return x;
};


