'''
Main test file
'''
import pytest

from libsim.mesh import Mesh1D_SPM as Mesh1D_SPM


    

test_parameter_list=[]
for i in range(1,10):
    test_parameter_list.append((i,7.0))
    

@pytest.mark.parametrize('inp, expected', test_parameter_list)
def test_spm_add_single_node(inp,expected):
    
    
    n_timestep=10
    length=10.0
    n_elements=10
    dr=1.0
    x_0=0.0
    mesh_test=Mesh1D_SPM(n_timestep)
    for i in range(inp):
        mesh_test.add_node(x_0,expected)
        print(i)
        print(mesh_test.node_container)
    print(mesh_test.node_container)
    print("inp")
    print(inp)
    assert len(mesh_test.node_container)==inp
    node_test=mesh_test.node_container[inp-1]
    print(len(mesh_test.node_container))
    print(expected)
    assert node_test.concentration[0,0]==expected

def test_spm_add_nodes():
    
    n_timestep=10
    length=10.0
    n_elements=10
    dr=1.0
    initial_concentration=7.0
    x_0=0.0
    mesh=Mesh1D_SPM(n_timestep)
    mesh.add_nodes(length,n_elements,initial_concentration)
    
    node=mesh.node_container[0]
    assert mesh.n_nodes==11
    assert mesh.node_id==11
    assert len(mesh.node_container)==11
    
    assert node.node_id==0
    assert node.x==x_0
    assert node.concentration[0,0]==initial_concentration
    
    node5=mesh.node_container[4]
    assert node5.node_id==4
    assert node5.x==4.0
    assert node5.concentration[0,0]==initial_concentration
    
def test_get_concentration_by_id():
    n_timestep=10
    length=10.0
    n_elements=10
    dr=1.0
    initial_concentration=7.0
    x_0=0.0
    mesh=Mesh1D_SPM(n_timestep)
    mesh.add_nodes(length,n_elements,initial_concentration)
    
    node=mesh.node_container[0]
    assert mesh.get_concentration_by_id(0,0)==initial_concentration
    
    node5=mesh.node_container[4]
    assert node5.node_id==4
    assert node5.x==4.0
    assert mesh.get_concentration_by_id(4,0)==initial_concentration
    

    


    

test_parameter_list=[]
for i in range(0,10):
    test_parameter_list.append((i,7.0))
    

@pytest.mark.parametrize('inp, expected', test_parameter_list)
def test_concentration(inp,expected):
    n_timestep=10
    length=10.0
    n_elements=10
    dr=1.0
    initial_concentration=7.0
    x_0=0.0
    mesh=Mesh1D_SPM(n_timestep)
    mesh.add_nodes(length,n_elements,initial_concentration)
    print(expected)
    assert mesh.node_container[inp].concentration[0,0]==expected
    assert mesh.get_concentration_by_id(inp,0)==expected
    

    
    
#test_parameter_list=[]
#for i in range(n_timestep):
#    test_parameter_list.append((i,2.0))
    

#@pytest.mark.parametrize('inp, expected', test_parameter_list) 

def test_concentration_set():
    n_timestep=10
    length=10.0
    n_elements=10
    dr=1.0
    initial_concentration=7.0
    x_0=0.0
    mesh=Mesh1D_SPM(n_timestep)
    mesh.add_nodes(length,n_elements,initial_concentration)
    mesh.node_container[2].concentration[0,0]=2.0
    assert mesh.node_container[2].concentration[0,0]==2.0