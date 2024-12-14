import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from ImportandDictionaries import vrbo_ids, amen_dropdown
import selenium.webdriver.support.expected_conditions as ec
import pandas as pd
import time
import os
import re

class AirBnbListings:
    def __init__(self):
        chrome_service = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--disable-cookies")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-webrtc')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = uc.Chrome(service=chrome_service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 5)
        self.action = ActionChains(self.driver)
        self.driver.maximize_window()

    def land_required_page(self, target_url):
        self.driver.get(target_url)
        self.driver.execute_script("document.body.style.zoom='33%'")
        self.driver.implicitly_wait(5)

    def get_listing_title(self):
        try:
            title = self.wait.until(ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "toieuka atm_c8_2x1prs atm_g3_1jbyh58")]/h2'))).text
            return title
        except Exception as e:
            return e
        
    def get_listing_address(self):
        try:
            address = self.wait.until(ec.presence_of_element_located((By.XPATH, '//div[@class="s1qk96pm atm_gq_p5ox87 dir dir-ltr"]'))).text
            return address
        except:
            return ""
        
    def get_bedrooms(self):
        try:
            beds = self.wait.until(ec.presence_of_element_located((By.XPATH, '//li[contains(@class, "l7n4lsf ") and contains(text(), "bedroom")]'))).text
            beds = re.sub(r"[^0-9]", "", beds)
            return beds
        except:
            return ""
        
    def get_baths(self):
        try:
            baths = self.wait.until(ec.presence_of_element_located((By.XPATH, '//li[contains(@class, "l7n4lsf ") and contains(text(), "bathroom")]'))).text
            baths = re.sub(r"[^0-9]", "", baths)
            return baths
        except:
            return ""
    
    def get_sleeps(self):
        try:
            sleeps = self.wait.until(ec.presence_of_element_located((By.XPATH, '//li[contains(@class, "l7n4lsf ") and contains(text(), "guest")]'))).text
            sleeps = re.sub(r"[^0-9]", "", sleeps)
            return sleeps
        except Exception as e:
            return e
    
    def get_description(self):
        try:
            try:
                show_more = self.wait.until(ec.presence_of_element_located((By.XPATH, '//button[@aria-label="Show more about this place"]')))
                self.action.click(show_more).perform()
            except:
                print("Show More Button Not Found.....")
            
            try:
                description = self.wait.until(ec.presence_of_element_located((By.XPATH, '//div[@data-section-id="DESCRIPTION_MODAL"]'))).text
                description = description.replace("About this space\n", "") if "About this space" in description else description
            except Exception as e:
                print(e)
                description = ""
            
            try:
                close = self.driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
                self.driver.implicitly_wait(3)
                close.click()
            except:
                print("Fail to close Description.....")

            return description
        except:
            return ""
        
    def get_amenities(self):
        try:
            openamen = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, '//button[contains(text(), "amenities")]'))
            )
            self.driver.execute_script("arguments[0].click();", openamen)
            amenities = self.wait.until(ec.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "twad414") and not(contains(@id, "pdp_unavailable"))]')))
            amenities = [a.text.lower().replace(" ", "_") for a in amenities if a.text.title() in amen_dropdown]
            amenities = ", ".join(amenities)
            return amenities
        except:
            return ""
        
    def simplified_amentities(self):
        all_ammen = {
            "Essentials": '//div[@class="_11jhslp" and div//h2[contains(text(), "Heating and cooling")]]/ul/li',
            "Kitchen": '//div[@class="_11jhslp" and div//h2[contains(text(), "Kitchen")]]/ul/li',
            "Pool & spa": "",
            "Outside": '//div[@class="_11jhslp" and div//h2[contains(text(), "Outdoor")]]/ul/li',
            "Entertainment": '//div[@class="_11jhslp" and div//h2[contains(text(), "Entertainment")]]/ul/li',
            "Baby & toddler": '//div[@class="_11jhslp" and div//h2[contains(text(), "Family")]]/ul/li',
            "Laundry": '//div[@class="_11jhslp" and div//h2[contains(text(), "laundry")]]/ul/li',
            "Parking": '//div[@class="_11jhslp" and div//h2[contains(text(), "Parking")]]/ul/li',
            "Safety": '//div[@class="_11jhslp" and div//h2[contains(text(), "Home safety")]]/ul/li',
            "Location Type": "",
            "Nearby Activities": '//div[@class="_11jhslp" and div//h2[contains(text(), "Location features")]]/ul/li',
            "Suitability": "",
            "Accessability": "",
            "Breakfast": "",
            "Services": '//div[@class="_11jhslp" and div//h2[contains(text(), "Services")]]/ul/li',
        }
        amen_dict = {}
        amen = []
        for key, value in all_ammen.items():
            if value == "":
                amen_dict[key] = ""
            else:
                try:
                    kitchen = self.wait.until(ec.presence_of_all_elements_located((By.XPATH, value)))
                    for k in kitchen:
                        kit = k.text
                        if "\n" in kit:
                            k = kit.split("\n")
                            k = k[0]+" ("+k[1]+")"
                            amen.append(k)
                        else:
                            amen.append(kit)
                    kitchen = ", ".join(amen)
                    amen.clear()
                    amen_dict[key] = kitchen
                except:
                     amen_dict[key] = ""   

        try:
            close_amen = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close"]')))
            self.action.click(close_amen).perform()
        except:
            print("Fail to close amenities....")

        amen.clear()
        return amen_dict

    def get_max_attendies(self):
        try:
            max = self.wait.until(ec.presence_of_element_located((By.XPATH, '//li[contains(@class, "l7n4lsf ") and contains(text(), "guest")]'))).text
            max = re.sub(r"[^0-9]", "", max)
            return max
        except:
            return ""

    def get_total_reviews(self):
        try:
            total_rev = self.wait.until(ec.presence_of_element_located((By.XPATH, '//a[contains(@class, "l1ovpqvx") and contains(text(), "review")]'))).text
            total_rev = re.sub(r"[^0-9]", "", total_rev)
            return total_rev
        except:
            try:
                total_rev = self.wait.until(ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "r16onr0j")]'))).text
                return total_rev
            except:
                return ""
        
    def get_all_images(self):
        try:
            try:
                open_images = self.wait.until(ec.presence_of_element_located((By.XPATH, '//div[@data-section-id="HERO_DEFAULT"]//img[1]')))
                self.driver.execute_script("arguments[0].click();", open_images)
            except:
                print("Fail to open images...")

            try:
                body = self.driver.find_element(By.TAG_NAME, 'body')
                self.driver.implicitly_wait(3)
                for _ in range(0, 15):
                    body.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.2)
            except:
                print("Fail with body.....")

            try:
                images = self.wait.until(ec.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="photo-viewer-section"]//img')))
                images = [i.get_attribute('src') for i in images]
                images = ", ".join(images)
            except Exception as e:
                images = ""

            try:
                close_amen = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close"]')))
                self.action.click(close_amen).perform()
            except:
                print("Fail to close images....")
            return images
        except:
            print("Fail to get images")


    def collect_main_data_file(self, id, state, user_id):
        main_data = {}
        group_name = self.get_listing_title()
        post_location = self.get_listing_address()
        property_beds = self.get_bedrooms()
        property_baths = self.get_baths()
        sleeps = self.get_sleeps()
        size = ""
        group_desc = self.get_description()
        total_reviews = self.get_total_reviews()
        attendees = self.get_max_attendies()
        amenities_dropdown = self.get_amenities()
        all_amenities = self.simplified_amentities()
        images = self.get_all_images()
        main_data['group_id'] = id
        main_data['state'] = state
        main_data['usa_islands'] = state
        main_data['group_name'] = group_name
        main_data['post_location'] = post_location
        main_data['property_beds'] = property_beds.strip()
        main_data['property_baths'] = property_baths.strip()
        main_data['sleeps'] = sleeps.strip()
        main_data['size'] = size
        main_data['group_desc'] = group_desc
        main_data['total_reviews'] = total_reviews.strip()
        main_data['images'] = images
        main_data['attendees'] = attendees
        for k, v in all_amenities.items():
            main_data[k] = v
        main_data['amenities_dropdown'] = amenities_dropdown
        main_data['user_id'] = user_id
        main_data['post_link'] = self.driver.current_url.strip().split('?')[0]
        main_data['affiliate_link'] = ''
        return main_data

    def get_reviews(self, rev_id):
        try:
            go_down = self.driver.find_element(By.XPATH, '//h2[contains(text(), "Meet your Host")]')
            self.driver.implicitly_wait(3)
            self.action.move_to_element(go_down).perform()
        except:
            pass

        scraped = []
        try:
            all_reviews = self.wait.until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="pdp-show-all-reviews-button"]')))
            self.driver.execute_script("arguments[0].click();", all_reviews)
            reviews_all = self.wait.until(ec.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "r1are2x1")]')))
            for r in reviews_all:
                rev_dict = {}
                rev_dict['review_id'] = rev_id
                try:
                    rev_by = WebDriverWait(r, 5).until(
                        ec.presence_of_element_located((By.XPATH, './/h2[contains(@class, "hpipapi") and not(contains(@class, "Response"))]'))).text
                    rev_dict['review_by'] = rev_by
                except:
                    rev_dict['review_by'] = ""

                try:
                    element = WebDriverWait(r, 5).until(
                        ec.presence_of_element_located((By.XPATH, './/div[contains(@class, "s78n3tv")]')))
                    review_date = self.driver.execute_script("""
                                                        var parent = arguments[0];
                                                        var childDivs = parent.querySelectorAll("div");
                                                        childDivs.forEach(child => child.remove());
                                                        return parent.textContent.trim();
                                                    """, element)
                    rev_dict['review_date'] = review_date
                except:
                    rev_dict['review_date'] = ""

                rev_dict['review_title'] = ""
                try:
                    body = WebDriverWait(r, 5).until(
                        ec.presence_of_element_located((By.XPATH, './/span[contains(@class, "l1h825yc")]'))).text
                    rev_dict['review_body'] = body
                except:
                    rev_dict['review_body'] = ""

                rev_dict['review_rating'] = ""

                scraped.append(rev_dict)

        except:
            reviews = self.wait.until(ec.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "r1ovlb5h")]')))
            for r in reviews:
                rev_dict = {}
                rev_dict['review_id'] = rev_id
                try:
                    rev_by = WebDriverWait(r, 5).until(ec.presence_of_element_located((By.XPATH, './/h3[contains(@class, "hpipapi")]'))).text
                    rev_dict['review_by'] = rev_by
                except:
                    rev_dict['review_by'] = ""

                try:
                    element = WebDriverWait(r, 5).until(ec.presence_of_element_located((By.XPATH, './/div[contains(@class, "s78n3tv")]')))
                    review_date = self.driver.execute_script("""
                                        var parent = arguments[0];
                                        var childDivs = parent.querySelectorAll("div");
                                        childDivs.forEach(child => child.remove());
                                        return parent.textContent.trim();
                                    """, element)
                    rev_dict['review_date'] = review_date
                except:
                    rev_dict['review_date'] = ""

                rev_dict['review_title'] = ""
                try:
                    body = WebDriverWait(r, 5).until(ec.presence_of_element_located((By.XPATH, './/span[contains(@class, "l1h825yc")]'))).text
                    rev_dict['review_body'] = body
                except:
                    rev_dict['review_body'] = ""
                rev_dict['review_rating'] = ""

                scraped.append(rev_dict)
        return scraped

    def get_beds(self, bed_id):
        try:
            go_down = self.driver.find_element(By.XPATH, '//h2[contains(text(), "What this place offers")]')
            self.driver.implicitly_wait(3)
            self.action.move_to_element(go_down).perform()
        except:
            pass

        beds = []
        try:
            bed_image = self.wait.until(ec.presence_of_all_elements_located((By.XPATH, '//div[@class="_ctz3yu"]')))
            for b in bed_image:
                bed_dict = {}
                bed_dict['listing_id'] = bed_id
                try:
                    name = WebDriverWait(b, 5).until(ec.presence_of_element_located((By.XPATH, './/div[@class="_1owbxvp"]'))).text
                    bed_dict['bed_type'] = name
                except:
                    bed_dict['bed_type'] = ""

                try:
                    bed_desc = WebDriverWait(b, 5).until(ec.presence_of_element_located((By.XPATH, './/div[@class="_1o122dv"]'))).text
                    bed_dict['bed_description'] = bed_desc
                except:
                    bed_dict['bed_description'] = ""
                beds.append(bed_dict)
        except:
            while True:
                try:
                    bed_click = self.wait.until(ec.presence_of_element_located((By.XPATH, "//span[@class='isqgmsg dir dir-ltr']//*[name()='svg' and @aria-label='Next']")))
                    self.action.click(bed_click).perform()
                    time.sleep(0.5)
                except:
                    break
            bed_simple = self.wait.until(ec.presence_of_all_elements_located((By.XPATH, '//div[@class="_muswv4"]')))
            print(len(bed_simple))
            for b in bed_simple:
                bed_dict = {}
                bed_dict['listing_id'] = bed_id
                try:
                    name = WebDriverWait(b, 5).until(
                        ec.presence_of_element_located((By.XPATH, './/div[@class="_19g9i1v"]'))).text       
                    bed_dict['bed_type'] = name       
                except:       
                    bed_dict['bed_type'] = ""       
       
                try:       
                    bed_desc = WebDriverWait(b, 5).until(
                        ec.presence_of_element_located((By.XPATH, './/div[@class="_1a412m6"]'))).text
                    bed_dict['bed_description'] = bed_desc
                except:
                    bed_dict['bed_description'] = ""
                beds.append(bed_dict)
        return beds


    def file_handling(self, file_path, data_dict, review_dict, bed_dict):
        df1 = pd.DataFrame([data_dict])
        df2 = pd.DataFrame(review_dict)
        df3 = pd.DataFrame(bed_dict)
        if os.path.exists(file_path):
            with pd.ExcelWriter(file_path, engine="openpyxl", mode='a', if_sheet_exists='overlay') as writer:
                df1.to_excel(writer, sheet_name="Data File", index=False, header=False,
                             startrow=writer.sheets['Data File'].max_row)
                df2.to_excel(writer, sheet_name="Review File", index=False, header=False,
                             startrow=writer.sheets['Review File'].max_row)
                df3.to_excel(writer, sheet_name="Bed File", index=False, header=False,
                             startrow=writer.sheets['Bed File'].max_row)
        else:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df1.to_excel(writer, sheet_name="Data File", index=False)
                df2.to_excel(writer, sheet_name="Review File", index=False)
                df3.to_excel(writer, sheet_name="Bed File", index=False)

    def quit_driver(self):
        self.driver.__del__ = None
        self.driver.quit()
        
    



def scrape_by_link_list(link_list):
    url_list = link_list
    start_id = int(input("Enter Starting ID: "))
    state = str(input("Enter State Name: ")).lower()
    file_path = str(input("Enter File Path: "))
    if " " in state:
        state = state.replace(" ", "_")
    try:
        user_id = vrbo_ids[state]
    except:
        user_id = ""
    bot = AirBnbListings()
    for u in url_list:
        bot.land_required_page(u)
        data = bot.collect_main_data_file(start_id, state, user_id)
        for k, v in data.items():
            print(k + ": ", v)
        try:
            reviews = bot.get_reviews(start_id)
            print(reviews)
        except:
            reviews = [{}]
        try:
            beds = bot.get_beds(start_id)
            print(beds)
        except:
            beds = [{}]
        bot.file_handling(file_path, data, reviews, beds)
        start_id = start_id + 1
    bot.quit_driver()

def scrape_single_link(link):
    start_id = int(input("Enter Starting ID: "))
    state = str(input("Enter State Name: ")).lower()
    file_path = str(input("Enter File Path: "))
    if " " in state:
        state = state.replace(" ", "_")
    try:
        user_id = vrbo_ids[state]
    except:
        user_id = ""
    bot = AirBnbListings()
    bot.land_required_page(link)
    data = bot.collect_main_data_file(start_id, state, user_id)
    for k, v in data.items():
        print(k + ": ", v)
    try:
        reviews = bot.get_reviews(start_id)
        print(reviews)
    except:
        reviews = [{}]
    try:
        beds = bot.get_beds(start_id)
        print(beds)
    except:
        beds = [{}]
    bot.file_handling(file_path, data, reviews, beds)
    bot.quit_driver()

def scrape_by_link_dict(link_dict):
    url_list = link_dict
    start_id = int(input("Enter Starting ID: "))
    file_path = str(input("Enter File Path: "))
    bot = AirBnbListings()
    for key, value in url_list.items():
        if " " in key:
            key = key.lower().replace(" ", "_")
        else:
            key = key.lower()
        try:
            user_id = vrbo_ids[key]
        except:
            user_id = ""
        for vl in value:
            bot.land_required_page(vl)
            data = bot.collect_main_data_file(start_id, key, user_id)
            for k, v in data.items():
                print(k + ": ", v)
            try:
                reviews = bot.get_reviews(start_id)
                print(reviews)
            except:
                reviews = [{}]
            try:
                beds = bot.get_beds(start_id)
                print(beds)
            except:
                beds = [{}]
            bot.file_handling(file_path, data, reviews, beds)
            start_id = start_id + 1
    bot.quit_driver()

choice = int(input("""Please Enter one of these:
1 For Single Link Scrape
2 For List of Links Scrape 
3 For Dictionary of Links Scrape
Enter here: 
"""))

links = 'https://www.airbnb.ie/rooms/1110233388154535195'  #paste here link or link_list or link_dict

if choice == 1:
    scrape_single_link(links)
elif choice == 2:
    scrape_by_link_list(links)
elif choice == 3:
    scrape_by_link_dict(links)
else:
    print("Invalid Choice")
        
        


    
            
        