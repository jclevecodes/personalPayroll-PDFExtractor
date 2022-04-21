import pdfplumber
import re
# from tabula import read_pdf

# def getPrintStatus(line):
#     shouldPrint = False

plDictionary = {}

class PayrollLiability:
    def __init__(self):
        self.Agency = ""
        self.Rate = ""
        self.EEWithheld = ""
        self.ERContrib = ""

    def __str__(self):
        str = self.Agency + ", , , ," + self.EEWithheld + "," + self.ERContrib 
        return str

    def __repr__(self):
        str = self.Agency + ", , , ," + self.EEWithheld + "," + self.ERContrib
        return str
    
    @staticmethod
    def getHeader():
        str = "Agency,Rate,EEWithheld,ERContrib,EEWithheldADP,ERContribADP\n"
        return str
        
def processLine(line):

    #Removing Federal and State from start of lines
    if line.startswith("Federal "):
        line = line.replace("Federal ", "", 1).strip()
    elif line.startswith("State "):
        line = line.replace("State ", "", 1).strip()

    pl = PayrollLiability()

    #Split line into payroll liability parts
    delim = "-"
    line = re.sub("\s+", delim, line)
    liabilityParts = line.split(delim) 

    #Store required liability parts into PayrollLiability object
    pl.Agency = "$" + liabilityParts[0].replace(",", "")
    pl.EEWithheld = "$" + liabilityParts[1].replace(",", "")

    #Store optionable liability parts into PayrollLiability object
    if (line.startswith("SocialSecurity") or line.startswith("Medicare")):
        pl.ERContrib = "$" + liabilityParts[2].replace(",", "")

    plDictionary[pl.Agency] = pl
    #print(plDictionary)
        # print(liabilityParts)
        # print(line)
    #print(line)

if __name__ == "__main__":

    with pdfplumber.open("/Volumes/NO NAME/Payroll_Liability.pdf") as pdf:
        page = pdf.pages[1].extract_text()
        #print(page)
        #replacement = page.replace("\n", "\n\n")

        taxes = page.split("\n")
        #print(len(taxes))

    counter = 1
    shouldPrint = False

    for line in taxes:

        if shouldPrint:
            processLine(line)

        #Determination of print of status
        line = line.strip()
        if line.startswith("Agency"):
            shouldPrint = True
        elif line.startswith("TotalTaxes"):
            shouldPrint = False
        counter += 1

    #Write all liabilities to txt file
    payrollFile = open("payroll.csv", "w")
    payrollFile.write(PayrollLiability.getHeader())
    for key, value in plDictionary.items():
        payrollFile.write(str(value) + "\n")
    payrollFile.close()

    # df = tabula.read_pdf("/Volumes/NO NAME/Payroll_Liability.pdf")[1]
    # tabula.convert_into("Payroll_Liability.pdf", "Payroll_Liability.csv", output_format="csv", pages='all')
    # print(df)