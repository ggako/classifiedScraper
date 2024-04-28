from selenium import webdriver
import pandas as pd
import time

def main():
    """
    Scrapes data from an alumni classifieds page and generates a readable csv file as output.

    Working as of April 20, 2024 version of the webpage

    In case the script doesn't work for the present version of the webpage, it could be due to:
    1.) Page not loading completely
        Solution: Increase the timeToWait parameter found below to allow for page to fully load (currently set as 4)
    2.) Changes in the site (that would require modifying the path parameters or the script structure).
        Solution: Create an issue describing the error encountered
    """
    url  = 'https://www.ustaa.au/'

    # Wait-time parameter
    timeToWait = 4

    # Fetching data
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(timeToWait) # Wait for page to load
    # driver.implicitly_wait(timeToWait) 

    # Initialize list of database variables
    name = []
    state = []
    college = []
    course = []
    year = []
    profileLink = []
    pageTitle = []
    pageLink = []

    # Initialize page state checking variables
    nextButtonExists = False
    initialPage = True

    # Check if page has ">" navigation button
    # Note: ">" navigation button has length 0
    navButtons = driver.find_elements(by='xpath', value='//button[contains(@class, "w-8")]')
    if len(navButtons[-1].text) == 0: # Only check the rightmost button where ">" is expected to be located
        nextButtonExists = True

    # Checks if next button exists, if it exists - will execute while loop to read the current page
    while nextButtonExists == True:
    
        if initialPage == False:
            # Go to next page
            navButtons[-1].click()
            time.sleep(timeToWait) # Added to prevent Stale Exception error / provide waittime for DOM to load
            print("Navigating to the next page")
            navButtons = driver.find_elements(by='xpath', value='//button[contains(@class, "w-8")]')
            
            # Checks if page has ">" navigation button (absence of button, will prevent next iteration)
            # Note: ">" navigation button has length 0
            if len(navButtons[-1].text) == 0: # Only check the rightmost button where ">" is expected to be located
                nextButtonExists = True
            else:
                nextButtonExists = False

        # Getting profile elements of current page
        profiles = driver.find_elements(by='xpath', value="//div[contains(@class,'self-stretch')]")

        # Scraping specific data
        for profile in profiles:
            
            # Getting name, state
            name.append(profile.find_element(by='xpath', value='.//h2[contains(@class,"text-xl")]').text)
            try:
                state.append(profile.find_element(by='xpath', value='.//h2[contains(@class,"uppercase")]').text)
            except:
                state.append("")

            # Getting college, course, year
            subprofile = profile.find_elements(by='xpath', value='.//div[contains(@class,"my-[16px]")]') # List with 1 item
            subprofileElements = subprofile[0].text.split("\n")
            if len(subprofileElements) == 3:
                college.append(subprofileElements[0])
                course.append(subprofileElements[1])
                year.append(subprofileElements[2])
            else:
                college.append("")
                course.append("")
                year.append("")

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

    # Check for data completeness
    if len(name) == len(state) == len(college) == len(course) == len(year) == len(profileLink) == len(pageTitle) == len(pageLink):
        # Create CSV file
        df_profiles = pd.DataFrame({'Name': name, 'State' : state, 'College': college, 'Course': course, 'Year': year, 'Profile': profileLink, 'Page': pageTitle, 'Page Link': pageLink})
        df_profiles.to_csv('profiles.csv', index=False)
        print("Successfully created csv file")
    else:
        raise Exception("Missing data")

    driver.quit()

if __name__ == "__main__":
    main()