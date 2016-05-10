import subprocess
import gzip

class Parse(object):
    wheels=9
    file_list = []
    d = {}
        
    def __init__(self,location):
        self.location = location
        
    def checkIfNotPresentAndSet(self, f):
        if (f not in self.file_list):
            self.file_list.append(f)
            return True
        else:
            return False
    
    def openAndSet(self, fil):
        f = self.location+'/'+fil
        if f.endswith('.gz'):
            logs = gzip.open(f, 'rb')
        else:
            logs = open(f, 'rb')
            
        for line in logs:

            #Add lob to the Data Structure only if "TCP_TUNNEL" and "TCP_MISS" in the line
            if "TCP_TUNNEL" in line or "TCP_MISS" in line:
                l = line.split()
                if len(l) < 10:
                    print "Invalid File"
                    break
                ip = l[2]
                url = l[6]
                payloadLen = l[4]
                timeStamp = l[0]
                                
                urlDict = {}
                payloadTimeList = []
                payloadTimeList = self.getlistPayloadTime(payloadLen,timeStamp)
                urlDict = self.getUrlDict(url, payloadTimeList)
                    
                #check if IP exists in the dictionary
                if ip in self.d:
                    
                    #check if url is in the that IP's list of URLs
                    if url in self.d[ip]:
                                        
                        #Find th URL
                        for item in self.d[ip]:
                                if url in item:
                                    item[url].append(payloadTimeList)
        
                    else:
                        self.d[ip].append(urlDict)
                        
                else:
                    self.d.setdefault(ip, [])
                    self.d[ip].append(urlDict)


    def getlistPayloadTime(self, payload, time):
        PayloadTime = []
        PayloadTime.append(payload)
        PayloadTime.append(time)
        return PayloadTime
        
    def getUrlDict(self, url, payloadTimeList):
        urlDict = {}
        urlDict.setdefault(url, [])
        urlDict[url].append(payloadTimeList)
        return urlDict
        
    def main(self):
    #               while(1):
        p = subprocess.Popen(["ls", self.location], stdout=subprocess.PIPE)
        output, err = p.communicate()
        files = output.split()
        for fil in files:
            if(self.checkIfNotPresentAndSet(fil)):
                self.openAndSet(fil)
                    return self.d