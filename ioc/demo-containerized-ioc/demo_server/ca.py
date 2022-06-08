from caproto.server import PVGroup, pvproperty, run
import multiprocessing 
import logging

logger = logging.getLogger(__name__)


class CAServer(multiprocessing.Process):

	def __init__(
		self,
		pv_vals,
		*args,
		**kwargs
	) -> None:
		"""Initialize CA server process."""
		super().__init__(*args, **kwargs)
		self.exit_event = multiprocessing.Event()
		self.ioc =  None
		self.pv_vals = pv_vals

	def run(self) -> None:
		"""Start server process."""
		self.ioc =  self.build_ioc()
		try:
			run(self.ioc.pvdb)
		except Exception as e:
			self.exit_event.set()
			raise e


	def build_ioc(self):
		attributes = {key: pvproperty(value=value, name=key) for  key, value in self.pv_vals.items()}
		ioc_type = type("MyIOC", (PVGroup,), attributes) 

		return ioc_type(prefix="")
