# Báo cáo cá nhân 
Họ tên: Nguyễn Thanh Trúc
MSSV: 23133080
Môn học: Trí tuệ nhân tạo
 ## 1. Mục tiêu
Mục tiêu của chương trình là mô phỏng và so sánh hiệu suất các thuật toán tìm kiếm không có thông tin (uninformed search) trong việc giải bài toán 8-Puzzle, với trọng tâm là Medium Map ([1, 2, 3, 4, 0, 5, 6, 7, 8]) để đánh giá hiệu quả trên trường hợp tiêu chuẩn. Easy Map ([1, 2, 3, 4, 5, 6, 0, 7, 8]) được sử dụng để kiểm tra khả năng hoạt động của các thuật toán, đặc biệt là những thuật toán không tối ưu cho 8-Puzzle. Hard Map ([8, 6, 7, 2, 5, 4, 3, 0, 1]) được bổ sung để thử nghiệm tính phù hợp của các thuật toán uninformed search với bài toán 8-Puzzle, đồng thời đánh giá khả năng xử lý trên các map khó với độ sâu giải pháp lớn hơn (khoảng 20 bước). Chương trình:
- Triển khai các thuật toán uninformed search (BFS, DFS, UCS, IDS) để giải bài toán 8-Puzzle.
- Ghi lại kết quả thực thi (thời gian, số bước, trạng thái) vào file results.csv.
- Mô tả cách mỗi thuật toán giải quyết vấn đề (solution) thông qua cơ chế và đặc điểm.
- So sánh hiệu suất trên Medium Map, đồng thời kiểm tra khả năng xử lý Easy Map và Hard Map.

## 2. Nội dung
### 2.1. Uninformed Search
#### Thành phần chính:
Các thuật toán tìm kiếm không có thông tin (uninformed search) là những phương pháp tìm kiếm không sử dụng thông tin heuristic, chỉ dựa trên cấu trúc không gian trạng thái và các quy tắc di chuyển hợp lệ trong bài toán 8-Puzzle. Nhóm này bao gồm:
- Breadth-First Search (BFS): Khám phá trạng thái theo mức độ sâu.
- Depth-First Search (DFS): Khám phá một nhánh đến độ sâu tối đa.
- Uniform Cost Search (UCS): Mở rộng trạng thái có chi phí thấp nhất.
- Iterative Deepening Search (IDS): Kết hợp BFS và DFS với độ sâu tăng dần.
#### Cách các thuật toán Uniformed Search giải quyết vấn đề
1. Breadth-First Search (BFS):
    - Cơ chế: Sử dụng hàng đợi (queue) để khám phá tất cả trạng thái ở một mức độ sâu trước khi chuyển sang mức sâu hơn. BFS duyệt qua các trạng thái gần trạng thái ban đầu trước, đảm bảo tìm được đường đi ngắn nhất đến đích.
    - Đặc điểm: Luôn tạo ra giải pháp tối ưu (đường đi ngắn nhất), nhưng yêu cầu bộ nhớ lớn để lưu trữ các trạng thái trong hàng đợi. Phù hợp với Medium map do không gian trạng thái không quá lớn.
2. Depth-First Search (DFS):
    - Cơ chế: Sử dụng ngăn xếp (stack) để khám phá một nhánh đến độ sâu tối đa (giới hạn tại max_depth=30 trong mã) trước khi quay lại (backtrack) để thử nhánh khác.
    - Đặc điểm: Tiết kiệm bộ nhớ vì chỉ lưu một nhánh tại một thời điểm, nhưng giải pháp không đảm bảo tối ưu và có thể thất bại trên Medium map nếu nhánh sâu không dẫn đến đích. Trên Easy map, DFS thường thành công nhanh do độ sâu nhỏ.
3. Uniform Cost Search (UCS):
    - Cơ chế: Sử dụng hàng đợi ưu tiên (priority queue) để mở rộng trạng thái có chi phí thấp nhất (số bước di chuyển). Trong 8-Puzzle, do chi phí đồng đều, UCS hoạt động tương tự BFS.
    - Đặc điểm: Giải pháp tối ưu, nhưng yêu cầu bộ nhớ lớn tương tự BFS. Hiệu quả trên Medium map do số bước cần thiết nhỏ.
4. Iterative Deepening Search (IDS):
    - Cơ chế: Chạy DFS nhiều lần với độ sâu tăng dần, kết hợp tính tối ưu của BFS và tiết kiệm bộ nhớ của DFS. Mỗi lần lặp, IDS khám phá các trạng thái đến một độ sâu nhất định trước khi tăng giới hạn.
    - Đặc điểm: Giải pháp tối ưu, tiết kiệm bộ nhớ hơn BFS, nhưng thời gian thực thi dài hơn do lặp lại các trạng thái ở độ sâu thấp hơn. Phù hợp cho cả Medium và Easy map.
#### So sánh hiệu suất:
![BFS](./gif/BFS.gif)
![DFS](./gif/DFS.gif)
![UCS](./gif/UCS.gif)
![IDS](./gif/IDS.gif)
![Biểu đồ so sánh hiệu suất](./image/uninformed.png)
#### Nhận xét hiệu suất:
•	DFS: 
-	Điểm mạnh: Nhanh nhất về thời gian (0.018s), phù hợp với lý thuyết rằng DFS có thể nhanh nếu nhánh chứa giải pháp được chọn sớm. DFS tiết kiệm bộ nhớ nhờ chỉ lưu một nhánh tại một thời điểm.
-	Điểm yếu: Số bước đi cao (28), gấp đôi các thuật toán khác, cho thấy DFS không tối ưu trong trường hợp này. Điều này có thể do nhánh được chọn không phải là đường đi ngắn nhất.
•	BFS: 
-	Điểm mạnh: Số bước đi tối ưu (14), đúng với lý thuyết rằng BFS đảm bảo tìm đường đi ngắn nhất trong bài toán 8-Puzzle. Thời gian thực thi (0.025s) là hợp lý, nhanh hơn UCS và IDS.
-	Điểm yếu: Chậm hơn DFS (0.018s), do phải khám phá toàn bộ các mức độ sâu, dẫn đến yêu cầu bộ nhớ lớn hơn.
•	UCS: 
-	Điểm mạnh: Số bước đi tối ưu (14), phù hợp với lý thuyết rằng UCS đảm bảo đường đi ngắn nhất trong các bài toán có chi phí đồng đều như 8-Puzzle.
-	Điểm yếu: Thời gian thực thi cao nhất (0.042s), chậm hơn nhiều so với DFS và BFS. UCS yêu cầu bộ nhớ lớn do sử dụng hàng đợi ưu tiên để quản lý các trạng thái.
•	IDS: 
-	Điểm mạnh: Số bước đi tối ưu (14), tiết kiệm bộ nhớ hơn BFS và UCS nhờ lặp lại với độ sâu tăng dần. IDS là lựa chọn tốt khi cần cân bằng giữa tính tối ưu và yêu cầu bộ nhớ.
-	Điểm yếu: Thời gian thực thi cao (0.039s), do phải lặp lại việc khám phá trạng thái ở các độ sâu thấp hơn, khiến nó chậm hơn DFS và BFS.
Tổng kết:
-	Trên Medium map: DFS nhanh nhất (0.018s), nhưng số bước đi cao (28), không tối ưu. BFS, UCS, và IDS đều đạt số bước tối ưu (14), với BFS có thời gian thực thi tốt hơn (0.025s) so với UCS (0.042s) và IDS (0.039s).
-	Đề xuất: Nếu ưu tiên tốc độ, DFS là lựa chọn tốt nhất trên Medium map, nhưng cần lưu ý tính không ổn định về số bước. Nếu cần đường đi tối ưu, BFS là phù hợp hơn, đặc biệt khi tài nguyên hệ thống đủ lớn. IDS là lựa chọn cân bằng khi cần tiết kiệm bộ nhớ mà vẫn đảm bảo tính tối ưu.
