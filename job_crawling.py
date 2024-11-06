# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging

def setup_chrome_driver(headless=False, download_path=None):
    """
    Chrome WebDriver를 자동으로 설정하는 함수
    
    Args:
        headless (bool): 헤드리스 모드 실행 여부
        download_path (str): 파일 다운로드 경로 (선택사항)
    
    Returns:
        webdriver: 설정된 Chrome WebDriver 인스턴스
    """
    # 로깅 설정
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Chrome 옵션 설정
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless')  # 헤드리스 모드
        
        # 기본 옵션 설정
        chrome_options.add_argument('--start-maximized')  # 창 최대화
        chrome_options.add_argument('--disable-notifications')  # 알림 비활성화
        chrome_options.add_argument('--no-sandbox')  # 샌드박스 비활성화
        chrome_options.add_argument('--disable-dev-shm-usage')  # 공유 메모리 사용 비활성화
        
        # 브라우저 크래시 방지
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        
        # 불필요한 로그 제거
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # 다운로드 경로 설정 (지정된 경우)
        if download_path:
            prefs = {
                "download.default_directory": download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
        
        # Chrome 드라이버 자동 설치 및 설정
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 페이지 로드 타임아웃 설정
        driver.set_page_load_timeout(30)
        
        logger.info("Chrome WebDriver가 성공적으로 설정되었습니다.")
        return driver
    
    except Exception as e:
        logger.error(f"Chrome WebDriver 설정 중 오류 발생: {str(e)}")
        raise

def test_driver_setup():
    """
    드라이버 설정 테스트
    """
    try:
        # 드라이버 설정
        driver = setup_chrome_driver()
        
        # 테스트를 위해 Google 접속
        driver.get("https://www.goldenjob.or.kr/job/find-person-tab1.asp")
        print("어르신 취업 페이지에 성공적으로 접속했습니다.")
        
        # 브라우저 제목 출력
        print(f"페이지 제목: {driver.title}")
        
        return True
        
    except Exception as e:
        print(f"테스트 중 오류 발생: {str(e)}")
        return False
        
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    # 필요한 패키지 설치 안내
    print("다음 패키지들이 필요합니다:")
    print("pip install selenium webdriver-manager")
    
    # 드라이버 설정 테스트 실행
    success = test_driver_setup()
    if success:
        print("드라이버 설정 테스트가 성공적으로 완료되었습니다.")
    else:
        print("드라이버 설정 테스트가 실패했습니다.")


