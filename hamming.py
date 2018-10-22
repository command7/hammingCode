from random import random
import matplotlib.pyplot as plt

#returns a random bit
def source():
    if random() < 0.5:
        return 0
    else:
        return 1

#uses source() to create and return a word of four random data bits
def createRandomMessage():
    dataBitArray = []
    dataBitArray.append(source())
    dataBitArray.append(source())
    dataBitArray.append(source())
    dataBitArray.append(source())
    return dataBitArray

#calculates the parity bits
def calculateParity(bitOne, bitTwo, bitThree, bitFour = None):
    numberOfOnes = 0
    numberOfZeros = 0
    if bitOne == 1:
        numberOfOnes += 1
    elif bitOne == 0:
        numberOfZeros += 1
    if bitTwo == 1:
        numberOfOnes += 1
    elif bitTwo == 0:
        numberOfZeros += 1
    if bitThree == 1:
        numberOfOnes += 1
    elif bitThree == 0:
        numberOfZeros += 1
    if bitFour == None:
        if numberOfOnes == 2:
            return 0
        else:
            return 1
    else:
        if bitFour == 1:
            numberOfOnes += 1
        elif bitFour == 0:
            numberOfZeros += 1
        if numberOfOnes == 2 or numberOfOnes == 4:
            return 0
        else:
            return 1

#toggles the bit in a specific location
def toggle(array, index):
    if array[index] == 1:
        array[index] = 0
    else:
        array[index] = 1

#encodes 4 bit word to 7 bit word using hamming code
def encoder(fourBitWord):
    parityOne = calculateParity(fourBitWord[0], fourBitWord[1], fourBitWord[3])
    parityTwo = calculateParity(fourBitWord[0], fourBitWord[2], fourBitWord[3])
    parityThree = calculateParity(fourBitWord[1], fourBitWord[2], fourBitWord[3])
    encodedMessage = [parityOne, parityTwo, fourBitWord[0], parityThree, fourBitWord[1], fourBitWord[2], fourBitWord[3]]
    return encodedMessage

#randomly introduces error into encoded bits.
def bsc(encodedMessage, Pc):
    encMsgWithErrors = encodedMessage[:]
    for i in range(0,7):
        if random() < Pc:
            toggle(encMsgWithErrors,i)
    return encMsgWithErrors

# def decoder(encodedMessage):
# return[encodedMessage[2],encodedMessage[4],encodedMessage[5],encodedMessage[6]]

#decodes hamming code
def decoder(encodedMessage):
    encMsg = encodedMessage[:]
    Syndrome = []
    Syndrome.append(calculateParity(encMsg[3], encMsg[4], encMsg[5], encMsg[6]))
    Syndrome.append(calculateParity(encMsg[1], encMsg[2], encMsg[5], encMsg[6]))
    Syndrome.append(calculateParity(encMsg[0], encMsg[2], encMsg[4], encMsg[6]))
    SyndromeString = ''
    for bit in Syndrome:
        SyndromeString += str(bit)
    SyndromeDecimal = int(SyndromeString, 2)
    if SyndromeDecimal == 0:
        decMsg = [encMsg[2],encMsg[4],encMsg[5],encMsg[6]]
        return decMsg
    if SyndromeDecimal == 1:
        toggle(encMsg, 0)
        decMsg = [encMsg[2],encMsg[4],encMsg[5],encMsg[6]]
        return decMsg
    if SyndromeDecimal == 2:
        toggle(encMsg, 1)
        decMsg = [encMsg[2],encMsg[4],encMsg[5],encMsg[6]]
        return decMsg
    if SyndromeDecimal == 3:
        toggle(encMsg, 2)
        decMsg = [encMsg[2],encMsg[4],encMsg[5],encMsg[6]]
        return decMsg
    if SyndromeDecimal == 4:
        toggle(encMsg, 3)
        decMsg = [encMsg[2],encMsg[4],encMsg[5],encMsg[6]]
        return decMsg
    if SyndromeDecimal == 5:
        toggle(encMsg, 4)
        decMsg = [encMsg[2],encMsg[4],encMsg[5],encMsg[6]]
        return decMsg
    if SyndromeDecimal == 6:
        toggle(encMsg, 5)
        decMsg = [encMsg[2],encMsg[4],encMsg[5],encMsg[6]]
        return decMsg
    if SyndromeDecimal == 7:
        toggle(encMsg, 6)
        decMsg = [encMsg[2],encMsg[4],encMsg[5],encMsg[6]]
        return decMsg

PcRange = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
errate = []
for Pc in PcRange:
    ecount = 0
    wcount = 0
    for i in range (1,1000000):
        wcount += 1
        word = createRandomMessage()
        encodedWord = encoder(word)
        errEncWord = bsc(encodedWord, Pc)
        decodedWord = decoder(errEncWord)
        for i in range(0,4):
            if word[i] != decodedWord[i]:
                ecount += 1
                break
        if ecount > 1000:
            errate.append(ecount/wcount)
            break
print(errate)

Pc = [0.1,0.09,0.08,0.07,0.06,0.05,0.04,0.03,0.02,0.01]
theober = [((1-pc)**7)+(7*pc)*((1-pc)**6) for pc in Pc]
expber = errate
plt.semilogy(Pc,theober,label="Theoretical")
plt.semilogy(Pc,expber,label="Experimental")
plt.semilogy(Pc,Pc,label="No code")
plt.legend(loc='upper right')
plt.gca().invert_xaxis()
plt.xlabel("Pc")
plt.ylabel("BER")
plt.grid()
plt.savefig('ber_hamming.png')
plt.close()
