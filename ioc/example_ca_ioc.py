from demo_server.ioc import IOCServer


if __name__ == "__main__":
	server = IOCServer(	
		{"test:k8:pv:SCALAR": 0,
			"test:k8:pv:ARRAY": [1, 0, 0]
		},
        serve_pva=False, serve_ca=True
	)

	server.start()