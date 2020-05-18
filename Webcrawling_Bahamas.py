from selenium import webdriver
import os
import time
import string
import pyodbc
import pypyodbc

#Invoke URL
baseURL = "https://www.luxuryretreats.com/"
driver = webdriver.Chrome()
driver.get(baseURL)
driver.maximize_window()
driver.implicitly_wait(20)

#Capture landing page heading

pageHeading = driver.find_element_by_xpath("//div[@class='_26gx0u9']")
pageHeadingText = pageHeading.text
#time.sleep(5)

#Validate Luxury Retreat Home page heading

if pageHeading.is_displayed():
    print("Luxury Retreat Home page heading displayed properly : " + str(pageHeadingText))
else:
    print("Luxury Retreat Home page heading not being displayed properly")

#Verify Search button display
objLocation= driver.find_element_by_xpath("//input[@id='Koan-guided-search-location__input']")
if objLocation.is_displayed():
    print("Location input box is Present in the page ")
else:
    print("Location input box is not present")

#Click on Search button
objLocation.click()
objLocation.send_keys("Bahamas, Caribbean")
searchBtn = driver.find_element_by_xpath("//button[@type='submit' and @class='_4ghhpo6']")
if searchBtn.is_displayed():
    print("Search Button is Present")
else:
    print("Search button is not present")

#Click on Search button
searchBtn.click()

#time.sleep(15)

nextPageHeading = driver.find_element_by_xpath("//span[@class='_kmlcs7']")
nextPageHeadingText = nextPageHeading.text

if nextPageHeading.is_displayed():
    print("User has clicked on Search button and  navigated successfully to Searched page. Heading :" + str(nextPageHeadingText))
    print("Searched page Heading :" + str(nextPageHeadingText))
else:
    print("User has not been navigated successfully to Searched page")

#Capture heading for Searched page
ResortHeading = driver.find_element_by_xpath("//h3[@class='_1mafdrow']//div")
ResortsHeadingText = str(ResortHeading.text)
print(ResortsHeadingText)
ResortsHeadingText_Splitted = ResortsHeadingText.split()

NoOfResortsCaptured=ResortsHeadingText_Splitted[0]
#Print total No of Resorts
print("Total No. of Resorts captured in heading of first page is:" + NoOfResortsCaptured)

# Capture Resort Names and store into list

ResortNames = driver.find_elements_by_xpath("//div[@class='_1p0spma2']")

# Get No of items in list and print the number
#NoOfResortsDisplayed = len(ResortNames)
#print("No of Resorts displayed in the page:" + str(NoOfResortsDisplayed))

# Capture Resort Names and store into list
masterList=[]
ResortNameList=[]
currentPage=1
nextBtn=driver.find_element_by_xpath("//a[@aria-label='Next']")

totalNoOfPagesObj= driver.find_element_by_xpath("//li[@class='_i66xk8d']/preceding-sibling::li[1]")

totalNoOfPages=totalNoOfPagesObj.text

print("Total No of Pages in the application:" +str(totalNoOfPages))
try:
    while(currentPage<=int(totalNoOfPages)):
        ResortNames = driver.find_elements_by_xpath("//div[@class='_1p0spma2']")
        print("User is currently in page =" + str(currentPage))
        print("Number of resorts in page " + str(currentPage) + " is: " + str(len(ResortNames)))
        NoOfResortsDisplayed = len(ResortNames)

        masterList = masterList + ResortNames
        for resort in range(NoOfResortsDisplayed):
            ResortNameList.append(ResortNames[resort].text)

        if currentPage<int(totalNoOfPages):
            print("Next button is displayed in page: " + str(currentPage))
            nextBtn.click()
            time.sleep(2)

        elif currentPage==int(totalNoOfPages):
            break
        else:
            print("Next button is not displayed in page: " + str(currentPage))

        driver.execute_script("window.scrollTo(0,2100);")
        time.sleep(3)
        currentPage = currentPage +1

except StaleElementReferenceException:
#    raise Exception("This is an exception")
    print("next button is not present in last page")

# Get No of items in list and print the number
NoOfResortsAllPages = len(ResortNameList)
print("Number of Resorts displayed in all the pages:" + str(NoOfResortsAllPages))

if str(NoOfResortsCaptured)==str(NoOfResortsCaptured):
    print("Number of elemnts captured in heading of first page is matching with total number of Resorts in all pages")
# Print Names of all the Resorts
for resorts in range(NoOfResortsAllPages):
    print("Name of Resort " + str(resorts) + " is: " + ResortNameList[resorts])

#Create connection string
con = pyodbc.connect('Driver={SQL Server};'
                     'Server=sezcpu219;'
                     'Database=PMSBahamasUATClean;'
                     'UID=sa;'
                     'PWD=admin#123;'
                     'Trusted_Connection=no;')
cur = con.cursor()

#Insert the values from list into database
for Resort in range(NoOfResortsAllPages):
    #SQLCommand = "Insert into tblTestWebScriping(PropertyName)  Values ('" + ResortNameList[Resort].text + "')"
    SQLCommand = "Insert into tblTestWebScriping(PropertyName)  Values ('" + ResortNameList[Resort] + "')"
    print(SQLCommand)
    cur.execute(SQLCommand)
    con.commit()
cur.execute('Select PropertyName from tblTestWebScriping')
for row in cur:
    print(row)
        #print("3" + str(row))

#Click on Next button
nextBtn=driver.find_element_by_xpath("//li[@class='_i66xk8d']//a[@aria-label='Next']")
nextBtn.click()

#Close Browser
driver.quit()
driver.close()

