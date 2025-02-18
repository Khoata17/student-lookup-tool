import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_lookup():
    file_path = "danh_sach_mssv.xlsx"  # Đặt tên file danh sách MSSV cố định
    
    df = pd.read_excel(file_path)
    if 'Mã sinh viên' not in df.columns:
        print("Lỗi: File Excel phải có cột 'Mã sinh viên'")
        return
    
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")  # Mở trình duyệt toàn màn hình
    driver = webdriver.Edge(options=options)
    driver.get("https://iaps9.poly.edu.vn/")  # Cập nhật đúng đường dẫn đăng nhập
    
    print("Vui lòng đăng nhập thủ công và chọn cơ sở PTCĐ Cần Thơ...")
    input("Nhấn Enter sau khi đã đăng nhập thành công...")
    
    results = []
    for index, row in df.iterrows():
        mssv = str(row['Mã sinh viên'])
        student_url = f"https://iaps9.poly.edu.vn/admin/profile?user_code={mssv}#lich_su_hoc"
        ghi_chu = ""
        
        try:
            driver.get(student_url)
            time.sleep(2)  # Chờ trang tải hoàn toàn
            
            # Thử click vào tab "Lịch sử học" nếu chưa mở
            try:
                lich_su_hoc_tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Lịch sử học')]"))
                )
                lich_su_hoc_tab.click()
                time.sleep(2)  # Đợi trang load sau khi click
            except:
                print(f"Không tìm thấy tab 'Lịch sử học' cho MSSV {mssv}, thử tiếp tục...")
            
            # Chờ tối đa 2 phút để dữ liệu hiển thị
            try:
                WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, "//table/tbody"))
                )
                time.sleep(2)
            except:
                print(f"Không tìm thấy dữ liệu lịch sử học cho MSSV {mssv}")
                ghi_chu = "Lịch sử học chưa đồng bộ, cán bộ đồng bộ thủ công và quét lại"
                results.append([mssv, "", "", "", "", "", "", ghi_chu])
                continue
            
            rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
            
            da_tham_gia, studying, studying_missing, passed, failed = [], [], [], [], []
            
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) < 5:
                    continue  # Bỏ qua dòng trống
                subject_code = cols[2].text  # Mã môn
                subject_conversion = cols[3].text  # Mã chuyển đổi
                status = cols[-1].text  # Trạng thái môn học
                
                key = subject_code if subject_code == subject_conversion else f"{subject_code} ({subject_conversion})"
                
                if "Đã tham gia" in status:
                    da_tham_gia.append(key)
                elif "Studying (Missing points)" in status:
                    studying_missing.append(key)
                elif "Studying" in status:
                    studying.append(key)
                elif "Passed" in status:
                    passed.append(key)
                elif "Failed" in status:
                    failed.append(key)
            
            # Loại bỏ các môn trong Failed nếu chúng tồn tại trong Passed hoặc có 6 ký tự đầu trùng nhau
            filtered_failed = []
            passed_short_codes = {p[:6] for p in passed}
            for f in failed:
                if f not in passed and f[:6] not in passed_short_codes:
                    filtered_failed.append(f)
            
            results.append([
                mssv, ", ".join(da_tham_gia), ", ".join(studying), ", ".join(studying_missing), ", ".join(passed), ", ".join(filtered_failed), ghi_chu
            ])
        except Exception as e:
            print(f"Lỗi khi lấy lịch sử học MSSV {mssv}: {e}")
            ghi_chu = "Lỗi hệ thống, kiểm tra lại"
            results.append([mssv, "", "", "", "", "", "", ghi_chu])
    
    driver.quit()
    
    df_results = pd.DataFrame(results, columns=['Mã sinh viên', 'Đã tham gia', 'Studying', 'Studying (Missing points)', 'Passed', 'Failed', 'Ghi chú'])
    output_file = "ket_qua_tra_cuu.xlsx"
    df_results.to_excel(output_file, index=False)
    print(f"Hoàn thành: Đã lưu kết quả vào {output_file}")

# Chạy chương trình
if __name__ == "__main__":
    start_lookup()
