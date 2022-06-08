import multiprocessing 
from p4p.server import Server
from p4p.server.thread import SharedPV
from p4p.nt import NTScalar, NTNDArray
import numpy as np
import time



class Handler(object):
    def put(self, pv, op):
        # allow client to modify all fields.  eg. including .timeStamp
        pv.post(op.value())
        op.done()


class PVAServer(multiprocessing.Process):

	def __init__(
		self,
		pv_vals,
		*args,
		**kwargs
	) -> None:
		"""Initialize server process."""
		super().__init__(*args, **kwargs)
		self._exit_event = multiprocessing.Event()
		self._providers = {}
		self._pv_vals = pv_vals

	def run(self):
		self.build_ioc()

		server =  Server(providers=[self._providers])

		while not self._exit_event.is_set():
			try:
				time.sleep(0.1)

			except:
				self._exit_event.set()
				server.stop()


	def build_ioc(self):
		for pvname, val in self._pv_vals.items():
			if isinstance(val, (float,int, )):
				self._providers[pvname] = SharedPV(nt=NTScalar('d'), # scalar double
              	initial=val, handler=Handler()) 

			elif isinstance(val, (list, np.ndarray)):
				self._providers[pvname] =  SharedPV(nt=NTNDArray(),
              	initial=val, handler=Handler()) 
				
if __name__ == "__main__":
	import os
	my_env = os.environ.copy()
	server = PVAServer(	
		{"test:ca:SCALAR": 0,
			"test:ca:ARRAY": [1, 0, 0]
		},
	)

	server.run()
