


import opencortex.core as oc

import neuroml

nml_doc, network = oc.generate_network("SimpleNet")

scale = 7
min_pop_size = 1

def scale_pop_size(baseline):
    return max(min_pop_size, int(baseline*scale))

xDim = 500
yDim = 100
zDim = 500
offset = 0

#####   Cells

oc.include_opencortex_cell(nml_doc, 'izhikevich/RS.cell.nml')
# TODO: add method oc.add_spike_generator_poisson(...)
spike_gen = neuroml.SpikeGeneratorPoisson(id="poissonInput",
                                          average_rate="50Hz")
                                          
nml_doc.spike_generator_poissons.append(spike_gen)



#####   Synapses


oc.include_neuroml2_file(nml_doc,'AMPA_NMDA.synapse.nml')

                         

#####   Input types

                             
pfs100 = oc.add_poisson_firing_synapse(nml_doc,
                                   id="poissonFiringSyn100",
                                   average_rate="100 Hz",
                                   synapse_id='AMPA_noplast')
                                   
pg0 = oc.add_pulse_generator(nml_doc,
                       id="pg0",
                       delay="1000ms",
                       duration="1000ms",
                       amplitude="0.2nA")
                                     
                             
#####   Populations

pop0 = oc.add_population_in_rectangular_region(network,
                                              'pop0',
                                              'RS',
                                              scale_pop_size(1),
                                              0,offset,0,
                                              xDim,yDim,zDim)
offset+=yDim

pop1 = oc.add_population_in_rectangular_region(network,
                                              'pop1',
                                              'RS',
                                              scale_pop_size(1),
                                              0,offset,0,
                                              xDim,yDim,zDim)


#####   Projections


oc.add_probabilistic_projection(network,
                                "proj1",
                                pop0,
                                pop1,
                                'AMPA_NMDA',
                                0.7)
          
#####   Inputs

oc.add_inputs_to_population(network, 
                            "Stim0",
                            pop0, 
                            pfs100.id,
                            all_cells=True,
                            number_per_cell=5)

oc.add_inputs_to_population(network, 
                            "Stim1",
                            pop0, 
                            pg0.id,
                            all_cells=True)


#####   Save NeuroML and LEMS Simulation files

nml_file_name = '%s.net.nml'%network.id
oc.save_network(nml_doc, nml_file_name, validate=True)

lems_file_name, lems_sim = oc.generate_lems_simulation(nml_doc, 
                                                        network, 
                                                        nml_file_name, 
                                                        duration =      3000, 
                                                        dt =            0.025)
            
syn_conds = 'Conds'
lems_sim.create_display(syn_conds,syn_conds,-.1,1.6)     
syn_currs = 'Currs'
lems_sim.create_display(syn_currs,syn_currs,-.1,1.6)    
syn_blocks = 'NMDA_block'
lems_sim.create_display(syn_blocks,syn_blocks,-.1,1.1)    
syn_plast1 = 'AMPA_plast'
lems_sim.create_display(syn_plast1,syn_plast1,-80,30)    
syn_diff = 'AMPA_diff'
lems_sim.create_display(syn_diff,syn_diff,-10,30)    
syn_plast2 = 'AMPA_plast_factor'
lems_sim.create_display(syn_plast2,syn_plast2,-.1,1.1)               

for syn in ['AMPA','NMDA']:

    for i in range(pop1.size):
        lems_sim.add_line_to_display(syn_conds, '%s_g_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/g'%(pop1.id,i,pop1.component,syn),scale='1nS')
        lems_sim.add_line_to_display(syn_currs, '%s_i_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/i'%(pop1.id,i,pop1.component,syn),scale='1pA')
        if syn=='AMPA':
            #lems_sim.add_line_to_display(syn_plast1, '%s_u_dep_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/stdp/u_dep'%(pop1.id,i,pop1.component,syn),scale='1mV')
            lems_sim.add_line_to_display(syn_plast1, '%s_u_pot_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/stdp/u_pot'%(pop1.id,i,pop1.component,syn),scale='1mV')
            lems_sim.add_line_to_display(syn_plast1, '%s_u1_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/stdp/u_1'%(pop1.id,i,pop1.component,syn),scale='1mV')
            
            #lems_sim.add_line_to_display(syn_diff, '%s_dep_diff_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/stdp/u_dep_diff'%(pop1.id,i,pop1.component,syn),scale='1mV')
            lems_sim.add_line_to_display(syn_diff, '%s_pot_diff_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/stdp/u_pot_diff'%(pop1.id,i,pop1.component,syn),scale='1mV')
            lems_sim.add_line_to_display(syn_diff, '%s_v_diff_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/stdp/v_diff'%(pop1.id,i,pop1.component,syn),scale='1mV')
            
            lems_sim.add_line_to_display(syn_plast2, '%s_p_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/stdp/plasticityFactor'%(pop1.id,i,pop1.component,syn),scale='1')
            #lems_sim.add_line_to_display(syn_plast2, '%s_x_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/stdp/x'%(pop1.id,i,pop1.component,syn),scale='1')
            #lems_sim.add_line_to_display(syn_plast2, '%s_ltpr_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/stdp/ltp_rate'%(pop1.id,i,pop1.component,syn),scale='1')
            
        if syn=='NMDA':
            lems_sim.add_line_to_display(syn_blocks, '%s_block_%i'%(syn,i), '%s/%i/%s/synapses:AMPA_NMDA:0/%s/blockFactor'%(pop1.id,i,pop1.component,syn),scale='1')
            
    #create_output_file[ampa_conds,ampa_conds+".dat"]

lems_sim.save_to_file(lems_file_name)
                                              
