class Logger:
    def __init__(self,acik=True):
        self.acik = acik
        
    def acKapa(self):
        self.acik = not self.acik
    
    def log(self,kaynak,konu,*ayrintilar):
        if self.acik:
            print(kaynak,":",end=" ")
            print(konu,*ayrintilar,sep=" - ")
            
if __name__ == "__main__":
    logger = Logger()
    logger.log("Deneyici","Test - 1","Bu birinci test")
    logger.acKapa()
    logger.log("Deneyici","Test - 2","Bu ikinci test")
    logger.acKapa()
    logger.log("Deneyici","Test - 3","Bu üçüncü test")