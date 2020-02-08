def ReadRequest(requestStr):
    if(requestStr[17:28]=="04030004FF00"):
        return "Disconnected";
    elif(requestStr[16:28]=="04030004FF01"):
        return "Connected"
    elif(requestStr[16:28]=="810300019000"):
        return "Data Response"
    elif(requestStr[16:28]=="810300029001"):
        return "Start Blowing"
    elif(requestStr[16:28]=="810300029002"):
        return "finish blowing"
    elif(requestStr[16:28]=="810300029003"):
        return "Blowing Discontinue"
    elif(requestStr[16:28]=="810300029004"):
        return "Refuse Blowing"
    elif(requestStr[16:28]=="810300029005"):
        return "Measurement Result Completion"
    elif(requestStr[16:26]=="8104000390"):
        result=FetchResult(requestStr)
        return "BAC Value is: "+str(result)+" %"

def FetchResult(responseStr):
    return (int(responseStr[28:30])*256+int(responseStr[26:28]))/100






