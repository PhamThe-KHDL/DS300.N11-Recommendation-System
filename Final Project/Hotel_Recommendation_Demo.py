import numpy as np
import pandas as pd
import pandas as sqrt
from numpy.lib.function_base import average
from numpy import sqrt
import time
from sklearn.metrics import mean_squared_error
import math
from sklearn.metrics import mean_absolute_error
import tqdm
from numpy import dot
from numpy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st
import numpy as np
import pandas as pd
import pandas as sqrt
from numpy.lib.function_base import average
from numpy import sqrt
import time
from sklearn.metrics import mean_squared_error
import math
from sklearn.metrics import mean_absolute_error
import tqdm
from numpy import dot
from numpy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st

ratings = pd.read_csv('hotels_users_ratings.csv')

def get_rating(userid,hotelid):
      return (ratings.loc[(ratings.UserID==userid) & (ratings.HotelID == hotelid),'Rating'].iloc[0])

#def get_NameHotel(userid,location):
#    return (ratings_test.loc[(ratings_test.UserID==userid)&(ratings_test.Location == location),'Name Hotel'].tolist())

def get_hotelids(userid,location):
    return (ratings.loc[(ratings.UserID==userid)&(ratings.Location == location),'HotelID'].tolist())

def get_hotel_title(hotelid):
    return (ratings.loc[(ratings.HotelID == hotelid),'Name Hotel'].iloc[0])

def get_url(hotelid):
    return (ratings.loc[(ratings.HotelID == hotelid),'URL Hotel'].iloc[0])

def get_description(hotelid):
    return (ratings.loc[(ratings.HotelID == hotelid),'Descriptions'].iloc[0])

def get_address(hotelid):
    return (ratings.loc[(ratings.HotelID == hotelid),'Address'].iloc[0])



def pearson_correlation_score(user1,user2,location):
    both_vatch_count= []

    list_hotel_user1 = ratings.loc[(ratings.UserID == user1) & (ratings.Location == location) ,'HotelID'].to_list()
    list_hotel_user2 = ratings.loc[(ratings.UserID == user2) & (ratings.Location == location), 'HotelID'].to_list()
    for element in list_hotel_user1:
        if element in list_hotel_user2:
            both_vatch_count.append(element)
  
        if (len(both_vatch_count)==0):
            return 0
    avg_rating_sum_1 = average([get_rating(user1, i) for i in both_vatch_count])# rating trung bình user1

    avg_rating_sum_2 = average([get_rating(user2, i) for i in both_vatch_count])# rating trung bình user2

    tu = sum([(get_rating(user1, i)- avg_rating_sum_1)*(get_rating(user2, i)- avg_rating_sum_2) for i in both_vatch_count])

    mau = sqrt(sum([pow((get_rating(user1, i) - avg_rating_sum_1),2) for i in both_vatch_count])) * sqrt(sum([pow((get_rating(user2, i)- avg_rating_sum_2),2) for i in both_vatch_count]))

    if mau == 0:
        return 0
    return tu/mau

def distance_similarity_score(user1,user2,location):

    both_watch_count = 0
    list_hotel_user1 = ratings.loc[(ratings.UserID == user1) & (ratings.Location == location) ,'HotelID'].to_list()
    list_hotel_user2 = ratings.loc[(ratings.UserID == user2) & (ratings.Location == location), 'HotelID'].to_list()
    for element in list_hotel_user1:
        if element in list_hotel_user2:
            both_watch_count += 1
    if both_watch_count == 0 :
        return 0
    

    rating1 = []
    rating2 = []
    for element in list_hotel_user1:
        if element in list_hotel_user2:
            rating1.append(get_rating(user1,element))
            rating2.append(get_rating(user2,element))

#    print(rating1)
#    print(rating2)

    return dot(rating1, rating2)/(norm(rating1)*norm(rating2))

def most_similar_user(user1, number_of_user,location, similarity_name):
    
  user_ID = ratings.UserID.unique().tolist()
  print(len(user_ID))

  if(similarity_name == "pearson"):
    similarity_score = [(pearson_correlation_score(user1, user_i,location),user_i)  for user_i in user_ID[0:1500] if user_i != user1] #danh sách user quá nhiều nên tình chỉ tính tên dánh sách có 50 users

  if(similarity_name == "cosine"):
    similarity_score = [(distance_similarity_score(user1, user_i,location),user_i)  for user_i in user_ID[0:1500] if user_i != user1]
  

  similarity_score.sort() #tăng dần
  similarity_score.reverse() #tăng dần

  return similarity_score[:number_of_user] # có thể thay đổi số lượng lân cận

#lấy ra danh sách khuyến nghị từ top populars
def get_recommendation(userid,number_of_user,location,similarity_name):# lấy ra danh sách khuyến nghị của n người tương đồng phim có rating cao để khuyến nghị cho userid dựa vào độ đo
    # user_ids = ratings.userId.unique().tolist()
    total = {}
    similariy_sum = {}
    list_user_popular = most_similar_user(userid, number_of_user,location,similarity_name)
    # Iterating over subset of user ids.

    for pearson, user in list_user_popular:
        
        score = pearson

        for hotelid in get_hotelids(user,location): #-> dánh sách các id movie đã xem bởi user khác và khởi tạo giá trị =0
          if hotelid not in get_hotelids(userid,location):
            total[hotelid] = 0
            similariy_sum[hotelid] = 0

        for hotelid in get_hotelids(user,location): #-> dánh sách các id movie đã xem bởi user khác
          if hotelid not in get_hotelids(userid,location):
            total[hotelid] += get_rating(user,hotelid) * score
            similariy_sum[hotelid] += score
        # print(total)
        # for movieid in get_movieids_(user): #-> dánh sách các id movie đã xem vởi user khác
        #     # Only considering not watched/rated movies
        #     if movieid not in get_movieids(userid):# or get_rating(userid,movieid) == 0:
        #       total[movieid] = 0
        #       total[movieid] += get_rating(user,movieid) * score #=> person nhân cho ratings của user ứng cử tương ứng
        #     similariy_sum[movieid] = 0
        #     similariy_sum[movieid] += score # tổng tổng độ tương tự của user target và các user khác 

    
    # Normalizing ratings
    ranking = []
    # Normalizing ratings
    for hotelid,tot in total.items():
        if similariy_sum[hotelid] == 0:
            ranking.append((8,hotelid))
        else:
            rating = tot/(similariy_sum[hotelid])
            ranking.append((rating,hotelid))
    ranking.sort() # sắp xếp tăng dần
    ranking.reverse() # đẩo chiều cho giảm dần
    
    
    recommendations = [(get_hotel_title(hotelid), score, get_address(hotelid),get_description(hotelid), get_url(hotelid)) for score,hotelid in ranking]
    return recommendations[:number_of_user]


#print(get_recommendation(1187,10,'Huế','cosine'))

#---------------------------------------------------------------------------------------------------------------------#
from sklearn.feature_extraction.text import TfidfVectorizer
#thêm thư viện linear_kernel
#core here
from sklearn.metrics.pairwise import linear_kernel
hotels_merg = pd.read_csv('data_merge_full_6471.csv')
hotels = pd.read_csv('hotels (1).csv')
# Hàm demo content based
def recommendations_content(userid):
    a  = hotels#[(hotels.Location == 'Đà Lạt')]
    vectorizer = TfidfVectorizer(max_features= 4500)
    overview_matrix = vectorizer.fit_transform(a['Descriptions'])
    overview_matrix1 = vectorizer.fit_transform(hotels_merg['Descriptions'])
    cosine_sim = linear_kernel(overview_matrix1, overview_matrix)
    for i in range(len(hotels_merg['UserID'])):
        if (hotels_merg['UserID'][i] == userid):
            sim_scores = list(enumerate(cosine_sim[i]))

          # Sắp xếp phim dựa trên điểm số tương tự
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

          # Lấy điểm của 10 phim giống nhất
            sim_scores = sim_scores[1:11]

            hotel_indices = [i[0] for i in sim_scores]
      # b = a['Name Hotel'].iloc[hotel_indices]
            a['Name Hotel'].iloc[hotel_indices].to_list()
    return [a['Name Hotel'].iloc[hotel_indices].to_list(), 
    a['Rating'].iloc[hotel_indices].to_list(),
    a['Address'].iloc[hotel_indices].to_list(),
    a['Descriptions'].iloc[hotel_indices].to_list(),
    a['URL Hotel'].iloc[hotel_indices].to_list()]
#---------------------------------------------------------------------------------------------------------------------#


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


#st.sidebar.success("Select a demo above.")

# Using "with" notation
with st.sidebar:
    add_userID = st.number_input('Enter User Id:')
    with st.form('form1'):
        if add_userID <= 6471:
            add_password = st.text_input('Enter password:')
        st.form_submit_button('Enter')
time.sleep(1)
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

st.title("Hotels Recommendation System")
st.header("Welcome to Demo")
#ten = st.number_input("Enter your userID: ")

#st.write('UserID: ',ten)

location = st.text_input("Enter the place: ")

st.write('Location: ',location)

click = st.button('Search')

list_recommendations_content = recommendations_content(add_userID)
for i in range(len(list_recommendations_content[0])):
    if location:
        break
    col1,col2 = st.columns(2)
    with col1:
        st.image('khach-san'+str(i)+'.jpg',caption = '')
        
    with col2:
        st.markdown(f'**Name Hotel**: {list_recommendations_content[0][i]}')
        st.markdown(f'**Rating**: {list_recommendations_content[1][i]}')
        st.markdown(f'**Address**: {list_recommendations_content[2][i]}')
        st.markdown(f'**Description**: {list_recommendations_content[3][i][:200]}...')
        st.markdown(f'[Go to Website]({list_recommendations_content[4][i]})')

list_recommen = get_recommendation(add_userID,10,location,'cosine')
#col1,col2,col3,col4,col5 = st.columns(5)

if click:
    for i in range(len(list_recommen)):
        col1,col2 = st.columns(2)
        with col1:
            st.image('khach-san'+str(i)+'.jpg',caption = '')
            
        with col2:
            st.markdown(f'**Name Hotel**: {list_recommen[i][0]}')
            st.markdown(f'**Rating**: {list_recommen[i][1]}')
            st.markdown(f'**Address**: {list_recommen[i][2]}')
            st.markdown(f'**Description**: {list_recommen[i][3][:200]}...')
            st.markdown(f'[Go to Website]({list_recommen[i][4]})')
            #st.write('URL Hotel: ', list_recommen[i][1])
            # st.markdown('Streamlit is **_really_ cool**.')


