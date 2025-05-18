import matplotlib.pyplot as plt

# Dữ liệu từ Medium Map
algorithms = ["AND-OR Search", "Partially Observable Search", "Belief State Search"]
times = [0.003, 0.002, 0.002]
steps = [2, 2, 2]

# Thiết lập biểu đồ
fig, ax1 = plt.subplots(figsize=(10, 5))

# Thiết lập vị trí và chiều rộng của cột
bar_width = 0.35
x = range(len(algorithms))

# Vẽ cột cho thời gian thực thi (trục y bên trái)
ax1.bar([i - bar_width/2 for i in x], times, bar_width, label="Thời gian thực thi (giây)", color="#FF6384")
ax1.set_xlabel("Thuật toán")
ax1.set_ylabel("Thời gian thực thi (giây)", color="#FF6384")
ax1.tick_params(axis="y", labelcolor="#FF6384")

# Tạo trục y thứ hai cho số bước đi
ax2 = ax1.twinx()
ax2.bar([i + bar_width/2 for i in x], steps, bar_width, label="Số bước đi", color="#36A2EB")
ax2.set_ylabel("Số bước đi", color="#36A2EB")
ax2.tick_params(axis="y", labelcolor="#36A2EB")

# Thiết lập nhãn trục x
plt.xticks(x, algorithms)

# Tiêu đề và chú thích
plt.title("So sánh thời gian thực thi và số bước đi trên Medium Map (Complex Environment)")
fig.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2)

# Điều chỉnh layout để không bị cắt
plt.tight_layout()

# Lưu biểu đồ
plt.savefig("complex_env_time_steps_medium.png")