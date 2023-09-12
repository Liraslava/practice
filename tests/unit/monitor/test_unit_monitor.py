from policies import check_operation
import pytest
from params import configurations



@pytest.mark.parametrize('data', configurations)
def test_unit_monitor(data):    
    assert data['result'] == check_operation(data['id'], data)
   








