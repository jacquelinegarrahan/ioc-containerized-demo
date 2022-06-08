from caproto import pva
import logging
from demo_server.ca import CAServer
from demo_server.pva import PVAServer
import multiprocessing
import time

try:
	multiprocessing.set_start_method("spawn")
except:
	pass

logger = logging.getLogger(__name__)



class IOCServer():

	def __init__(self, pv_vals, serve_pva=True, serve_ca=False):

		# exit events for triggering shutdown
		self._exit_event = multiprocessing.Event()

		self._process_exit_events = [self._exit_event]

		self.pva_process=None
		if serve_pva:
			self.pva_process = PVAServer(	
				pv_vals,
			)
			self._process_exit_events.append(self.pva_process.exit_event)

		self.ca_process=None
		if serve_ca:
			self.ca_process = CAServer(	
				pv_vals,
			)
			self._process_exit_events.append(self.ca_process.exit_event)


	def start(self):
		if self.pva_process is not None:
			self.pva_process.start()

		elif self.ca_process is not None:
			self.ca_process.start()

		while not any(
					[
						exit_event.is_set()
						for exit_event in self._process_exit_events
					]
				):
			try:
				time.sleep(1)

			except:
				# set exit events
				for exit_event in self._process_exit_events:
					exit_event.set()

				if self.ca_process is not None:
					self.ca_process.join()

				if self.pva_process is not None:
					self.pva_process.join()
