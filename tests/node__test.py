'''
Node test
'''
import pytest
from libsim.node import Node_SPM as Node_SPM


class MockMesh:
   def __init__(self,n_timestep):
        self.n_timestep=n_timestep
initial_concentration=7.0
test_parameter_list=[]
for i in range(1,10):
    test_parameter_list.append((i,initial_concentration))
    
mesh=MockMesh(10)
@pytest.mark.parametrize('inp, expected', test_parameter_list)
def test_spm_initial_concentration(inp,expected):

    node=Node_SPM(mesh,inp,inp,initial_concentration)
    assert node.concentration[0,0]==expected
    
def test_spm_x():
    mesh=MockMesh(10)
    node=Node_SPM(mesh,1,10.0,20)
    assert node.x==10
    
def test_spm_node_id():
    mesh=MockMesh(10)
    node=Node_SPM(mesh,1,10.0,20)
    assert node.node_id==1