# DS300.N11 - Recommendation System


DS307.N11 - Hệ Khuyến Nghị

Học kỳ 1 Năm 4 Năm học 2022-2023 

## Hotel Recommendation System

**Giảng Viên:** 
- ThS Nguyễn Văn Kiệt
- CN Huỳnh Văn Tín


**Nhóm SVTH:**
- Phạm Đức Thể
- Trần Thành Luân


### Bộ dữ liệu

- Sử dụng ngôn ngữ lập trình Python kết hợp với hai framework được hỗ trợ mạnh mẽ cho việc cào dữ liệu là Selenium và BeautifulSoup để thu thập thông tin về công việc và ứng viên. Chi tiết về quy trình thu thập dữ liệu được trình bày ở Hình 1. Bộ dữ liệu được thu thập gồm hai bộ là: bộ dữ liệu công việc (jobs) và bộ dữ liệu ứng viên (users). Bộ dữ liệu công việc được chúng tôi thu tập trên hai trang web [topcv.vn](https://www.topcv.vn/viec-lam) và [timviec365.vn](https://timviec365.vn/) gồm 14,634 công việc với 18 thuộc tính. Bộ dữ ứng viên được chúng tôi thu tập trên trang web [timviec365.vn](https://timviec365.vn/) gồm 14,868 ứng viên với 17 thuộc tính.
- Bộ dữ liệu được chúng tôi công bố tại [Hotel Booking Rating Dataset](https://www.kaggle.com/datasets/phamtheds/hotel-booking-rating-dataset)


### Nội dung đồ án

- Thu thâp, xây dựng và phân tích bộ dữ liệu
- Hướng tiếp cận: Để tạo ra mô hình khuyến nghị công việc cho các ứng viên dựa trên thông tin của ứng viên, chúng tôi tiến hành xây dựng các mô hình khuyến nghị dựa trên nội dung sử dụng các thuộc tính khác nhau trong bộ dữu liệu và các phương pháp: TF-IDF, Word2Vec, BERT. Để đánh giá mô hình chúng tôi tiến hành gán nhãn bằng tay, sau đó so khớp giữa công việc mong muốn của ứng viên và công việc được đề xuất bởi mô hình.


- Kết quả tốt nhất mà chúng tôi đạt được là 12.66 MSE, 3.56 RMSE, 2.60 MAE và 0.34 NMAE.












## Thực hiện

```
Phạm Đức Thể

Thể ~/~
```
