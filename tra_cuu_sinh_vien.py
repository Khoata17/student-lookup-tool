from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

edge_options = Options()
edge_options.add_argument("--headless")  # Chạy không giao diện
edge_options.add_argument("--disable-gpu")  
edge_options.add_argument("--no-sandbox")  
edge_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/msedgedriver")
driver = webdriver.Edge(service=service, options=edge_options)

driver.get("https://iaps9.poly.edu.vn/")  # Mở trang web
print(driver.title)  # Kiểm tra xem mở trang có thành công không
