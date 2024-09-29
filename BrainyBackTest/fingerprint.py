import random




class Fingerprint:


    _Fingerprints = []


    def __init__(self):
        
        pass
    #


    def new_fingerprint(self):

        while (True):

            newFingerPrint = random.randint(1000000, 10000000-1)

            if(newFingerPrint not in Fingerprint._Fingerprints):
                
                Fingerprint._Fingerprints.append(newFingerPrint)
                
                break
            #
        #


        return (Fingerprint._Fingerprints[-1])
    #
#