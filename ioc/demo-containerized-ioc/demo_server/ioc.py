from caproto import pva
import logging
from demo_server.ca import CAServer
import multiprocessing
import time

try:
	multiprocessing.set_start_method("spawn")
except:
	pass

logger = logging.getLogger(__name__)



class IOCServer():

	def __init__(self, pv_vals):

		self._exit_event =  multiprocessing.Event()
		
		
		#self._running_indicator = multiprocessing.Value("b", False)

		# exit events for triggering shutdown
		self._exit_event = multiprocessing.Event()
		ca_server_exit_event =  multiprocessing.Event()
		pva_server_exit_event = multiprocessing.Event()
		self._process_exit_events = [ca_server_exit_event, pva_server_exit_event, self._exit_event]


		self.ca_process = CAServer(	
			pv_vals,
			ca_server_exit_event
		)

		self._process_exit_events = [self.ca_process._exit_event, pva_server_exit_event, self._exit_event]


		#self.pva_process =


	def start(self):
		self.ca_process.start()

		while not any(
					[
						exit_event.is_set()
						for exit_event in self._process_exit_events
						+ [self._exit_event]
					]
				):
			try:
				time.sleep(1)

			except:
				# set exit events
				for exit_event in self._process_exit_events:
					exit_event.set()

				self.ca_process.join()
				print("Process joined")



if __name__ == "__main__":
	server = IOCServer(	
		{"test:ca:SCALAR": 0,
			"test:ca:ARRAY": [1, 0, 0]
		}
	)

	server.start()