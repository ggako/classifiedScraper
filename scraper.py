from selenium import webdriver
import pandas as pd
import time

url  = 'https://www.ustaa.au/'

# Fetching data
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(5) # Wait for page to load

# Initialize list of database variables
name = []
state = []
college = []
course = []
year = []
profileLink = []
pageTitle = []
pageLink = []

# Page state checking variables
nextButtonExists = False
initialPage = True

# Check if page has ">" navigation button
# Note: ">" navigation button has length 0
navButtons = driver.find_elements(by='xpath', value='//button[contains(@class, "w-8")]')
if len(navButtons[-1].text) == 0: # Only check the rightmost button
    nextButtonExists = True

# Checks if next button exists, if it exists - read the current page
while nextButtonExists == True:

    if initialPage == False:
        # Go to next page
        navButtons[-1].click()
        time.sleep(5) # Added this to prevent Stale Exception error / provide waittime for DOM to load
        print("Navigating to the next page")
        navButtons = driver.find_elements(by='xpath', value='//button[contains(@class, "w-8")]')
        
        # Checks if page has ">" navigation button (absence of button, will prevent next iteration)
        # Note: ">" navigation button has length 0
        if len(navButtons[-1].text) == 0:
            nextButtonExists = True
        else:
            nextButtonExists = False

    # Getting profile elements of current page
    profiles = driver.find_elements(by='xpath', value="//div[contains(@class,'self-stretch justify-center flex flex-col sm:max-w-[450px] shadow-lg rounded-md')]")

    # Scraping specific data
    for profile in profiles:
        
        # Getting name, state, college, course, year
        name.append(profile.find_element(by='xpath', value='.//h2[contains(@class,"text-xl")]').text)
        state.append(profile.find_element(by='xpath', value='.//h2[contains(@class,"uppercase")]').text)
        subprofile = profile.find_elements(by='xpath', value='.//div[contains(@class,"my-[16px]")]') # List with 1 item
        subprofileElements = subprofile[0].text.split("\n")
        # print(subprofileElements)
        college.append(subprofileElements[0])
        course.append(subprofileElements[1])
        year.append(subprofileElements[2])

        # Getting links to profile
        linkElement = profile.find_elements(by='xpath', value='.//a[contains(@class,"text-primary")]') # List with 1 item
        href_value = linkElement[0].get_attribute("href")
        profileLink.append(href_value)

        # Getting title and links of pages
        pageElement = profile.find_elements(by='xpath', value='.//a[contains(@class,"text-sky-400")]') # List with 0 or 1 items
        if len(pageElement) == 0:
            pageTitle.append("")
            pageLink.append("")
        else:
            pageTitle.append(pageElement[0].text)
            pageLink.append(pageElement[0].get_attribute("href"))

    initialPage = False

# Check if variables have same lengths (implies complete expected data)
if len(name) == len(state) == len(college) == len(course) == len(year) == len(profileLink) == len(pageTitle) == len(pageLink):
    # Making CSV
    df_profiles = pd.DataFrame({'Name': name, 'State' : state, 'College': college, 'Course': course, 'Year': year, 'Profile': profileLink, 'Page': pageTitle, 'Page Link': pageLink})
    df_profiles.to_csv('profiles.csv', index=False)
    print("Successfully created csv file")
else:
    raise Exception("Missing data")

driver.quit()
