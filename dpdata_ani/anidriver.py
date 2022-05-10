import dpdata
import torchani
import torch
import numpy as np
from torchani.units import hartree2ev
from dpdata.driver import Driver
from dpdata.periodic_table import Element


@Driver.register("ani")
class ANIDriver(Driver):
    def __init__(self, model, device: str=None):
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        self.model = model.to(self.device)

    def label(self, data):
        ori_sys = dpdata.System.from_dict({'data': data})
        labeled_sys = dpdata.LabeledSystem()
        atomic_z = np.array([Element(xx).Z for xx in data['atom_names']], dtype=int)

        species = np.array([atomic_z[data['atom_types']]])
        species = torch.tensor(species, device=self.device)

        for ss in ori_sys:
            coordinates = torch.tensor(ss['coords'],
                            requires_grad=True, device=self.device, dtype=torch.float32)
            energy = hartree2ev(self.model((species, coordinates)).energies)
            derivative = torch.autograd.grad(energy.sum(), coordinates)[0]
            force = -derivative
    
            data = ss.data
            data['energies'] = energy.cpu().detach().numpy().reshape((1, 1))
            data['forces'] = force.cpu().detach().numpy().reshape((1, ss.get_natoms(), 3))

            this_sys = dpdata.LabeledSystem.from_dict({'data': data})
            labeled_sys.append(this_sys)
        return labeled_sys.data

@Driver.register("ani/1x")
class ANI1xDriver(ANIDriver):
    def __init__(self, device: str=None):
        ANIDriver.__init__(self, torchani.models.ANI1x(periodic_table_index=True), device=device)
