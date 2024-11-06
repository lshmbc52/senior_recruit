import pandas as pd

def base_data_func():

    base_data=pd.DataFrame({
        "work":['미화원','경비원','조리사','요양보호사'],
        "region":['서울','부산','대구',None],
        "experience":[0,1,5,10],
        "salary":["150만원","200만원","250만원","300만원"]
    })
    print(base_data)
    return base_data

if __name__ == "__main__":
    base_data_func()