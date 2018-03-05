import os
import pyslha
import subprocess

class MicroMegas:
    micromegas_path = "../../Coding/micromegas_5.0/T12A/main"

    def __init__(self, slha_file_path):
        self.slha_input_file_path = slha_file_path
        self.slha_output_file_path = "/tmp/{}-miromegas-output.slha".format(os.getpid())

        self.Omega = None
        self.proton_SI = None
        self.proton_SD = None
        self.neutron_SI = None
        self.neutron_SD = None

    def calculate(self):
        self.run_micromegas()
        self.read_slha_output()

    def run_micromegas(self):
        subprocess.call([self.micromegas_path, self.slha_input_file_path, self.slha_output_file_path],
                        stdout=open(os.devnull, 'wb'))

    def read_slha_output(self):
        data = pyslha.read(self.slha_output_file_path, ignorenomass=True)

        self.Omega = data.blocks["OMEGA"][1]

        self.proton_SI = data.blocks["DIRECT"][1]
        self.proton_SD = data.blocks["DIRECT"][2]
        self.neutron_SI = data.blocks["DIRECT"][3]
        self.neutron_SD = data.blocks["DIRECT"][4]