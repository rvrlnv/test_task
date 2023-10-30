import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from bagpy import bagreader

bag_path = "D:/test/example_data.bag"

# Чтение данных из rosbag-файла
b = bagreader(bag_path)
data = b.message_by_topic('/state/arm/1/arm_state')

# Преобразование данных в DataFrame
df = pd.DataFrame(data)

# Отображение основной статистической информации
statistics = df[['tool_vector_actual_0', 'tool_vector_actual_1', 'tool_vector_actual_2']].describe()
print(statistics)

# Визуализация изменения позиций на виде сверху
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='tool_vector_actual_0', y='tool_vector_actual_1')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Change in Positions (X, Y)')
plt.show()

# Определение моментов времени с максимальной и минимальной скоростью сочленений
max_speed_time = df['time'][df['joint_speed'].idxmax()]
min_speed_time = df['time'][df['joint_speed'].idxmin()]
print("Максимальная скорость сочленений:", max_speed_time)
print("Минимальная скорость сочленений:", min_speed_time)

# Функция для интерполяции позиций робота в заданный момент времени
def interpolate_positions(t):
    interpolated_values = df[['time', 'tool_vector_actual_0', 'tool_vector_actual_1', 'tool_vector_actual_2']].interpolate(method='linear')
    interpolated_positions = interpolated_values.loc[interpolated_values['time'] == t, ['tool_vector_actual_0', 'tool_vector_actual_1', 'tool_vector_actual_2']].values.flatten()
    return interpolated_positions

# Пример использования функции
t = 10.0  # Заданный момент времени
interpolated_positions = interpolate_positions(t)
print("Интерполированные значения позиций робота в момент времени", t, ":", interpolated_positions)
