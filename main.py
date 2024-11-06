import streamlit as st
import pandas as pd
from base_data import base_data_func
import senior_job_postings

class JobSearch:
    def __init__(self, base_data_func, save_csv_function):
        self.base_data = base_data_func
        self.save_csv_function = save_csv_function
    
    def search(self, keyword, location, experience):
        return self.base_data[(self.base_data['원하는 업종'].str.contains(keyword)) &
                           (self.base_data['근무지역'] == location) &
                           (self.base_data['경력'] >= experience)]

def create_dataframe():
    columns = ["회사명", "업종", "급여", "경력", "근무지", "등록일", "마감일"]
    return pd.DataFrame(senior_job_postings.data, columns=columns)

def filter_data(df, keyword, location):
    # 초기 조건 - 모든 행을 True로 설정
    mask = pd.Series([True] * len(df), index= df.index)
    
    # keyword가 비어있지 않으면 업종 필터링
    if keyword:
        mask = mask & df['업종'].str.contains(keyword, na=False)
    
    # location이 비어있지 않으면 근무지 필터링
    if location:
        if location == 'None':
            mask = mask & df['근무지'].isna()
        else:
            mask = mask & df['근무지'].str.contains(location, na=False)
    
    return df[mask]

def main():
    base_data = base_data_func()
    job_search = JobSearch(base_data, senior_job_postings.save_csv)
    
    st.title("Senior 일자리 검색")
    
    # 데이터프레임 생성
    df = create_dataframe()
    
    #검색필터 UI
    col1, col2 = st.columns(2)
    
    with col1:
        # 고정된 업종 리스트
        업종_list = ["", "미화원", "경비원", "조리사", "요양보호사"]
        # 고정된 지역 리스트
        지역_list = ["", "서울", "부산", "대구", "None"]
        
        keyword = st.selectbox("업종 선택", 업종_list)
        location = st.selectbox("지역 선택", 지역_list)
    
    with col2:
        experience = st.slider("최소경력", 0, 10, 0, key="experience_slider")
    
    if st.button("검색", type="primary"):
        # 검색 조건에 따라 데이터 필터링
        filtered_results = filter_data(df, keyword, location)
        
        if filtered_results.empty:
            st.warning("검색 결과가 없습니다.")
        else:
            st.success(f"전체 {len(filtered_results)}개의 결과를 찾았습니다.")
            st.dataframe(filtered_results)

if __name__ == "__main__":
    main()