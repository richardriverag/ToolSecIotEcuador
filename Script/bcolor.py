class bcolors:
    
    HEADER = '\33[92m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m' #AMARILLO
    FAIL = '\033[31m' #RED
    ENDC = '\033[0m'
    TITLE = '\033[34m' #Blue
    

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        self.TITLE = ''
